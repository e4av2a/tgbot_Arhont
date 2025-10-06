import telebot
from telebot import types

BOT_TOKEN = "8365312991:AAGxY-g9KSXMxYy8EOB1vo2tVDx064VDZHM"
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'restart'])
def start_dialog(message):
    chat_id = message.chat.id

    # Первый вопрос
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Кто вы?", callback_data="who")
    btn2 = types.InlineKeyboardButton("Вайб?", callback_data="vibe")
    btn3 = types.InlineKeyboardButton("А чё копаете??", callback_data="dig")
    btn4 = types.InlineKeyboardButton("А где вас найти?", callback_data="search")
    btn5 = types.InlineKeyboardButton("Собрания и прочее...", callback_data="other")

    markup.add(btn1, btn2, btn3)
    markup.add(btn4)
    markup.add(btn5)

    bot.send_message(
        chat_id,
        "Мы студенческий археологический отряд \"Архонт\" 💀 \n"
        "Можешь выбрать вопрос...",
        reply_markup=markup,
        parse_mode='Markdown'
    )


@bot.callback_query_handler(func=lambda call: call.data in ["who", "vibe", "dig", "search", "other", "question"])
def who_we_are(call):
    chat_id = call.message.chat.id

    btn1 = types.InlineKeyboardButton("Кто вы?", callback_data="who")
    btn2 = types.InlineKeyboardButton("Вайб?", callback_data="vibe")
    btn3 = types.InlineKeyboardButton("А чё копаете??", callback_data="dig")
    btn4 = types.InlineKeyboardButton("А где вас найти?", callback_data="search")
    btn5 = types.InlineKeyboardButton("Собрания и прочее...", callback_data="other")
    btn6 = types.InlineKeyboardButton("Я хочу задать другие вопросы!", callback_data="question")

    # Кто мы?
    if call.data == "who":
        bot.answer_callback_query(call.id, "Кто мы?")
        about_us = "Мы первый студенческий археологический отряд в России, " \
                   "а каждое лето проводим в экспедициях, путешествуя по всей стране и даже за границей!\n\n" \
                   "Выезжаем мы обычно в конце июля, а возвращаемся только к началу учёбы. " \
                   "Архонт - это не только про археологию, незабываемое лето, " \
                   "но и про самых близких и верных друзей.\n\n"

        markup = types.InlineKeyboardMarkup()
        markup.add(btn2, btn3)
        markup.add(btn4)
        markup.add(btn5)

        bot.send_message(chat_id, about_us)

        try:
            # Отправка фото из файла
            with open('images/who.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo)
        except FileNotFoundError:
            bot.send_message(chat_id, "Тут могло быть красивое фото... Но посмотри пока сам в "
                                      "[группе в вк](https://vk.com/sao_arhont)!",
                             parse_mode='Markdown')

        bot.send_message(
            chat_id,
            "Жми кнопки ниже, чтобы узнать больше...",
            reply_markup=markup,
            parse_mode='Markdown'
        )
    # Чокопайки
    elif call.data == "dig":
        bot.answer_callback_query(call.id, "Сейчас расскажем, что копаем, хихихи")

        markup = types.InlineKeyboardMarkup()
        markup.add(btn1, btn2)
        markup.add(btn4)
        markup.add(btn5)

        bot.send_message(
            chat_id,
            "Жми кнопки ниже, чтобы узнать больше...",
            reply_markup=markup,
            parse_mode='Markdown'
        )
    # Вайб
    elif call.data == "vibe":
        bot.answer_callback_query(call.id, "Наш вайб...")

        markup = types.InlineKeyboardMarkup()
        markup.add(btn1, btn3)
        markup.add(btn4)
        markup.add(btn5)

        bot.send_message(
            chat_id,
            "Жми кнопки ниже, чтобы узнать больше...",
            reply_markup=markup,
            parse_mode='Markdown'
        )
    # Ссылки
    elif call.data == "search":

        text = "Вот наш тг: [ссылочка](https://t.me/CAO_arhont) \n" \
               "Вот наш вк: [ссылочка](https://vk.com/sao_arhont)"

        markup = types.InlineKeyboardMarkup()
        markup.add(btn1, btn2, btn3)
        markup.add(btn5)
        markup.add(btn6)

        bot.send_message(
            chat_id,
            text,
            reply_markup=markup,
            parse_mode='Markdown'
        )
    # Собрания
    elif call.data == "other":
        bot.answer_callback_query(call.id, "Так приятно, что Вы хотите узнать больше!")

        text = "пу пу пу кнопка ещё не прописана"

        markup = types.InlineKeyboardMarkup()
        markup.add(btn1, btn2, btn3)
        markup.add(btn4)
        markup.add(btn6)

        bot.send_message(
            chat_id,
            text,
            reply_markup=markup,
            parse_mode='Markdown'
        )
    # Комиссар
    elif call.data == "question":
        bot.answer_callback_query(call.id, "Так приятно, что Вы хотите узнать больше!")

        text = "В отрядах есть такой общительный и весёлый человек - **комиссар**. " \
               "В Архонте это наш любимый [Дамир](https://vk.com/the.guydie) 😘 \n\n" \
               "Напишу ему, он обязательно ответит!"

        markup = types.InlineKeyboardMarkup()
        markup.add(btn1, btn2, btn3)
        markup.add(btn4)
        markup.add(btn5)

        bot.send_message(
            chat_id,
            text,
            reply_markup=markup,
            parse_mode='Markdown'
        )


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
