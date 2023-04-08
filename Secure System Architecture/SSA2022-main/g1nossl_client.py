import socket
import pwinput
import uuid
import random
#import ssl


#Function to get the MAC Address
def get_mac():
  mac_num = hex(uuid.getnode()).replace('0x', '').replace('L', '').upper()
  mac_num = mac_num.zfill(12)
  mac = '-'.join(mac_num[i: i + 2] for i in range(0, 11, 2))
  return mac
	

def client_program():
	mylist = ['reset','over','latency','bye']
	#host = socket.gethostname()  # Both Client and Server running on same machine
	#host='127.0.0.1'
	host="128.199.141.149"
	port = 1236  # socket server port number
	
	client_socket = socket.socket()  # instantiate the socket
	client_socket.connect((host, port))  # connect to the server
	#client_socket = ssl.wrap_socket(client_socket,ca_certs="/root/group1/client/g1server.crt",cert_reqs=ssl.CERT_REQUIRED)

	message = input("Enter Device Name: ")  # take input
	client_socket.send(message.encode())	
	data_devicename = client_socket.recv(1024).decode() 
	print(data_devicename+'\n')  # show in terminal

	if data_devicename=='Device Name not found':
		print('Session will be closed')  # show in terminal
		client_socket.close()
	
	else:
		message = pwinput.pwinput(prompt='Enter Password: ') 

		client_socket.send(message.encode())
		data_password_status = client_socket.recv(1024).decode()
		print(data_password_status+'\n')  # show in terminal
	
		if data_password_status=='Password is wrong':
			print('Session will be closed due to wrong password')  # show in terminal
			client_socket.close()
	
		else:
			message = get_mac()
			print('Send MAC Address: '+ str(message)+' to Server')  # show in terminal
			client_socket.send(message.encode())
		
			data_mac_status = client_socket.recv(1024).decode()
		
			if data_mac_status=='MAC Address is wrong':
				print('Session will be closed due to wrong MAC Address')  # show in terminal
				client_socket.close()
	
			else:

				print("Available options: ")
				print("reset = Reset temperature sensor")
				print("latency = Query latency")				
				print("bye = end the session"+'\n')

				print('Wait for input... ')  # show in terminal

				#data = client_socket.recv(1024).decode() # receive response

				#message = input("Input-> ")  # take input	
				message = 'Waiting for input'
				
				while message.lower().strip() != 'bye':
					
					client_socket.send(message.encode())  # send message
					data = client_socket.recv(1024).decode()  # receive response			
					
					print('From the Controller: ' + data)  # show in terminal
					
					if data.lower() == 'lock':
						message = 'Device is locked'
						print(message)						

				
					elif data.lower() == 'unlock':
						message = 'Device is Unlocked' 
						print(message)
						
					
					elif data.lower() == 'status':
						rand_num = random.randint(30, 70)
						
						if rand_num <= 50:
							device_temp = 0
							message = ('Device temperature is normal: '+str(rand_num))
						else: 
							device_temp = 1
							message = ('Device temperature is high: '+str(rand_num))

					elif data.lower() == 'over':
						message = 'Assigned with communication role' 
						print(message)
						message = input("Input-> ")  # take input	
						
						while message.lower() not in mylist:
							print ("Invalid Command")
							message = input('Input-> ')
												
											
					elif data.lower() == 'bye':
						message = 'Session has ended' 
						print(message)
						break

											
					else:
						message = 'Unknown command'
						print(message)
						message = input("Input-> ")  # again take input				
					
					
				client_socket.close()  # close the connection

		

if __name__ == '__main__':

    client_program()
