from _thread import *
import threading

def server_thread(connection,address):
    ip, port = str(address[0]), str(address[1])
    print('Connected to',ip,':',port)

    while True:
        client_message = connection.recv(1024)
        sentence = client_message.decode('utf-8')

        print('Received message from', ip,':',port,'is:',sentence)

        if sentence == 'close':
            print("Client",ip,':',port," is requesting to quit")
            response = 'Connection closed'
            connection.send(response.encode('utf-8'))
            break

        else:          
            response = sentence.upper()       
            connection.send(response.encode('utf-8'))

    connection.close()
    print("Connection with",ip,':',port,"closed")

