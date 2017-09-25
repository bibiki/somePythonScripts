import pypyodbc
import os
import subprocess
import time
import smtplib
import pyping
from email.mime.text import MIMEText


class PingMonitor:

	def __init__(self, email_adress_to, email_adress_from, host_to_ping, email_message, db_connection, smtp_server, ping_frequency_in_seconds, phone_to_send_sms, phone_operator, first_ping_seconds = 5, second_ping_seconds = 30):
		self.adress_to = email_adress_to
		self.adress_from = email_adress_from
		self.phone_to_send_sms = phone_to_send_sms
		self.host_to_ping = host_to_ping
		self.email_message = email_message
		self.db_connection = db_connection
		self.smtp_server = smtp_server
		self.phone_operator = phone_operator
		self.quit_listening = False
		self.notification_sent = False
		self.last_ping_time = int(round(time.time() * 1000))#assumes there has been ping when app started
		self.first_ping_seconds = first_ping_seconds
		self.second_ping_seconds = second_ping_seconds
		self.ping_frequency_in_seconds = ping_frequency_in_seconds
	
	def should_notify(self, last_ping_t):
		if self.quit_listening:
			return False
		if self.notification_sent and (int(round(time.time() * 1000)) - last_ping_t >= self.second_ping_seconds*1000):
			self.quit_listening = True
			return True
		elif not self.notification_sent and int(round(time.time() * 1000)) - last_ping_t >= self.first_ping_seconds*1000:
			return True

	def send_email(self, adresa_to, adresa_from, message):
		s = smtplib.SMTP(self.smtp_server)
		s.sendmail(adresa_from, adresa_to, message)
		s.quit()
		
	def send_sms(self):
		"""implement as you see fit"""
		print("SENDING SMS")
		
	def is_there_ping(self, host):
		response = pyping.ping(host)
		return response.ret_code == 0

	def reset(self):
		self.notification_sent = False
		self.quit_listening = False

	def monitor(self):
		while True:
			time.sleep(self.ping_frequency_in_seconds)
			if self.is_there_ping(self.host_to_ping):
				print("there has been ping")
				self.last_ping_time = int(round(time.time() * 1000))
				self.reset()
				continue
			if self.should_notify(self.last_ping_time):
				self.send_email(self.adress_to, self.adress_from, self.email_message)
				self.send_sms()
				self.notification_sent = True
