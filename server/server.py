import socket
from server_thread import *
from sys import exit
from _thread import *


class Server:
  
  def __init__(self, address):
    self.ip, self.port = address
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.bind(address)

  def run(self):
    self.socket.listen()
    print('Server running at port',self.port)

    while True: 
      connection, address = self.socket.accept()
      start_new_thread(server_thread, (connection, address))
    
def main():
  address = ("localhost", 20000)
  server = Server(address)
  server.run()

if __name__ == '__main__':
  main()
