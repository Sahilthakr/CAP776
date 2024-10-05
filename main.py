import csv 
import bcrypt 
import re 
import requests 
from geocoding_api import get_coordinates   
import logging

API_KEY = '77e9ddd6a9feaf4a9449833c97233a03'   
CREDENTIALS_FILE = 'mydata.csv' 
LOG_FILE = 'process_log.csv'

DEFAULT_SECURITY_QUESTION = "What is your favorite color?" 

EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+" 
PASSWORD_REGEX = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&*(),.?\":{}|<>]).{8,}$" 

# Setup logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, 
                    format='%(asctime)s, %(message)s')

def log_event(message):
    """Logs events to the CSV file."""
    logging.info(message)

def register_user(email, password, security_answer): 
    """Registers a new user, validating inputs and storing credentials securely.""" 
    if not re.match(EMAIL_REGEX, email): 
        print("Invalid email format. Please use a valid email address.") 
        return False 

    if not re.match(PASSWORD_REGEX, password): 
        print("Password must meet complexity requirements: \n" 
              "- At least 8 characters long\n" 
              "- Include at least one uppercase letter, one lowercase letter, one digit, and one special character") 
        return False 

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') 
    hashed_answer = bcrypt.hashpw(security_answer.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') 

    try: 
        with open(CREDENTIALS_FILE, mode='a', newline='') as file: 
            writer = csv.writer(file) 
            writer.writerow([email, hashed_password, DEFAULT_SECURITY_QUESTION, hashed_answer]) 
        print("User registered successfully!") 
        log_event(f"User registered: {email}")
        return True 
    except Exception as e: 
        print(f"An error occurred while registering: {e}") 
        return False 

def login_user(email, password): 
    """Authenticates a user based on email and password.""" 
    try: 
        with open(CREDENTIALS_FILE, mode='r') as file: 
            reader = csv.reader(file) 
            for row in reader: 
                if row[0] == email: 
                    if bcrypt.checkpw(password.encode('utf-8'), row[1].encode('utf-8')): 
                        print("Login successful!") 
                        log_event(f"User logged in: {email}")
                        return True 
                    else: 
                        print("Incorrect password.") 
                        return False 
        print("Email not found. Please check your email address.") 
        return False 
    except FileNotFoundError: 
        print(f"User database '{CREDENTIALS_FILE}' not found. Please run registration first.") 
        return False 

def reset_password(email): 
    """Allows a user to reset their password using a security question.""" 
    try: 
        with open(CREDENTIALS_FILE, mode='r') as file: 
            reader = csv.reader(file) 
            users = list(reader) 

        for row in users: 
            if row[0] == email: 
                security_question = row[2] 
                print(f"Security Question: {security_question}") 
                answer = input("Your answer: ") 

                if bcrypt.checkpw(answer.encode('utf-8'), row[3].encode('utf-8')): 
                    new_password = input("Enter your new password: ") 
                    if register_user(email, new_password, row[3]):  # Use the existing answer 
                        print("Password reset successfully!") 
                        log_event(f"Password reset for user: {email}")
                        return 
                else: 
                    print("Incorrect answer.") 
                    return 

        print("Email not found. Please check your email address.") 
    except FileNotFoundError: 
        print(f"User database '{CREDENTIALS_FILE}' not found. Please run registration first.") 

def fetch_aqi(city, api_key): 
    """Fetches air quality data for a given city using the OpenWeather API.""" 
    latitude, longitude = get_coordinates(city, api_key)  # Get coordinates from geocoding API 

    if latitude and longitude: 
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?appid={api_key}&lat={latitude}&lon={longitude}" 
        response = requests.get(url) 
        if response.status_code == 200: 
            log_event(f"Fetched AQI data for {city}: {response.json()}")
            return response.json() 
        else: 
            print(f"Error fetching air pollution data. Status Code: {response.status_code}") 
            log_event(f"Error fetching AQI data for {city}: {response.status_code}")
            return None 
    else: 
        print(f"Error getting coordinates for {city}.") 
        log_event(f"Error getting coordinates for {city}.")
        return None 

def main(): 
    """Main application loop for user interaction and AQI data retrieval.""" 
    while True: 
        print("\n--- Air Quality Monitoring System ---") 
        print("1. Register") 
        print("2. Login") 
        print("3. Forgot Password") 
        print("4. Exit") 

        choice = input("Choose an option (1-4): ") 

        if choice == '1': 
            email = input("Enter your email: ") 
            password = input("Enter your password: ") 
            security_answer = input(f"Enter your answer to the security question: {DEFAULT_SECURITY_QUESTION} ") 
            register_user(email, password, security_answer)

        elif choice == '2': 
            attempts = 0 
            while attempts < 5: 
                email = input("Enter your email: ") 
                password = input("Enter your password: ") 
                if login_user(email, password): 
                    city = input("Enter city name for AQI data: ") 
                    aqi_data = fetch_aqi(city, API_KEY) 
                    if aqi_data: 
                        print("\n--- Air Quality Data for", city, "---") 
                        print("AQI:", aqi_data['list'][0]['main']['aqi']) 
                        print("Pollutants:", aqi_data['list'][0]['components']) 
                    break 
                else: 
                    attempts += 1 
                    print(f"Attempts remaining: {5 - attempts}") 
            if attempts == 5: 
                print("Too many failed attempts. Exiting application.") 
                break   

        elif choice == '3': 
            email = input("Enter your registered email: ") 
            reset_password(email) 

        elif choice == '4': 
            print("Exiting the application.") 
            break 

        else: 
            print("Invalid option. Please choose again.") 

if __name__ == "__main__": 
    main()
