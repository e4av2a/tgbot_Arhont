import telebot
from telebot import types

BOT_TOKEN = "8365312991:AAGxY-g9KSXMxYy8EOB1vo2tVDx064VDZHM"
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'restart'])
def start_dialog(message):
    chat_id = message.chat.id

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    btn1 = types.KeyboardButton("Кто вы?")
    btn2 = types.KeyboardButton("Вайб?")
    btn3 = types.KeyboardButton("А чё копаете??")
    btn4 = types.KeyboardButton("А где вас найти?")
    btn5 = types.KeyboardButton("Собрания и прочее...")
    markup.add(btn1, btn2, btn3, btn4, btn5)

    welcome_text = (
        "Мы студенческий археологический отряд \"Архонт\" 💀 \n"
        "Можешь выбрать вопрос..."
    )

    bot.send_message(chat_id, welcome_text, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Кто вы?")
def who_we_are(message):
    chat_id = message.chat.id

    # bot.answer_callback_query(chat_id, "Кто мы?")
    about_us = "Мы первый студенческий археологический отряд в России, " \
               "а каждое лето проводим в экспедициях, путешествуя по всей стране и даже за границей!\n\n" \
               "Выезжаем мы обычно в конце июля, а возвращаемся только к началу учёбы. " \
               "Архонт - это не только про археологию, незабываемое лето, " \
               "но и про самых близких и верных друзей.\n\n"

    bot.send_message(chat_id, about_us)

    try:
        # Отправка фото из файла
        with open('images/who.jpg', 'rb') as photo:
            bot.send_photo(chat_id, photo)
    except FileNotFoundError:
        bot.send_message(chat_id, "Тут могло быть красивое фото... Но посмотри пока сам в "
                                  "[группе в вк](https://vk.com/sao_arhont)!",
                         parse_mode='Markdown')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Назад")
    markup.add(btn1)

    bot.send_message(
        chat_id,
        "Жми кнопки ниже, чтобы узнать больше...",
        reply_markup=markup,
        parse_mode='Markdown'
    )


# Вайб
@bot.message_handler(func=lambda message: message.text == "Вайб?")
def vibe_message(message):
    chat_id = message.chat.id

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Назад")
    markup.add(btn1)

    bot.send_message(
        chat_id,
        "Жми кнопки ниже, чтобы узнать больше...",
        reply_markup=markup,
        parse_mode='Markdown'
    )


# Чокопайки
@bot.message_handler(func=lambda message: message.text == "А чё копаете??")
def dig_message(message):
    chat_id = message.chat.id

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Назад")
    markup.add(btn1)

    bot.send_message(
        chat_id,
        "Жми кнопки ниже, чтобы узнать больше...",
        reply_markup=markup,
        parse_mode='Markdown'
    )


# Ссылки
@bot.message_handler(func=lambda message: message.text == "А где вас найти?")
def search_message(message):
    chat_id = message.chat.id

    text = "Вот наш тг: [ссылочка](https://t.me/CAO_arhont) \n" \
           "Вот наш вк: [ссылочка](https://vk.com/sao_arhont)"

    # здесь можно перейти на инлайн-кнопки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Назад")
    markup.add(btn1)

    bot.send_message(
        chat_id,
        text,
        reply_markup=markup,
        parse_mode='Markdown'
    )


# Комиссар
@bot.message_handler(func=lambda message: message.text == "Я хочу узнать больше!")
def more_message(message):
    chat_id = message.chat.id

    text = "В отрядах есть такой общительный и весёлый человек - **комиссар**. " \
           "В Архонте это наш любимый [Дамир](https://vk.com/the.guydie) 😘 \n\n" \
           "Напишу ему, он обязательно ответит!"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Назад")
    markup.add(btn1)

    bot.send_message(
        chat_id,
        text,
        reply_markup=markup,
        parse_mode='Markdown'
    )


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


if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()
