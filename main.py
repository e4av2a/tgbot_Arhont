import random

import telebot
from telebot import types

from json_handler import ExpeditionsData
import logging
from users_handler import load_users, add_user_in_file

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('arhont_bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

users_log = load_users()

BOT_TOKEN = ""
bot = telebot.TeleBot(BOT_TOKEN)

# ссылка на анкету кандидата
url_anketa = "https://forms.gle/BoXqMuKwVwyphhn58"

expeditions_data = ExpeditionsData('history.json')
years = ["2013 г.", "2014 г.", "2015 г.", "2016 г.", "2017 г.", "2018 г.", "2019 г.", "2020 г.", "2021 г.", "2022 г.", "2023 г.", "2024 г.", "2025 г."]

timeout = 60

# что хотелось бы ещё:
# все большие текстовые блоки запихнуть в текстовые файлы и править при необходимости их


@bot.message_handler(commands=['start', 'restart'])
def start_dialog(message):
    user = message.from_user
    user_info = f"{user.id} (@{user.username}) {user.first_name} {user.last_name}"

    welcome_text = ""

    if str(user.id) not in users_log:
        add_user_in_file(user.id)
        users_log.add(str(user.id))
        logging.info(f"НОВЫЙ ПОЛЬЗОВАТЕЛЬ: {user_info}")
        logging.info(f"Всего пользователей: {len(users_log)}")
        welcome_text = "Архонт приветствует тебя! 🥰\n\nЕсли ты любишь природу, сон в палатке и завтраки на свежем " \
                       "воздухе — тебе точно к нам! Нам интересно открывать новое, путешествовать в неизведанные " \
                       "места!\n\nХочешь узнать, где мы уже побывали и, что раскопали? — Задавай вопросы, с радостью " \
                       "на всё ответим! "
        # отправка сообщения Дамиру о новом пользователе
        bot.send_message(1275982334, f"Дамир, приффки, сейчас в бота уже зашли пользователей: {len(users_log)}\n"
                                     f"Конкретно сейчас присоединился @{user.username}")
    else:
        welcome_text = (
            "Мы студенческий археологический отряд \"Архонт\" 💀 \n"
            "Можешь выбрать вопрос..."
        )

    chat_id = message.chat.id

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    btn1 = types.KeyboardButton("Кто вы?")
    btn2 = types.KeyboardButton("Какие вы?")
    btn3 = types.KeyboardButton("А чё копаете??")
    btn4 = types.KeyboardButton("А как к вам попасть?")
    btn5 = types.KeyboardButton("Собрания и прочее...")
    markup.add(btn1, btn2, btn3, btn4, btn5)

    bot.send_message(chat_id, welcome_text, reply_markup=markup)
    logging.info(f"Команда /start от: {user_info}")


@bot.message_handler(func=lambda message: message.text == "Кто вы?")
def who_we_are(message):
    chat_id = message.chat.id

    # bot.answer_callback_query(chat_id, "Кто мы?")
    about_us = "Мы первый студенческий археологический отряд в России, " \
               "а каждое лето проводим в экспедициях, путешествуя по всей стране и даже за границей!\n\n" \
               "Выезжаем мы обычно в конце июля, а возвращаемся только к началу учёбы. " \
               "Архонт - это не только про археологию, незабываемое лето, " \
               "но и про самых близких и верных друзей."

    # bot.send_message(chat_id, about_us)

    del_mes = bot.send_message(chat_id, "Загружаем красивое фото...", parse_mode='Markdown')

    try:
        # Отправка фото из файла
        with open('images/who.jpg', 'rb') as photo:
            bot.send_photo(chat_id, photo, caption=about_us, timeout=timeout)
    except FileNotFoundError:
        bot.send_message(chat_id, about_us,
                         parse_mode='Markdown')

    bot.delete_message(chat_id, del_mes.message_id)

    back_message(chat_id)


# Вайб
@bot.message_handler(func=lambda message: message.text == "Какие вы?")
def vibe_message(message):
    chat_id = message.chat.id

    del_mes = bot.send_message(chat_id, "Загружаем красивое фото...", parse_mode='Markdown')

    random_n = random.randint(0, 43)
    try:
        # Отправка фото из файла
        with open(f'images/вайб/Вайб_{random_n}.jpg', 'rb') as photo:
            bot.send_photo(chat_id, photo,
                           caption="Вот твоя вайб фотка, которая даст заряд энергии словно чашка кофе! 🤗", timeout=timeout)
    except FileNotFoundError:
        logging.info(f"Рандомная фотография {random_n} не нашлась")

    bot.delete_message(chat_id, del_mes.message_id)

    text = "Каждый отряд имеет свой неповторимый дух. " \
           "Его ты сможешь ощутить, поехав с нами на сезон, " \
           "но мы попробуем передать через фотографии, музыку и видео."

    markup_inline = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("фотографии 📸",
                                      url="https://drive.google.com/drive/folders/1USTWWbUK9HZWwxBdQ4AMMCWa6mREYnS6?dmr=1&ec=wgc-drive-globalnav-goto")
    btn2 = types.InlineKeyboardButton("музыка 🎧",
                                      url="https://vk.com/audios-47403562?z=audio_playlist-47403562_1")
    btn3 = types.InlineKeyboardButton("видео 🎞",
                                      url="https://vk.com/sao_arhont?z=video-47403562_456239125%2Fvideos-47403562%2Fpl_-47403562_-2")
    markup_inline.add(btn1)
    markup_inline.add(btn2, btn3)

    bot.send_message(
        chat_id,
        text,
        reply_markup=markup_inline,
        parse_mode='Markdown'
    )

    back_message(chat_id)


# Чокопайки
@bot.message_handler(func=lambda message: message.text in ["А чё копаете??", "А чё ещё копаете?"])
def dig_message(message):
    chat_id = message.chat.id

    text = "У Архонта было много экспедиций, можешь узнать про любую из них"

    back_message(chat_id, mes=text, komissar=True, other_btn=years)


# Информация об экспедиции за год
@bot.message_handler(func=lambda message: message.text in years)
def year_of_expedition(message):
    chat_id = message.chat.id

    year = int(message.text[:4])
    bot.send_message(
        chat_id,
        expeditions_data.get_expedition_info(year),
        parse_mode='HTML'
    )

    del_mes = bot.send_message(chat_id, "Загружаем красивое фото...", parse_mode='Markdown')

    media = expeditions_data.get_media_album(year)
    if media is not None:
        bot.send_media_group(chat_id, media, timeout=timeout)

    bot.delete_message(chat_id, del_mes.message_id)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("А чё ещё копаете?")
    markup.add(btn1)

    bot.send_message(
        chat_id,
        "Хочешь узнать больше?",
        reply_markup=markup,
        parse_mode='Markdown'
    )


# Ссылки
@bot.message_handler(func=lambda message: message.text == "А как к вам попасть?")
def search_message(message):
    chat_id = message.chat.id

    text = "Вот ссылочки, где будут актуальные новости: "

    markup_inline = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("наш тг", url="https://t.me/CAO_arhont")
    btn2 = types.InlineKeyboardButton("наш вк", url="https://vk.com/sao_arhont")
    markup_inline.add(btn1, btn2)

    bot.send_message(
        chat_id,
        text,
        reply_markup=markup_inline,
        parse_mode='Markdown'
    )

    text2 = "А ещё заполняй анкету кандидата и с тобой обязательно свяжутся!"

    markup_inline2 = types.InlineKeyboardMarkup()
    btn3 = types.InlineKeyboardButton("анкета кандидата", url=url_anketa)
    markup_inline2.add(btn3)

    bot.send_message(
        chat_id,
        text2,
        reply_markup=markup_inline2,
        parse_mode='Markdown'
    )

    back_message(chat_id, "Подписывайтесь на нас!", True, other_btn=["Собрания и прочее..."])


# Комиссар
@bot.message_handler(func=lambda message: message.text == "Я хочу узнать больше!")
def more_message(message):
    chat_id = message.chat.id

    text = "В отрядах есть такой общительный и весёлый человек - **комиссар**. " \
           "В Архонте это наш любимый [Дамир](https://vk.com/the.guydie) 😘 \n\n" \
           "Напишу ему, он обязательно ответит!"

    back_message(chat_id, text)


# Собрания
@bot.message_handler(func=lambda message: message.text == "Собрания и прочее...")
def meeting_message(message):
    chat_id = message.chat.id

    text = "Мы не только в телеграме и вк, а очень ждём именно тебя на нашем первом собрании," \
           "которое состоится:\n\n" \
           "📍Когда? 28 октября (вторник)\n📍Во сколько?: 18:30 \n📍Где? НИК, 2.03\n\n" \
           "Больше подробностей в [группе вк](https://vk.com/sao_arhont)."

    back_message(chat_id, text, komissar=True)


@bot.message_handler(func=lambda message: message.text == "Назад")
def back_to_main(message):
    # Возвращаемся к главному меню
    start_dialog(message)


# Обработка любых других сообщений
@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    chat_id = message.chat.id

    bot.send_message(
        chat_id,
        "А кнопки для кого делали, нужно жмакать на них. \n"
        "Или для разнообразия напиши /start "
    )


# mes - сообщение перед сменой меню на кнопку "Назад"
# komissar - нужно ли выводить информацию про комиссара, по умолчанию False
# other_btn - добавление других кнопок в меню - формат list
def back_message(chat_id, mes="Жми кнопку ниже, чтобы узнать больше...", komissar=False, other_btn=None):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if other_btn is not None:
        n = len(other_btn)
        for i in range(0, n - 3, 3):
            btn1 = types.KeyboardButton(other_btn[i])
            btn2 = types.KeyboardButton(other_btn[i + 1])
            btn3 = types.KeyboardButton(other_btn[i + 2])
            markup.add(btn1, btn2, btn3)
        if n % 3 == 1:
            markup.add(types.KeyboardButton(other_btn[n - 1]))
        if n % 3 == 2:
            markup.add(types.KeyboardButton(other_btn[n - 2], other_btn[n - 1]))

    btn1 = types.KeyboardButton("Назад")
    markup.add(btn1)
    if komissar:
        btn2 = types.KeyboardButton("Я хочу узнать больше!")
        markup.add(btn2)

    bot.send_message(
        chat_id,
        mes,
        reply_markup=markup,
        parse_mode='Markdown'
    )


if __name__ == "__main__":
    logging.info("=== Бот запущен ===")
    bot.infinity_polling()
