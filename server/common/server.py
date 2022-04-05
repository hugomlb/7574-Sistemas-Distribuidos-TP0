import socket
import logging
import signal
import sys
from multiprocessing import Pool

from common.clientHandler import ClientHandler


class Server:
    def __init__(self, port, listen_backlog):
        # Initialize server socket
        signal.signal(signal.SIGTERM, self.__handle_sigterm)
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(('', port))
        self._server_socket.listen(listen_backlog)
        self._running = True
        self._client_socket = None

    def run(self):
        """
        Dummy Server loop
        Server that accept a new connections and establishes a
        communication with a client. After client with communucation
        finishes, servers starts to accept new connections again
        """

        # TODO: Modify this program to handle signal to graceful shutdown
        # the server

        processPool = Pool()
        while self._running:
            client_sock = self.__accept_new_connection()
            processPool.apply_async(ClientHandler.run, args=(ClientHandler, client_sock), 
            callback=logging.info,error_callback= logging.info
            )

        processPool.close()
        processPool.join()

        logging.info("Ending Program")
    
    def __handle_sigterm(self, signum, frame):
        logging.info('Handling SIGTERM')
        self._running = False
        logging.info('Closing Server Socket')
        self._server_socket.close()

    def __accept_new_connection(self):
        """
        Accept new connections
        Function blocks until a connection to a client is made.
        Then connection created is printed and returned
        """

        # Connection arrived
        try:
            logging.info("Proceed to accept new connections")
            c, addr = self._server_socket.accept()
            logging.info('Got connection from {}'.format(addr))
            return c
        except OSError:
            if self._running:
                logging.info("Error while accepting connection")
            return None
