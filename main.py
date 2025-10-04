import telebot
from telebot import types

BOT_TOKEN = "8365312991:AAGxY-g9KSXMxYy8EOB1vo2tVDx064VDZHM"
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Создаем инлайн-клавиатуру
    markup = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton("Вариант 1", callback_data="option1")
    btn2 = types.InlineKeyboardButton("Вариант 2", callback_data="option2")
    btn3 = types.InlineKeyboardButton("Открыть сайт", url="https://google.com")
    btn4 = types.InlineKeyboardButton("Поделиться", switch_inline_query="Посмотри на этого бота!")

    markup.add(btn1, btn2)
    markup.add(btn3)
    markup.add(btn4)

    bot.send_message(
        message.chat.id,
        "Выберите опцию:",
        reply_markup=markup
    )


# Обработчик нажатий на инлайн-кнопки
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "option1":
        bot.answer_callback_query(call.id, "Вы выбрали вариант 1!")
        bot.send_message(call.message.chat.id, "🎉 Вы выбрали вариант 1!")
    elif call.data == "option2":
        bot.answer_callback_query(call.id, "Вы выбрали вариант 2!")
        bot.send_message(call.message.chat.id, "🚀 Вы выбрали вариант 2!")


@bot.message_handler(commands=['menu'])
def show_menu(message):
    markup = types.InlineKeyboardMarkup(row_width=2)

    items = [
        types.InlineKeyboardButton("Купить", callback_data="buy"),
        types.InlineKeyboardButton("Продать", callback_data="sell"),
        types.InlineKeyboardButton("Поддержка", callback_data="support"),
        types.InlineKeyboardButton("О нас", callback_data="about")
    ]

    markup.add(*items)

    bot.send_message(message.chat.id, "📋 Главное меню:", reply_markup=markup)

if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()