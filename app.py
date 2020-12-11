from newsapi import NewsApiClient
from flask import Flask, render_template, request
from twilio.twiml.messaging_response import MessagingResponse
import pandas as pd

def get_urls(x):
    l='Here are the news that you are looking for-\n'
    for i in range(len(x)):
        l=l+str(i+1)+'. '+x[i]+'\n'
    l=l+'MADE BY RAVI'
    return l

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/recommend")
def recommend():
    query = request.args.get('query')
    newsapi=NewsApiClient(api_key='3598dccc5c4e4a09ae1fa00e4d317ccb')
    data=newsapi.get_everything(q=query,language='en',page_size=10)
    data=pd.DataFrame(data)
    r=[x['url'] for x in data.iloc[:,2]]
    if type(r)==type('string'):
        return render_template('recommend.html',query=query,r=r,t='s')
    else:
        return render_template('recommend.html',query=query,r=r,t='l')

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    query = request.form.get('Body')
    query=str(query)
    newsapi=NewsApiClient(api_key='3598dccc5c4e4a09ae1fa00e4d317ccb')
    data=newsapi.get_everything(q=query,language='en',page_size=10)
    data=pd.DataFrame(data)
    urls=[x['url'] for x in data.iloc[:,2]]
    l=get_urls(urls)
    resp = MessagingResponse()
    if len(urls)>1:
        resp.message(l)
    else:
        resp.message('Hey there!! Try with more detailed query.\n MADE BY RAVI')
    return str(resp)

if __name__ == "__main__":
    app.run()