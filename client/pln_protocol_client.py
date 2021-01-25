import io

class PLN_Protocol_Client:

    def __init__(self,command):
        self.valid_commands = ['DISCONNECT','CV','TFIDF']  
        self.command = command
        self.valid = command in self.valid_commands

        if self.valid:
            self.need_data = None
            self.disconnect_successful = False
            self.valid_data = True

            self.status_messages = {
                '200' : 'SUCCESS',
                '300' : 'INVALID DATA',
                '301' : 'ALGORITHM RUN FAILED',
                '400' : 'INVALID COMMAND',
                '500' : 'DISCONNECTED',
            }
            
            if self.command == 'DISCONNECT':
                self.need_data = False
            else:
                self.need_data = True

        else:
            print('Request not sent to the server.')
            print('STATUS 400 - INVALID COMMAND\n')

    def format_message(self,data):
        print('Formating the message to be sent...\n')

        message = self.command + '\n'

        if self.need_data:
            if not type(data) == list:
                self.valid_data = False
                print('The received data is not a list.')
                print('Request not sent to the server.')
                print('STATUS 300 - INVALID DATA')
                return None
            
            if len(data) < 1:
                self.valid_data = False
                print('The received data is an empty list.')
                print('Request not sent to the server.')
                print('STATUS 300 - INVALID DATA')
                return None

            for text in data:
                if not type(text) == str:
                    print('The received data contains non string elements.')
                    print('Request not sent to the server.')
                    print('STATUS 300 - INVALID DATA')
                    return None
                
                if text == '':
                    print('The received data contains empty strings. This can cause problems for the protocol to parse the message.')
                    print('Request not sent to the server.')
                    print('STATUS 300 - INVALID DATA')
                    return None

                text = text.replace('\n',' ')
                message += text + '\n'

        message += '\n'

        print('Finished formating.\n')

        return message

    def parse_response(self,response):
        print('Parsing the received response...\n')

        buffer = io.StringIO(response)
        response_status = buffer.readline().replace('\n','')

        result = None

        if self.need_data:
            empty = False
            result = []

            while not empty:              
                row = buffer.readline().replace('\n','')

                if row == '':
                    empty = True

                else:
                    row = row.split(';')
                    for i in range(len(row)):
                        row[i] = float(row[i])

                    result.append(row)

        if response_status == '500':
            self.disconnect_successful = True

        print('Finished parsing.\n')

        print('STATUS',response_status,'-',self.status_messages[response_status],'\n')

        return result           
    