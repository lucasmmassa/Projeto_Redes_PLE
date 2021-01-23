from abc import ABC, abstractclassmethod
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

def pre_process_text(text):
  no_numbers_text = re.sub("[a-zA-Z]*[0-9]+[a-z-A-Z]*",'',text)
  no_numbers_text = no_numbers_text.lower()
  no_numbers_text = no_numbers_text.replace('\n', ' ')
  return no_numbers_text

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

class CV_Command(Command):

    def __init__(self,status,ip,port,data):
        super().__init__()
        self.status = status
        self.origin_ip = ip
        self.origin_port = port
        self.data = data


    def run(self):
        for i in range(len(self.data)):
            self.data[i] = pre_process_text(self.data[i])

        cv = CountVectorizer(lowercase=True,max_features=5000)
        self.result = cv.fit_transform(self.data).toarray().tolist()

        print('COMMAND=CV - STATUS=200 - CLIENT='+self.origin_ip+':'+self.origin_port+'\n')

class TFIDF_Command(Command):

    def __init__(self,status,ip,port,data):
        super().__init__()
        self.status = status
        self.origin_ip = ip
        self.origin_port = port
        self.data = data


    def run(self):
        for i in range(len(self.data)):
            self.data[i] = pre_process_text(self.data[i])

        tfidf = TfidfVectorizer(lowercase=True,max_features=5000)
        self.result = tfidf.fit_transform(self.data).toarray().tolist()

        print('COMMAND=CV - STATUS=200 - CLIENT='+self.origin_ip+':'+self.origin_port+'\n')
