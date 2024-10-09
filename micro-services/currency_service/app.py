import requests
from flask import Flask, jsonify, Response

app = Flask(__name__)

# Function to convert price
def convert_usd(currency):
    url = 'https://api.fxratesapi.com/latest'

    response = requests.get(url)

    if response.status_code == 200:
        currency_data = response.json()
        #print(currency_data['rates'][f'{currency}'])
        return currency_data['rates'][f'{currency.upper()}']

#convert_usd('EUR')
@app.route('/currency/<string:currency>/<int:price>')
def get_currency(price, currency):
    rate = convert_usd(currency)
    converted_price = price * rate
    return jsonify({
        f'{currency.upper()}': f'{converted_price}',
        'usd'.upper(): f'{price}',
        })

app.run(host="0.0.0.0")
