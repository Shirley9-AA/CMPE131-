import requests
import json
from datetime import datetime

def test_collect_data():
    city = "Sunnyvale"
    response = requests.get("http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=8f75b82e9e2d26d65e44237f9f40a553")
    data = json.loads(response.text)
    assert response.status_code == 200
    assert data["name"] == city

def test_analyze_data():
    with open("weather_data.txt", "w") as file:
        file.write("2022-05-01 12:00:00,Sunnyvale,20,50\n")
        file.write("2022-05-02 12:00:00,Sunnyvale,25,60\n")
    with open("weather_data.txt", "r") as file:
        data = file.read().splitlines()
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
    assert avg_temperature == 22.5
    assert avg_humidity == 55.0

def test_transmit_data():
    with open("weather_data.txt", "r") as file:
        data = file.read()
    response = requests.post("http://example.com/data", data=data)
    assert response.status_code == 200
