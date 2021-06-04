##  @file 2DChess.py

import chessPieces
import pygame
import socket
import yaml


## La funzione converte la matrice degli scacchi in una stringa
# @param chessboard matrice del campo di gioco
# @return string la scacchiera fatta a stringa


def from_chessboard_to_string(chessboard):
    string = ''
    for line in chessboard:
        for piece in line:
            string += piece + '*'
    return string


## La funzione converte la scacchiera in forma di stringa in matrice
# @param string la stringa da convertire
# @param rows il numero di righe della scacchiera
# @param columns il numero di colonne della scacchiera
# @return chessboard la versione in matrice della scacchiera


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


## La funzione stampa graficamente la scacchiera
# @param config file di configurazione
# @param height altezza della finestra
# @param width larghezza della finestra
# @param buttons vettore dei pezzi
# @param pieceColor colore dei pezzi del giocatore
# @param window oggetto rappresentante la finestra
# @param chessboard la matrice della scacchiera
# @param moves_button vettori dei bottoni delle mosse


def chessboard_print(config, height, width, buttons, pieceColor, window, chessboard, moves_button):
    background = pygame.image.load(config['imagePath']['gameBackground'])
    background = pygame.transform.scale(background, (width, height))
    window.blit(background, (0, 0))

    YELLOW = (config['color']['yellow']['red'], config['color']['yellow']['green'],
              config['color']['yellow']['blue'])
    LIGHT_GREEN = (config['color']['light_green']['red'], config['color']['light_green']['green'],
                   config['color']['light_green']['blue'])
    sizes = height // 8
    y = 0

    color = False

    for i in range(config['chessConfig']['rows']):
        x = (width - (sizes * 8)) / 2
        for j in range(config['chessConfig']['columns']):
            if color:
                pygame.draw.rect(window, LIGHT_GREEN, pygame.Rect(x, y, sizes, sizes))
                color = False
            else:
                pygame.draw.rect(window, YELLOW, pygame.Rect(x, y, sizes, sizes))
                color = True
            x += sizes
        color = not color
        y += sizes

    y = 0

    for moves in moves_button:
        moves.show(window, config)

    for lines in chessboard:
        x = 0
        for piece in lines:
            if piece[0:1] != pieceColor and piece != config['chessConfig']['vp']:
                icon = pygame.image.load(config['imagePath'][piece[0:2]])
                icon = pygame.transform.scale(icon, (sizes, sizes))
                window.blit(icon, ((x * sizes) + (width - (sizes * 8)) / 2, (y * sizes)))
            x += 1
        y += 1

    for items in buttons:
        items.show(window)


def update(chessboard, piece_name, coordinates, zero):
    for lists in chessboard:
        for item in range(len(lists)):
            if lists[item] == piece_name:
                lists[item] = zero

    chessboard[coordinates[0]][coordinates[1]] = piece_name
    return chessboard


## Classe per la generazione dei pezzi del colore del giocatore


