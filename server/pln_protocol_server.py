import io
from commands import *

def create_invalid_command(status,ip,port):
    return Invalid_Command(status,ip,port)

def create_invalid_data(status,ip,port):
    return Invalid_Data(status,ip,port)

def create_disconnect_command(status,ip,port):
    return Disconnect_Command(status,ip,port)

def create_cv_command(status,ip,port,data):
    return CV_Command(status,ip,port,data)

def create_tfidf_command(status,ip,port,data):
    return TFIDF_Command(status,ip,port,data)

class PLN_Protocol_Server:

    def __init__(self):
        self.valid_commands = ['DISCONNECT','CV','TFIDF']  
        self.command_hash = {
            'INVALID': create_invalid_command,
            'INVALID DATA': create_invalid_data,
            'DISCONNECT': create_disconnect_command,
            'CV': create_cv_command,
            'TFIDF': create_tfidf_command,
        }  

    def format_response(self,status,result):
        response = status + '\n'

        for row in result:
            aux = []
            for element in row:
                aux.append(str(element))

            response += ';'.join(aux)
            response += '\n'

        return response + '\n'

    def parse_message(self,message,ip,port):

        buffer = io.StringIO(message)

        command_message = buffer.readline().replace('\n','')
        command = None

        if not (command_message in self.valid_commands):
            command = self.command_hash['INVALID'](status='400',ip=ip,port=port)
            
        else:
            if command_message == 'DISCONNECT':
                command = self.command_hash['DISCONNECT'](status='500',ip=ip,port=port)
                

            else:
                failure = False
                empty = False
                data = []
                
                try:       
                    while not empty:
                        text = buffer.readline().replace('\n','')

                        if text == '':
                            empty = True

                        else:
                            data.append(text)
                except:
                    failure = True
                    command = self.command_hash['INVALID DATA'](status='300',ip=ip,port=port)

                if not failure:
                    command = self.command_hash[command_message](status='200',ip=ip,port=port,data=data)

        return command
                
