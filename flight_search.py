import requests
from flight_data import FlightData
import pprint

# URL_TEQUILA = 'https://api.tequila.kiwi.com'
# TEQUILA_API_KEY = {"apikey": "6GzZ28f8kaEiziiXlwKTMQ68RymTlR7l"}

# Connection travelpayouts api aviasales
AVIASALES_TOKEN = {"X-Access-Token":  "4b5bc811512909feca0abb4a671ecfc8"}
AVIASALES_URL = "https://api.travelpayouts.com/aviasales/v3/grouped_prices"

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.

    def get_iata_code(self, city_name):
        self.__autocomplete_url = "https://autocomplete.travelpayouts.com/places2"
        self.__aviasales_token = AVIASALES_TOKEN
        query = {'term': city_name, "locale": "en", "types": ["city"],}
        tequila_response = requests.get(url=self.__autocomplete_url, params=query, headers=self.__aviasales_token)
        result_iata = tequila_response.json()[0]
        code_iata = result_iata["code"]
        return code_iata

    def get_flight_price(self, from_city, to_city, depart_month):
        headers = AVIASALES_TOKEN
        query = {
            "currency": "RUB",
            "origin": from_city,
            "destination": to_city,
            "group_by": "month",
            "departure_at": depart_month,
            "market": "ru",
            "direct": "true",
            # "return_at": return_month,

        }

        response_search = requests.get(
            url=AVIASALES_URL,
            params= query,
            headers=headers
        )

        data = response_search.json()
        current_data_flight = data["data"][f"{depart_month}"]

        flight_data = FlightData(
            flight_origin= current_data_flight["origin"],
            flight_destination = current_data_flight["destination"],
            flight_price = current_data_flight["price"],
            flight_depart = current_data_flight["departure_at"].split("T")[0],
            flight_link = current_data_flight["link"],

        )
        return flight_data





