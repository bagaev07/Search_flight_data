#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager


origin_flight = "LED"
depart_month = "2023-05"
# RETURN_MONTH = "2023-03-30"

sheet_data = DataManager()
flight_search = FlightSearch()
send_message = NotificationManager()
sheet_data_iata = sheet_data.get_request_sheet()["prices"]
sheet_flight_price = sheet_data.get_request_sheet()["prices"]


for i in sheet_data_iata:
    if i["iata"] == "":
        city_code = flight_search.get_iata_code(i["city"])
        sheet_data.set_sheet_iata(i['id'], city_code)

for y in sheet_flight_price:
    flight_destination = y['iata']
    current_flight = flight_search.get_flight_price(origin_flight, flight_destination, depart_month)
    sheet_flight_price = y['lowestPrice']
    if current_flight.flight_price < sheet_flight_price:
        NotificationManager().send_message(current_flight)
        NotificationManager().send_emails(current_flight)





