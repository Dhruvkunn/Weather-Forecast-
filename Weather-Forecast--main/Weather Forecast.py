# import tkinter as tk
import requests
api_key = "a6eb68361de0dfd18785829749df2032"
user_input_city = input("Enter city name: ")
weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={user_input_city}&appid={api_key}&units=metric"

response = requests.get(weather_url)
data = response.json()

weather = wearher_data = {
    "City": data["name"],
    "Temperature": f"{data['main']['temp']} °C",
    "Feels Like": f"{data['main']['feels_like']} °C",
    "Condition": data["weather"][0]["description"].capitalize(),
    "Humidity": f"{data['main']['humidity']}%",
    "Wind Speed": f"{data['wind']['speed']} m/s",
    "Sunrise": f"{data['sys']['sunrise']}",
    "Sunset": f"{data['sys']['sunset']}"

    print(weather)  


# root = tk.Tk()
# root.title("weather Forecast")
# root.geometry("500x650")
# root.configure(bg = '#161616')
# root.resizable(False, False)

# #Title

# title = tk.Label(
#     root,
#     text = "Weather Forecast",
#     font= ("Segoe UI",22, "bold"),
#     bg= '#161616',
#     fg= "white"
# )

# title.grid(row=0,column=0, columnspan=2, pady=20)


# city_label = tk.Label(
#     root,
#     text="Enter City",
#     font=("Segoe UI", 12),
#     bg="#161616",
#     fg="white"
# )

# city_label.grid(row=1, column=0, pady=10)


# city_entry = tk.Entry(
#     root,
#     width=25,
#     font=("Segoe UI", 12)
# )

# city_entry.grid(row=1, column=1, padx=10)

# search_btn = tk.Button(
#     root,
#     text="Search",
#     font=("Segoe UI", 11, "bold"),
#     bg="#0A58CA",
#     fg="white",
#     width=15
# )

# search_btn.grid(row=2, column=0, columnspan=2, pady=20)

# separator = tk.Frame(
#     root,
#     bg="#333333",
#     height=2,
#     width=420
# )

# separator.grid(row=3, column=0, columnspan=2, pady=15)

# # Label 

# weather_info = [
#     " City",
#     " Temperature",
#     " Feels Like",
#     " Condition",
#     " Humidity",
#     " Wind Speed",
#     " Sunrise",
#     " Sunset"
# ]

# for i, item in enumerate(weather_info):
#     label = tk.Label(
#         root,
#         text=f"{item}:",
#         font=("Segoe UI", 12),
#         bg="#161616",
#         fg="white",
#         anchor="w",
#         width=30
#     )

#     label.grid(row=i+4, column=0, columnspan=2, sticky="w", padx=40, pady=8)

# # dictionary
# weather_value ={} 

# root.mainloop() 
