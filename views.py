import telebot
from models import *

token = '5795074181:AAEYHOalWk9jR69mFeJvoHbo1BdPPXcym_g'
bot = telebot.TeleBot(token)


def create_user(message):
    bot.send_message(message.chat.id, 'Введите Ваше имя:')
    bot.register_next_step_handler(message, set_first_name)


def set_first_name(message):
    first_name = message.text
    bot.send_message(message.chat.id, 'Введите Вашу фамилию:')
    bot.register_next_step_handler(message, set_last_name, first_name=first_name)


def set_last_name(message, first_name):
    last_name = message.text
    bot.send_message(message.chat.id, 'Введите Ваш email:')
    bot.register_next_step_handler(message, set_email, first_name=first_name, last_name=last_name)


def set_email(message, first_name, last_name):
    email = message.text
    bot.send_message(message.chat.id, 'Введите пароль:')
    bot.register_next_step_handler(message, set_password, first_name=first_name, last_name=last_name, email=email)


def set_password(message, first_name, last_name, email):
    password = message.text
    bot.send_message(message.chat.id, 'Введите Ваш возраст:')
    bot.register_next_step_handler(message, set_age, first_name=first_name, last_name=last_name, email=email,
                                   password=password)


def set_age(message, first_name, last_name, email, password):
    age = message.text
    bot.send_message(message.chat.id, 'Введите Ваш пол:')
    bot.register_next_step_handler(message, set_male, first_name=first_name, last_name=last_name, email=email,
                                   password=password, age=age)


def set_male(message, first_name, last_name, email, password, age):
    male = message.text
    bot.send_message(message.chat.id, 'Введите город проживания:')
    bot.register_next_step_handler(message, set_city, first_name=first_name, last_name=last_name, email=email,
                                   password=password, age=age, male=male)


def set_city(message, first_name, last_name, email, password, age, male):
    city = message.text

    # create the user in the database
    person = Person.create(
        telegram_id=message.chat.id,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        age=age,
        male=male,
        city=city
    )

    bot.send_message(message.chat.id, 'Регистрация успешно завершена.')


def create_complaint(message):
    bot.send_message(message.chat.id, 'Введите описание нарушения:')
    bot.register_next_step_handler(message, set_description)


def set_description(message):
    description = message.text
    bot.send_message(message.chat.id, 'Введите место нарушения:')
    bot.register_next_step_handler(message, set_place, description=description)


def set_place(message, description):
    place = message.text
    bot.send_message(message.chat.id, 'Введите дату и время нарушения (в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС):')
    bot.register_next_step_handler(message, set_date_time, description=description, place=place)


def set_date_time(message, description, place):
    date_time = message.text
    complaint = Complaint(person=Person.select().where(Person.telegram_id == message.chat.id),
                          description=description,
                          place=place,
                          date_time=date_time)
    complaint.save()
    bot.send_message(message.chat.id, 'Жалоба успешно зарегистрирована!')


def check_status(message):
    pass  # TODO: Implement function for checking the status of a complaint
