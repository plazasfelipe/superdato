"""
Modulo para generar emojis en codigo UTF

"""
import json

from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


class Keyboard():
    def __buttons_per_rows(self, list_buttons, n_items):
        self.list_buttons = list_buttons
        self.n_items = n_items

        new_list = [self.list_buttons[x:x+self.n_items]
                    for x in range(0, len(self.list_buttons), self.n_items)]

        return new_list

    def yes_or_no(self, true_str, false_str):
        self.true_str = true_str
        self.false_str = false_str

        buttons = [InlineKeyboardButton(self.true_str, callback_data='true'),
                   InlineKeyboardButton(self.false_str, callback_data='false')]

        keyboard = InlineKeyboardMarkup(self.__buttons_per_rows(buttons, 2))

        return json.dumps(keyboard.to_dict())

    def graph(self, true_str, false_str):
        self.true_str = true_str
        self.false_str = false_str

        buttons = [InlineKeyboardButton(self.true_str, callback_data='graph'),
                   InlineKeyboardButton(self.false_str, callback_data='no_graph')]

        keyboard = InlineKeyboardMarkup(self.__buttons_per_rows(buttons, 2))

        return json.dumps(keyboard.to_dict())

    def topics(self, topics):
        list_topics = []
        buttons = []

        for topic in topics:
            list_topics.append(topic['topic_name'])

        for item in list_topics:
            buttons.append(InlineKeyboardButton(
                item, callback_data=item))

        keyboard = InlineKeyboardMarkup(self.__buttons_per_rows(buttons, 2))

        return json.dumps(keyboard.to_dict())
