import logging
from flask import Flask, request
import requests
from googletrans import Translator
from twilio.twiml.messaging_response import MessagingResponse
from bs4 import BeautifulSoup as BS
from gunicorn_config import PORT
import git

RANDOM_QUOTE_URL = "https://api.quotable.io/random"
RANDOM_CAT_IMG_URL = "https://cataas.com/cat"
HORSES_GENERATOR_URL = "https://generatorfun.com"
RANDOM_HORSE_PAGE = "random-horse-image"
RANDOM_HORSE_PAGE_GENERATOR_URL = f"{HORSES_GENERATOR_URL}/{RANDOM_HORSE_PAGE}"
ENGLISH_DETECTED = "en"

repo = git.Repo(search_parent_directories=True)
REPO_HEAD_SHA = repo.head.object.hexsha[:4]
TEXT2PEACE_HEADER = f"*Text2Peace* (v{REPO_HEAD_SHA})"

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
translator = Translator()


@app.route('/', methods=['GET', 'POST'])
def test():
    return f"Server running... (v{REPO_HEAD_SHA})"


@app.route('/bot', methods=['POST'])
def bot():
    resp = MessagingResponse()
    response = resp.message()
    request_body = request.values.get('Body', '')
    app.logger.debug(f"Incoming: {request.values}")
    app.logger.info(f"Incoming: {request_body}")
    incoming_msg = request_body.lower()
    understood = False
    if 'quote' in incoming_msg:
        understood = True
        handle_quote_request(response)
    if 'cat' in incoming_msg:
        understood = True
        handle_cat_request(response)
    if 'horse' in incoming_msg:
        understood = True
        handle_horse_request(response)
    if translator.detect(incoming_msg).lang != ENGLISH_DETECTED:
        understood = True
        handle_nonenglish_text(incoming_msg, response)
    if not understood:
        handle_misunderstanding(response)
    outgoing_msg = str(resp)
    app.logger.info(f"Outgoing: {response}")
    return outgoing_msg


def handle_quote_request(response):
    try:
        text = get_famous_quote()
    except Exception as probelm:
        app.logger.warning(probelm)
        text = 'I could not retrieve a quote at this time, sorry.'
    set_text(response, text)


def handle_cat_request(response):
    set_image(response, RANDOM_CAT_IMG_URL)


def handle_horse_request(response):
    try:
        horse_img_url = get_horse_img_url()
        set_image(response, horse_img_url)
    except Exception as probelm:
        app.logger.warning(probelm)
        set_text(response, "I could not retrieve a horse image this time, sorry.")


def handle_misunderstanding(response):
    set_text(response, f"{TEXT2PEACE_HEADER}\nIf you text me in a foreign language, I'll translate for you. " 
                       "Otherwise, if you ask me nicely I can send you some famous quotes, or images of cats and " 
                       "horses. That's all I can do fow now!")


def get_famous_quote():
    quote_json_page = requests.get(RANDOM_QUOTE_URL)
    if quote_json_page.status_code == 200:  # status OK
        return get_formatted_quote(quote_json_page)
    else:
        raise Exception(f"Could not get from {RANDOM_QUOTE_URL}")


def get_formatted_quote(quote_json_page):
    quote = quote_json_page.json()
    return f'{quote["content"]} ({quote["author"]})'


def get_horse_img_url():
    random_horse_page = requests.get(RANDOM_HORSE_PAGE_GENERATOR_URL)
    if random_horse_page.status_code == 200:  # status OK
        return find_horse_img_url(random_horse_page.text)
    else:
        raise Exception(f"Could not get from {RANDOM_HORSE_PAGE_GENERATOR_URL}")


def find_horse_img_url(random_horse_page_html):
    random_horse_soup = BS(random_horse_page_html, features="html.parser")
    # the first image in the page is the horse
    horse_img_path = random_horse_soup.find_all('img')[0]['src']
    return f"{HORSES_GENERATOR_URL}/{horse_img_path}"


def handle_nonenglish_text(nonenglish_text, response):
    translated_text = translator.translate(text=nonenglish_text, dest='en').text
    set_text(response, f"{TEXT2PEACE_HEADER}\n{translated_text}")


def set_image(msg, img_url):
    msg.media(img_url)


def set_text(msg, text):
    msg.body(text)


if __name__ == '__main__':
    print("bot running...")
    app.run(port=PORT)
