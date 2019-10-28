#!/usr/bin/python3
import requests

url = 'https://api.binance.com/api/v1/exchangeInfo'

data = requests.get(url).json()

f = open('symbols','w')

for symbol in data['symbols']:
	f.write(symbol['symbol']+'\n')

print(len(data['symbols'])) #643 symbols