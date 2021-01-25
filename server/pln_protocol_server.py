'''
O texto abaixo dá informações a respeito do protocolo criado.
O código se encontra logo após essa explicação.

#############################################################################################################

FORMATO DA MENSAGEM ENVIADA QUANDO CONTÉM TEXTOS:       FORMATO DA MENSAGEM ENVIADA QUANDO NÃO CONTÉM TEXTOS:

    COMANDO                                                 COMANDO
    TEXTO 1                                                 LINHA VAZIA
    TEXTO 2
    TEXTO 3
    ...
    TEXTO N
    LINHA VAZIA

#############################################################################################################

FORMATO DA RESPOSTA CONTENDO VETORES:                   FORMATO DA RESPOSTA SEM VETORES:

    STATUS                                                  STATUS
    X11;X12;...;X1m                                         LINHA VAZIA
    X21;X22;...;X2m
    X31;X32;...;X3m
    ...
    Xn1;Xn2;...;Xnm
    LINHA VAZIA

#############################################################################################################

As requisições podem resultar nos seguites códigos de status:

* 200 - SUCCESS: indica que uma requisição de vetorização foi bem sucedida;
* 300 - INVALID DATA: os textos dados de entrada não seguem o padrão exigido;
* 301 - ALGORITHM RUN FAILED: houve uma falha ao tentar executar o algoritmo nos textos enviados;
* 400 - INVALID COMMAND: o comando requisitado não faz parte da lista de comandos disponíveis;
* 500 DISCONNECTED: indica que a requisição de desconexão foi bem sucedida.
'''

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
                
