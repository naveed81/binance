#!/usr/bin/python3
import json,sys,os,datetime
from pprint import pprint
from itertools import repeat

def chunks(l, n):
    #yield successive n-sized chunks from l
    for i in range(0, len(l), n):
        yield l[i:i + n]

def get_nminute_data(data,minutes):
	dict = {}
	tstamps = [int(x) for x in list(data.keys())]
	ts = [min(x) for x in list(chunks(tstamps,minutes))]

	values = list(data.values())
	vs = list(chunks(values,minutes))

	for i in range(0,len(vs)):

		#transpose the values matrix
		v = list(map(list, zip(*vs[i])))

		v[0] = float(v[0][0])                #Open is the first entry in the transposed matrix
		v[1] = max([float(x) for x in v[1]]) #High is max of all high elements
		v[2] = min([float(x) for x in v[2]]) #Low is min of all low elements
		v[3] = float(v[3][-1])               #Close is last element of all close elements
		v[4] = sum([float(x) for x in v[4]]) #Total volume is sum of all volume elements

		dict[ts[i]] = v

	return dict

#directory name
dirname = sys.argv[1]

for fname in os.listdir('json/'+dirname):
	market = fname.split('_')[0]
	# print(market)

	with open('json/'+dirname+'/'+fname) as json_data: 
		data = json.load(json_data)
		
		i = 0
		for dict in map(get_nminute_data,repeat(data),[1,5,10,30,60]):

			d = {0:'1m',1:'5m',2:'10m',3:'30m',4:'60m'}

			for key,value in dict.items():
				value = [str(x) for x in value]
				dt = datetime.datetime.fromtimestamp(int(key)/1000).strftime("%Y-%m-%d %H:%M:%S")
				msg = "{},{},{},{}".format(market,key,dt,','.join(value))
				
				#print to one file per nminute slot per date for all markets.
				#prepare file name and path
				f = 'data/'+dirname+'/'+d[i]+'_'+dirname+'.csv'

				open(f,'a').write(msg+'\n')
				# print(msg)

			i += 1