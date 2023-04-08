import socket
#import ssl
import datetime
import time
import os
import threading
import hashlib
import re

from pythonping import ping

#Function to get the ip address of the remote device
def find_enclosed(s): 
    # find all matches
    matches = re.findall(r"\('(.*?)\'", s) 
    #matches = re.findall(r'(\w+', s) 
    # if there are no matches return None
    if len(matches) == 0:
        return None
    # if it is a valid number change its type to a number
    for i in range(len(matches)):
        try:
            matches[i] = int(matches[i])
        except:
            pass
    # if there is only one match return it without a list
    if len(matches) ==  1:
        return matches[0]
    
    return matches
    
# Function to encrypt password
def encrypt_password (passwd):
   #Encrypt the password and return the sha digest.
   hash_passwd = (passwd)
   hash_passwd = hash_passwd.encode("utf8")
   return hashlib.sha256(hash_passwd).hexdigest()
   
   
# Function to check if an username existed in asmis.txt
def check_username(username):
   for line in open("/root/group1/asmis.txt","r").readlines(): #File open asmis.txt in read mode
       login_info = line.split() # Split into two segments, first segment is the username, second is the hash password
       if username == login_info[0]:  #only the username will be checked
           return True
 
   return False

# Function to user name and user password matched the record in the file?
def check_password(username,userpasswd):
   for line in open("/root/group1/asmis.txt","r").readlines(): #File open asmis.txt in read mode
       login_info = line.split() # Split into two segments, first segment is the username, second is the hash password
       if username == login_info[0] and encrypt_password(userpasswd) == login_info[1]:
           return True 
   return False 

# Function to user name, user password  and MAC Address matched the record in the file
def check_device(username,userpasswd,macaddr):
   for line in open("/root/group1/asmis.txt","r").readlines(): #File open asmis.txt in read mode
       login_info = line.split() # Split into two segments, first segment is the username, second is the hash password
       if username == login_info[0] and encrypt_password(userpasswd) == login_info[1] and macaddr == login_info[2]:
           return True 
   return False 

   
def server_program():
	
	mylist = ['lock','unlock','status','over','bye']
	# get the hostname
	#host = socket.gethostname()
	#host='127.0.0.1'
	host = '128.199.141.149'
	port = 1236  # initiate port no above 1024
			
	server_socket = socket.socket()  # get instance
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	#server_socket = ssl.wrap_socket(server_socket,server_side=True,certfile="/root/group1/server/g1server.crt",keyfile="/root/group1/server/server.key")
	
	# look closely. The bind() function takes tuple as argument
	server_socket.bind((host, port))  # bind host address and port together

	# configure how many client the server can listen simultaneously
	server_socket.listen(2)
	print("Waiting for connection")
    
	conn, address = server_socket.accept()  # accept new connection
	#conn.settimeout(10)  #disconnect afer x seconds
	
	print("Connection from: " + str(address))
	
	remote_ipaddr = find_enclosed(str(address))

	data_userdevice = conn.recv(1024).decode()
	print("Received from connected: " + str(data_userdevice))


	if check_username(data_userdevice)==False:
		data = 'Device Name not found'
		conn.send(data.encode())  # send data to the client
		server_socket.close()

	else:
		data = 'Device:'  + data_userdevice + ' is found'
		conn.send(data.encode())  # send data to the client

		#Get password
	
		data_password = conn.recv(1024).decode()
		print("Received harsh password from client: " + str(encrypt_password(data_password)))

		if check_password(data_userdevice,data_password)==False:
			data = 'Password is wrong'
			print("Password is wrong: " + str(data))
			conn.send(data.encode())  # send data to the client
			server_socket.close()

		else:

			data = 'Password is correct'
			conn.send(data.encode())  # send data to the client	
		
			#Get MAC Address
			data_mac = conn.recv(1024).decode()


			if check_device(data_userdevice,data_password,data_mac)==False:
				data ='MAC Address is wrong'
				print("MAC Address is wrong")
				conn.send(data.encode())  # send data to the client
				server_socket.close()
			else:
					
				data = 'MAC Address is correct'
				print("Received from client MAC: " + str(data_mac)+'\n')
				print("Available options: ")
				print("lock = lock the device")
				print("unlock = unlock the device")
				print("status = request status from device")
				print("over = allow communicator rights from the device")
				print("bye = end the session"+'\n')
				conn.send(data.encode())  # send data to the client	
	
				#data = input('Input-> ')
				#conn.send(data.encode())  # send data to the client			

				while True and data != 'bye':
					# receive data stream. it won't accept data packet greater than 1024 bytes
					data = conn.recv(1024).decode()	
				
					if not data:
					# if data is not received break
						break
					print("From the connected device: " + str(data))

					if data == 'reset':
					
						print("Reset temperature sensor")

					elif data == 'latency':
						result = ping(remote_ipaddr, count=2, timeout=2)
						print('avg_latency: ' + str(result.rtt_avg_ms)+ 'ms') 
						print('min_latency:' + str(result.rtt_min_ms)+ 'ms')
						print('max_latency:' + str(result.rtt_max_ms)+ 'ms')
						print('packet_loss:' + str(result.packet_loss))
																										
					data = input('Input-> ')
					
					while data.lower() not in mylist:
						print ("Invalid Command")
						data = input('Input-> ')
					
					conn.send(data.encode())
				
					
				conn.close()  # close the connection



if __name__ == '__main__':

    server_program()


