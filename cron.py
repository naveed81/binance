#!/usr/bin/python3
import subprocess,datetime,requests

subprocess.call(['python3','proc.py'])
dirname = datetime.datetime.now().strftime("%d%B")
subprocess.call(['python3','nminutes.py',dirname])

#copy data files to webroot for access over http
subprocess.call('cp -r data/{} /var/www/html/data'.format(dirname),shell=True)

#copy log file to logs directory
subprocess.call('cp logs/log_{}.csv /var/www/html/logs'.format(dirname),shell=True)

logfile = "log_"+dirname+".csv"
try:
	n = subprocess.check_output('grep -cv "0$" /home/naveed/mudrex/logs/{}'.format(logfile),shell=True).strip().decode('utf-8')
except subprocess.CalledProcessError as e:
	n = 0

open('reports/report_'+dirname,'a').write("Number of markets with missing data: {}\n\n".format(0))

subprocess.call(['python3','send_email.py'])