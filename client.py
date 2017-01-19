#!/usr/bin/env python

import socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

# AF_INET means we want an IPv4 socket
# SOCK_STREAM means we want a TCP socket

clientSocket.connect( ("www.google.com", 80) ) #address, port
#accepts tuples, which is why there's double (())
#has to do with C programming and structs lol

request = "GET / HTTP/1.0\r\n\r\n" #first / means location on server, 
                #HTTP... is protocol number, then DOS-stle new lines

clientSocket.sendall(request) #send request to the server


#get response back from Google

response = bytearray()

while True:
    part = clientSocket.recv(1024)
    if (part):
        response.extend(part)
    else:
        break

print response
