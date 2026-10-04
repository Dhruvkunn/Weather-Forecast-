import requests

api_key = "Enter Your Api Key"
user_input_city = input("Enter city name: ")
weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={user_input_city}&appid={api_key}&units=metric"

response = requests.get(weather_url)
data = response.json()

if data["cod"] == "404":
    print("City not found. Please check the city name and try again.")

else:

    weather = {
    "City": data["name"],
    "Temperature": f"{data['main']['temp']} °C",
    "Feels Like": f"{data['main']['feels_like']} °C",
    "Condition": data["weather"][0]["description"].capitalize(),
    "Humidity": f"{data['main']['humidity']}%",
    "Wind Speed": f"{data['wind']['speed']} m/s",
    "Sunrise": f"{data['sys']['sunrise']}",
    "Sunset": f"{data['sys']['sunset']}"
}

print(weather)
