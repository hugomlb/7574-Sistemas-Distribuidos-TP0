import socket
import logging
import signal
import sys


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

        while self._running:
            self.__accept_new_connection()
            if (self._client_socket is not None):
                self.__handle_client_connection()

        logging.info("Ending Program")
    
    def __handle_sigterm(self, signum, frame):
        logging.info('Handling SIGTERM')
        self._running = False
        logging.info('Closing Server Socket')
        self._server_socket.close()
        self._close_client_socket()

    def __handle_client_connection(self):
        """
        Read message from a specific client socket and closes the socket

        If a problem arises in the communication with the client, the
        client socket will also be closed
        """
        try:
            msg = self._client_socket.recv(1024).rstrip().decode('utf-8')
            logging.info(
                'Message received from connection {}. Msg: {}'
                .format(self._client_socket.getpeername(), msg))
            self._client_socket.sendall("Your Message has been received: {}\n".format(msg).encode('utf-8'))
        except OSError:
            if self._running:
                logging.info("Error while reading socket {}".format(self._client_socket))
        finally:
            self._close_client_socket()

    def _close_client_socket(self):
        if (self._client_socket is not None):
            logging.info('Closing Client Socket')
            self._client_socket.close()
            self._client_socket = None

    def __accept_new_connection(self):
        """
        Accept new connections

        Function blocks until a connection to a client is made.
        Then connection created is printed and returned
        """

        # Connection arrived
        try: 
            logging.info("Proceed to accept new connections")
            self._client_socket = None
            self._client_socket, addr = self._server_socket.accept()
            logging.info('Got connection from {}'.format(addr))
        except OSError:
            if self._running:
                logging.info("Error while accepting connection")
