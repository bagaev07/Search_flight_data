import requests
URL_SHEET = "https://api.sheety.co/566d9f4e55beffd0ada98fa062927e71/avbFlightDeals/prices"
HEADER_SHEET = {
    "Authorization": "Basic dHJhdmVsX2V5ZTpwYXNzd29yZHM=",
}

class DataManager():
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.__sheet_url = URL_SHEET
        self.__header_sheet = HEADER_SHEET

    def get_request_sheet(self):
        sheets_response = requests.get(url=self.__sheet_url, headers=self.__header_sheet)
        sheets_response.raise_for_status()
        sheets_data = sheets_response.json()
        return sheets_data


    def set_sheet_iata(self, city_id, city_iata_code):
        params = {
            'price':{
                'iata': city_iata_code,
            }
        }
        response = requests.put(url=f"{self.__sheet_url}/{city_id}", json=params, headers=self.__header_sheet)
        response.raise_for_status()

    def get_city(self, city_code):
        response = requests.get(url="https://api.travelpayouts.com/data/en/cities.json", headers=self.__header_sheet)
        data = response.json()
        for i in range(len(data)):
            code = data[i]['code']
            if code == city_code:
                city = data[i]['name']
                return city






