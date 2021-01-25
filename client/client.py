import socket
import os
import pandas as pd
import numpy as np
from pln_protocol_client import PLN_Protocol_Client

class Client:

    def __init__(self,connection_info):
        self.connection_ip, self.connection_port = connection_info
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.texts = None
        self.text_vectors = None

    def valid_file_and_content(self,file):
        if not os.path.isfile(file):
            print('The typed path is not a file.')
            return None

        extension = file.split('.')[-1]
        if extension != 'csv':
            print('The typed path is not a .csv file.')
            return None

        file_size = os.path.getsize(file)
        if file_size > 40960000:
            print('The chosen file is too big.')
            return None

        df = pd.read_csv(file)
        if not ('content' in df.columns):
            print("The .csv file does not contain a 'content' column.")
            return None

        return  df['content'].tolist()

    def run(self):
        self.socket.connect((self.connection_ip,self.connection_port))
        print('Client initialized and connected to', self.connection_ip,':',self.connection_port)

        while True:
            command = input("Type a sentence or 'DISCONNECT' to exit\n") #TODO lista o nome dos comandos

            protocol = PLN_Protocol_Client(command)

            if protocol.valid:
                
                if protocol.need_data:
                    print('Please send a .csv file which contains the texts inside a column named content.')
                    file = input('Type the file path:\n')

                    self.texts = self.valid_file_and_content(file)

                    if self.texts != None:

                        print('Valid file.\n')

                        formated = protocol.format_message(self.texts)

                        if protocol.valid_data:
                            print('Sending request to the server...\n')
                            self.socket.send(formated.encode('utf-8'))

                            response = self.socket.recv(40960000)
                            response = response.decode('utf-8')

                            self.text_vectors = np.array(protocol.parse_response(response))
                            np.save('test.npy',self.text_vectors)

                    else:
                        print('Invalid file.')
                        print('Please check if the file has the requested format.\n')


                else:
                    formated = protocol.format_message(None)     

                    print('Sending request to the server...\n')
                    self.socket.send(formated.encode('utf-8'))

                    response = self.socket.recv(1024)
                    response = response.decode('utf-8')

                    self.text_vectors = protocol.parse_response(response)

                    if protocol.disconnect_successful:
                        break

        print('Finishing client process.')            

def main():
    ip = input("Please type the server IP address or localhost\n")
    address = (ip, 20000)
    client = Client(address)
    client.run()

if __name__ == '__main__':
    main()