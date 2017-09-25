Note
====
When using this class, you need to be running as an administrator or else pyping.ping(host) will fail.

How to run
==========
You need a file that reads config files and starts a MyPingMonitor instance for each config file. So, one host to monitor - one config file.
In here, I am using host_monitor.py as the entry point that reads config files and starts the monitoring instances.
host_monitor.py assumes that you have a hosts_to_check folder in the same location as where host_monitor.py is. It then seeks for all .properties files in hosts_to_check, and assumes that each of those files provides config information for monitoring one host.
To see a sample .properties files, please see app.properties in hosts_to_check.
To better keep track of what file configures what host, you can name your files using the convention host_ip.properties.