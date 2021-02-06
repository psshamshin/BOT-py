import telebot
import config
from telebot import types
from datetime import datetime

bot = telebot.TeleBot(config.TOKEN)
day_of_week = config.day_of_week
start = config.start
end = config.end
timetable = config.timetable


def gap(str1, str2):
    str1 = list(map(int, str1.split(':')))
    str2 = list(map(int, str2.split(':')))
    a = str2[0] * 60 * 60 + str2[1] * 60 + str2[2] - str1[0] * 60 * 60 - str1[1] * 60 - str1[2]
    return str(a // 3600) + ':' + str(a % 3600 // 60) + ':' + str(a % 60)


@bot.message_handler(commands=['start'])
def welcome(message):
    # markup keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    but_1 = types.KeyboardButton("☂")
    but_2 = types.KeyboardButton("⏳")
    but_3 = types.KeyboardButton("❔")

    markup.add(but_1, but_2, but_3)

    bot.send_message(message.chat.id, "Общий салам, {0.first_name} \nВремени с UNIX: {1} секунд"
                     .format(message.from_user, message.date),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def chat(message):
    current_time = datetime.fromtimestamp(message.date).strftime('%H:%M:%S')
    if message.chat.type == 'private':
        if message.text == '⏳':
            bot.send_message(message.chat.id, "Дата: {0}\nДень недели: {1}"
                             .format(datetime.fromtimestamp(message.date).strftime('%d.%m.%Y\n%H:%M:%S'),
                                     day_of_week[datetime.fromtimestamp(message.date).today().weekday()]))
            # subjects table
            flag = True
            for i in range(len(timetable[day_of_week[datetime.fromtimestamp(message.date).today().weekday()]])):
                if datetime.fromtimestamp(message.date).today().weekday() != 5 or 6:
                    bot.send_message(message.chat.id, 'чил')
                    break
                if current_time > start[i]:
                    if current_time < end[i]:
                        # lesson is going
                        bot.send_message(message.chat.id, '✅' +
                                         timetable[day_of_week[datetime.fromtimestamp(message.date).today().weekday()]]
                                         [i] + ' - ' + str(gap(current_time, end[i])) + ' до конца')
                        flag = False
                    else:
                        # end of lesson
                        bot.send_message(message.chat.id, '❌' +
                                         timetable[day_of_week[datetime.fromtimestamp(message.date).today().weekday()]]
                                         [i])
                        flag = True
                else:
                    if flag:
                        bot.send_message(message.chat.id, '✓' +
                                         timetable[day_of_week[datetime.fromtimestamp(message.date).today().weekday()]]
                                         [i] + ' - ' + str(gap(current_time, start[i])) + ' до начала')
                        flag = False
                    else:
                        bot.send_message(message.chat.id, '✓' +
                                         timetable[day_of_week[datetime.fromtimestamp(message.date).today().weekday()]]
                                         [i])
        elif message.text == '❔':
            markup2 = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Да", callback_data='good')
            item2 = types.InlineKeyboardButton("Нет", callback_data='bad')
            markup2.add(item1, item2)

            bot.send_message(message.chat.id, 'Пойди нахуй?', reply_markup=markup2)
        else:
            bot.send_message(message.chat.id, "(((нэт)))")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и отлично')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Неправильный ответ')

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="ОПА",
                                  reply_markup=None)

            # bot.answer_callback_qeury(chat_id=call.message.chat.id, show_alert=False, text = "POH")
    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)
