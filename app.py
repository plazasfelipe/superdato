# bot.py
import requests
import json
import os

from flask import Flask, request
from bot.mind import speak
from bot.api import post_response, get_topics, get_insight, get_terms, get_insight_by_terms
from bot.emoji import EmojiEngine
from bot.options import Keyboard
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

BOT_URL = f'https://api.telegram.org/bot{os.environ["SUPERDATO_BOT_KEY"]}/'


app = Flask(__name__)

topic_selected = None


@app.route('/', methods=['POST'])
def main():
    data = request.json
    emojis = EmojiEngine()
    keyboard = Keyboard()
    topics = get_topics()

    global topic_selected

    try:
        chat_id = data['message']['chat']['id']
        message_text = data['message']['text']
        first_name = data['message']['from']['first_name']
        date = data['message']['date']
        user_id = data['message']['from']['id']
    except:
        chat_id = data['callback_query']['message']['chat']['id']
        callback_data = data['callback_query']['data']
        callback_id = data['callback_query']['id']
        date = data['callback_query']['message']['date']
        user_id = data['callback_query']['from']['id']

    post_response(user_id, date, data)

    if topic_selected is None:

        if 'message' in data.keys():
            if 'entities' in data['message'].keys():
                if message_text == '/start':
                    json_data = {
                        'chat_id': chat_id,
                        'text': f'Hola {first_name}, este es el listado de temas de los que podemos hablar',
                        'reply_markup': keyboard.topics(topics),
                    }

                elif message_text == '/ayuda':
                    json_data = {
                        'chat_id': chat_id,
                        'text': 'Este es el listado de temas de los que podemos hablar',
                        'reply_markup': keyboard.topics(topics),
                    }

                else:
                    json_data = {
                        'chat_id': chat_id,
                        'text': 'Aún no conozco ese comando',
                    }

            else:
                json_data = {
                    'chat_id': chat_id,
                    'text': f'Hola {first_name}, este es el listado de temas de los que podemos hablar',
                    'reply_markup': keyboard.topics(topics),
                }

        else:
            if callback_data == 'true':
                json_data = {
                    'chat_id': chat_id,
                    'text': 'Este es el listado de temas de los que podemos hablar',
                    'reply_markup': keyboard.topics(topics),
                }

            elif callback_data == 'false':
                json_data = {
                    'chat_id': chat_id,
                    'text': 'Bueno... me hubiese gustado que hablaramos un poco más{emoji}'.format(emoji=emojis.get_emoji('crying')),
                }

            else:
                tema = data['callback_query']['data']
                json_data = {
                    'chat_id': chat_id,
                    'text': f'Sabias que {get_insight(tema)}. \n\nQueres ver de nuevo los temas para preguntar algo mas?',
                    'reply_markup': keyboard.yes_or_no('Dale! {emoji}'.format(emoji=emojis.get_emoji('smile')),
                                                       'No, es todo por hoy{emoji}'.format(emoji=emojis.get_emoji('ok'))),
                }

                # json_data = {
                #     'callback_query_id': callback_id,
                #     'text': 'prueba de alerta',
                #     'show_alert': 'TRUE',
                # }

                # message_url = BOT_URL + 'answerCallbackQuery'
                # requests.post(message_url, json=json_data)

    else:
        json_data = {
            'chat_id': chat_id,
            'text': 'Queres hacer otra consulta',
        }
        topic_selected = None

    message_url = BOT_URL + 'sendMessage'
    requests.post(message_url, json=json_data)

    return ''


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
