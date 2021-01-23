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
        message = self.command + '\n'

        if self.need_data:


            #TODO checar se os dados são iteraveis com string
            
            if len(data) < 1:
                self.valid_data = False
                print('Request not sent to the server.')
                print('STATUS 300 - INVALID DATA')
                return None

            for text in data:
                text = text.replace('\n',' ')
                message += text + '\n'

        message += '\n'

        return message

    def parse_response(self,response):
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


        print('STATUS',response_status,'-',self.status_messages[response_status])

        return result           
    