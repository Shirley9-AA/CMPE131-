import requests
import json
from datetime import datetime
from tkinter import *
import matplotlib
matplotlib.use('Agg')
import pytest

# Set up GUI
root = Tk()
root.title("Weather Station App")
root.geometry("400x400")

# Create labels
label_city = Label(root, text="City: ")
label_city.grid(row=0, column=0)

label_temp = Label(root, text="Temperature: ")
label_temp.grid(row=1, column=0)

label_humidity = Label(root, text="Humidity: ")
label_humidity.grid(row=2, column=0)

# Create entry fields
entry_city = Entry(root)
entry_city.grid(row=0, column=1)

entry_temp = Entry(root)
entry_temp.grid(row=1, column=1)

entry_humidity = Entry(root)
entry_humidity.grid(row=2, column=1)

# Define data collection function
def collect_data():
    city = entry_city.get()
    response = requests.get("http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=8f75b82e9e2d26d65e44237f9f40a553")
    
    if response.status_code != 200:
        print("Error: Failed to retrieve weather data for " + city)
        return
    
    data = json.loads(response.text)
    print(data)
    
    try:
        temperature = round(data["main"]["temp"] - 273.15, 2) # Convert temperature from Kelvin to Celsius and round to 2 decimal places
        humidity = data["main"]["humidity"]
    except KeyError:
        print("Error: Invalid weather data for " + city)
        return
    
    entry_temp.delete(0, END)
    entry_temp.insert(0, str(temperature) + "°C")

    entry_humidity.delete(0, END)
    entry_humidity.insert(0, str(humidity) + "%")

    with open("weather_data.txt", "a") as file:
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        file.write(current_time + "," + city + "," + str(temperature) + "," + str(humidity) + "\n")

# Define data analysis function
def analyze_data():
    with open("weather_data.txt", "r") as file:
        data = file.read().splitlines()

    # Calculate average temperature and humidity
    temperatures = []
    humidities = []

    for line in data:
        parts = line.split(",")
        temperature = float(parts[2])
        humidity = int(parts[3])
        temperatures.append(temperature)
        humidities.append(humidity)

    avg_temperature = round(sum(temperatures) / len(temperatures), 2)
    avg_humidity = round(sum(humidities) / len(humidities), 2)

    # Display results in message box
    message = "Average Temperature: " + str(avg_temperature) + "°C\nAverage Humidity: " + str(avg_humidity) + "%"
    messagebox.showinfo("Data Analysis Results", message)

# Define data transmission function
def transmit_data():
    with open("weather_data.txt", "r") as file:
        data = file.read()

    # Send data to remote server
    response = requests.post("http://example.com/data", data=data)

    # Display server response in message box
    messagebox.showinfo("Data Transmission Results", response.text)

# Create buttons
button_collect_data = Button(root, text="Collect Data", command=collect_data)
button_collect_data.grid(row=3, column=0)

button_analyze_data = Button(root, text="Analyze Data", command=analyze_data)
button_analyze_data.grid(row=3, column=1)

root.mainloop()