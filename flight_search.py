import requests
from flight_data import FlightData

# Connection travelpayouts api aviasales
AVIASALES_TOKEN = {"X-Access-Token":  "4b5bc811512909feca0abb4a671ecfc8"}
AVIASALES_URL = "https://api.travelpayouts.com/aviasales/v3/grouped_prices"
AVIASALES_ALTERNATIVE = "http://api.travelpayouts.com/v2/prices/nearest-places-matrix?"

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
            "direct": 'true',

        }
        response_search = requests.get(
            url=AVIASALES_URL,
            params= query,
            headers=headers
        )
        try:
            data = response_search.json()
            current_data_flight = data["data"][f"{depart_month}"]
        except:
            alternative = AVIASALES_ALTERNATIVE
            query = {
                "currency": "RUB",
                "origin": from_city,
                "destination": to_city,
                "limit": "5",
                "show_to_affiliates": "false",
                "depart_date": depart_month,
                "market": "ru",
                "flexibility": "7",

            }

            response_search = requests.get(
                url=alternative,
                params=query,
                headers=headers
            )
            try:
                transfer_stop = response_search.json()
                data = transfer_stop['prices']
                stops = self.stops_option(data)
            except:
                print("Data not found!")
            else:
                alt_flight = FlightData(
                    flight_origin=stops["origin"],
                    flight_destination=stops["destination"],
                    flight_price=stops["price"],
                    flight_depart=stops["depart_date"].split("T")[0],
                    flight_link=stops["link"],
                    flight_trans=stops['transfers']

                )
                return alt_flight

        else:
            flight_data = FlightData(
                flight_origin=current_data_flight["origin"],
                flight_destination=current_data_flight["destination"],
                flight_price=current_data_flight["price"],
                flight_depart=current_data_flight["departure_at"].split("T")[0],
                flight_link=current_data_flight["link"],

            )
            return flight_data

    def stops_option(self, data):
        option = {
            'origin': "",
            'destination': "",
            'depart_date': "",
            "link": "",
            "price": 0,
            "transfers": 0,
        }

        price = []
        for i in data:
            price.append(i['price'])
            price.sort()

        option['price'] = price[0]
        for y in data:
            if option['price'] == y['price']:
                option["origin"] = y['origin']
                option['destination'] = y['destination']
                option['depart_date'] = y["depart_date"]
                option['link'] = y['link']
                option['transfers'] = y['transfers']

        return option













