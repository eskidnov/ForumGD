# -*- coding: utf-8 -*-

import telebot
import config
import utils

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def start(message):
    print('Бот запущен пользователем', message.from_user.id)
    bot.send_message(message.chat.id, config.main_menu, parse_mode='markdown', reply_markup=main_menu_keyboard)

@bot.message_handler(commands=['help'])
def start(message):
    print('Пользоватль', message.from_user.id, 'открыл список комманд')
    msg = '/start - запустить бота\n/help - отобразить список доступных команд'
    bot.send_message(message.chat.id, msg, parse_mode='markdown', reply_markup=hidden_keyboard)

@bot.message_handler(func=lambda item: item.text == config.back_button, content_types=['text'])
def back(message):
    """
    Возврат в меню (кнопка "Назад")
    :param message: Сообщение о нажатой кнопке
    """
    print('Пользователь', message.from_user.id, 'вернулся в основное меню')
    bot.send_message(message.chat.id, config.main_menu, reply_markup=main_menu_keyboard)

@bot.message_handler(func=lambda item: item.text == config.main_menu_keyboard[0], content_types=['text'])
def about_forum(message):
    """
    Обработка нажатия на кнопку "О форуме"
    :param message: Сообщение о нажатой кнопке
    """
    print('Пользователь', message.from_user.id, 'открыл "О форуме"')
    bot.send_message(message.chat.id, '*'+config.main_menu_keyboard[0]+'*', parse_mode='Markdown')
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(telebot.types.KeyboardButton(text=config.location))
    keyboard.add(telebot.types.KeyboardButton(text=config.back_button))
    for msg in config.description:
        bot.send_message(message.chat.id, msg, reply_markup=keyboard, parse_mode='Markdown')

@bot.message_handler(func=lambda item: item.text == config.location, content_types=['text'])
def location(message):
    """
    Обработка нажатия на кнопку "Местоположение"
    :param message: Сообщение о нажатой кнопке
    """
    print('Пользователь', message.from_user.id, 'открыл "Местоположение"')
    bot.send_location(message.chat.id, 55.757977, 37.615315, reply_markup=back_keyboard)

@bot.message_handler(func=lambda item: item.text == config.main_menu_keyboard[1], content_types=['text'])
def table(message):
    """
    Обработка нажатия на кнопку "Расписание"
    :param message: Сообщение о нажатой кнопке
    """
    print('Пользователь', message.from_user.id, 'открыл "Расписание"')
    table_keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    buttons = (telebot.types.InlineKeyboardButton(text=button_text, callback_data=button_text)
               for button_text in config.dates)
    table_keyboard.add(*buttons)
    bot.send_message(message.chat.id, '*'+config.main_menu_keyboard[1]+'*', reply_markup=table_keyboard,
                     parse_mode='Markdown')

    now_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    now_keyboard.add(telebot.types.KeyboardButton(text=config.now))
    now_keyboard.add(telebot.types.KeyboardButton(text=config.back_button))
    bot.send_message(message.chat.id, config.now_msg, reply_markup=now_keyboard)

@bot.callback_query_handler(func=lambda query: query.data == config.dates[0])
def november20(query):
    """
    Обработка нажатия на кнопку "20 ноября"
    :param query: Запрос на вывод расписания на 20 ноября
    """
    print('Пользователь', query.from_user.id, 'открыл расписание на 20 ноября"')
    bot.answer_callback_query(query.id)
    bot.delete_message(query.message.chat.id, query.message.message_id+1)
    bot.edit_message_text(utils.table(query.data), query.message.chat.id, query.message.message_id,
                          parse_mode='Markdown')
    bot.send_message(query.message.chat.id, config.menu_return, reply_markup=back_keyboard)

@bot.callback_query_handler(func=lambda query: query.data == config.dates[1])
def november21(query):
    """
    Обработка нажатия на кнопку "21 ноября"
    :param query: Запрос на вывод расписания на 21 ноября
    """
    print('Пользователь', query.from_user.id, 'открыл расписание на 21 ноября"')
    bot.answer_callback_query(query.id)
    bot.delete_message(query.message.chat.id, query.message.message_id+1)
    bot.edit_message_text(utils.table(query.data), query.message.chat.id, query.message.message_id,
                          parse_mode='Markdown')
    bot.send_message(query.message.chat.id, config.menu_return, reply_markup=back_keyboard)

@bot.message_handler(func=lambda item: item.text == config.now, content_types=['text'])
def now(message):
    """
    Обработка нажатия на кнопку "Что происходит сейчас?"
    :param message: Сообщение о нажатой кнопке
    """
    print('Пользователь', message.from_user.id, 'открыл "Что происходит сейчас?"')
    bot.send_message(message.chat.id, utils.now(), parse_mode='Markdown', reply_markup=back_keyboard)



