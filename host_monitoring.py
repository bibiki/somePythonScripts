import os
import thread
import MyPingMonitor
import pypyodbc

def print_time(a, b):
	#time.sleep(10)
	while True:
		print('time' + " " + a + " " + b)


def start_up():
	"""kqyr a e ki folderin, nese jo, lajmro edhe nalu"""
	if(not os.path.exists("hosts_to_check")):
		print("""\\Per me funksionu, mua me duhet nje hosts_to_check follder ku 
					jane nje liste .properties fajllash - per secilin host qe 
					deshiron me e monitoru nga nje fajll""")
		exit()
	
	"""nxjeri krejt .properties fajllat, edhe per secilin prej tyne:"""
	property_files = ["hosts_to_check\\" + f for f in os.listdir("hosts_to_check") if f.strip().endswith(".properties")]
	if len(property_files) < 1:
		print("nuk eshte ofruar konfigurim per asnje host per te bere ping")
		exit()

	for property_file in property_files:
		print("duke lexuar konfigurim prej: " + property_file)
		thread.start_new_thread(get_host_to_ping_configuration(property_file).monitor, ())
	while True:
		pass

def get_host_to_ping_configuration(config_file_name):
	try:
		properties_file = open(config_file_name)
		properties = dict();
		for property in properties_file:
			k_v = property.split("=")
			properties[k_v[0]] = k_v[1]
		
		adresses_to = properties["adress_to"].strip().split(",")
		adress_from = properties["adress_from"].strip()
		ping_frequency_in_seconds = int(properties["ping_frequency_in_seconds"].strip())
		smtp_server = properties["smtp_server"].strip()
		phones_to_receive_sms = properties["phones_to_receive_sms"].strip().split(",")
		phone_operator = properties["phone_operator"].strip()
		reconnect_notification_message = properties["reconnect_notification_message"].strip()
		atm_down_email_message = properties["atm_down_email_message"].strip()
		atm_up_email_message = properties["atm_up_email_message"].strip()
		first_ping_seconds = int(properties["first_ping_seconds"].strip())
		second_ping_seconds = int(properties["second_ping_seconds"].strip())
		start_listening_period=int(properties["start_listening_period"].strip())#0 eshte sekondi i pare i dites
		end_listening_period=int(properties["end_listening_period"].strip())#86400 eshte sekondi i fundit i dites
		db_connection = pypyodbc.connect("DRIVER={{SQL Server}};SERVER={0}; database={1}; trusted_connection=no;UID={2};PWD={3}".format("servername","dbname","dbusername","dbpassword"))
		
		host_to_ping = properties["host_to_ping"].strip()
		
		monitor = MyPingMonitor.PingMonitor(adresses_to, adress_from, host_to_ping, atm_down_email_message, db_connection, smtp_server, ping_frequency_in_seconds, phones_to_receive_sms, phone_operator, first_ping_seconds, second_ping_seconds)
		return monitor
	except Exception as e:
		print("PER TE SHFRYTEZUAR KETE APLIKACION:")
		print("sigurohu qe e ke nje .properties file ku definohen parametrat ne vijim")
		print("adress_to")
		print("adress_from")
		print("host_to_ping")
		print("email_message")
		print("ping_frequency_in_seconds")
		print("reconnect_notification_message")
		print("smtp_server")
		print("phones_to_receive_sms")
		print("phone_operator")
		print("-----------------------")
		print("NJE SHEMBULL KONFIGURIMI ESHTE NE VIJIM")
		print("adress_to=adres_to_notify@host.com")
		print("adress_from=notifier_adress@host.com")
		print("host_to_ping=some.ip")
		print("email_message=no ping for host")
		print("ping_frequency_in_seconds=3")
		print("reconnect_notification_message=host back up")
		print("smtp_server=smtp.somehost.com")
		print("phone_to_receive_sms=1234567")
		print("phone_operator=OPERATOR")
		print(e)
		exit()
start_up()
	
