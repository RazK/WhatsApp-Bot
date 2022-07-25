from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
from bs4 import BeautifulSoup as BS
from gunicorn_config import PORT

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def test():
    return "Hello, World!"


@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if 'quote' in incoming_msg:
        # return a quote
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        msg.body(quote)
        responded = True
    if 'cat' in incoming_msg:
        # return a cat pic
        msg.media('https://cataas.com/cat')
        responded = True
    if 'horse' in incoming_msg:
        GENERATOR_FUN_BASE_URL = "https://generatorfun.com"
        GET_HORSE_PATH = "random-horse-image"
        r = requests.get(f"{GENERATOR_FUN_BASE_URL}/{GET_HORSE_PATH}")
        if r.status_code == 200:
            soup = BS(r.text, features="html.parser")    
            horse_img_path = soup.find_all('img')[0]['src']
            horse_url = f"{GENERATOR_FUN_BASE_URL}/{horse_img_path}"
            msg.media(horse_url)
            responded = True
        else:
            quote = "I could not retrieve a horse picture at this time, sorry."
            msg.body(quote)
    if not responded:
        msg.body('I only know about famous quotes, cats, and horses. Sorry!')
    return str(resp)


if __name__ == '__main__':
    print("bot running...")
    app.run(port=PORT)
