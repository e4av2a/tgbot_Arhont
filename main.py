import telebot
from telebot import types
from json_handler import ExpeditionsData

BOT_TOKEN = ""
bot = telebot.TeleBot(BOT_TOKEN)

# ссылка на анкету кандидата
url_anketa = "https://forms.gle/BoXqMuKwVwyphhn58"

expeditions_data = ExpeditionsData('history.json')

# что хотелось бы ещё:
# все большие текстовые блоки запихнуть в текстовые файлы и править при необходимости их


@bot.message_handler(commands=['start', 'restart'])
def start_dialog(message):
    chat_id = message.chat.id

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    btn1 = types.KeyboardButton("Кто вы?")
    btn2 = types.KeyboardButton("Вайб?")
    btn3 = types.KeyboardButton("А чё копаете??")
    btn4 = types.KeyboardButton("А как к вам попасть?")
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

    back_message(chat_id)


# Вайб
@bot.message_handler(func=lambda message: message.text == "Вайб?")
def vibe_message(message):
    chat_id = message.chat.id

    text = "Каждый отряд имеет свой неповторимый вайб. " \
           "Его ты сможешь ощутить, поехав с нами на сезон, " \
           "но мы попробуем передать через фотографии, музыку и видео."

    markup_inline = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("фотографии 📸", url="https://vk.com/album-47403562_304419511")
    btn2 = types.InlineKeyboardButton("музыка 🎧", url="https://vk.com/audios-47403562?z=audio_playlist-47403562_1")
    btn3 = types.InlineKeyboardButton("видео 🎞",
                                      url="https://vk.com/sao_arhont?z=video-47403562_456239114%2Fvideos-47403562%2Fpl_-47403562_-2")
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

    markup_inline = types.InlineKeyboardMarkup()
    btn_2017 = types.InlineKeyboardButton("2017 г.", callback_data="2017")
    btn_2018 = types.InlineKeyboardButton("2018 г.", callback_data="2018")

    markup_inline.add(btn_2017, btn_2018)

    bot.send_message(
        chat_id,
        "У Архонта было много экспедиций, можешь узнать про любую из них:",
        reply_markup=markup_inline,
        parse_mode='Markdown'
    )

    back_message(chat_id, mes="Можешь, конечно, назад вернуться", komissar=True)


# Информация об экспедиции за год
@bot.callback_query_handler(func=lambda call: call.data in ["2017", "2018"])
def year_of_expedition(call):
    chat_id = call.message.chat.id

    bot.send_message(
        chat_id,
        expeditions_data.get_expedition_info(int(call.data)),
        parse_mode='Markdown'
    )

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

    back_message(chat_id, "Подписывайтесь на нас!", True)


# Комиссар
@bot.message_handler(func=lambda message: message.text == "Я хочу узнать больше!")
def more_message(message):
    chat_id = message.chat.id

    text = "В отрядах есть такой общительный и весёлый человек - **комиссар**. " \
           "В Архонте это наш любимый [Дамир](https://vk.com/the.guydie) 😘 \n\n" \
           "Напишу ему, он обязательно ответит!"

    back_message(chat_id, text)


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
def back_message(chat_id, mes="Жми кнопку ниже, чтобы узнать больше...", komissar=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
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
    print("Бот запущен...")
    bot.infinity_polling()
