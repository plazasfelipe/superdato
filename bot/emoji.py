"""
Modulo para generar emojis en codigo UTF

"""


class EmojiEngine():
    def __init__(self):
        self.emojis = {'crying': '\U0001F622',
                       'sunglasses': '\U0001F60E', 'nerd': '\U0001F913',
                       'smile': '\U0001F642', 'ok': '\U0001F44C',
                       'neutral': '\U0001F610', 'knocked': '\U0001F635'}

    def get_emoji(self, name):
        return self.emojis[name]
