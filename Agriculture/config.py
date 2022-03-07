weather_api_key = "cbb7d92c294d51618c73edfd89f119cd"



def user():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM user WHERE id = %s', (session['id'],))
        account = cursor.fetchone()

# import requests

# def weather_fetch(city_name):
#     """
#     Fetch and returns the temperature and humidity of a city
#     :params: city_name
#     :return: temperature, humidity
#     """
#     api_key = weather_api_key
#     base_url = "http://api.openweathermap.org/data/2.5/weather?"

#     complete_url = base_url + "appid=" + api_key + "&q=" + city_name
#     response = requests.get(complete_url)
#     x = response.json()

#     if x["cod"] != "404":
#         y = x["main"]
#         r= x["visibility"]
#         r = x["weather"]

#         temperature = round((y["temp"] - 273.15), 2)
#         humidity = y["humidity"]
#         #rain = r["3h"]
        
#         print("Temperature ", temperature)
#         print("Humidity  ", humidity)
#         print("Humidity  ", r)
#         return temperature, humidity
#     else:
#         return None
# city = input("Enter city? ")
# weather_fetch(city)
