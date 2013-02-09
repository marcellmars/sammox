import socket
import logging

logging.basicConfig(filename = 'hellonetworking.log', 
                    level = logging.DEBUG, 
                    format ='%(asctime)s: %(filename)s >> %(levelname)s - %(message)s')


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("", 1972))
server.listen(5)

while True:
    client, address = server.accept()
    data = client.recv(1024)
    if data:
        logging.info("Server received: %s from %s" % (data, address))
        client.send("Server is echoing: %s to %s" % (data, address))
        client.close()

#### testing it from two shells:
## 1. tail -f hellonetworking.log 
#### the same .log file prepared in logging.basicConfig which
#### is waiting for something to be logged/written
## 2. echo "echo+nc says hello to server" | nc localhost 1972
## 2a. echo "echo+nc says hello to server" | nc localhost 1972 >> hellonetworking.log
#### nc sends to port 1972 string "echo+nc says hello to server" piped from echo
#### logging.info writes what it gets on socket s
