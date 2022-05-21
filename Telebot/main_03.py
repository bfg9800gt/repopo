import time
import re
import requests
import json
from flask import Flask,request,Response
from bs4 import BeautifulSoup
from random import randint, choice
from flask_sslify import SSLify

from lists import *


app = Flask(__name__)
sslify = SSLify(app)

def hark_soup(r,less,more):
    text=''
    while len(text) < less or len(text) > more:
        try:
            soup = BeautifulSoup(r['threads'][randint(1,6)]['posts'][randint(1,5)]['comment'], 'html.parser')
            text_souped = soup.get_text(separator=u"\n")
            text = re.sub(r'>.*','',text_souped)
            if not text:
                continue
            if text[0] == u"\n":
                text = text[1].lower() + text[2:]
            else:
                text = text[0].lower() + text[1:]
        except:
            continue
    return text

def hark_request(username, txt, less, more): # запрос текста 
    board = choice(boards)
    url_hk = f'https://2ch.hk/{board}/index.json'
    r = requests.get(url_hk, headers={'Accept': 'application/json; charset=utf-8'}).json()
    return f'{choice(eval(username))}, {hark_soup(r,less,more)}'


def sovet_request(username, txt):
    url_sovet = 'http://fucking-great-advice.ru/api/random'
    r = requests.get(url_sovet, headers={'Accept': 'application/json; charset=utf-8'}).json()
    sovet = r['text']
    if txt:
        sovet = sovet[0].lower() + sovet[1:]
        return f'{choice(eval(username))}, {sovet}'
    else:
        return sovet


def send_message(chat_id,username,txt): # отправить сообщение в телегу
    time.sleep(randint(1,2))
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {'chat_id':chat_id, 'text':txt}
    r = requests.post(url, json=payload)
    return r
    

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        chat_id,username,txt = parse_answer(msg)
        if txt:
            if any(word.lower() in txt.lower() for word in poslovica_trigger):
                poslovica = choice(poslovici)
                poslovica_body = poslovica[0].lower() + poslovica[1:]
                poslovica = f'{choice(poslovica_nachalo_list)} {poslovica_body}{choice(poslovica_konec_list)}'
                send_message(chat_id,username,poslovica)
            elif any(word in txt.lower() for word in sovet_trigger):
                sovet = sovet_request(username,txt)
                send_message(chat_id,username,sovet)
            elif any(word in txt.lower() for word in pasta_trigger):
                text = hark_request(username,txt,80,2000)
                send_message(chat_id,username,text)
            elif randint(1,100) < chance_to_trig:
                text = hark_request(username,txt,3,150)
                send_message(chat_id,username,text)
        return Response('OK', status=200)
    else:
        return '<h1>Вас приветствует дух Трахтенберга.</h1>'

def parse_answer(answer):
    if 'message' in answer:
        if 'text' in answer['message']:
            chat_id = answer['message']['chat']['id']
            if answer['message']['chat']['type'] == 'private':
                username = answer['message']['chat']['username']
            else:
                username = answer['message']['from']['username']
            txt = answer['message']['text']

            
            return chat_id,username,txt
    return '','',''


if __name__ == "__main__":
    app.run(debug=True)
