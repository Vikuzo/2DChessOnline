import threading
import socket
import yaml


def chessboard_first_generation():
    with open('Configuration.yaml', 'r') as yamlConfig:
        config = yaml.load(yamlConfig, Loader=yaml.FullLoader)

    vp = config['chessConfig']['vp']
    br = config['chessConfig']['blackPieces']['br']
    bk = config['chessConfig']['blackPieces']['bk']
    bb = config['chessConfig']['blackPieces']['bb']
    bq = config['chessConfig']['blackPieces']['bq']
    bK = config['chessConfig']['blackPieces']['bK']
    bp = config['chessConfig']['blackPieces']['bp']
    wr = config['chessConfig']['whitePieces']['wr']
    wk = config['chessConfig']['whitePieces']['wk']
    wb = config['chessConfig']['whitePieces']['wb']
    wq = config['chessConfig']['whitePieces']['wq']
    wK = config['chessConfig']['whitePieces']['wK']
    wp = config['chessConfig']['whitePieces']['wp']

    chessboard = [[br + '1', bk + '1', bb + '1', bq, bK, bb + '2', bk + '2', br + '2'],
                  [bp + '1', bp + '2', bp + '3', bp + '4', bp + '5', bp + '6', bp + '7', bp + '8'],
                  [vp, vp, vp, vp, vp, vp, vp, vp],
                  [vp, vp, vp, vp, vp, vp, vp, vp],
                  [vp, vp, vp, vp, vp, vp, vp, vp],
                  [vp, vp, vp, vp, vp, vp, vp, vp],
                  [wp + '1', wp + '2', wp + '3', wp + '4', wp + '5', wp + '6', wp + '7', wp + '8'],
                  [wr + '1', wk + '1', wb + '1', wq, wK, wb + '2', wk + '2', wr + '2']]

    return chessboard


def from_chessboard_to_string(chessboard):
    string = ''
    for line in chessboard:
        for piece in line:
            string += piece + '*'
    return string


class ChessServer:
    __connection = False
    __clients = []

    def __init__(self):
        with open('Configuration.yaml', 'r') as yamlConfig:
            self.__config = yaml.load(yamlConfig, Loader=yaml.FullLoader)

        try:
            serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serverSocket.bind((self.__config['socketConfig']['serverIP'], self.__config['socketConfig']['serverPort']))
            serverSocket.listen(self.__config['socketConfig']['serverListen'])
            serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            print('Server in piedi ed operativo!')

            connectionThread = threading.Thread(target=self.connection, args=(serverSocket,))
            connectionThread.start()

            connectionThread.join()
        except socket.error:
            print('Errore in fasi di avvio. Riavvio del server in corso...\n')
            self.__init__()

    def connection(self, serverSocket):
        self.__connection = True

        while self.__connection:
            try:
                chessboard = chessboard_first_generation()

                whiteSocket, address = serverSocket.accept()
                print('Utente connesso: ' + str(address))

                blackSocket, address = serverSocket.accept()
                print('Utente connesso: ' + str(address))

                whiteSocket.send(self.__config['chessConfig']['whitePieces']['startLetter'].encode('utf-8'))
                whiteSocket.send(from_chessboard_to_string(chessboard).encode('utf8'))
                blackSocket.send(self.__config['chessConfig']['blackPieces']['startLetter'].encode('utf-8'))
                blackSocket.send(from_chessboard_to_string(chessboard).encode('utf-8'))

                self.__clients.append((whiteSocket, blackSocket))

                buffer = self.__config['socketConfig']['buffer']
                communicationThread = threading.Thread(target=self.communication, args=(whiteSocket, blackSocket,
                                                                                        buffer))
                communicationThread.start()
            except socket.error:
                print('Il server si sta chiudendo, bye bye!')

    def communication(self, whiteSocket, blackSocket, buffer):
        run = True

        while run:
            chessboard = whiteSocket.recv(buffer).decode('utf-8')
            print(whiteSocket, end=' -->')
            print(chessboard)
            blackSocket.send(chessboard.encode('utf-8'))
            chessboard = blackSocket.recv(buffer).decode('utf-8')
            print(blackSocket, end=' -->')
            print(chessboard)
            whiteSocket.send(chessboard.encode('utf-8'))

        self.update((whiteSocket, blackSocket))

    def update(self, sockets):
        c = 0
        for client in self.__clients:
            c += 1
            if client == sockets:
                self.__clients.pop(c)

        sockets[0].close()
        sockets[1].close()

    def broadcast(self):
        for client in self.__clients:
            client[0].close()
            client[1].close()
            self.__clients.pop(0)

    def server_shutdown(self, serverSocket):
        while input() != 'close':
            pass

        self.broadcast()
        serverSocket.close()
        raise socket.error

    def set_connection_run(self):
        self.__connection = not self.__connection

    def get_connection_run(self):
        return self.__connection


def __main__():
    _ = ChessServer()


if __name__ == '__main__':
    __main__()
