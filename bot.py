import telebot
import config
from telebot import types
from datetime import datetime

bot = telebot.TeleBot(config.TOKEN)
day_of_week = config.day_of_week
start = config.start
end = config.end
timetable = config.timetable1


def gap(str1, str2):
    str1 = list(map(int, str1.split(':')))
    str2 = list(map(int, str2.split(':')))
    a = str2[0] * 60 * 60 + str2[1] * 60 + str2[2] - str1[0] * 60 * 60 - str1[1] * 60 - str1[2]
    return str(a // 3600) + ':' + str(a % 3600 // 60) + ':' + str(a % 60)


@bot.message_handler(commands=['start'])
def welcome(message):
    # markup keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    but_1 = types.KeyboardButton("✉")
    but_2 = types.KeyboardButton("⏳")
    but_3 = types.KeyboardButton("❔")
    but_4 = types.KeyboardButton("✒")
    but_5 = types.KeyboardButton("✏")

    markup.add(but_1, but_2, but_3, but_4, but_5)

    bot.send_message(message.chat.id, "Общий салам, {0.first_name} \nВремени с UNIX: {1} секунд"
                     .format(message.from_user, message.date + 10800),
                     parse_mode='html', reply_markup=markup)
    bot.send_message(message.chat.id, 'Функции бота:\n✉ - расписание (фото)\n⏳ - динамическое расписание\n❔ - ВАПРОС'
                                      '\n✒ - Spooky-dance\n✏ - список программ')


@bot.message_handler(content_types=['text'])
def chat(message):
    current_date_of_week = datetime.fromtimestamp(message.date + 10800).today().weekday()
    current_time = datetime.fromtimestamp(message.date + 10800).strftime('%H:%M:%S')
    if message.chat.type == 'private':
        if message.text == '⏳':
            bot.send_message(message.chat.id, "Дата: {0}\nДень недели: {1}"
                             .format(datetime.fromtimestamp(message.date + 10800).strftime('%d.%m.%Y\n%H:%M:%S'),
                                     day_of_week[datetime.fromtimestamp(message.date + 10800).weekday()]))
            # subjects table
            flag = True
            for i in range(len(timetable[day_of_week[datetime.fromtimestamp(message.date + 10800).weekday()]])):
                if current_date_of_week == 5 or current_date_of_week == 6:
                    bot.send_message(message.chat.id, 'чил')
                    break
                if current_time > start[i]:
                    if current_time < end[i]:
                        # lesson is going
                        bot.send_message(message.chat.id, '✅' +
                                         timetable[day_of_week[datetime.fromtimestamp(message.date + 10800).
                                         weekday()]][i] + ' - ' + str(gap(current_time, end[i])) + ' до конца')
                        flag = False
                    else:
                        # end of lesson
                        bot.send_message(message.chat.id, '❌' +
                                         timetable[day_of_week[datetime.fromtimestamp(message.date + 10800).weekday()]][i])
                        flag = True
                else:
                    if flag:
                        bot.send_message(message.chat.id, '✓' +
                                         timetable[day_of_week[
                                             datetime.fromtimestamp(message.date + 10800).weekday()]][i] + ' - ' +
                                         str(gap(current_time, start[i])) + ' до начала')
                        flag = False
                    else:
                        bot.send_message(message.chat.id, '✓' +
                                         timetable[day_of_week[
                                             datetime.fromtimestamp(message.date + 10800).weekday()]][i])
        elif message.text == '❔':
            markup2 = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Да", callback_data='good')
            item2 = types.InlineKeyboardButton("Нет", callback_data='bad')
            markup2.add(item1, item2)

            bot.send_message(message.chat.id, 'Пойди нахуй?', reply_markup=markup2)
        elif message.text == '✒':
            bot.send_animation(chat_id=message.chat.id, animation='https://i.gifer.com/O9Yw.gif')
        elif message.text == '✏':
            bot.send_message(message.chat.id, 'Команды:\n/random - рандомное значение кубика\n/poll - голосование\n'
                                              '/voice - голосовое\n/send_action - поставить статус')
        elif message.text == '/voice':
            bot.send_voice(chat_id=message.chat.id,
                           voice='https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3',
                           caption="ЛОЛ")
        elif message.text == '/random':
            bot.send_dice(chat_id=message.chat.id, emoji='🎲')
        elif message.text == '/poll':
            bot.send_poll(chat_id=message.chat.id, question='Лох', options=['да', 'да', 'да'])
        elif message.text == '/send_action':
            # bot.send_chat_action(chat_id=message.chat.id, action='typing')
            bot.send_poll(chat_id=message.chat.id, question='Тип статуса', options=['пишет...', 'не пишет...', 'да'])
        elif message.text == '✉':
            bot.send_photo(chat_id=message.chat.id, photo='https://sun9-47.userapi.com/impg/b_EUaMN45'
                                                          '-EtPfd6WpaVGw1_kszLS5j8SQeMZg/xq6vTxs9dhk.jpg?size'
                                                          '=1218x1624&quality=96&proxy=1&sign'
                                                          '=4ad3ec8afbbacbfcd75253b9e3777c50&type=album')
            bot.send_photo(chat_id=message.chat.id, photo='https://sun9-34.userapi.com/impg'
                                                          '/Rbrca4CUrtppbhh8IXQe4lThb5pyHQ8S4wTWrA/4tB7ixGmuQo.jpg'
                                                          '?size=1218x1624&quality=96&proxy=1&sign'
                                                          '=fd4101f0b0a76f36a877e16c401b4b24&type=album')
        else:
            bot.send_message(message.chat.id, 'непонял')

            # bot.send_video_note(chat_id=message.chat.id, video_note='')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и отлично')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Неправильный ответ')

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='ОПА',
                                  reply_markup=None)
            # bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            # bot.answer_callback_qeury(chat_id=call.message.chat.id, show_alert=False, text = "POH")
    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)
