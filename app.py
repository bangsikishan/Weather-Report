import json
import requests
from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    data = []

    if request.method == 'POST':
        req = request.form
        # print(req['location'])

        # EXTRACTED FROM RAPIDAPI DOCS
        url = "https://community-open-weather-map.p.rapidapi.com/weather"
        querystring = {"q":req['location'], "units":"metric"}

        headers = {
	        "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
	        "X-RapidAPI-Key": "18c306bc69mshb23a0887ef2afd2p1db0b1jsn62832e13d30a"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        json_obj = json.loads(response.text)
        
        data.append("Country: " + json_obj['sys']['country'])
        data.append("Weather: " + json_obj['weather'][0]['main'])
        data.append("Description: " + json_obj['weather'][0]['description'])
        data.append("Feels like: " + str(json_obj['main']['feels_like']) + "C")
        data.append("Min Temp: " + str(json_obj['main']['temp_min']) + "C")
        data.append("Max Temp: " + str(json_obj['main']['temp_max']) + "C")
        data.append("Pressure: " + str(json_obj['main']['pressure']) + " hPa")
        data.append("Humidity: " + str(json_obj['main']['humidity']) + "%")
        data.append("Wind Speed: " + str(json_obj['wind']['speed']) + " m/s")
        data.append("Wind Degree: " + str(json_obj['wind']['deg']) + " degrees")

        sunrise = json_obj['sys']['sunrise']
        sunrise_obj = datetime.fromtimestamp(int(sunrise))
        data.append("Sunrise: " + sunrise_obj.strftime("%d.%m.%y %H:%M:%S"))

        sunset = json_obj['sys']['sunset']
        sunset_obj = datetime.fromtimestamp(int(sunset))
        data.append("Sunset: " + sunset_obj.strftime("%d.%m.%y %H:%M:%S"))


    return render_template('home.html', data=data)

if __name__ == '__main__':
    app.run()