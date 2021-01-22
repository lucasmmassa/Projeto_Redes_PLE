import io
from commands import *

def create_invalid_command(status,ip,port):
    return Invalid_Command(status,ip,port)

def create_disconnect_command(status,ip,port):
    return Disconnect_Command(status,ip,port)

class PLN_Protocol:

    def __init__(self):
        self.valid_commands = ['DISCONNECT'] #TODO adicionar os comandos restantes  
        self.command_hash = {
            'INVALID': create_invalid_command,
            'DISCONNECT': create_disconnect_command,
        }  

    def format_response(self,status,result):
        response = status + '\n'

        for row in result:
            response += str(row[0]) + ';' + str(row[1]) + '\n'

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
                pass #TODO
