class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, flight_origin, flight_destination, flight_price, flight_depart, flight_link, flight_trans=''):
        self.flight_origin = flight_origin
        self.flight_destination = flight_destination
        self.flight_price = flight_price
        self.flight_date_depart = flight_depart
        self.flight_link = flight_link
        self.transfer = flight_trans



