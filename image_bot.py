import requests
from flask import Flask, request
import telegram
from telegram.ext import Dispatcher, MessageHandler, Filters
import random
import configparser
# https://api.telegram.org/bot1999866482:AAEoC-RzXTbDdkT6aAEiBOxwP6a56M1YjC0/setWebhook?url=https://47f5-2001-b011-8010-1f7f-511a-957d-3759-c8ec.ngrok.io/hook
# https://47f5-2001-b011-8010-1f7f-511a-957d-3759-c8ec.ngrok.io
config = configparser.ConfigParser()
config.read("config.ini")
bot = telegram.Bot(token=(config['TELEGRAM']['ACCESS_TOKEN']))
app = Flask(__name__)

@app.route('/hook', methods=['POST'])
def webhook_handler():
    """Set route /hook with POST method will trigger this method."""
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        # Update dispatcher process that handler to process this message
        dispatcher.process_update(update)
    return 'ok'

def reply_handler(update ,bot):
    """Reply message."""
    # print(update)
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
        'key' :  'AIzaSyCvC61kVRE8V-Q8If3NwEBzRxcF3vzOt4U',
        'cx' : "84d6a80a82edac1ae",
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
        r = items[random.randint(0, len(items)-1)]['link']
    except:
        print(j)
    return r

dispatcher = Dispatcher(bot, None)
dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))

if __name__ == "__main__":
    # Running server
    app.run(debug=True)