class Button:

    ## Costruttore
    #  @param self riferimento all'oggeto stesso
    # @param icon valore dell'icona
    # @param pos tupla delle coordinate
    # @param size grandezza del rettangolo che occuperà il bottone
    # @param piece_name nome del pezzo rappresentato

    def __init__(self, icon, pos, size, piece_name):
        self.x, self.y = pos
        self.icon = icon
        self.size = size
        self.piece_name = piece_name
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    ## Mostra il bottone
    #  @param self riferimento all'oggeto stesso
    # @param window riferimento alla finestra

    def show(self, window):
        icon = pygame.image.load(self.icon)
        icon = pygame.transform.scale(icon, (self.size, self.size))
        window.blit(icon, (self.x, self.y))

    ## La funzione che gestisce il click sul bottone
    #  @param self riferimento all'oggeto stesso
    # @param event vettore degli eventi
    # @param config file di configurazione
    # @param height altezza della finestra
    # @param width larghezza della finestra
    # @param all_pieces vettore degli scacchi del giocatore
    # @param buttons vettore dei bottoni degli scacchi del giocatore
    # @param pieceColor colore dei pezzi del giocatore
    # @param window riferimento all'oggetto finestra
    # @param chessboard la matrice della scacchiera
    # @param moves_button vettore dei bottoni di movimento

    def click(self, event, config, height, width, all_pieces, buttons, pieceColor, window, chessboard, moves_button):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    moves_button.clear()
                    for item in all_pieces:
                        if item.get_piece_name() == self.piece_name:
                            moves = item.piece_possible_moves(chessboard)
                            if moves != [(8, 8)]:
                                for move in moves:
                                    moves_button.append(
                                        movesButton(((move[1] * self.size) + (width - (self.size * 8)) / 2,
                                                    (move[0] * self.size)), self.size, self.piece_name))
                            else:
                                if pieceColor == config['chessConfig']['whitePieces']['startLetter']:
                                    x, y = 0, 0
                                    moves_button.append(choiceButton(config['imagePath']['wq'], (x, y),
                                                        self.size, self.piece_name,
                                                        config['chessConfig']['whitePieces']['wq']))
                                    y += self.size
                                    moves_button.append(choiceButton(config['imagePath']['wb'], (x, y),
                                                        self.size, self.piece_name,
                                                        config['chessConfig']['whitePieces']['wb']))
                                    y += self.size
                                    moves_button.append(choiceButton(config['imagePath']['wk'], (x, y),
                                                        self.size, self.piece_name,
                                                        config['chessConfig']['whitePieces']['wk']))
                                    y += self.size
                                    moves_button.append(choiceButton(config['imagePath']['wr'], (x, y),
                                                        self.size, self.piece_name,
                                                        config['chessConfig']['whitePieces']['wr']))
                                else:
                                    x, y = 0, 0
                                    moves_button.append(choiceButton(config['imagePath']['bq'], (x, y),
                                                        self.size, self.piece_name,
                                                        config['chessConfig']['blackPieces']['bq']))
                                    y += self.size
                                    moves_button.append(choiceButton(config['imagePath']['bb'], (x, y),
                                                        self.size, self.piece_name,
                                                        config['chessConfig']['blackPieces']['bb']))
                                    y += self.size
                                    moves_button.append(choiceButton(config['imagePath']['bk'], (x, y),
                                                        self.size, self.piece_name,
                                                        config['chessConfig']['blackPieces']['bk']))
                                    y += self.size
                                    moves_button.append(choiceButton(config['imagePath']['br'], (x, y),
                                                        self.size, self.piece_name,
                                                        config['chessConfig']['blackPieces']['br']))
                    chessboard_print(config, height, width, buttons, pieceColor, window, chessboard,
                                     moves_button)
                    pygame.draw.rect(window, (config['color']['cyan']['red'], config['color']['cyan']['green'],
                                              config['color']['cyan']['blue']), self.rect)
                    self.show(window)

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y


## Bottone dei movimenti


