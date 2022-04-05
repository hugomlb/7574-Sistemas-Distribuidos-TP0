import logging
import os


class ClientHandler:

    def run(self, client_sock):
        """
        Read message from a specific client socket and closes the socket

        If a problem arises in the communication with the client, the
        client socket will also be closed
        """
        if(client_sock is not None):
          try:
              msg = client_sock.recv(1024).rstrip().decode('utf-8')
              logging.info(
                  'Message received from connection {} in process {}. Msg: {}'
                  .format(client_sock.getpeername(), os.getpid(), msg))
              #TODO: poner un for para saber cuanto falta enviar
              client_sock.send("Your Message has been received: {}\n".format(msg).encode('utf-8'))
          except OSError:
              logging.info("Error while reading socket {}".format(client_sock))
          finally:
              client_sock.close()