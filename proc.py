#!/usr/bin/python3 -W ignore

import os, requests, json, time, datetime, multiprocessing, datetime, subprocess
from pprint import pprint

#create date wise directories inside json and data directories to hold json dump and minute wise data
dirname = datetime.datetime.now().strftime("%d%B") #ex: 27October

#create directory if it doesnt exist
if not os.path.exists('json/'+dirname): os.mkdir('json/'+dirname)
if not os.path.exists('data/'+dirname): os.mkdir('data/'+dirname)

fname = datetime.datetime.now().strftime("%d%B")+'.csv'

logfile = 'logs/log_'+fname

if os.path.exists(logfile): os.remove(logfile)

def get_hist_data(market):
	#fetch 1m tick data for past 1000 minutes
	url = 'https://api.binance.com/api/v1/klines?symbol='+market+'&interval=1m&limit=1000'
	output = requests.get(url,verify=False).json()
	return {x[0]: x[1:6] for x in output}

def get_data(market,duration=None):
	#duration is in minutes
	data = get_hist_data(market)
	# data = {}

    #if duration is not set this part will be skipped and only historic data will be taken
	if duration:
		t_end = time.time() + 60 * duration

		while time.time() < t_end:

			url = 'https://api.binance.com/api/v1/klines?symbol='+market+'&interval=1m&limit=5'
			resp = requests.get(url)

			if resp.status_code != 200:
				print(market,resp.status_code)
			else:
				output = requests.get(url).json()[0][:6]
				key = output[0]
				data[output[0]] = output[1:]
				dt = datetime.datetime.fromtimestamp(int(key)/1000).strftime("%Y-%m-%d %H:%M:%S")
				Openn(rawdata,'a').write("{},{},{},{}".format(market,key,dt,','.join(output[1:]))+'\n')

				#wait for 30 sec before querying the API again
				time.sleep(30)

	#dump data dictionary to file. overwrite file if exists. one file per market per date
	fname = datetime.datetime.now().strftime("{}_%d%B".format(market))+'.json'

	open('json/'+dirname+'/'+fname,'w').write(json.dumps(data))

	# #check for missing timestamps in data
	tstamps = [int(x) for x in list(data.keys())]
	values = list(data.values())

	start = tstamps[0]
	end = tstamps[-1]

	start_dt = datetime.datetime.fromtimestamp(int(start)/1000).strftime("%Y-%m-%d %H:%M:%S")
	end_dt = datetime.datetime.fromtimestamp(int(end)/1000).strftime("%Y-%m-%d %H:%M:%S")

	exp = int((end - start)/60000) + 1
	cap = len(tstamps)

	#finds the difference of range function and tstamps list
	missing_tstamps = list(set(range(start,end+60000,60000)).difference(tstamps))

	msg = "{},{},{},{},{},{}".format(market,start_dt,end_dt,exp,cap,len(missing_tstamps))

	#write to log file. one log file per date, for all markets.
	open(logfile,'a').write(msg+'\n')

# get_data('BTCUSDT')

# symbols = open(os.environ['HOME']+'/mudrex/symbols').read().splitlines()

jobs = []

markets = requests.get('https://api.binance.com/api/v1/exchangeInfo').json()['symbols']

total_markets = len(markets)

f = open('reports/report_'+dirname,'w')
f.write("Process start time (IST): {}.\n".format(datetime.datetime.now().strftime("%Y-%b-%d %H:%M:%S")))
f.write("Data collected for past 1000 minutes from now\n\n")
f.write("Total no. of markets: {}\n".format(total_markets))

markets_trading, markets_break = [],[]

for market in markets:
	symbol = market['symbol']

	if market['status'] == "TRADING":
		markets_trading.append(symbol)

		p = multiprocessing.Process(target=get_data,args=(symbol,))
		jobs.append(p)
		time.sleep(0.1)
		p.start()

	else:
		markets_break.append(symbol)

f.write("Total no. of markets with status as BREAK: {}\n".format(len(markets_break)))
f.write("Total no. of markets with status as TRADING: {}\n".format(len(markets_trading)))