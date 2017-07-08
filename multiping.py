#!/usr/bin/env python3
# 
# Ping multiple destinations and print out statistics

import argparse
import threading
import subprocess
import time
import sys
import re
import os.path

from datetime import datetime

try:
	from colorama import init, deinit, Fore, Style
	
except ImportError:
	print("\nColorama package is not installed on this system!")
	print("Get it from https://pypi.python.org/pypi/colorama")
	print("Closing program...\n")
	sys.exit()


def time_conversion(matched_object):
    
	""" Convert unix time to readable time """
	
	timestamp = matched_object.group(1)
	return datetime.fromtimestamp(float(timestamp)).strftime("%d/%m/%Y %H:%M:%S")


def ping(dest):
    
	""" Ping and record the result associated with datetime """
	
	# The ping command to execute
	cmd = "ping -n %s -D" % dest
	
	# The log filename
	log = dest + ".log"
	
	# The path to store log file
	path = os.path.join("/home/hoangtnk/Logs", log)
	
	# Ping and record the result to file
	with open(path, "w") as ping_log:
		proc = subprocess.Popen(cmd, shell=True, stdout=ping_log, stderr=ping_log)
		proc.wait()


def analyze_ping(host_list):
    
	""" Analyze ping results """
	
	print(Fore.CYAN + Style.BRIGHT + "========================== BEGIN OF STATISTICS ==========================")
	
	for host in host_list:
		print(Fore.GREEN + Style.BRIGHT + "\n+ %s:" % host.upper())
		
		log = host + ".log"
		path = os.path.join("/home/hoangtnk/Logs", log)
		
		# Read the ping log content
		with open(path, "r") as ping_log:
			ping_log.seek(0)
			log_content = ping_log.read()
		
		# Convert unix time to readable time and update to log file
		log_content = re.sub(r"\[(.+)\]", time_conversion, log_content)
		with open(path, "w") as ping_log:
			ping_log.seek(0)
			ping_log.write(log_content)
		
		# Get the ping output
		ping_output = re.findall(r"(\d+/\d+/\d+ \d+:\d+:\d+) (.+) (icmp_seq=\d+) (.+)", log_content)
		
		# Create an ICMP sequence list and a corresponding datetime list
		if len(ping_output) == 0:
			print(Fore.RED + Style.BRIGHT + "No successful ping to %s. Please check log for detail." % host)
		else:
			ping_datetime = []
			ping_seq = []
			ping_detail = []
			for output in ping_output:
				ping_datetime.append(output[0])
				ping_seq.append(output[2].split("=")[1])
				ping_detail.append(output[3])
			
			# Get the ping statistics
			try:
				ping_statistics = re.search(r"(\d+) packets transmitted, (\d+) received(.+?)(\d+)%(.+)(\nrtt min/avg/max/mdev = (.+)/(.+)/(.+)/(.+))?", log_content)
				total_requests = ping_statistics.group(1)
				total_received = ping_statistics.group(2)
				percent_packets_lost = ping_statistics.group(4) + "%"
			
				if (ping_statistics.group(7) == None):
					min_latency = "n/a"
					max_latency = "n/a"
					avg_latency = "n/a"
				else:
					min_latency = ping_statistics.group(7) + " ms"
					max_latency = ping_statistics.group(9) + " ms"
					avg_latency = ping_statistics.group(8) + " ms"
			
			except AttributeError:
				print(Fore.RED + Style.BRIGHT + "\nThere was an error when extracting ping statistics!")
				print("Closing program...\n")
				deinit()
				sys.exit()
			
			# Print to screen any timestamp where the number of continuous packets lost > 1
			i = 0
			total_packets_lost = 0
			while (i < len(ping_seq) - 1):
				if ("Unreachable" in ping_detail[i]) or ("filtered" in ping_detail[i]):
					j = i
					packets_lost = 0
					while (j < len(ping_detail)) and ("Unreachable" in ping_detail[j] or "filtered" in ping_detail[j]):
						packets_lost += 1
						j += 1
					
					if (packets_lost > 1):
						print(Fore.RED + Style.BRIGHT + "(%d packets lost) at %s" % (packets_lost, ping_datetime[i]))
						
					total_packets_lost += packets_lost
					i = j
				else:
					packets_lost = int(ping_seq[i+1]) - int(ping_seq[i])
					if (packets_lost > 1):
						packets_lost -= 1
						if (packets_lost > 1):
							print(Fore.RED + Style.BRIGHT + "(%d packets lost) at %s" % (packets_lost, ping_datetime[i]))
							
						total_packets_lost += packets_lost	
					i += 1
			
			# Handle the situation where all of the last ping packets were lost
			# until we manually stop the ping by KeyboardInterrupt
			if (int(total_requests) - int(total_received) != total_packets_lost):
				packets_lost = int(total_requests) - int(total_received) - total_packets_lost
				if (packets_lost > 1):
					print(Fore.RED + Style.BRIGHT + "(%d packets lost) at %s" % (packets_lost, ping_datetime[len(ping_datetime)-1]))
				
				total_packets_lost += packets_lost
			
			# Print out the ping statistics
			print(Fore.RESET + Style.RESET_ALL + "Total packets sent: %s" % total_requests)
			print("Total packets received: %s" % total_received)
			
			if (total_packets_lost > 0):
				print(Fore.RED + Style.BRIGHT + "Total packets lost: %d (%s)" % (total_packets_lost, percent_packets_lost))
			else:
				print(Fore.RESET + Style.RESET_ALL + "Total packets lost: %d (%s)" % (total_packets_lost, percent_packets_lost))
			
			print(Fore.RESET + Style.RESET_ALL + "Minimum latency: %s" % min_latency)
			print("Maximum latency: %s" % max_latency)
			print("Average latency: %s" % avg_latency)
	
	print(Fore.CYAN + Style.BRIGHT + "\n=========================== END OF STATISTICS ===========================")
				
				
def main():
	
    """ Main function """
    
    init()
    parser = argparse.ArgumentParser(description="HoangTNK's multiping v1.0")
    parser.add_argument("--version", action="version", version="%(prog)s 1.0")
    parser.add_argument("host", nargs="+", help="IP/hostname of destination")
    args = parser.parse_args()
    print(Fore.RESET + Style.RESET_ALL + "\nPing logs will be recorded to '/home/hoangtnk/Logs' directory.")
    print("\nSending pings to the listed destinations...")
    print("\nPress 'Ctrl-C' to stop the ping and view statistics.\n")
    try:
        # Use threading to ping multiple destinations simultaneously
        threads = []
        for host in args.host:
            th = threading.Thread(target=ping, args=(host,))
            th.start()
            threads.append(th)
	
        for th in threads:
            th.join()
    except KeyboardInterrupt:
        print("\n\nAnalyzing ping results. Please wait...\n")
        time.sleep(2)  # Wait for ping statistics to be written to log file
        analyze_ping(args.host)
		
    print("")
    deinit()


if __name__ == "__main__":
	main()
