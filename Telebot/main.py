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



def hark_request(username, txt, less, more): # запрос текста 
    # board = choice(boards)
    # url_hk = f'https://2ch.hk/{board}/index.json'
    # r = requests.get(url_hk, headers={'Accept': 'application/json; charset=utf-8'}).json()
    if more != 7000:
        if username in known_names:
            return f'{choice(eval(username))}, {hark_soup(less,more)}'
        else:
            return f'{choice(username)}, {hark_soup(less,more)}'
    return hark_soup(less,more)


def hark_soup(less,more):
    text=''
    while len(text) < less or len(text) > more:
        time.sleep(0.3)
        pages = choice(['index','1','2'])
        board = choice(boards)
        url_hk = f'https://2ch.hk/{board}/{pages}.json'
        req = requests.get(url_hk, headers={'Accept': 'application/json; charset=utf-8'}).json()
        try:
            soup = BeautifulSoup(req['threads'][randint(1,6)]['posts'][randint(1,4)]['comment'], 'html.parser')
        except IndexError:
            continue
        text = soup.get_text(separator=u"\n")
        if not text:
            continue
        if more != 7000:
            text = re.sub(r'>.*','',text)
            if text[0] == u"\n":
                text = text[1].lower() + text[2:]
            else:
                text = text[0].lower() + text[1:]
        else:
            text = re.sub(r'(>.*)',r'<i>\1</i>',text)
    return text


def sovet_request(username, txt):
    url_sovet = 'http://fucking-great-advice.ru/api/random'
    try:
        r = requests.get(url_sovet, headers={'Accept': 'application/json; charset=utf-8'}).json()
        sovet = r['text']
    except:
        sovet = "Сегодня советочная закрыта."
    if txt:
        sovet = sovet[0].lower() + sovet[1:]
        if username in known_names:
            return f'{choice(eval(username))}, {sovet}'
        else:
            return f'{choice(username)}, {sovet}'
    else:
        return sovet


def send_message(chat_id,username,txt): # отправить сообщение в телегу
    time.sleep(randint(1,2))
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {'chat_id':chat_id, 'text':txt, 'parse_mode':'HTML'}
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
                poslovica_text = f'{choice(poslovica_nachalo_list)} {poslovica_body}{choice(poslovica_konec_list)}'
                send_message(chat_id,username,poslovica_text)
            elif any(word.lower() in txt.lower() for word in dota_trigger) and randint(1,100) < 70:
                dota_text = choice(dota_pastes)
                send_message(chat_id,username,dota_text)
            elif any(word.lower() in txt.lower() for word in old_trigger):
                send_message(chat_id,username,choice(old))
            elif any(word.lower() in txt.lower() for word in pastes_trigger) and randint(1,100) < 60:
                paste_text = choice(pastes)
                send_message(chat_id,username,paste_text)
            elif any(word in txt.lower() for word in sovet_trigger):
                sovet_text = sovet_request(username,txt)
                send_message(chat_id,username,sovet_text)
            elif any(word in txt.lower() for word in pasta_trigger):
                pasta_text = hark_request(username,txt,500,7000)
                send_message(chat_id,username,pasta_text)
            elif any(word.lower() in txt.lower() for word in hk_reply_trigger):
                text = hark_request(username,txt,3,1500)
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
                try:
                    username = answer['message']['chat']['username']
                except KeyError:
                    username = answer['message']['chat']['first_name']

            else:
                try:
                    username = answer['message']['from']['username']
                except KeyError:
                    username = answer['message']['from']['first_name']
            txt = answer['message']['text']

            return chat_id,username,txt
    return '','',''


if __name__ == "__main__":
    app.run()
