Weather Dashboard

A simple weather dashboard built with Python that serves a web interface and provides current weather data using the OpenWeather API.

The application supports searching for weather by city name or by latitude and longitude.

Features

🌤️ Get current weather information

📍 Search using your current coordinates

🏙️ Search by city name

🌡️ Temperature and feels-like temperature

💧 Humidity

💨 Wind speed

🌬️ Atmospheric pressure

👁️ Visibility

🌅 Sunrise and sunset times

⛅ Weather description and icon

⚠️ User-friendly error messages

🔒 API key stored using an environment variable

Requirements

Python 3.9 or newer

An OpenWeather API key

Internet connection

Install the required Python package:

pip install requests

Project Structure
weather-dashboard/
├── app.py
├── static/
│   ├── index.html
│   ├── style.css
│   └── script.js
└── README.md


Your Python file can have any name, but the examples below assume it is called app.py.

Getting an OpenWeather API Key

Create an account with OpenWeather and obtain an API key.

Do not put your API key directly into your Python source code or commit it to Git.

The application expects the following environment variable:

OPENWEATHER_API_KEY

Configure the API Key
Windows PowerShell

Open PowerShell and run:

$env:OPENWEATHER_API_KEY="YOUR_API_KEY"


Then start the application:

python app.py

Windows Command Prompt
set OPENWEATHER_API_KEY=YOUR_API_KEY
python app.py


Then:

python app.py

macOS / Linux
export OPENWEATHER_API_KEY="YOUR_API_KEY"
python app.py


Then:

python app.py

Important

The Python application must read the variable using:

params["appid"] = os.environ.get("OPENWEATHER_API_KEY", "")


Do not use the API key itself as the argument to os.environ.get().

For example, this is incorrect:

os.environ.get("YOUR_API_KEY", "")


os.environ.get() expects the name of the environment variable, not the API key.

Running the Application

Start the server:

python app.py


By default, the application runs at:

http://127.0.0.1:8000


Open that address in your browser.

You can change the port using the PORT environment variable.

Windows PowerShell
$env:PORT="5000"
python app.py

macOS / Linux
PORT=5000 python app.py


The application will then be available at:

http://127.0.0.1:5000

API Endpoint

The application provides the following endpoint:

GET /api/weather

Search by City

Example:

/api/weather?city=London

Search by Coordinates

Example:

/api/weather?lat=51.5074&lon=-0.1278


The API returns weather information in JSON format.

Example response:

{
  "name": "London",
  "country": "GB",
  "temp": 15.2,
  "feels_like": 14.7,
  "description": "broken clouds",
  "main": "Clouds",
  "icon": "04d",
  "humidity": 76,
  "wind_speed": 4.1,
  "pressure": 1012,
  "visibility": 10000,
  "sunrise": 1727500000,
  "sunset": 1727540000,
  "timezone": 3600
}

Error Handling

The application handles several common errors.

Status	Meaning
200	Weather data retrieved successfully
400	Invalid or missing location
404	City/place not found
502	Weather service or API error
503	API key missing or weather service unavailable
504	Weather service timed out

If you see:

Weather service is not configured. Set OPENWEATHER_API_KEY and restart the app.


check that:

The environment variable is named exactly OPENWEATHER_API_KEY.

The API key is correct.

The variable is set in the same terminal/environment used to start the application.

You restarted the Python application after setting the variable.

You can test whether Python can see the environment variable:

import os

print(bool(os.environ.get("OPENWEATHER_API_KEY")))


The expected output is:

True


Never print the actual API key.

Security

Keep your OpenWeather API key private.

Do not commit it to Git:

.env


can be added to .gitignore if you choose to store configuration in a .env file.

Example .gitignore:

.env
__pycache__/
*.pyc


If an API key has accidentally been uploaded to GitHub or shared publicly, revoke/rotate it through your OpenWeather account and replace it with a new key.

Troubleshooting
requests is not installed

Run:

pip install requests

API key error

Check:

OPENWEATHER_API_KEY


and make sure your code contains:

os.environ.get("OPENWEATHER_API_KEY", "")

The browser cannot connect

Make sure the Python server is running and that you are opening:

http://127.0.0.1:8000

City cannot be found

Check the spelling of the city name and try again.

Location does not work

Make sure the browser has permission to access your location and that both latitude and longitude are provided.

License

This project is provided for educational and personal use.
