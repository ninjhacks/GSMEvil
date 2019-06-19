# coding: latin-1

"""
About: This program shows you IMSI , TMSI, LAC, CI of cellphones around you.

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
import datetime

class ImsiEvil:

    sql_conn = None
    imsi = ""
    tmsi = ""
    mcc = ""
    mnc = ""
    lac = ""
    ci = ""
    id_ = 0
    live_db = {}

    def sql_db(self):
        import sqlite3
        self.sql_conn = sqlite3.connect(options.save)
        self.sql_conn.execute('CREATE TABLE IF NOT EXISTS imsi_data(id INTEGER PRIMARY KEY, imsi TEXT, tmsi TEXT, mcc INTEGER, mnc INTEGER, lac INTEGER, ci INTEGER, date_time timestamp)')

    def save_data(self):
        date_time = datetime.datetime.now()
        self.sql_conn.execute('INSERT INTO imsi_data(imsi, tmsi, mcc, mnc, lac, ci, date_time) VALUES ( ?, ?, ?, ?, ?, ?, ?)',(self.imsi, self.tmsi, self.mcc, self.mnc, self.lac, self.ci, date_time))
        self.sql_conn.commit()

    def get_data(self):
        self.cur = self.sql_conn.cursor()
        self.cur.execute('SELECT * FROM imsi_data WHERE imsi=' + self.imsi)
        self.data = self.cur.fetchall()

    def update_data(self, id_, tmsi):
        self.sql_conn.execute('UPDATE imsi_data SET tmsi = ?, date_time = ? WHERE id= ?',(tmsi, id_, datetime.datetime.now()))
        self.sql_conn.commit()

    def filter_imsi(self):
        if options.save:
            self.sql_db()
            self.get_data()
            data = self.data
            if data:
                data = self.data[0]
                if(self.imsi != data[1]):
                    self.save_data()
                else:
                    if (self.tmsi != data[2]) & (self.tmsi != ''): #Check if tmsi is different than update in file db
                        self.update_data(data[0],self.tmsi)
            else:
                self.save_data()
        
        if self.imsi in self.live_db:
            if self.live_db[self.imsi]['tmsi'] != self.tmsi: #Check if tmsi is different than update in live db
                self.live_db[self.imsi]['tmsi'] = self.tmsi
        else:
            self.id_ += 1
            self.live_db[self.imsi] = {"id" : self.id_,"tmsi" : self.tmsi, "mcc" : self.mcc, "mnc" : self.mnc}
        self.output()

    def get_imsi(self, capture):
        for packet in capture:
            layer = packet.highest_layer
            if layer == "GSM_A.CCCH":
                if packet[4].layer_name == 'gsm_a.ccch':
                    gsm_a_ccch = packet[4]
                    if hasattr(gsm_a_ccch, "gsm_a_bssmap_cell_ci"):
                        self.ci = int(gsm_a_ccch.gsm_a_bssmap_cell_ci, 16)
                        self.lac = int(gsm_a_ccch.gsm_a_lac, 16)
                    elif hasattr(gsm_a_ccch, 'e212.imsi'):
                        self.imsi = gsm_a_ccch.e212_imsi #[-11:-1]
                        self.mcc = gsm_a_ccch.e212_mcc
                        self.mnc = gsm_a_ccch.e212_mnc
                        if hasattr(gsm_a_ccch,'gsm_a_rr_tmsi_ptmsi'):
                            self.tmsi = gsm_a_ccch.gsm_a_rr_tmsi_ptmsi
                        elif hasattr(gsm_a_ccch,'gsm_a_tmsi'):
                            self.tmsi = gsm_a_ccch.gsm_a_tmsi
                        else:
                            self.tmsi = ''
                        if options.imsi == '':
                            self.filter_imsi()
                        elif options.imsi == self.imsi:
                            self.filter_imsi()
                elif packet[6].layer_name == 'gsm_a.ccch':
                    gsm_a_ccch = packet[6]
                    if hasattr(gsm_a_ccch, "gsm_a_bssmap_cell_ci"):
                        self.ci = int(gsm_a_ccch.gsm_a_bssmap_cell_ci, 16)
                        self.lac = int(gsm_a_ccch.gsm_a_lac, 16)

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
                          ☠️  丨爪丂丨 匚卂ㄒ匚卄乇尺  ☠️'''
        print ("\033[0;31;48m" + title)
        print ("................................................................................")
        print("\033[0;37;48m ID \033[0;31;48m; \033[0;37;48m       IMSI       \033[0;31;48m;     \033[0;37;48mTMSI     \033[0;31;48m;   \033[0;37;48mMCC   \033[0;31;48m;  \033[0;37;48mMNC  \033[0;31;48m; \033[0;37;48m  LAC   \033[0;31;48m; \033[0;37;48m    CI\033[0;31;48m    ;")
        print ("\033[0;31;48m................................................................................")
    
    def output(self):
        print("\033[0;37;48m {:3s}\033[0;31;48m; \033[0;37;48m {:16s} \033[0;31;48m; \033[0;37;48m {:12s}\033[0;31;48m; \033[0;37;48m\033[0;37;48m  {:5s} \033[0;31;48m;\033[0;37;48m   {:4s}\033[0;31;48m; \033[0;37;48m {:5}  \033[0;31;48m; \033[0;37;48m {:6}   \033[0;31;48m;".format(str(self.live_db[self.imsi]["id"]), self.imsi, self.live_db[self.imsi]["tmsi"], self.mcc, self.mnc, self.lac, self.ci))
        print ("\033[0;31;48m................................................................................")

if __name__ == "__main__":
	parser = OptionParser(usage="%prog: [options]")
	parser.add_option("-i", "--iface", dest="iface", default="lo", help="Interface (default : lo)")
	parser.add_option("-p", "--port", dest="port", default="4729", type="int", help="Port (default : 4729)")    
	parser.add_option("-m", "--imsi", dest="imsi", default="", type="string", help='IMSI to track (default : None, Example: 123456789101112)')
	parser.add_option("-s", "--save", dest="save", default=None, type="string", help="Save all text messages to sqlite file. (default : None)")
	(options, args) = parser.parse_args()

try:
    ImsiEvil = ImsiEvil()
    ImsiEvil.header()
    capture = pyshark.LiveCapture(interface=options.iface, bpf_filter="port {} and not icmp and udp".format(options.port))
    ImsiEvil.get_imsi(capture)
except:
    print ("Stop sniffing")