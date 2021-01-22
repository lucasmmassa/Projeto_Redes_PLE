from abc import ABC, abstractclassmethod

class Command(ABC):

    def __init__(self):
        super().__init__()
        self.status = None
        self.result = []

    @abstractclassmethod
    def run(self):
        pass

class Invalid_Command(Command):

    def __init__(self,status,ip,port):
        super().__init__()
        self.status = status
        self.origin_ip = ip
        self.origin_port = port


    def run(self):
        print('COMMAND=INVALID - STATUS=400 - CLIENT='+self.origin_ip+':'+self.origin_port+'\n')

class Disconnect_Command(Command):

    def __init__(self,status,ip,port):
        super().__init__()
        self.status = status
        self.origin_ip = ip
        self.origin_port = port


    def run(self):
        print('COMMAND=DISCONNECT - STATUS=500 - CLIENT='+self.origin_ip+':'+self.origin_port+'\n')