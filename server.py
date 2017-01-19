#!usr/bin/env python

import socket, os, sys, errno, select

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serverSocket.bind( ("0.0.0.0", 8000) ) #bind to a port
serverSocket.listen(5) #listen on a port, allow 5 to form a queue, more are turned away

#wait for connection to come in
while True:
    (incomingSocket, address) = serverSocket.accept() #open communication with who's trying to conenct w us. address is info on who
    print"Got a connection from %s" % (repr(address))
    try:
        reaped = os.waitpid(0, os.WNOHANG)
    except OSError, e:
        if e.errno == errno.ECHILD:
            pass
        else:
            raise
    else:
        print "Reaped %s" % (repr(reaped))
#FORK CALL
    if (os.fork() != 0 ): #parent
        continue

##############################

#child's work

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

    clientSocket.connect( ("www.google.com", 80) ) #address, port

    #enable nonblocking i/o
    incomingSocket.setblocking(0)
    clientSocket.setblocking(0)


    while True:
        request = bytearray()
        while True:
            try:
                part = incomingSocket.recv(1024)
            except IOError, e:
                if e.errno == socket.errno.EAGAIN:
                    break
            if (part):
                request.extend(part)
                clientSocket.sendall(part)
            else:
                #empty string, so exit
                sys.exit(0) 
        if len(request) > 0:       
            print(request)

#send something to google
        response = bytearray()
        while True:
            try:
                part = clientSocket.recv(1024)
            except IOError, e:
                if e.errno == socket.errno.EAGAIN:
                    break
                else:
                    raise
            if (part):
                response.extend(part)
                incomingSocket.sendall(part)
            else:
                #exit the program
                sys.exit(0) 

                
        if len(response) > 0:
            print(response) #spies on it!
            
        select.select(
            [incomingSocket, clientSocket], #read
            [],                             #write
            [incomingSocket, clientSocket], #exceptions
            1.0)                            #timeout
