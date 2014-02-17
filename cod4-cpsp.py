#############################################################################################
#
# cod4-cpsp.py
#
#
# The exploit that this script protects against is a flooder. The flooder will send
# the correct connection sequence to the server in an attempt to join the server, then
# drop the response. The server is then locked into a non returning handshake for as
# long as the server's timeout is set to. This results in slots being eaten up by the
# bot, not allowing anyone to connect because there will be no open slots to connect to.
#
# Anyways, all this does is poll the server every 10 seconds for CNCT players
# and counts up the number of those players who have the same IP and then uses
# CSF to firewall the IP.
#
# NOTE: Be sure to Tmux this as root.
# 
# RIGHTS: You are free to distribute this as you wish, even with modifications as long
#         as you keep this header in the script along with the right author (Zinglish).
#
# AUTHOR: Zinglish
#
#############################################################################################


# === EDIT THESE ============================
SERVER_IP = "127.0.0.1"
SERVER_PORT = 28960
SERVER_RCON_PASS = "rconpasswordhere"

CHECK_TIME = 10 # In seconds
MAX_CNCT_PER_IP = 3
SHELL_CMD = "csf -d %s 'cod4 cps flooder'" # Defaulted to using CSF
# ===========================================

# === Imports ===============================
import socket
import time
import re
import os
# ===========================================

# === Program start =========================
 
# Set up UDP socket comms
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, SERVER_PORT + 99))

# Infinite loop
while True:
	cnctPlayers = []
	cnctPlayersCnt = []
	ipFound = 0;
	concatData = ""

	print("Checking for fake players")

	# Send a request for "status" to the server
	sock.sendto("\xff\xff\xff\xffrcon\r"+SERVER_RCON_PASS+"\rstatus\0", (SERVER_IP, SERVER_PORT))

	# Request the status from the server and concatinate all the data into one giant string
	data, addr = sock.recvfrom(2048) # buffer size is 1024 bytes
	data = re.sub('^.{4}print\n','',data)
	concatData = concatData + data

	try:
		while data:
			sock.settimeout(2)
			data, addr = sock.recvfrom(2048) # buffer size is 1024 bytes

			data = re.sub('^.{4}print\n','',data)
			concatData = concatData + data
	except socket.timeout:
		print("End of stream")

	# Split the output up by line and do a regex search on each line to search for the IP address
	lines = concatData.split('\n')
	for line in lines:
		m = re.search('^\s+(\d+)\s+\d+\sCNCT.+\^7\s+\d+\s(.+):', line)

		if m:
			for i in range(len(cnctPlayers)):
				if cnctPlayers[i] == m.group(2):
					# print("Same IP found")
					cnctPlayersCnt[i] = cnctPlayersCnt[i] + 1
					ipFound = 1

			# Add the IP to the array and add 1 to the counter
			if ipFound == 0:
				cnctPlayers.append(m.group(2))
				cnctPlayersCnt.append(1)

	# Ban the players in the array
	for i in range(len(cnctPlayers)):
		if cnctPlayersCnt[i] > MAX_CNCT_PER_IP:
			print("IP "+cnctPlayers[i]+" was found to be CNCT in "+str(cnctPlayersCnt[i])+" slots, now banning")
			resp = os.system(SHELL_CMD.replace("%s", cnctPlayers[i]))
			#print resp

	time.sleep(CHECK_TIME)
