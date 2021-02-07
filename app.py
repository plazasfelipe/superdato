# bot.py
import requests
import json
import os

from flask import Flask, request
from bot.api import post_response, get_topics, get_insight
from bot.emoji import EmojiEngine
from bot.options import Keyboard
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

BOT_URL = f'https://api.telegram.org/bot{os.environ["SUPERDATO_BOT_KEY"]}/'


app = Flask(__name__)

insight_graph = None


@app.route('/', methods=['POST'])
def main():
    data = request.json
    emojis = EmojiEngine()
    keyboard = Keyboard()
    topics = get_topics()

    global insight_graph

    try:
        chat_id = data['message']['chat']['id']
        message_text = data['message']['text']
        first_name = data['message']['from']['first_name']
        date = data['message']['date']
        user_id = data['message']['from']['id']
    except:
        chat_id = data['callback_query']['message']['chat']['id']
        callback_data = data['callback_query']['data']
        #callback_id = data['callback_query']['id']
        date = data['callback_query']['message']['date']
        user_id = data['callback_query']['from']['id']

    post_response(user_id, date, data)

    if insight_graph is None:

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
                        'text': 'Aún no conozco ese comando... {emoji}'.format(emoji=emojis.get_emoji('knocked')),
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
                topic_selected = data['callback_query']['data']
                insight = get_insight(topic_selected)
                insight_selected = insight[0]
                insight_graph = insight[1]

                json_data = {
                    'chat_id': chat_id,
                    'text': f'Sabias que {insight_selected}. \n\nTe gustaría graficar esto en una serie de tiempo?',
                    'reply_markup': keyboard.graph('Dale! {emoji}'.format(emoji=emojis.get_emoji('nerd')),
                                                        'Mmm... No {emoji}'.format(emoji=emojis.get_emoji('neutral'))),
                }

                # json_data = {
                #     'callback_query_id': callback_id,
                #     'text': 'prueba de alerta',
                #     'show_alert': 'TRUE',
                # }

                # message_url = BOT_URL + 'answerCallbackQuery'
                # requests.post(message_url, json=json_data)

    else:
        if callback_data == 'graph':
            json_data = {
                'chat_id': chat_id,
                'photo': f'https://superdato-img.s3.amazonaws.com/{insight_graph}',
            }
            message_url = BOT_URL + 'sendPhoto'
            requests.post(message_url, json=json_data)
            

            json_data = {
                'chat_id': chat_id,
                'text': 'Querés hacer otra consulta?',
                'reply_markup': keyboard.yes_or_no('Si! {emoji}'.format(emoji=emojis.get_emoji('smile')),
                                                    'No, es todo por ahora {emoji}'.format(emoji=emojis.get_emoji('ok'))),
            }

            insight_graph = None

        else:
            json_data = {
                'chat_id': chat_id,
                'text': 'Querés hacer otra consulta?',
                'reply_markup': keyboard.yes_or_no('Si! {emoji}'.format(emoji=emojis.get_emoji('smile')),
                                                    'No, es todo por ahora {emoji}'.format(emoji=emojis.get_emoji('ok'))),
            }
            insight_graph = None

    message_url = BOT_URL + 'sendMessage'
    requests.post(message_url, json=json_data)

    return ''


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
