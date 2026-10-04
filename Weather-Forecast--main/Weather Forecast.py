import json
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import requests


APP_DIR = Path(__file__).resolve().parent
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


class WeatherHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(APP_DIR / "static"), **kwargs)

    def do_GET(self):
        if urlsplit(self.path).path == "/api/weather":
            self.handle_weather_request()
            return
        super().do_GET()

    def handle_weather_request(self):
        query = parse_qs(urlsplit(self.path).query)
        city = query.get("city", [""])[0].strip()
        latitude = query.get("lat", [""])[0]
        longitude = query.get("lon", [""])[0]

        if bool(latitude) != bool(longitude):
            self.send_json({"error": "Provide both location coordinates."}, 400)
            return
        if not city and not (latitude and longitude):
            self.send_json({"error": "Enter a city or share your location."}, 400)
            return

        params = {"units": "metric"}
        if latitude and longitude:
            try:
                lat, lon = float(latitude), float(longitude)
            except ValueError:
                self.send_json({"error": "Location coordinates are invalid."}, 400)
                return
            if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                self.send_json({"error": "Location coordinates are outside the valid range."}, 400)
                return
            params.update({"lat": lat, "lon": lon})
        else:
            params["q"] = city

        params["appid"] = os.environ.get("OPENWEATHER_API_KEY", "")
        if not params["appid"]:
            self.send_json(
                {"error": "Weather service is not configured. Set OPENWEATHER_API_KEY and restart the app."},
                503,
            )
            return

        try:
            response = requests.get(WEATHER_URL, params=params, timeout=10)
        except requests.exceptions.Timeout:
            self.send_json({"error": "The weather service took too long to respond. Try again."}, 504)
            return
        except requests.exceptions.RequestException:
            self.send_json({"error": "Could not reach the weather service. Check your connection and try again."}, 502)
            return

        if response.status_code == 404:
            self.send_json({"error": "We couldn't find that place. Check the spelling and try again."}, 404)
            return
        if response.status_code == 401:
            self.send_json({"error": "The weather service rejected its API key. Check OPENWEATHER_API_KEY."}, 502)
            return
        if response.status_code == 429:
            self.send_json({"error": "The weather service is busy. Please try again in a moment."}, 503)
            return
        if not response.ok:
            self.send_json({"error": "The weather service returned an error. Please try again."}, 502)
            return

        try:
            data = response.json()
            weather = {
                "name": data["name"],
                "country": data["sys"]["country"],
                "temp": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "description": data["weather"][0]["description"],
                "main": data["weather"][0]["main"],
                "icon": data["weather"][0]["icon"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
                "pressure": data["main"]["pressure"],
                "visibility": data.get("visibility"),
                "sunrise": data["sys"]["sunrise"],
                "sunset": data["sys"]["sunset"],
                "timezone": data["timezone"],
            }
        except (KeyError, IndexError, TypeError, ValueError):
            self.send_json({"error": "The weather service returned an unexpected response."}, 502)
            return

        self.send_json(weather)

    def send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    address = ("127.0.0.1", int(os.environ.get("PORT", "8000")))
    server = ThreadingHTTPServer(address, WeatherHandler)
    print(f"Weather dashboard running at http://{address[0]}:{address[1]}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down weather dashboard.")
    finally:
        server.server_close()
