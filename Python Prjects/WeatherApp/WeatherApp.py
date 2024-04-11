import requests
import tkinter as tk
from tkinter import messagebox

def update_labels(weather_data):
    labels_info = {
        "Description": weather_data['weather'][0]['description'],
        "Temperature": f"{weather_data['main']['temp']}°C",
        "Humidity": f"{weather_data['main']['humidity']}%",
        "Wind Speed": f"{weather_data['wind']['speed']} m/s",
        "Pressure": f"{weather_data['main']['pressure']} hPa"
    }

    # Display weather information in labels
    for i, (label_text, label_value) in enumerate(labels_info.items()):
        labels[i]["text"] = f"{label_text}: {label_value}"

    if 'rain' in weather_data:
        if '1h' in weather_data['rain']:
            precipitation = weather_data['rain']['1h']
            precipitation_percentage = (precipitation / 10) * 100
            labels[5]["text"] = f"Precipitation: {precipitation_percentage}%"
        else:
            labels[5]["text"] = "Precipitation: No data available for the last 1 hour."
    else:
        labels[5]["text"] = "Precipitation: No data available."

def get_weather():
    city_name = entry.get()
    api_key = "4c0f8aa1267fe06e61779d994cdcb0c4"  # Replace with your OpenWeatherMap API key
    
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        update_labels(weather_data)
    else:
        messagebox.showerror("Error", f"City not found or unexpected error. Error Code: {response.status_code}")

window = tk.Tk()
window.title("Weather Forecast")

labels_text = [
    "Description", "Temperature", "Humidity",
    "Wind Speed", "Pressure", "Precipitation"
]

# Create labels for weather information
labels = [tk.Label(window, text="", font=("Arial", 12)) for _ in range(6)]
for i, label in enumerate(labels):
    label.grid(row=i+1, column=0, sticky="w", padx=20, pady=5)
    label.config(fg="white", bg="#2c3e50", padx=10, pady=5)

# Set the labels' initial text
for i, label_text in enumerate(labels_text):
    labels[i]["text"] = f"{label_text}: "

entry_label = tk.Label(window, text="Enter Your Location:", font=("Arial", 12))
entry_label.grid(row=0, column=0, padx=20, pady=5, sticky="w")

entry = tk.Entry(window, width=40, font=("Arial", 12))
entry.grid(row=0, column=1, padx=20, pady=5)

search_button = tk.Button(window, text="Search", width=10, height=1, command=get_weather, font=("Arial", 12))
search_button.grid(row=0, column=2, padx=20, pady=5)

window.mainloop()
