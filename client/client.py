import socket
import os
import pandas as pd

class Client:

    def __init__(self,connection_info):
        self.connection_ip, self.connection_port = connection_info
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.texts = None
        self.raw_coordinates = None

    def valid_file_and_content(self,file):
        if not os.path.isfile(file):
            return None

        extension = file.split('.')[-1]
        if extension != 'csv':
            return None

        df = pd.read_csv(file)
        if not ('content' in df.columns):
            return None

        return  df['content'].tolist()

    def format_message(self,command,texts):
        formated = command + '\n'

        for t in texts:
            t.replace('\n',' ')
            formated += t + '\n'

        return formated + '\n'

    def parse_response(self):
        pass #TODO

    def run(self):
        self.socket.connect((self.connection_ip,self.connection_port))
        print('Client initialized and connected to', self.connection_ip)

        while True:
            command = input("Type a sentence or 'DISCONNECT' to exit\n") #TODO lista o nome dos comandos
            
            if command == 'DISCONNECT':
                formated = self.format_message(command,[])
                self.socket.send(formated.encode('utf-8'))
                response = self.socket.recv(1024)
                response = response.decode('utf-8')

                print('Received response is:',response)
                print('---------------------\n')
                
                print('Closing client')
                self.socket.close()
                break

            else:
                print('Please send a .csv file which contains the texts inside a column named content.')
                file = input('Type the file path:\n')

                self.texts = self.valid_file_and_content(file)

                if self.texts != None:

                    print('Valid file.')

                    formated = self.format_message(command,self.texts) 

                    ('Sending request to server...')                 

                    self.socket.send(formated.encode('utf-8'))

                    response = self.socket.recv(40960000)
                    response = response.decode('utf-8')

                    print('Received response is:',response)
                    print('---------------------\n')

                else:
                    print('Invalid file.\n')

def main():
    address = ("localhost", 20000)
    client = Client(address)
    client.run()

if __name__ == '__main__':
    main()