from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)


markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Список книг')],
                                       [KeyboardButton(text='Заказать книгу')],
                                       [KeyboardButton(text='Настройки')]],
                                       resize_keyboard=True,
                                       input_field_placeholder='Выберите пункт меню...')


spisok = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Пушкин',callback_data='pushkin')],
                                               [InlineKeyboardButton(text='Толстой',callback_data='tolstoy')],
                                               [InlineKeyboardButton(text='Лермонтов',callback_data='lermontov')]])


get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить номер',
                                                           request_contact=True)]],
                                            resize_keyboard=True)