@bot.message_handler(func=lambda item: item.text == config.main_menu_keyboard[2], content_types=['text'])
def speakers(message):
    """
    Обработка нажатия на кнопку "Спикеры"
    :param message: Сообщение о нажатой кнопке
    """
    print('Пользователь', message.from_user.id, 'открыл "Спикеры"')
    speakers_keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    buttons = (telebot.types.InlineKeyboardButton(text=button_text, callback_data='s_' + button_text)
               for button_text in config.dates)
    speakers_keyboard.add(*buttons)
    speakers_keyboard.add(telebot.types.InlineKeyboardButton(text=config.deputates, callback_data=config.deputates))
    bot.send_message(message.chat.id, '*'+config.main_menu_keyboard[2]+'*', reply_markup=speakers_keyboard,
                     parse_mode='Markdown')

    bot.send_message(message.chat.id, config.menu_return, reply_markup=back_keyboard)

@bot.callback_query_handler(func=lambda query: query.data == 's_'+config.dates[0])
def speakers_november20(query):
    """
    Обработка нажатия на кнопку "20 ноября"
    :param query: Запрос на вывод таблицы спикеров на 20 ноября
    """
    chat_id = query.message.chat.id
    print('Пользователь', query.from_user.id, 'открыл расписание на 20 ноября"')
    bot.answer_callback_query(query.id)
    bot.delete_message(chat_id, query.message.message_id+1)
    bot.delete_message(chat_id, query.message.message_id)
    speakers = utils.speakers(config.dates[0])
    for speaker in range(len(speakers)):
        bot.send_message(chat_id, '*'+speakers[speaker][0]+'*', parse_mode='Markdown')
        bot.send_photo(chat_id, speakers[speaker][2], caption=speakers[speaker][1])
    bot.send_message(chat_id, config.menu_return, reply_markup=back_keyboard)


@bot.callback_query_handler(func=lambda query: query.data == 's_'+config.dates[1])
def speakers_november21(query):
    """
    Обработка нажатия на кнопку "21 ноября"
    :param query: Запрос на вывод таблицы спикеров на 21 ноября
    """
    chat_id = query.message.chat.id
    print('Пользователь', query.from_user.id, 'открыл расписание на 21 ноября"')
    bot.answer_callback_query(query.id)
    bot.delete_message(chat_id, query.message.message_id + 1)
    bot.delete_message(chat_id, query.message.message_id)
    speakers = utils.speakers(config.dates[1])
    for speaker in range(len(speakers)):
        bot.send_message(chat_id, '*' + speakers[speaker][0] + '*', parse_mode='Markdown')
        bot.send_photo(chat_id, speakers[speaker][2], caption=speakers[speaker][1])
    bot.send_message(chat_id, config.menu_return, reply_markup=back_keyboard)

@bot.callback_query_handler(func=lambda query: query.data == config.deputates)
def speakers_deputates(query):
    """
    Обработка нажатия на кнопку "Депутаты"
    :param query: Запрос на вывод таблицы депутатов
    """
    chat_id = query.message.chat.id
    print('Пользователь', query.from_user.id, 'открыл расписание депутатов"')
    bot.answer_callback_query(query.id)
    bot.delete_message(query.message.chat.id, query.message.message_id+1)
    bot.delete_message(chat_id, query.message.message_id)
    speakers = utils.deputates()
    for topic in range(len(speakers)):
        bot.send_message(chat_id, '*' + speakers[topic][0] + '*', parse_mode='Markdown')
        for speaker in speakers[topic]:
            if speaker != speakers[topic][0]:
                bot.send_photo(chat_id, speaker[1], caption=speaker[0])
    bot.send_message(chat_id, config.menu_return, reply_markup=back_keyboard)



@bot.message_handler(func=lambda item: item.text == config.main_menu_keyboard[3], content_types=['text'])
def FAQ(message):
    """
    Обработка нажатия на кнопку "Организационные вопросы"
    :param message: Сообщение о нажатой кнопке
    """
    print('Пользователь', message.from_user.id, 'открыл "Организационные вопросы"')
    chat_id = message.chat.id
    bot.send_message(chat_id, '*'+config.main_menu_keyboard[3]+'*', reply_markup=back_keyboard,
                     parse_mode='Markdown')
    for text in config.FAQ:
        question = '*Вопрос:*\n' + text
        answer = '*Ответ:*\n' + config.FAQ[text][0]
        bot.send_message(chat_id, question+'\n'+answer, parse_mode='Markdown')
        bot.send_location(chat_id, config.FAQ[text][1], config.FAQ[text][2])
        #bot.send_message(message.chat.id, answer, parse_mode='Markdown')

