import requests
import time
from data_manager import DataManager

TOKEN = ""
URL = "https://api.telegram.org/bot"
REQUEST = URL + TOKEN + "/"
reg_users = DataManager()

USER = {}


class NewUser:

    def __init__(self, name):
        self.name = name
        self.last_name = None
        self.email = None


def getUpdates(offset=0):
    response = requests.get(url=f'{REQUEST}getUpdates?offset={offset}').json()
    return response['result']


def send_message(chat_id, text):
    result = requests.get(f'{URL}{TOKEN}/sendMessage?chat_id={chat_id}&text={text}')
    return result


def check_message(message):
    get_message = message['message']
    text_message = get_message['text']
    chat_id = get_message['chat']['id']

    for mes in text_message.lower().replace(',', '').split():
        if mes in ["/start"]:
            first_name = get_message['from']['first_name']
            new_user = NewUser(first_name)
            USER[chat_id] = new_user
            send_message(chat_id, f"Привет {USER[chat_id].name}! Введи свою фамилию:")
            print(USER[chat_id])

        elif USER[chat_id].last_name is None:
            user = USER[chat_id]
            try:
                user.last_name = text_message
                send_message(chat_id, f'{user.name}, фамилия добавлена! Следующий шаг: введите свой email')
                print(USER[chat_id])
            except:
                send_message(chat_id, f'{user.name}, возникла ошибка')

        elif USER[chat_id].email == None:
            user = USER[chat_id]
            try:
                user.email = text_message
                send_message(chat_id, f"{user.name}, продублируйте свое email?")
                print(USER[chat_id])
            except:
                send_message(chat_id, f'{user.name}, возникла ошибка')

        elif USER[chat_id].email != None:
            user = USER[chat_id]
            if USER[chat_id].email == text_message:
                send_message(chat_id, f'{user.name} Регистрация завершена! Начинаем поиск!')
                reg_users.get_new_user(user.name, user.last_name, user.email)
                print(USER[chat_id])
            elif USER[chat_id].email != text_message:
                send_message(chat_id, f'{user.name} email несовпадает! введите заново!')


def run_update():
    update_id = getUpdates()[-1]["update_id"]
    while True:
        time.sleep(2)
        messages = getUpdates(update_id)
        for message in messages:
            if update_id < message["update_id"]:
                update_id = message["update_id"]
                check_message(message)


if __name__ == "__main__":
    run_update()
