import io
from commands import *

def create_invalid_command(status,ip,port):
    return Invalid_Command(status,ip,port)

def create_disconnect_command(status,ip,port):
    return Disconnect_Command(status,ip,port)

def create_cv_command(status,ip,port,data):
    return CV_Command(status,ip,port,data)

class PLN_Protocol_Server:

    def __init__(self):
        self.valid_commands = ['DISCONNECT','CV','TFIDF']  
        self.command_hash = {
            'INVALID': create_invalid_command,
            'DISCONNECT': create_disconnect_command,
            'CV': create_cv_command,
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

        if not (command_message in self.valid_commands):
            command = self.command_hash['INVALID'](status='400',ip=ip,port=port)
            return command

        else:
            if command_message == 'DISCONNECT':
                command = self.command_hash['DISCONNECT'](status='500',ip=ip,port=port)
                return command

            else:
                empty = False
                data = []

                while not empty:
                    text = buffer.readline().replace('\n','')

                    if text == '':
                        empty = True

                    else:
                        data.append(text)

                command = self.command_hash[command_message](status='200',ip=ip,port=port,data=data)
                return command