@bot.message_handler(func=lambda item: item.text == config.main_menu_keyboard[4], content_types=['text'])
def contacts(message):
    """
    Обработка нажатия на кнопку "Контакты"
    :param message: Сообщение о нажатой кнопке
    """
    chat_id = message.chat.id
    print('Пользователь', message.from_user.id, 'открыл "Контакты"')
    bot.send_message(chat_id, '*'+config.main_menu_keyboard[4]+'*', reply_markup=back_keyboard, parse_mode='Markdown')
    bot.send_message(chat_id, config.contacts, parse_mode='Markdown', disable_web_page_preview=True)

@bot.message_handler(func=lambda item: item.text == config.main_menu_keyboard[5], content_types=['text'])
def offers(message):
    """
    Обработка нажатия на кнопку "Предложения"
    :param message: Сообщение о нажатой кнопке
    """
    print('Пользователь', message.from_user.id, 'открыл "Предложения"')
    back_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    back_keyboard.add(telebot.types.KeyboardButton(text=config.back_button))
    bot.send_message(message.chat.id, '*'+config.main_menu_keyboard[5]+'*', reply_markup=hidden_keyboard,
                     parse_mode='Markdown')
    bot.send_message(message.chat.id, config.cancel)
    bot.send_message(message.chat.id, config.name)
    bot.register_next_step_handler(message, process_name_step)

def process_name_step(message):
    try:
        chat_id = message.chat.id
        if not (('/start' in message.text) or ('/help' in message.text)):
            name = message.text
            user = User(name)
            user_dict[chat_id] = user
            bot.send_message(chat_id, config.contact)
            bot.register_next_step_handler(message, process_contact_step)
    except Exception:
        bot.reply_to(message, config.error)

def process_contact_step(message):
    try:
        chat_id = message.chat.id
        if not (('/start' in message.text) or ('/help' in message.text)):
            contact = message.text
            user = user_dict[chat_id]
            user.contact = contact
            bot.send_message(chat_id, config.offer)
            bot.register_next_step_handler(message, process_offer_step)
    except Exception:
        bot.reply_to(message, config.error)

def process_offer_step(message):
    try:
        chat_id = message.chat.id
        if not (('/start' in message.text) or ('/help' in message.text)):
            offer = message.text
            user = user_dict[chat_id]
            user.offer = offer
            msg = user.name + '\n' + user.contact + '\n' + user.offer
            bot.send_message(config.chanel, msg)
            bot.send_message(chat_id, config.thanks.format(user.name, user.contact), parse_mode='Markdown',
                             reply_markup=back_keyboard)
    except Exception:
        bot.reply_to(message, config.error)

@bot.message_handler(func=lambda item: item.text == config.main_menu_keyboard[6], content_types=['text'])
def volonteers(message):
    """
    Обработка нажатия на кнопку "Команды"
    :param message: Сообщение о нажатой кнопке
    """
    chat_id = message.chat.id
    print('Пользователь', message.from_user.id, 'открыл "Команды"')
    bot.send_message(chat_id, '*' + config.main_menu_keyboard[6] + '*', parse_mode='Markdown')
    bot.send_message(chat_id, utils.volonteers(), parse_mode='HTML', reply_markup=back_keyboard,
                     disable_web_page_preview=True)

@bot.message_handler(func=lambda item: item.text == config.main_menu_keyboard[7], content_types=['text'])
def developers(message):
    """
    Обработка нажатия на кнопку "Разработчики"
    :param message: Сообщение о нажатой кнопке
    """
    chat_id = message.chat.id
    print('Пользователь', message.from_user.id, 'открыл "Разработчики"')
    bot.send_message(chat_id, '*'+config.main_menu_keyboard[7]+'*', parse_mode='Markdown')
    bot.send_photo(chat_id, config.botograth_logo, caption=config.botograth_caption, reply_markup=back_keyboard)
    bot.send_message(chat_id, config.our_contacts, parse_mode='Markdown')

@bot.message_handler(content_types=['photo'])
def add_speaker_photo(message):
    print(message.photo[0].file_id)

if __name__ == '__main__':
    main_menu_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = (telebot.types.KeyboardButton(text=button_text) for button_text in config.main_menu_keyboard
               if config.main_menu_keyboard.index(button_text) < 6)
    main_menu_keyboard.add(*buttons)
    main_menu_keyboard.row(config.main_menu_keyboard[6])
    main_menu_keyboard.row(config.main_menu_keyboard[7])

    back_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    back_keyboard.add(telebot.types.KeyboardButton(text=config.back_button))

    hidden_keyboard = telebot.types.ReplyKeyboardRemove()

    class User:
        def __init__(self, name):
            self.name = name
            self.contact = None
            self.offers = None

    user_dict = {}

    bot.polling(none_stop=True)


