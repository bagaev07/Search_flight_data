import requests
from data_manager import DataManager

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    #Low prices alert! Only price to fly from St. Petersburg - IATA to NAME - IATA,
    # from date
    def send_message(self, current_flight):
        price = current_flight.flight_price
        origin_iata = current_flight.flight_origin
        origin_name = DataManager().get_city(origin_iata)
        dest_iata = current_flight.flight_destination
        dest_name = DataManager().get_city(dest_iata )
        depart_date = current_flight.flight_date_depart
        flight_link = current_flight.flight_link
        text = f"Low prices alert 🔥! Only {price}RUB to fly from {origin_iata}-{origin_name} to {dest_iata}-{dest_name}, from {depart_date} \n\n 'https://www.aviasales.com{flight_link}"
        self.telegram_bot(text)

    def telegram_bot(self, text):
        token = "5702975022:AAEgm-x5InxywdkerFHFk6RO2Z1K7iWftXw"
        url = "https://api.telegram.org/bot"
        channel_id = "-1001838681899"
        url += token
        method = url + "/sendMessage"
        query = {
            "chat_id": channel_id,
            "text": text
        }
        response = requests.get(method, data=query)

        if response.status_code != 200:
            raise Exception("post_text error")

