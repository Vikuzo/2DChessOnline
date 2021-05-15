import chessPieces
import threading
import socket
import yaml


def from_chessboard_to_string(chessboard):
    string = ''
    for line in chessboard:
        for piece in line:
            string += piece + '*'
    return string


def from_string_to_chessboard(string, rows, columns):
    chessboard = []
    c = 0
    for row in range(rows):
        lis = []
        for column in range(columns):
            lis.append(string[c:string.find('*', c)])
            c = string.find('*', c) + 1
        chessboard.append(lis)

    return chessboard


def show_chessboard(chessboard):
    for lines in chessboard:
        for piece in lines:
            print(piece, end=' ')
        print('\n')


def update(chessboard, piece_name, coordinates, zero):
    for lists in chessboard:
        for item in range(len(lists)):
            if lists[item] == piece_name:
                lists[item] = zero

    chessboard[coordinates[0]][coordinates[1]] = piece_name
    return from_chessboard_to_string(chessboard)


class ChessClient:
    __run = False
    __pieceColor = ''
    __rows = ''
    __columns = ''
    __all_pieces = []

    def __init__(self):
        with open('Configuration.yaml', 'r') as yamlConfig:
            self.__config = yaml.load(yamlConfig, Loader=yaml.FullLoader)

        self.__rows = self.__config['chessConfig']['rows']
        self.__columns = self.__config['chessConfig']['columns']

        try:
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.connect((self.__config['socketConfig']['serverIP'],
                                  self.__config['socketConfig']['serverPort']))
            self.__pieceColor = clientSocket.recv(self.__config['socketConfig']['buffer']).decode('utf-8')
            chessboard = from_string_to_chessboard(clientSocket.recv(self.__config['socketConfig']['buffer']).
                                                   decode('utf-8'), self.__rows, self.__columns)

            gameThread = threading.Thread(target=self.game, args=(clientSocket, chessboard))
            gameThread.start()
            gameThread.join()
        except socket.error:
            self.__init__()

    def checking_selected_move(self, chessboard, piece_name, coordinates):
        c = 0
        while self.__all_pieces[c].get_piece_name() != piece_name:
            c += 1

        if coordinates in self.__all_pieces[c].piece_possible_moves(chessboard):
            self.__all_pieces[c].set_row(coordinates[0])
            self.__all_pieces[c].set_column(coordinates[1])
            return True

        return False

    def game(self, clientSocket, chessboard):
        self.__run = True

        if self.__pieceColor == self.__config['chessConfig']['whitePieces']['startLetter']:
            c1 = 0
            c2 = 0
            for lines in chessboard:
                for piece in lines:
                    if piece[0:1] == self.__pieceColor:
                        if piece[1:2] == self.__config['chessConfig']['whitePieces']['wp'][1:2]:
                            pawn = chessPieces.Pawn(piece, 6, c1)
                            self.__all_pieces.append(pawn)
                            c1 += 1
                        if piece[1:2] == self.__config['chessConfig']['whitePieces']['wr'][1:2]:
                            rook = chessPieces.Rook(piece, 7, c2)
                            self.__all_pieces.append(rook)
                            c2 += 1
                        if piece[1:2] == self.__config['chessConfig']['whitePieces']['wb'][1:2]:
                            bishop = chessPieces.Bishop(piece, 7, c2)
                            self.__all_pieces.append(bishop)
                            c2 += 1
                        if piece[1:2] == self.__config['chessConfig']['whitePieces']['wk'][1:2]:
                            knight = chessPieces.Knight(piece, 7, c2)
                            self.__all_pieces.append(knight)
                            c2 += 1
                        if piece[1:2] == self.__config['chessConfig']['whitePieces']['wK'][1:2]:
                            king = chessPieces.King(piece, 7, c2)
                            self.__all_pieces.append(king)
                            c2 += 1
                        if piece[1:2] == self.__config['chessConfig']['whitePieces']['wq'][1:2]:
                            queen = chessPieces.Queen(piece, 7, c2)
                            self.__all_pieces.append(queen)
                            c2 += 1
        else:
            c1 = 0
            c2 = 0
            for lines in chessboard:
                for piece in lines:
                    if piece[0:1] == self.__pieceColor:
                        if piece[1:2] == self.__config['chessConfig']['blackPieces']['bp'][1:2]:
                            pawn = chessPieces.Pawn(piece, 1, c1)
                            self.__all_pieces.append(pawn)
                            c1 += 1
                        if piece[1:2] == self.__config['chessConfig']['blackPieces']['br'][1:2]:
                            rook = chessPieces.Rook(piece, 0, c2)
                            self.__all_pieces.append(rook)
                            c2 += 1
                        if piece[1:2] == self.__config['chessConfig']['blackPieces']['bb'][1:2]:
                            bishop = chessPieces.Bishop(piece, 0, c2)
                            self.__all_pieces.append(bishop)
                            c2 += 1
                        if piece[1:2] == self.__config['chessConfig']['blackPieces']['bk'][1:2]:
                            knight = chessPieces.Knight(piece, 0, c2)
                            self.__all_pieces.append(knight)
                            c2 += 1
                        if piece[1:2] == self.__config['chessConfig']['blackPieces']['bK'][1:2]:
                            king = chessPieces.King(piece, 0, c2)
                            self.__all_pieces.append(king)
                            c2 += 1
                        if piece[1:2] == self.__config['chessConfig']['blackPieces']['bq'][1:2]:
                            queen = chessPieces.Queen(piece, 0, c2)
                            self.__all_pieces.append(queen)
                            c2 += 1

        show_chessboard(chessboard)

        while self.__run:
            if self.__pieceColor == self.__config['chessConfig']['whitePieces']['startLetter']:
                print('Sei i bianchi!')
                piece = input('Inserire il pezzo da muovere: ')
                row = int(input('A che riga va spostato: '))
                column = int(input('A che colonna va spostato: '))
                while not self.checking_selected_move(chessboard, piece, (row - 1, column - 1)):
                    print('Non puoi fare quella mossa')
                    piece = input('Inserire il pezzo da muovere: ')
                    row = int(input('A che riga va spostato: '))
                    column = int(input('A che colonna va spostato: '))
                clientSocket.send(update(chessboard, piece, (row - 1, column - 1),
                                         self.__config['chessConfig']['vp']).encode('utf-8'))
                show_chessboard(chessboard)
                chessboard = from_string_to_chessboard(clientSocket.recv(self.__config['socketConfig']
                                                       ['buffer']).decode('utf-8'), self.__rows, self.__columns)
                show_chessboard(chessboard)
            else:
                print('Sei i neri!')
                chessboard = from_string_to_chessboard(clientSocket.recv(self.__config['socketConfig']
                                                       ['buffer']).decode('utf-8'), self.__rows, self.__columns)
                show_chessboard(chessboard)
                piece = input('Inserire il pezzo da muovere: ')
                row = int(input('A che riga va spostato: '))
                column = int(input('A che colonna va spostato: '))
                while not self.checking_selected_move(chessboard, piece, (row - 1, column - 1)):
                    print('Non puoi fare quella mossa')
                    piece = input('Inserire il pezzo da muovere: ')
                    row = int(input('A che riga va spostato: '))
                    column = int(input('A che colonna va spostato: '))
                clientSocket.send(update(chessboard, piece, (row - 1, column - 1),
                                         self.__config['chessConfig']['vp']).encode('utf-8'))
                show_chessboard(chessboard)


def __main__():
    _ = ChessClient()


if __name__ == '__main__':
    __main__()
