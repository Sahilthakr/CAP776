## Air Quality Monitoring System

This Python application provides a simple interface for registering users, logging in, and retrieving air quality data for a specified city. It uses OpenWeatherMap's Geocoding and Air Pollution APIs to fetch location coordinates and air quality index (AQI) data. 

**Features:**

- User registration with email, password, and a security question for password reset.
- Secure password storage using bcrypt hashing.
- User login with email and password authentication.
- Password reset functionality using a security question.
- City-specific AQI data retrieval using OpenWeatherMap's API.
- Interactive command-line interface for user interaction.

**Dependencies:**

- requests
- bcrypt
- csv
- re

**How to Use:**

1. **Install dependencies:**
   ```bash
   pip install requests bcrypt
   ```
2. **Create a `mydata.csv` file:** This file will store user credentials. It should be empty initially.
3. **Obtain an API key:** Sign up for a free OpenWeatherMap account at [https://openweathermap.org/register](https://openweathermap.org/register) and obtain your API key.
4. **Replace `API_KEY` in the code with your actual API key.**
5. **Run the script:**
   ```bash
   python air_quality_monitor.py
   ```

**Usage:**

- **Register:** Choose option 1, provide your email, password, and answer to the security question.
- **Login:** Choose option 2, enter your registered email and password.
- **Forgot Password:** Choose option 3, enter your registered email and answer the security question to reset your password.
- **Fetch AQI Data:** After logging in, enter a city name to get the AQI data for that location.

**Notes:**

- The script uses a default security question, but you can modify this in the `register_user` function.
- The code includes error handling and input validation to enhance user experience and data security.
- The AQI data displayed includes the overall AQI index and a breakdown of individual pollutants.
- The number of login attempts is limited to 5 for security purposes.

**Potential Enhancements:**

- Implement a web interface for better user experience.
- Add more comprehensive AQI data visualization.
- Integrate with other weather data APIs for more detailed information.
- Allow users to save preferred cities for easy access to AQI data.
- Implement a user feedback system.

This is a basic implementation, but it provides a foundation for a more robust air quality monitoring system. Feel free to customize and expand it based on your requirements.