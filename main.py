import telebot
from telebot import types


BOT_TOKEN = "8365312991:AAGxY-g9KSXMxYy8EOB1vo2tVDx064VDZHM"
bot = telebot.TeleBot(BOT_TOKEN)

# Словарь для хранения состояния пользователя
user_data = {}


@bot.message_handler(commands=['start'])
def start_dialog(message):
    chat_id = message.chat.id
    # Сбрасываем состояние при начале нового диалога
    user_data[chat_id] = {'step': 1}

    # Первый вопрос
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Лето", callback_data="summer")
    btn2 = types.InlineKeyboardButton("Зима", callback_data="winter")
    markup.add(btn1, btn2)

    bot.send_message(
        chat_id,
        "Привет! Давай познакомимся поближе.\n\n"
        "📌 **Вопрос 1 из 3:**\n"
        "Какое время года тебе нравится больше?",
        reply_markup=markup,
        parse_mode='Markdown'
    )


@bot.callback_query_handler(func=lambda call: call.data == "restart")
def restart_dialog(call):
    chat_id = call.message.chat.id

    # ОБЯЗАТЕЛЬНО: Сбрасываем состояние пользователя
    user_data[chat_id] = {'step': 1}

    # Подтверждаем нажатие кнопки
    bot.answer_callback_query(call.id, "Начинаем заново!")

    # Первый вопрос
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Лето", callback_data="summer")
    btn2 = types.InlineKeyboardButton("Зима", callback_data="winter")
    markup.add(btn1, btn2)

    # Отправляем новое сообщение с первым вопросом
    bot.send_message(
        chat_id,
        "Отлично! Начинаем заново 🔄\n\n"
        "📌 **Вопрос 1 из 3:**\n"
        "Какое время года тебе нравится больше?",
        reply_markup=markup,
        parse_mode='Markdown'
    )


@bot.callback_query_handler(func=lambda call: call.data in ["summer", "winter", "cats", "dogs", "movies", "books"])
def handle_answers(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id

    # Инициализируем данные пользователя, если их нет
    if chat_id not in user_data:
        user_data[chat_id] = {'step': 1}

    current_step = user_data[chat_id]['step']

    if current_step == 1:
        # Обработка ответа на первый вопрос
        if call.data in ["summer", "winter"]:
            user_data[chat_id]['season'] = call.data
            user_data[chat_id]['step'] = 2

            # Подтверждение выбора
            season_map = {"summer": "Лето", "winter": "Зима"}
            bot.answer_callback_query(call.id, f"Выбрано: {season_map[call.data]}")

            # Второй вопрос (новое сообщение)
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton("Кошки", callback_data="cats")
            btn2 = types.InlineKeyboardButton("Собаки", callback_data="dogs")
            markup.add(btn1, btn2)

            bot.send_message(
                chat_id,
                f"Отлично! Ты выбрал(а) {season_map[call.data]} 🎉\n\n"
                "📌 **Вопрос 2 из 3:**\n"
                "Кто тебе больше нравится?",
                reply_markup=markup,
                parse_mode='Markdown'
            )

    elif current_step == 2:
        # Обработка ответа на второй вопрос
        if call.data in ["cats", "dogs"]:
            user_data[chat_id]['animals'] = call.data
            user_data[chat_id]['step'] = 3

            # Подтверждение выбора
            animal_map = {"cats": "Кошки", "dogs": "Собаки"}
            bot.answer_callback_query(call.id, f"Выбрано: {animal_map[call.data]}")

            # Третий вопрос (новое сообщение)
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton("Фильмы", callback_data="movies")
            btn2 = types.InlineKeyboardButton("Книги", callback_data="books")
            markup.add(btn1, btn2)

            bot.send_message(
                chat_id,
                f"Интересный выбор! {animal_map[call.data]} - это здорово! 📝\n\n"
                "📌 **Вопрос 3 из 3:**\n"
                "Что предпочитаешь в свободное время?",
                reply_markup=markup,
                parse_mode='Markdown'
            )

    elif current_step == 3:
        # Обработка ответа на третий вопрос и завершение диалога
        if call.data in ["movies", "books"]:
            user_data[chat_id]['hobby'] = call.data

            # Подтверждение выбора
            hobby_map = {"movies": "Фильмы", "books": "Книги"}
            bot.answer_callback_query(call.id, f"Выбрано: {hobby_map[call.data]}")

            # Формируем результаты
            season_map = {"summer": "Лето", "winter": "Зима"}
            animal_map = {"cats": "Кошки", "dogs": "Собаки"}
            hobby_map = {"movies": "Фильмы", "books": "Книги"}

            result_text = (
                "🎊 **Спасибо за ответы! Вот твои предпочтения:**\n\n"
                f"🌤 **Время года:** {season_map[user_data[chat_id]['season']]}\n"
                f"🐾 **Животные:** {animal_map[user_data[chat_id]['animals']]}\n"
                f"🎭 **Хобби:** {hobby_map[user_data[chat_id]['hobby']]}\n\n"
                "Было приятно с тобой пообщаться! 😊"
            )

            # Кнопка для начала заново
            markup = types.InlineKeyboardMarkup()
            restart_btn = types.InlineKeyboardButton("🔄 Начать заново", callback_data="restart")
            markup.add(restart_btn)

            bot.send_message(
                chat_id,
                result_text,
                reply_markup=markup,
                parse_mode='Markdown'
            )


@bot.message_handler(commands=['reset'])
def reset_dialog(message):
    chat_id = message.chat.id
    if chat_id in user_data:
        del user_data[chat_id]
    bot.send_message(chat_id, "Диалог сброшен. Напишите /start чтобы начать заново.")


@bot.message_handler(commands=['my_data'])
def show_my_data(message):
    chat_id = message.chat.id
    if chat_id in user_data and user_data[chat_id].get('season'):
        season_map = {"summer": "Лето", "winter": "Зима"}
        animal_map = {"cats": "Кошки", "dogs": "Собаки"}
        hobby_map = {"movies": "Фильмы", "books": "Книги"}

        data = user_data[chat_id]
        result_text = (
            "📊 **Твои сохраненные ответы:**\n\n"
            f"🌤 Время года: {season_map[data['season']]}\n"
            f"🐾 Животные: {animal_map[data.get('animals', 'Еще не ответил')]}\n"
            f"🎭 Хобби: {hobby_map[data.get('hobby', 'Еще не ответил')]}"
        )
    else:
        result_text = "У тебя нет сохраненных данных. Напиши /start чтобы начать диалог."

    bot.send_message(chat_id, result_text, parse_mode='Markdown')


# Обработка любых других сообщений
@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    chat_id = message.chat.id
    if chat_id in user_data and user_data[chat_id]['step'] > 1:
        bot.send_message(
            chat_id,
            "Пожалуйста, используй кнопки для ответов на вопросы. "
            "Или напиши /start чтобы начать заново."
        )
    else:
        bot.send_message(
            chat_id,
            "Привет! Я бот для опроса. Напиши /start чтобы начать диалог."
        )


if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()