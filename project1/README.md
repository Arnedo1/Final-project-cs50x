# ARNEDO Currency Calculator

## CS50x Final Project

### Video Demo: [Watch on YouTube] (https://youtu.be/e_3Xk8YJOzo)

## Project Description

ARNEDO Currency Calculator is a web application developed as the final project for CS50x. It allows users to calculate exchange rates between their favorite currencies. The application uses an API to fetch current currency rates and provides a personalized experience for registered users.

### Key Features:

- Currency calculation for both guest and registered users
- User registration and login system
- Customizable list of favorite currencies for registered users
- Secure password storage using hashing
- Real-time currency conversion using up-to-date exchange rates

## Technologies Used

- **Frontend**: HTML5, CSS, JavaScript, Bootstrap
- **Backend**: Python, Flask
- **Database**: SQL (SQLite)
- **Additional**: CS50's Library for Python

## Project Structure

- `static/`: Contains static files (CSS, JavaScript, images)
  - `logo_icon.ico`: Application icon
  - `style.css`: Main stylesheet
- `templates/`: Contains HTML templates
  - `favorites.html`: Personal favorite currencies page
  - `index.html`: Landing page with basic currency calculator
  - `login.html`: User login page
  - `add.html`: Add currencies to favorites
  - `register.html`: User registration page
  - `remove.html`: Remove currencies from favorites
- `app.py`: Main Python file with application logic
- `calculator.db`: SQLite database for user data and favorites
- `currencies.py`: Python file containing currency data (symbols, flags)
- `requirements.txt`: List of Python dependencies

## Setup and Installation

1. Ensure you have Python 3 installed on your system.
2. Clone this repository to your local machine.
3. Navigate to the project directory in your terminal.
4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Run the application:
   ```
   flask run
   ```

## Usage

- **Guest Users**: Access the homepage to use the basic currency calculator with 5 pre-selected currencies.
- **Registered Users**:
  - Log in or register for an account
  - Add or remove currencies from your favorites list
  - Calculate exchange rates using your personalized list of currencies

## Development

This project was developed using Visual Studio Code. To set up the development environment:

1. Download and install [Visual Studio Code](https://code.visualstudio.com/)
2. Open the project folder in VS Code
3. Install the Python extension for VS Code

## Deployment

To deploy this application on a live system:

1. Set up a web server (e.g., Apache, Nginx)
2. Configure the server to run Flask applications
3. Follow the setup instructions above
4. Ensure all security measures are in place (e.g., HTTPS, proper database security)

## Author

- **Name**: Jose Arnedo
- **Location**: Rotterdam, The Netherlands
- **Date**: July 7, 2024
- **Edx username**: arnedo1

## Acknowledgments

- CS50x course staff and community
- Flask documentation and community
- Bootstrap framework
