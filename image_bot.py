import requests
from flask import Flask, request
import telegram
from telegram.ext import Dispatcher, MessageHandler, Filters
import random
import configparser


config = configparser.ConfigParser()
config.read("config.ini")


bot = telegram.Bot(token=(config['Telegram']['token']))
app = Flask(__name__)


@app.route('/hook', methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
    return 'ok'

def reply_handler(update ,bot):
    """Reply message."""
    try:
        text = update.message.text
        if text.endswith('.jpg') or text.endswith('.png') or text.endswith('.gif'):
            url = search_image(text)
            if not text.endswith('.gif'):
                update.message.reply_photo(url)
            else:
                update.message.reply_document(url)
    except Exception as e:
        print(e)
        pass
def search_image(q):
    payload = {
    'key' :  config['GCP']['key'],
    'cx' : config['GCP']['cx'],
    'searchType': 'image',
    'num' : 10,
    'page' : 0,
    'q' : q[:-4],
    'fileType': q[-3:],
    'json' : True
    }

    url = "https://customsearch.googleapis.com/customsearch/v1"
    res = requests.get(url,params=payload)

    j = res.json()
    r = None
    try:
        items = j['items']
        r = items[random.randint(0,len(items)-1)]['link']
    except:
        print(j)
    return r

dispatcher = Dispatcher(bot, None)
dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))

if __name__ == "__main__":
    # Running server
    app.run()
