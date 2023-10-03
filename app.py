from flask import Flask,request,render_template
from datetime import date
import requests
import json

global apikey,host

apikey = "PASTE YOUR API KEY HERE"
host = "google-translate1.p.rapidapi.com"

def list_all_languages():
    url = "https://google-translate1.p.rapidapi.com/language/translate/v2/languages"
    headers = {
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": host
    }
    response = requests.request("GET", url, headers=headers)
    return response.text

def detect_language(text):
    url = "https://google-translate1.p.rapidapi.com/language/translate/v2/detect"
    text = text.replace(' ','%20')
    payload = f"q={text}"
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": host
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    return response.text

def translatetext(text,l2,l1='en'):
    url = "https://google-translate1.p.rapidapi.com/language/translate/v2"
    text = text.replace(' ','%20')
    payload = f"q={text}&target={l2}&source={l1}"
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": host
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    return response.text


#### Defining Flask App
app = Flask(__name__)


#### Saving Date today in 2 different formats
datetoday = date.today().strftime("%m_%d_%y")
datetoday2 = date.today().strftime("%d-%B-%Y")

#### Our main page
@app.route('/')
def home():
    return render_template('home.html',datetoday2=datetoday2,res='')

@app.route('/translate',methods=['POST'])
def translate():
    input_text = request.form['sourcetext']
    targetlang = request.form['languages']
    input_lang = json.loads(detect_language(input_text))['data']['detections'][0][0]['language']
    res = translatetext(input_text,targetlang,input_lang)
    res = json.loads(res)
    res = res['data']['translations'][0]['translatedText']
    return render_template('home.html',datetoday2=datetoday2,res=res)


#### Our main function which runs the Flask App
if __name__ == '__main__':
    app.run(debug=True)
