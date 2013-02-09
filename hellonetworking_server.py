import socket
import logging

logging.basicConfig(filename = 'hellonetworking.log', 
                    level = logging.DEBUG, 
                    format ='%(asctime)s: %(filename)s >> %(levelname)s - %(message)s')


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 1972))
s.listen(5)

while True:
    client, address = s.accept()
    data = client.recv(1024)
    if data:
        logging.info("Server received: %s" % data)
        client.close()

#### testing it from two shells:
## 1. tail -f hellonetworking.log 
#### the same .log file prepared in logging.basicConfig which
#### is waiting for something to be logged/written
## 2. echo "hello networking" | nc localhost 1972
#### nc sends to port 1972 string "hello networking" piped from echo
#### logging.info writes what it gets on socket s
