from pln_protocol_server import PLN_Protocol_Server

def server_thread(connection,address):
    ip, port = str(address[0]), str(address[1])
    print('Connected to client',ip,':',port)

    protocol = PLN_Protocol_Server()

    while True:
        client_message = connection.recv(40960000)

        print('Request received from',ip,':',port,'\n')

        client_message = client_message.decode('utf-8')

        command = protocol.parse_message(client_message,ip,port)

        command.run()

        response = protocol.format_response(command.status,command.result)

        connection.send(response.encode('utf-8'))

        if command.status == '500':
            break

    connection.close()
    print("Connection with client",ip,':',port,"is closed")

