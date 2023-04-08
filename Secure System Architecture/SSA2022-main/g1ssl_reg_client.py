import socket
import pwinput
import uuid
import ssl

host = '128.199.141.149'
port = 1238

def get_mac():
  mac_num = hex(uuid.getnode()).replace('0x', '').replace('L', '').upper()
  mac_num = mac_num.zfill(12)
  mac = '-'.join(mac_num[i: i + 2] for i in range(0, 11, 2))
  return mac
  
# create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client = ssl.wrap_socket(client,ca_certs="/root/group1/client/g1server.crt",cert_reqs=ssl.CERT_REQUIRED)

# connect the client
# client.connect((target, port))
client.connect((host, port))
response = client.recv(2048)

# Input Device Name
name = input(response.decode())	
client.send(str.encode(name))
response = client.recv(2048)

# Input Password
# password = input(response.decode())	
password = pwinput.pwinput(response.decode(), mask='*')

client.send(str.encode(password))
''' Response : Status of Connection :
	1 : Registeration successful 
	2 : Connection Successful
	3 : Login Failed
'''
response = client.recv(2048)

# Get MAC Address and send to Server
# mac_addr = input(response.decode())	
mac_addr = get_mac()
client.send(str.encode(mac_addr))
response = client.recv(2048)


# Receive response 
#response = client.recv(2048)
response = response.decode()

print(response)
client.close()
