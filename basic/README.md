# Atmos weather dashboard

A responsive weather dashboard served by the included Python app. It uses the
OpenWeather current-weather API; the API key stays on the server and is never
sent to the browser.

## Run on Windows

1. Install the existing Python dependency if needed:

   ```powershell
   python -m pip install requests
   ```

2. Set your OpenWeather API key and start the server from this folder:

   ```powershell
   $env:OPENWEATHER_API_KEY = "your-api-key"
   python "Weather Forecast.py"
   ```

3. Open [http://127.0.0.1:8000](http://127.0.0.1:8000).

The dashboard supports city search, browser location, Celsius/Fahrenheit, and
refreshing the current conditions. Location requires browser permission.

Set `PORT` to use a different local port. The server binds to `127.0.0.1`.
