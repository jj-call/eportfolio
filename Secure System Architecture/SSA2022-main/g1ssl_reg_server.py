import socket
import os
import threading
import hashlib
import ssl


#host = '127.0.0.1'
host = '128.199.141.149'
port = 1238
ThreadCount = 0

# Create Socket (TCP) Connection
ServerSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM) 


try:
    ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # allow reuse of address
    ServerSocket = ssl.wrap_socket(ServerSocket,server_side=True,certfile="/root/group1/server/g1server.crt",keyfile="/root/group1/server/server.key")
    ServerSocket.bind((host, port))

except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(1)


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

# Function to check if an username, password and MAC address existed in asmis.txt
def check_device(username,userpasswd,macaddr):
   for line in open("/root/group1/asmis.txt","r").readlines(): #File open asmis.txt in read mode
       login_info = line.split() # Split into two segments, first segment is the username, second is the hash password
       if username == login_info[0] and encrypt_password(userpasswd) == login_info[1] and macaddr == login_info[2]:
           return True 
   return False 

# Function : For each client 
def threaded_client(connection):
    connection.send(str.encode('Enter Device Name : ')) # Request Username
    name = connection.recv(2048)
    
    connection.send(str.encode('Enter Password : ')) # Request Password
    password = connection.recv(2048)

    connection.send(str.encode('Enter MAC address : ')) # Request MAC Address
    mac_addr = connection.recv(2048)
        
    password = password.decode()
    mac_addr = mac_addr.decode()
    name = name.decode()
    
# Device Registration Process
# If new device,  register in asmis.txt
    if check_device(name,password,mac_addr)==False:
        connection.send(str.encode('Registeration Successful')) 

        gethash=encrypt_password(password)
        output_file = open("/root/group1/asmis.txt", "a") #append to the file
        output_file.writelines(name) #write username to the file
        output_file.writelines(" ") #Follow by a space
        output_file.writelines(gethash) #Write hash password
        output_file.writelines(" ") #Follow by a space
        output_file.writelines(mac_addr) #write MAC address       
        output_file.writelines("\n") #Write a new line 
        output_file.close() #close the file
        
    else:
        connection.send(str.encode('Existing Device, Please register a new device')) # Response Code for Connected Client 
        print('Device:',name, 'is an existing device. Please register a new device')

#        if check_username(name)==True:

    
#    while True:
#        break
#    connection.close()

while True:
    Client, address = ServerSocket.accept()
    client_handler = threading.Thread(
        target=threaded_client,
        args=(Client,)  
    )
    client_handler.start()
    ThreadCount += 1
    print('Connection Request: ' + str(ThreadCount))
ServerSocket.close()