class movesButton:

    ## Costruttore
    #  @param self riferimento all'oggeto stesso
    # @param pos tupla delle coordinate
    # @param size grandezza del rettangolo che occuperà il bottone
    # @param piece_name nome del pezzo rappresentato

    def __init__(self, pos, size, piece_name):
        self.x, self.y = pos
        self.size = size
        self.piece_name = piece_name
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    ## Mostra il bottone
    #  @param self riferimento all'oggeto stesso
    # @param window riferimento alla finestra
    # @param config file di configurazione

    def show(self, window, config):
        pygame.draw.rect(window, (config['color']['red']['red'], config['color']['red']['green'],
                                  config['color']['red']['blue']), self.rect)

    ## La funzione che gestisce il click sul bottone
    #  @param self riferimento all'oggeto stesso
    # @param event vettore degli eventi
    # @param config file di configurazione
    # @param height altezza della finestra
    # @param width larghezza della finestra
    # @param all_pieces vettore degli scacchi del giocatore
    # @param buttons vettore dei bottoni degli scacchi del giocatore
    # @param pieceColor colore dei pezzi del giocatore
    # @param window riferimento all'oggetto finestra
    # @param chessboard la matrice della scacchiera
    # @param moves_button vettore dei bottoni di movimento

    def click(self, event, chessboard, config, buttons, all_pieces, moves_button, height, width, pieceColor, window):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    for button in buttons:
                        if self.piece_name == button.piece_name:
                            button.set_x(self.x)
                            button.set_y(self.y)
                            button.rect = pygame.Rect(self.x, self.y, self.size, self.size)
                            for piece in all_pieces:
                                if piece.get_piece_name() == self.piece_name:
                                    piece.set_row(int(self.y // self.size))
                                    piece.set_column(int((self.x - ((width - (self.size * 8)) / 2)) // self.size))
                                    moves_button.clear()
                                    if piece.get_piece_name()[1:2] == config['chessConfig']['whitePieces']['wp'][1:2]:
                                        if piece.get_first_move():
                                            piece.set_first_move()
                                    chessboard_print(config, height, width, buttons, pieceColor, window, chessboard,
                                                     moves_button)
                                    return update(chessboard, piece.get_piece_name(),
                                                  (int(self.y // self.size),
                                                  int(self.x - ((width - (self.size * 8)) / 2)) // self.size),
                                                  config['chessConfig']['vp'])


## Bottone di modifica del pezzo


class choiceButton:

    ## Costruttore
    #  @param self riferimento all'oggeto stesso
    # @param icon valore dell'icona
    # @param pos tupla delle coordinate
    # @param size grandezza del rettangolo che occuperà il bottone
    # @param piece_name nome del pezzo rappresentato
    # @param new_piece nome del pezzo in cui il pezzo selezionato verrà trasformato

    def __init__(self, icon, pos, size, piece_name, new_piece):
        self.x, self.y = pos
        self.size = size
        self.piece_name = piece_name
        self.new_piece = new_piece
        self.icon = icon
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    ## Mostra il bottone
    #  @param self riferimento all'oggeto stesso
    # @param window riferimento alla finestra
    # @param config file di configurazione

    def show(self, window, config):
        pygame.draw.rect(window, (config['color']['red']['red'], config['color']['red']['green'],
                                  config['color']['red']['blue']), self.rect)
        icon = pygame.image.load(self.icon)
        icon = pygame.transform.scale(icon, (self.size, self.size))
        window.blit(icon, (self.x, self.y))

    ## La funzione che gestisce il click sul bottone
    #  @param self riferimento all'oggeto stesso
    # @param event vettore degli eventi
    # @param config file di configurazione
    # @param height altezza della finestra
    # @param width larghezza della finestra
    # @param all_pieces vettore degli scacchi del giocatore
    # @param buttons vettore dei bottoni degli scacchi del giocatore
    # @param pieceColor colore dei pezzi del giocatore
    # @param window riferimento all'oggetto finestra
    # @param chessboard la matrice della scacchiera
    # @param moves_button vettore dei bottoni di movimento
    # @return chessboard ritorna la matrice della scacchiera col nuovo pezzo

    def click(self, event, chessboard, config, buttons, all_pieces, moves_button, height, width, pieceColor, window):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    moves_button.clear()
                    c = 1
                    for lines in chessboard:
                        for element in lines:
                            if element[0:2] == self.piece_name[0:2]:
                                c += 1
                    i = 0

                    for piece in all_pieces:
                        if piece.get_piece_name() == self.piece_name:
                            if self.new_piece[1:2] == config['chessConfig']['whitePieces']['wb'][1:2]:
                                p = all_pieces.pop(i)
                                all_pieces.append(chessPieces.Bishop(self.new_piece + str(c), p.get_row(),
                                                                     p.get_column()))
                                chessboard[p.get_row()][p.get_column()] = self.new_piece + str(c)
                                print(chessboard)
                                for button in buttons:
                                    if button.piece_name == self.piece_name:
                                        button.icon = config['imagePath'][self.new_piece]
                                        button.piece_name = all_pieces[-1].get_piece_name()
                                chessboard_print(config, height, width, buttons, pieceColor, window, chessboard,
                                                 moves_button)
                                return chessboard
                            if self.new_piece[1:2] == config['chessConfig']['whitePieces']['wk'][1:2]:
                                p = all_pieces.pop(i)
                                all_pieces.append(chessPieces.Knight(self.new_piece + str(c), p.get_row(),
                                                                     p.get_column()))
                                chessboard[p.get_row()][p.get_column()] = self.new_piece + str(c)
                                for button in buttons:
                                    if button.piece_name == self.piece_name:
                                        button.icon = config['imagePath'][self.new_piece]
                                        button.piece_name = all_pieces[-1].get_piece_name()
                                chessboard_print(config, height, width, buttons, pieceColor, window, chessboard,
                                                 moves_button)
                                return chessboard
                            if self.new_piece[1:2] == config['chessConfig']['whitePieces']['wq'][1:2]:
                                p = all_pieces.pop(i)
                                all_pieces.append(chessPieces.Queen(self.new_piece + str(c), p.get_row(),
                                                                    p.get_column()))
                                chessboard[p.get_row()][p.get_column()] = self.new_piece + str(c)
                                for button in buttons:
                                    if button.piece_name == self.piece_name:
                                        button.icon = config['imagePath'][self.new_piece]
                                        button.piece_name = all_pieces[-1].get_piece_name()
                                chessboard_print(config, height, width, buttons, pieceColor, window, chessboard,
                                                 moves_button)
                                return chessboard
                            if self.new_piece[1:2] == config['chessConfig']['whitePieces']['wk'][1:2]:
                                p = all_pieces.pop(i)
                                all_pieces.append(chessPieces.Rook(self.new_piece + str(c), p.get_row(),
                                                                   p.get_column()))
                                chessboard[p.get_row()][p.get_column()] = self.new_piece + str(c)
                                for button in buttons:
                                    if button.piece_name == self.piece_name:
                                        button.icon = config['imagePath'][self.new_piece]
                                        button.piece_name = all_pieces[-1].get_piece_name()
                                chessboard_print(config, height, width, buttons, pieceColor, window, chessboard,
                                                 moves_button)
                                return chessboard
                        i += 1


## Classe che permette di collegarsi al server e giocare


class ChessClient:
    __run = False
    __pieceColor = ''
    __rows = ''
    __columns = ''
    __all_pieces = []
    __buttons = []
    __moves_button = []

    ## Costruttore
    #  @param self riferimento all'oggeto stesso

    def __init__(self):
        with open('Configuration.yaml', 'r') as yamlConfig:
            self.__config = yaml.load(yamlConfig, Loader=yaml.FullLoader)

        self.__rows = self.__config['chessConfig']['rows']
        self.__columns = self.__config['chessConfig']['columns']
        self.__running, self.__playing = True, False
        self.__width = self.__config['screenConfig']['width']
        self.__height = self.__config['screenConfig']['height']

        pygame.init()

        pygame.Surface((self.__width, self.__height))
        window = pygame.display.set_mode((self.__width, self.__height))
        pygame.display.set_caption('2DChessOnline - Menù')

        self.main_menu(window)

    def checking_selected_move(self, chessboard, piece_name, coordinates):
        c = 0
        while self.__all_pieces[c].get_piece_name() != piece_name:
            c += 1

        if coordinates in self.__all_pieces[c].piece_possible_moves(chessboard):
            self.__all_pieces[c].set_row(coordinates[0])
            self.__all_pieces[c].set_column(coordinates[1])
            return True

        return False

    ## La funzione genera tutto ciò che è visibile nel menù
    #  @param self riferimento all'oggeto stesso
    # @param riferimento alla finestra

    def menu_text(self, window):
        background = pygame.image.load(self.__config['imagePath']['menuBackground'])
        background = pygame.transform.scale(background, (self.__width, self.__height))
        window.blit(background, (0, 0))

        pygame.font.init()
        font = pygame.font.SysFont('Arial', self.__config['screenConfig']['textPT'])
        WHITE = (self.__config['color']['white']['red'], self.__config['color']['white']['green'],
                 self.__config['color']['white']['blue'])

        menuText = font.render('Premi invio per cercare una partita', True, WHITE)
        window.blit(menuText, ((self.__width // 2) - 60, self.__height // 3))

        pygame.display.update()

    ## La funzione si occupa di non lasciar chiudere il menù a meno che non sia l'utente a volerlo
    #  @param self riferimento all'oggeto stesso
    # @param riferimento alla finestra

    def main_menu(self, window):
        clock = pygame.time.Clock()
        icon = pygame.image.load(self.__config['imagePath']['icon'])
        pygame.display.set_icon(icon)
        self.menu_text(window)

        while self.__running:
            clock.tick(self.__config['screenConfig']['FPS'])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running, self.__playing = False, False

                key_pressed = pygame.key.get_pressed()
                if key_pressed[pygame.K_RETURN]:
                    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    clientSocket.connect((self.__config['socketConfig']['serverIP'],
                                          self.__config['socketConfig']['serverPort']))
                    self.__pieceColor = clientSocket.recv(self.__config['socketConfig']['buffer']).decode('utf-8')
                    chessboard = from_string_to_chessboard(clientSocket.recv(self.__config['socketConfig']['buffer']).
                                                           decode('utf-8'), self.__rows, self.__columns)
                    self.__running = True
                    self.game(window, chessboard, clientSocket)

                pygame.display.update()

        pygame.quit()

    ## La funzione che genera tutto ciò di correlato alla scacchiera (vettori di oggetti, vettori di bottoni ecc...)
    #  @param self riferimento all'oggeto stesso
    # @param riferimento alla finestra
    # @param chessboard la matrice della scacchiera

    def chessboard_generation(self, window, chessboard):
        sizes = self.__height // 8

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

        for items in self.__all_pieces:
            self.__buttons.append(Button(items.get_icon(), (((items.get_column() * sizes) + (self.__width - (sizes * 8))
                                                             / 2), (items.get_row() * sizes)), sizes,
                                         items.get_piece_name()))

        chessboard_print(self.__config, self.__height, self.__width, self.__buttons,
                         self.__pieceColor, window, chessboard, self.__moves_button)
        pygame.display.update()

    ## La funzione controlla se il re ha subito lo scacco matto oppure no
    #  @param self riferimento all'oggeto stesso
    # @param chessboard matrice della scacchiera
    # @param clientSocket socket di comunicazione col server

    def checkmate_check(self, chessboard, clientSocket):
        other_piece = []

        if self.__pieceColor == self.__config['chessConfig']['whitePieces']['startLetter']:
            c1 = 0
            for lines in chessboard:
                c2 = 0
                for piece in lines:
                    if piece[0:1] != self.__pieceColor:
                        if piece[1:2] == self.__config['chessConfig']['blackPieces']['bp'][1:2]:
                            pawn = chessPieces.Pawn(piece, c1, c2)
                            pawn.set_first_move()
                            other_piece.append(pawn)
                        if piece[1:2] == self.__config['chessConfig']['blackPieces']['br'][1:2]:
                            rook = chessPieces.Rook(piece, c1, c2)
                            other_piece.append(rook)
                        if piece[1:2] == self.__config['chessConfig']['blackPieces']['bb'][1:2]:
                            bishop = chessPieces.Bishop(piece, c1, c2)
                            other_piece.append(bishop)
                        if piece[1:2] == self.__config['chessConfig']['blackPieces']['bk'][1:2]:
                            knight = chessPieces.Knight(piece, c1, c2)
                            other_piece.append(knight)
                        if piece[1:2] == self.__config['chessConfig']['blackPieces']['bK'][1:2]:
                            king = chessPieces.King(piece, c1, c2)
                            other_piece.append(king)
                        if piece[1:2] == self.__config['chessConfig']['blackPieces']['bq'][1:2]:
                            queen = chessPieces.Queen(piece, c1, c2)
                            other_piece.append(queen)
                        c2 += 1

                c1 += 1

            king = chessPieces.King('bk', 0, 0)

            for pieces in self.__all_pieces:
                if pieces.get_piece_name() == self.__config['chessConfig']['whitePieces']['wK']:
                    king = pieces

            king_moves = (king.get_row(), king.get_column())

            for piece in other_piece:
                lis = piece.piece_possible_moves(chessboard)
                for element in lis:
                    if element[0] == king_moves[0]:
                        if element[1] == king_moves[1]:
                            clientSocket.send(self.__config['chessConfig']['wins'].encode('utf-8'))
                            return True
        else:
            c1 = 0
            for lines in chessboard:
                c2 = 0
                for piece in lines:
                    if piece[0:1] != self.__pieceColor:
                        if piece[1:2] == self.__config['chessConfig']['whitePieces']['wp'][1:2]:
                            pawn = chessPieces.Pawn(piece, c1, c2)
                            pawn.set_first_move()
                            other_piece.append(pawn)
                        if piece[1:2] == self.__config['chessConfig']['whitePieces']['wr'][1:2]:
                            rook = chessPieces.Rook(piece, c1, c2)
                            other_piece.append(rook)
                        if piece[1:2] == self.__config['chessConfig']['whitePieces']['wb'][1:2]:
                            bishop = chessPieces.Bishop(piece, c1, c2)
                            other_piece.append(bishop)
                        if piece[1:2] == self.__config['chessConfig']['whitePieces']['wk'][1:2]:
                            knight = chessPieces.Knight(piece, c1, c2)
                            other_piece.append(knight)
                        if piece[1:2] == self.__config['chessConfig']['whitePieces']['wK'][1:2]:
                            king = chessPieces.King(piece, c1, c2)
                            other_piece.append(king)
                        if piece[1:2] == self.__config['chessConfig']['whitePieces']['wq'][1:2]:
                            queen = chessPieces.Queen(piece, c1, c2)
                            other_piece.append(queen)
                        c2 += 1
                c1 += 1
            king = chessPieces.King('bk', 0, 0)

            for pieces in self.__all_pieces:
                if pieces.get_piece_name() == self.__config['chessConfig']['blackPieces']['bK']:
                    king = pieces

            king_moves = (king.get_row(), king.get_column())

            for piece in other_piece:
                lis = piece.piece_possible_moves(chessboard)
                for element in lis:
                    if element == king_moves:
                        clientSocket.send(self.__config['chessConfig']['wins'].encode('utf-8'))
                        return True

        return False

    ## La funzione si occupa di permettere all'utente di giocare
    #  @param self riferimento all'oggeto stesso
    # @param riferimento alla finestra
    # @param chessboard matrice della scacchiera
    # @param clientSocket socket di comunicazione col server

    def game(self, window, chessboard, clientSocket):
        pygame.display.set_caption('2DChessOnline - THE GAME')
        background = pygame.image.load(self.__config['imagePath']['gameBackground'])
        background = pygame.transform.scale(background, (self.__width, self.__height))
        window.blit(background, (0, 0))

        self.chessboard_generation(window, chessboard)

        win_or_lost = False
        after_game_screen = False

        if self.__pieceColor == self.__config['chessConfig']['blackPieces']['startLetter']:
            chessboard = from_string_to_chessboard(clientSocket.recv(
                self.__config['socketConfig']['buffer']).decode('utf-8'), self.__rows, self.__columns)
            chessboard_print(self.__config, self.__height, self.__width, self.__buttons,
                             self.__pieceColor, window, chessboard, self.__moves_button)

        while self.__running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running, self.__playing = False, False

                for item in self.__buttons:
                    item.click(event, self.__config, self.__height, self.__width, self.__all_pieces,
                               self.__buttons, self.__pieceColor, window, chessboard, self.__moves_button)

                for item in self.__moves_button:
                    c = item.click(event, chessboard, self.__config, self.__buttons, self.__all_pieces,
                                   self.__moves_button, self.__height, self.__width, self.__pieceColor, window)
                    if c is not None:
                        chessboard = c
                        chessboard_print(self.__config, self.__height, self.__width, self.__buttons,
                                         self.__pieceColor, window, chessboard, self.__moves_button)
                        if self.checkmate_check(chessboard, clientSocket):
                            self.__running = False
                            after_game_screen = True
                        else:
                            clientSocket.send(from_chessboard_to_string(chessboard).encode('utf-8'))
                            pygame.display.update()

                            message = clientSocket.recv(self.__config['socketConfig']['buffer']).decode('utf-8')
                            if message == self.__config['chessConfig']['wins']:
                                self.__running = False
                                after_game_screen = True
                                win_or_lost = True
                            else:
                                chessboard = from_string_to_chessboard(message, self.__rows, self.__columns)
                                lis = []
                                for line in chessboard:
                                    for piece in line:
                                        if piece[0:1] == self.__pieceColor:
                                            lis.append(piece)

                                new_all_pieces = []
                                for piece in self.__all_pieces:
                                    if piece.get_piece_name() in lis:
                                        new_all_pieces.append(piece)

                                self.__all_pieces = new_all_pieces

                                new_buttons = []
                                for button in self.__buttons:
                                    if button.piece_name in lis:
                                        new_buttons.append(button)

                                self.__buttons = new_buttons
                                chessboard_print(self.__config, self.__height, self.__width, self.__buttons,
                                                 self.__pieceColor, window, chessboard, self.__moves_button)
                                pygame.display.update()

            pygame.display.update()

        if win_or_lost:
            win = pygame.image.load(self.__config['imagePath']['winImage'])
            win = pygame.transform.scale(win, (self.__width//2, self.__height//2))
            window.blit(win, (self.__width//2 - (self.__width//4), self.__height//2 - (self.__height//4)))
        else:
            win = pygame.image.load(self.__config['imagePath']['loseImage'])
            win = pygame.transform.scale(win, (self.__width // 2, self.__height // 2))
            window.blit(win, (self.__width // 2 - (self.__width // 4), self.__height // 2 - (self.__height//4)))

        pygame.display.update()

        while after_game_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    after_game_screen, self.__playing = False, False

                key_pressed = pygame.key.get_pressed()
                if key_pressed[pygame.K_RETURN]:
                    after_game_screen = False
                    clientSocket.close()


## Funzione principale del programma, partirà da qui


def __main__():
    _ = ChessClient()


if __name__ == '__main__':
    __main__()
