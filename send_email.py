#!/usr/bin/python3

import smtplib, datetime, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

#sender mail address
fromaddr = "cqindia81@gmail.com"
#receiver mail address
toaddr = ["edul.patel@mudrex.com","edulpatel1989@gmail.com","ahmed0101@gmail.com"]
# toaddr = ['ahmed0101@gmail.com']
dirname = datetime.datetime.now().strftime("%d%B")

msg = MIMEMultipart()

msg['From'] = 'Naveed BinanceReport'
msg['To'] = ", ".join(toaddr)
msg['Subject'] = "Binance Report for {}".format(datetime.datetime.now().strftime("%d %B"))

body = open("reports/report_"+dirname,'r').read()
body += "To access 1m, 5m, 10m, 30m and 60m data click the link below: \nhttp://34.93.124.158/data\n\n"
body += "To access log file containing market wise data points count click below link\nhttp://34.93.124.158/logs/\n"
body += """It contains 6 columns:\n
		Col1: Market Symbol\n
		Col2: Starting timestamp\n
		Col3: Ending timestamp\n
		Col4: Expected data points count\n
		Col5: Captured data points count\n
		Col6: Missing data points count\n\n
"""
body += "Process end time: {}".format(datetime.datetime.now().strftime("%Y-%b-%d %H:%M:%S"))

msg.attach(MIMEText(body, 'plain'))

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.login(fromaddr, "hyderabad8111") #sender mail password
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()