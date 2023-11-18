import requests
URL_SHEET = ""
HEADER_SHEET = {
    "Authorization": "",
}

class DataManager:
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


    def get_new_user(self, first_name, last_name, email):
        sheets_new_user = ""
        params = {
            'user':{
                "firstName": first_name,
                "lastName": last_name,
                'email': email,
            }
        }
        response = requests.post(sheets_new_user, json=params, headers=self.__header_sheet)
        response.raise_for_status()








