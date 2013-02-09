import socket
import logging

logging.basicConfig(filename = 'hellonetworking.log', 
                    level = logging.DEBUG, 
                    format ='%(asctime)s: %(filename)s >> %(levelname)s - %(message)s')


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("", 1972))
client.send("Client sends greetings")
logging.info("Client received: %s" % client.recv(1024))
client.close()

#### run client *after* the server.
## 1. client sends string
## 2. client writes into logging file what it received from server
## 3. client closes session
