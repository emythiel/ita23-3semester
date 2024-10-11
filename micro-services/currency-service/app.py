import requests
from flask import Flask, jsonify, Response
import currency_list

app = Flask(__name__)

# Function to convert price
def convert_usd(currency):
    url = 'https://api.fxratesapi.com/latest'

    response = requests.get(url)

    if response.status_code == 200:
        currency_data = response.json()
        return currency_data['rates'][f'{currency.upper()}']

@app.route('/currency/<string:currency>/<int:price>')
def get_currency(price, currency):
    if currency.upper() not in currency_list.currency:
        return jsonify({'error': 'invalid currency entered'}), 400

    rate = convert_usd(currency)
    converted_price = price * rate
    return jsonify({
        'currency': f'{converted_price}'
        })

app.run(host="0.0.0.0", port=5420)
