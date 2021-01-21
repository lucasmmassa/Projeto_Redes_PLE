import socket

class Client:

    def __init__(self,connection_info):
        self.connection_ip, self.connection_port = connection_info
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        self.socket.connect((self.connection_ip,self.connection_port))
        print('Client initialized and connected to', self.connection_ip)

        while True:
            client_input = input("Type a sentence or 'close' to exit\n")
            
            if client_input == 'close':
                self.socket.send(client_input.encode('utf-8'))
                response = self.socket.recv(1024)
                response = response.decode('utf-8')

                print('Received response is:',response)
                print('---------------------\n')
                
                print('Closing client')
                self.socket.close()
                break

            else:
                self.socket.send(client_input.encode('utf-8'))

                response = self.socket.recv(1024)
                response = response.decode('utf-8')
                print('Received response is:',response)
                print('---------------------\n')

def main():
    address = ("localhost", 20000)
    client = Client(address)
    client.run()

if __name__ == '__main__':
    main()