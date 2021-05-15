import yaml


#  @file chessPieces.py

# Si occupa di fornire i metodi per la gestione, a livello basso, del giuco degli scacchi


# Classe da cui erediteranno tutti i pezzi metodi comuni


class ChessPiece:
    __piece_name = ''
    __row = 0
    __column = 0

    #  Costruttore
    #  @param self riferimento all'oggeto stesso
    #  @param piece_name indicazione sul pezzo in questione
    #  @param row posizione originaria sulle righe del campo di gioco del pezzo
    #  @param column posizione originaria sulle colonne del campo di gioco del pezzo

    def __init__(self, piece_name, row, column):
        self.__piece_name = piece_name
        self.__row = row
        self.__column = column

    # Si occupa di definire le possibili mosse attuabili da un pezzo; è astratto viene modificato dalle classi che la
    # ereditano
    # @param chessboard matrice del campo di gioco

    def piece_possible_moves(self, chessboard):
        pass

    # Aggiorna la coordinata y del pezzo
    # @param row nuovo valore della y

    def set_row(self, row):
        self.__row = row

    # Restituisce la coordinata y del pezzo

    def get_row(self):
        return self.__row

    # Aggiorna la coordinata x del pezzo
    # @param column nuovo valore della x

    def set_column(self, column):
        self.__column = column

    # Restituisce la coordinata y del pezzo

    def get_column(self):
        return self.__column

    # Restituisce il nome del pezzo

    def get_piece_name(self):
        return self.__piece_name


# Classe dedita alla gestione dei pedoni


class Pawn(ChessPiece):
    __first_move = True

    # Costruttore
    #  @param self riferimento all'oggeto stesso
    #  @param piece_name indicazione sul pezzo in questione
    #  @param row posizione originaria sulle righe del campo di gioco del pezzo
    #  @param column posizione originaria sulle colonne del campo di gioco del pezzo

    def __init__(self, piece_name, row, column):
        super().__init__(piece_name, row, column)

        with open('Configuration.yaml', 'r') as yamlConfig:
            self.__config = yaml.load(yamlConfig, Loader=yaml.FullLoader)

    # Si occupa di definire le possibili mosse attuabili da un pezzo; è astratto viene modificato dalle classi che la
    # ereditano, in questo caso i pedoni. Questa funzione, dopo i controlli vari, restituirà una lista di coordinate
    # alle quali sarà accettabile muovere la pedina
    # @param chessboard matrice del campo di gioco
    # @return acceptable_moves lista di coordinate di spostamenti accettabili della pedina

    def piece_possible_moves(self, chessboard):
        acceptable_moves = []
        max_movement = 1
        row_movement = 1
        start_letter = self.__config['chessConfig']['whitePieces']['startLetter']
        if self.__config['chessConfig']['blackPieces']['startLetter'] == self.get_piece_name()[0:1]:
            start_letter = self.__config['chessConfig']['blackPieces']['startLetter']
        rows = self.__config['chessConfig']['rows']
        columns = self.__config['chessConfig']['columns']
        vp = self.__config['chessConfig']['vp']

        if self.__first_move:
            max_movement = 2
            self.__first_move = False

        if self.__config['chessConfig']['whitePieces']['startLetter'] == self.get_piece_name()[0:1]:
            max_movement *= -1
            row_movement *= -1

        if max_movement > 0:
            if self.get_row() == rows - 1:
                return []  # Da modificare

        if max_movement < 0:
            if self.get_row() == 0:
                return []  # Da modificare

        if 2 == max_movement:
            if vp == chessboard[self.get_row() + max_movement][self.get_column()]:
                acceptable_moves.append((self.get_row() + max_movement, self.get_column()))
            max_movement -= 1

        if -2 == max_movement:
            if vp == chessboard[self.get_row() + max_movement][self.get_column()]:
                acceptable_moves.append((self.get_row() + max_movement, self.get_column()))
            max_movement += 1

        if vp == chessboard[self.get_row() + max_movement][self.get_column()]:
            acceptable_moves.append((self.get_row() + max_movement, self.get_column()))
        else:
            acceptable_moves.clear()

        if vp != chessboard[self.get_row() + row_movement][self.get_column() + 1] and self.get_column() < columns:
            if start_letter != chessboard[self.get_row() + row_movement][self.get_column() + 1][0:1]:
                acceptable_moves.append((self.get_row() + row_movement, self.get_column() + 1))

        if vp != chessboard[self.get_row() + row_movement][self.get_column() - 1] and self.get_column() > 0:
            if start_letter != chessboard[self.get_row() + row_movement][self.get_column() - 1][0:1]:
                acceptable_moves.append((self.get_row() + row_movement, self.get_column() - 1))

        return acceptable_moves


# Classe dedita alla gestione delle torri


class Rook(ChessPiece):

    # Costruttore
    #  @param self riferimento all'oggeto stesso
    #  @param piece_name indicazione sul pezzo in questione
    #  @param row posizione originaria sulle righe del campo di gioco del pezzo
    #  @param column posizione originaria sulle colonne del campo di gioco del pezzo

    def __init__(self, piece_name, row, column):
        super().__init__(piece_name, row, column)

        with open('Configuration.yaml', 'r') as yamlConfig:
            self.__config = yaml.load(yamlConfig, Loader=yaml.FullLoader)

    # Si occupa di definire le possibili mosse attuabili da un pezzo; è astratto viene modificato dalle classi che la
    # ereditano, in questo caso le torri. Questa funzione, dopo i controlli vari, restituirà una lista di coordinate
    # alle quali sarà accettabile muovere la pedina
    # @param chessboard matrice del campo di gioco
    # @return acceptable_moves lista di coordinate di spostamenti accettabili della pedina

    def piece_possible_moves(self, chessboard):
        row_acceptable_moves = []
        column_acceptable_moves = []
        rows = self.__config['chessConfig']['rows']
        columns = self.__config['chessConfig']['columns']
        vp = self.__config['chessConfig']['vp']

        if self.get_row() != rows - 1:
            keep = True
            movement = 1
            while keep:
                if self.get_row() + movement < rows:
                    if self.get_piece_name()[0:1] == chessboard[self.get_row() + movement][self.get_column()][0:1]:
                        keep = False
                    elif vp == chessboard[self.get_row() + movement][self.get_column()][0:1]:
                        row_acceptable_moves.append((self.get_row() + movement, self.get_column()))
                        movement += 1
                    else:
                        row_acceptable_moves.append((self.get_row() + movement, self.get_column()))
                        keep = False
                else:
                    keep = False

        if self.get_row() != 0:
            keep = True
            movement = -1
            while keep:
                if self.get_row() + movement >= 0:
                    if self.get_piece_name()[0:1] == chessboard[self.get_row() + movement][self.get_column()][0:1]:
                        keep = False
                    elif vp == chessboard[self.get_row() + movement][self.get_column()][0:1]:
                        row_acceptable_moves.append((self.get_row() + movement, self.get_column()))
                        movement -= 1
                    else:
                        row_acceptable_moves.append((self.get_row() + movement, self.get_column()))
                        keep = False
                else:
                    keep = False

        if self.get_column() != columns - 1:
            keep = True
            movement = 1
            while keep:
                if self.get_column() + movement < columns:
                    if self.get_piece_name()[0:1] == chessboard[self.get_row()][self.get_column() + movement][0:1]:
                        keep = False
                    elif vp == chessboard[self.get_row()][self.get_column() + movement][0:1]:
                        column_acceptable_moves.append((self.get_row(), self.get_column() + movement))
                        movement += 1
                    else:
                        column_acceptable_moves.append((self.get_row(), self.get_column() + movement))
                        keep = False
                else:
                    keep = False

        if self.get_column() != 0:
            keep = True
            movement = -1
            while keep:
                if self.get_column() + movement >= 0:
                    if self.get_piece_name()[0:1] == chessboard[self.get_row()][self.get_column() + movement][0:1]:
                        keep = False
                    elif vp == chessboard[self.get_row()][self.get_column() + movement][0:1]:
                        column_acceptable_moves.append((self.get_row(), self.get_column() + movement))
                        movement -= 1
                    else:
                        column_acceptable_moves.append((self.get_row(), self.get_column() + movement))
                        keep = False
                else:
                    keep = False

        acceptable_moves = row_acceptable_moves + column_acceptable_moves
        return acceptable_moves


# Classe dedita alla gestione degli alfieri


class Bishop(ChessPiece):

    # Costruttore
    #  @param self riferimento all'oggeto stesso
    #  @param piece_name indicazione sul pezzo in questione
    #  @param row posizione originaria sulle righe del campo di gioco del pezzo
    #  @param column posizione originaria sulle colonne del campo di gioco del pezzo

    def __init__(self, piece_name, row, column):
        super().__init__(piece_name, row, column)

        with open('Configuration.yaml', 'r') as yamlConfig:
            self.__config = yaml.load(yamlConfig, Loader=yaml.FullLoader)

    # Si occupa di definire le possibili mosse attuabili da un pezzo; è astratto viene modificato dalle classi che la
    # ereditano, in questo caso gli alfieri. Questa funzione, dopo i controlli vari, restituirà una lista di coordinate
    # alle quali sarà accettabile muovere la pedina
    # @param chessboard matrice del campo di gioco
    # @return acceptable_moves lista di coordinate di spostamenti accettabili della pedina

    def piece_possible_moves(self, chessboard):
        right_diagonal_acceptable_moves = []
        left_diagonal_acceptable_moves = []
        rows = self.__config['chessConfig']['rows']
        columns = self.__config['chessConfig']['columns']
        vp = self.__config['chessConfig']['vp']

        if self.get_row() != rows - 1:
            if self.get_column() != columns - 1:
                keep = True
                row_movement = 1
                column_movement = 1
                while keep:
                    if self.get_row() + row_movement < rows and self.get_column() + column_movement < columns:
                        if self.get_piece_name()[0:1] == chessboard[self.get_row() + row_movement][
                                                             self.get_column() + column_movement][0:1]:
                            keep = False
                        elif vp == chessboard[self.get_row() + row_movement][self.get_column() + column_movement][0:1]:

                            right_diagonal_acceptable_moves.append((self.get_row() + row_movement, self.get_column()
                                                                    + column_movement))
                            row_movement += 1
                            column_movement += 1
                        else:
                            right_diagonal_acceptable_moves.append((self.get_row() + row_movement, self.get_column()
                                                                    + column_movement))
                            keep = False
                    else:
                        keep = False

            if self.get_column() != 0:
                keep = True
                row_movement = 1
                column_movement = -1
                while keep:
                    if self.get_row() + row_movement < rows and self.get_column() + column_movement >= 0:
                        if self.get_piece_name()[0:1] == chessboard[self.get_row() + row_movement][
                                                             self.get_column() + column_movement][0:1]:
                            keep = False
                        elif vp == chessboard[self.get_row() + row_movement][self.get_column() + column_movement][0:1]:

                            left_diagonal_acceptable_moves.append((self.get_row() + row_movement, self.get_column()
                                                                   + column_movement))
                            row_movement += 1
                            column_movement -= 1
                        else:
                            left_diagonal_acceptable_moves.append((self.get_row() + row_movement, self.get_column()
                                                                   + column_movement))
                            keep = False
                    else:
                        keep = False

        if self.get_row() != 0:
            if self.get_column() != columns - 1:
                keep = True
                row_movement = -1
                column_movement = 1
                while keep:
                    if self.get_row() + row_movement < rows and self.get_column() + column_movement < columns:
                        if self.get_piece_name()[0:1] == chessboard[self.get_row() + row_movement][
                                                             self.get_column() + column_movement][0:1]:
                            keep = False
                        elif vp == chessboard[self.get_row() + row_movement][self.get_column() + column_movement][0:1]:

                            right_diagonal_acceptable_moves.append((self.get_row() + row_movement, self.get_column()
                                                                    + column_movement))
                            row_movement -= 1
                            column_movement += 1
                        else:
                            right_diagonal_acceptable_moves.append((self.get_row() + row_movement, self.get_column()
                                                                    + column_movement))
                            keep = False
                    else:
                        keep = False

            if self.get_column() != 0:
                keep = True
                row_movement = -1
                column_movement = -1
                while keep:
                    if self.get_row() + row_movement < rows and self.get_column() + column_movement >= 0:
                        if self.get_piece_name()[0:1] == chessboard[self.get_row() + row_movement][
                                                             self.get_column() + column_movement][0:1]:
                            keep = False
                        elif vp == chessboard[self.get_row() + row_movement][self.get_column() + column_movement][0:1]:

                            left_diagonal_acceptable_moves.append((self.get_row() + row_movement, self.get_column()
                                                                   + column_movement))
                            row_movement -= 1
                            column_movement -= 1
                        else:
                            left_diagonal_acceptable_moves.append((self.get_row() + row_movement, self.get_column()
                                                                   + column_movement))
                            keep = False
                    else:
                        keep = False

        acceptable_moves = right_diagonal_acceptable_moves + left_diagonal_acceptable_moves
        return acceptable_moves


# Classe dedita alla gestione dei cavalli


class Knight(ChessPiece):
    # Costruttore
    #  @param self riferimento all'oggeto stesso
    #  @param piece_name indicazione sul pezzo in questione
    #  @param row posizione originaria sulle righe del campo di gioco del pezzo
    #  @param column posizione originaria sulle colonne del campo di gioco del pezzo

    def __init__(self, piece_name, row, column):
        super().__init__(piece_name, row, column)

        with open('Configuration.yaml', 'r') as yamlConfig:
            self.__config = yaml.load(yamlConfig, Loader=yaml.FullLoader)

    # Si occupa di definire le possibili mosse attuabili da un pezzo; è astratto viene modificato dalle classi che la
    # ereditano, in questo caso i cavalli. Questa funzione, dopo i controlli vari, restituirà una lista di coordinate
    # alle quali sarà accettabile muovere la pedina
    # @param chessboard matrice del campo di gioco
    # @return acceptable_moves lista di coordinate di spostamenti accettabili della pedina

    def piece_possible_moves(self, chessboard):
        acceptable_moves = []
        l1_movement = 2
        l2_movement = 1
        rows = self.__config['chessConfig']['rows']
        columns = self.__config['chessConfig']['columns']
        vp = self.__config['chessConfig']['vp']

        if self.get_row() + l1_movement < rows:
            if self.get_column() + l2_movement < columns:
                if vp == chessboard[self.get_row() + l1_movement][self.get_column() + l2_movement]:
                    acceptable_moves.append((self.get_row() + l1_movement, self.get_column() + l2_movement))
                elif self.get_piece_name()[0:1] != chessboard[self.get_row() + l1_movement][self.get_column()
                                                                                            + l2_movement][0:1]:
                    acceptable_moves.append((self.get_row() + l1_movement, self.get_column() + l2_movement))
            l2_movement = -1
            if self.get_column() + l2_movement >= 0:
                if vp == chessboard[self.get_row() + l1_movement][self.get_column() + l2_movement]:
                    acceptable_moves.append((self.get_row() + l1_movement, self.get_column() + l2_movement))
                elif self.get_piece_name()[0:1] != chessboard[self.get_row() + l1_movement][self.get_column()
                                                                                            + l2_movement][0:1]:
                    acceptable_moves.append((self.get_row() + l1_movement, self.get_column() + l2_movement))

        l1_movement = -2
        l2_movement = 1

        if self.get_row() + l1_movement >= 0:
            if self.get_column() + l2_movement < columns:
                if vp == chessboard[self.get_row() + l1_movement][self.get_column() + l2_movement]:
                    acceptable_moves.append((self.get_row() + l1_movement, self.get_column() + l2_movement))
                elif self.get_piece_name()[0:1] != chessboard[self.get_row() + l1_movement][self.get_column()
                                                                                            + l2_movement][0:1]:
                    acceptable_moves.append((self.get_row() + l1_movement, self.get_column() + l2_movement))
            l2_movement = -1
            if self.get_column() + l2_movement >= 0:
                if vp == chessboard[self.get_row() + l1_movement][self.get_column() + l2_movement]:
                    acceptable_moves.append((self.get_row() + l1_movement, self.get_column() + l2_movement))
                elif self.get_piece_name()[0:1] != chessboard[self.get_row() + l1_movement][self.get_column()
                                                                                            + l2_movement][0:1]:
                    acceptable_moves.append((self.get_row() + l1_movement, self.get_column() + l2_movement))

        l1_movement = 2
        l2_movement = 1

        if self.get_column() + l1_movement < columns:
            if self.get_row() + l2_movement < rows:
                if vp == chessboard[self.get_row() + l2_movement][self.get_column() + l1_movement]:
                    acceptable_moves.append((self.get_row() + l2_movement, self.get_column() + l1_movement))
                elif self.get_piece_name()[0:1] != chessboard[self.get_row() + l2_movement][self.get_column()
                                                                                            + l1_movement][0:1]:
                    acceptable_moves.append((self.get_row() + l2_movement, self.get_column() + l1_movement))
            l2_movement = -1
            if self.get_row() + l2_movement >= 0:
                if vp == chessboard[self.get_row() + l2_movement][self.get_column() + l1_movement]:
                    acceptable_moves.append((self.get_row() + l2_movement, self.get_column() + l1_movement))
                elif self.get_piece_name()[0:1] != chessboard[self.get_row() + l2_movement][self.get_column()
                                                                                            + l1_movement][0:1]:
                    acceptable_moves.append((self.get_row() + l2_movement, self.get_column() + l1_movement))

        l1_movement = -2
        l2_movement = 1

        if self.get_column() + l1_movement >= 0:
            if self.get_row() + l2_movement < rows:
                if vp == chessboard[self.get_row() + l2_movement][self.get_column() + l1_movement]:
                    acceptable_moves.append((self.get_row() + l2_movement, self.get_column() + l1_movement))
                elif self.get_piece_name()[0:1] != chessboard[self.get_row() + l2_movement][self.get_column()
                                                                                            + l1_movement][0:1]:
                    acceptable_moves.append((self.get_row() + l2_movement, self.get_column() + l1_movement))
            l2_movement = -1
            if self.get_row() + l2_movement >= 0:
                if vp == chessboard[self.get_row() + l2_movement][self.get_column() + l1_movement]:
                    acceptable_moves.append((self.get_row() + l2_movement, self.get_column() + l1_movement))
                elif self.get_piece_name()[0:1] != chessboard[self.get_row() + l2_movement][self.get_column()
                                                                                            + l1_movement][0:1]:
                    acceptable_moves.append((self.get_row() + l2_movement, self.get_column() + l1_movement))

        return acceptable_moves


# Classe dedita alla gestione delle regine


class Queen(ChessPiece):

    # Costruttore
    #  @param self riferimento all'oggeto stesso
    #  @param piece_name indicazione sul pezzo in questione
    #  @param row posizione originaria sulle righe del campo di gioco del pezzo
    #  @param column posizione originaria sulle colonne del campo di gioco del pezzo

    def __init__(self, piece_name, row, column):
        super().__init__(piece_name, row, column)

        with open('Configuration.yaml', 'r') as yamlConfig:
            self.__config = yaml.load(yamlConfig, Loader=yaml.FullLoader)

    # Si occupa di definire le possibili mosse attuabili da un pezzo; è astratto viene modificato dalle classi che la
    # ereditano, in questo caso le regine. Questa funzione, dopo i controlli vari, restituirà una lista di coordinate
    # alle quali sarà accettabile muovere la pedina
    # @param chessboard matrice del campo di gioco
    # @return acceptable_moves lista di coordinate di spostamenti accettabili della pedina

    def piece_possible_moves(self, chessboard):
        row_acceptable_moves = []
        column_acceptable_moves = []
        right_diagonal_acceptable_moves = []
        left_diagonal_acceptable_moves = []
        rows = self.__config['chessConfig']['rows']
        columns = self.__config['chessConfig']['columns']
        vp = self.__config['chessConfig']['vp']

        if self.get_row() != rows - 1:
            keep = True
            movement = 1
            while keep:
                if self.get_row() + movement < rows:
                    if self.get_piece_name()[0:1] == chessboard[self.get_row() + movement][self.get_column()][0:1]:
                        keep = False
                    elif vp == chessboard[self.get_row() + movement][self.get_column()][0:1]:
                        row_acceptable_moves.append((self.get_row() + movement, self.get_column()))
                        movement += 1
                    else:
                        row_acceptable_moves.append((self.get_row() + movement, self.get_column()))
                        keep = False
                else:
                    keep = False

        if self.get_row() != 0:
            keep = True
            movement = -1
            while keep:
                if self.get_row() + movement >= 0:
                    if self.get_piece_name()[0:1] == chessboard[self.get_row() + movement][self.get_column()][0:1]:
                        keep = False
                    elif vp == chessboard[self.get_row() + movement][self.get_column()][0:1]:
                        row_acceptable_moves.append((self.get_row() + movement, self.get_column()))
                        movement -= 1
                    else:
                        row_acceptable_moves.append((self.get_row() + movement, self.get_column()))
                        keep = False
                else:
                    keep = False

        if self.get_column() != columns - 1:
            keep = True
            movement = 1
            while keep:
                if self.get_column() + movement < columns:
                    if self.get_piece_name()[0:1] == chessboard[self.get_row()][self.get_column() + movement][0:1]:
                        keep = False
                    elif vp == chessboard[self.get_row()][self.get_column() + movement][0:1]:
                        column_acceptable_moves.append((self.get_row(), self.get_column() + movement))
                        movement += 1
                    else:
                        column_acceptable_moves.append((self.get_row(), self.get_column() + movement))
                        keep = False
                else:
                    keep = False

        if self.get_column() != 0:
            keep = True
            movement = -1
            while keep:
                if self.get_column() + movement >= 0:
                    if self.get_piece_name()[0:1] == chessboard[self.get_row()][self.get_column() + movement][0:1]:
                        keep = False
                    elif vp == chessboard[self.get_row()][self.get_column() + movement][0:1]:
                        column_acceptable_moves.append((self.get_row(), self.get_column() + movement))
                        movement -= 1
                    else:
                        column_acceptable_moves.append((self.get_row(), self.get_column() + movement))
                        keep = False
                else:
                    keep = False

        if self.get_row() != rows - 1:
            if self.get_column() != columns - 1:
                keep = True
                row_movement = 1
                column_movement = 1
                while keep:
                    if self.get_row() + row_movement < rows and self.get_column() + column_movement < columns:
                        if self.get_piece_name()[0:1] == chessboard[self.get_row() + row_movement][
                                                             self.get_column() + column_movement][0:1]:
                            keep = False
                        elif vp == chessboard[self.get_row() + row_movement][self.get_column() + column_movement][0:1]:

                            right_diagonal_acceptable_moves.append((self.get_row() + row_movement, self.get_column()
                                                                    + column_movement))
                            row_movement += 1
                            column_movement += 1
                        else:
                            right_diagonal_acceptable_moves.append((self.get_row() + row_movement, self.get_column()
                                                                    + column_movement))
                            keep = False
                    else:
                        keep = False

            if self.get_column() != 0:
                keep = True
                row_movement = 1
                column_movement = -1
                while keep:
                    if self.get_row() + row_movement < rows and self.get_column() + column_movement >= 0:
                        if self.get_piece_name()[0:1] == chessboard[self.get_row() + row_movement][
                                                             self.get_column() + column_movement][0:1]:
                            keep = False
                        elif vp == chessboard[self.get_row() + row_movement][self.get_column() + column_movement][0:1]:

                            left_diagonal_acceptable_moves.append((self.get_row() + row_movement, self.get_column()
                                                                   + column_movement))
                            row_movement += 1
                            column_movement -= 1
                        else:
                            left_diagonal_acceptable_moves.append((self.get_row() + row_movement, self.get_column()
                                                                   + column_movement))
                            keep = False
                    else:
                        keep = False

        if self.get_row() != 0:
            if self.get_column() != columns - 1:
                keep = True
                row_movement = -1
                column_movement = 1
                while keep:
                    if self.get_row() + row_movement < rows and self.get_column() + column_movement < columns:
                        if self.get_piece_name()[0:1] == chessboard[self.get_row() + row_movement][
                                                             self.get_column() + column_movement][0:1]:
                            keep = False
                        elif vp == chessboard[self.get_row() + row_movement][self.get_column() + column_movement][0:1]:

                            right_diagonal_acceptable_moves.append((self.get_row() + row_movement, self.get_column()
                                                                    + column_movement))
                            row_movement -= 1
                            column_movement += 1
                        else:
                            right_diagonal_acceptable_moves.append((self.get_row() + row_movement, self.get_column()
                                                                    + column_movement))
                            keep = False
                    else:
                        keep = False

            if self.get_column() != 0:
                keep = True
                row_movement = -1
                column_movement = -1
                while keep:
                    if self.get_row() + row_movement < rows and self.get_column() + column_movement >= 0:
                        if self.get_piece_name()[0:1] == chessboard[self.get_row() + row_movement][
                                                             self.get_column() + column_movement][0:1]:
                            keep = False
                        elif vp == chessboard[self.get_row() + row_movement][self.get_column() + column_movement][0:1]:

                            left_diagonal_acceptable_moves.append((self.get_row() + row_movement, self.get_column()
                                                                   + column_movement))
                            row_movement -= 1
                            column_movement -= 1
                        else:
                            left_diagonal_acceptable_moves.append((self.get_row() + row_movement, self.get_column()
                                                                   + column_movement))
                            keep = False
                    else:
                        keep = False

        acceptable_moves = right_diagonal_acceptable_moves + left_diagonal_acceptable_moves
        acceptable_moves += row_acceptable_moves + column_acceptable_moves

        return acceptable_moves


# Classe dedita alla gestione dei re


class King(ChessPiece):

    # Costruttore
    #  @param self riferimento all'oggeto stesso
    #  @param piece_name indicazione sul pezzo in questione
    #  @param row posizione originaria sulle righe del campo di gioco del pezzo
    #  @param column posizione originaria sulle colonne del campo di gioco del pezzo

    def __init__(self, piece_name, row, column):
        super().__init__(piece_name, row, column)

        with open('Configuration.yaml', 'r') as yamlConfig:
            self.__config = yaml.load(yamlConfig, Loader=yaml.FullLoader)

    # Si occupa di definire le possibili mosse attuabili da un pezzo; è astratto viene modificato dalle classi che la
    # ereditano, in questo caso i re. Questa funzione, dopo i controlli vari, restituirà una lista di coordinate
    # alle quali sarà accettabile muovere la pedina
    # @param chessboard matrice del campo di gioco
    # @return acceptable_moves lista di coordinate di spostamenti accettabili della pedina

    def piece_possible_moves(self, chessboard):
        acceptable_moves = []
        rows = self.__config['chessConfig']['rows']
        columns = self.__config['chessConfig']['columns']
        vp = self.__config['chessConfig']['vp']

        if self.get_row() != rows - 1:
            movement = 1
            if vp == chessboard[self.get_row() + movement][self.get_column()]:
                acceptable_moves.append((self.get_row() + movement, self.get_column()))
            elif self.get_piece_name()[0:1] != chessboard[self.get_row() + movement][self.get_column()][0:1]:
                acceptable_moves.append((self.get_row() + movement, self.get_column()))
            if self.get_column() != columns - 1:
                column_movement = 1
                if vp == chessboard[self.get_row() + movement][self.get_column() + column_movement]:
                    acceptable_moves.append((self.get_row() + movement, self.get_column() + column_movement))
                elif self.get_piece_name()[0:1] != chessboard[self.get_row() + movement][self.get_column()
                                                                                         + column_movement][0:1]:
                    acceptable_moves.append((self.get_row() + movement, self.get_column() + column_movement))
            if self.get_column() != 0:
                column_movement = -1
                if vp == chessboard[self.get_row() + movement][self.get_column() + column_movement]:
                    acceptable_moves.append((self.get_row() + movement, self.get_column() + column_movement))
                elif self.get_piece_name()[0:1] != chessboard[self.get_row() + movement][self.get_column()
                                                                                         + column_movement][0:1]:
                    acceptable_moves.append((self.get_row() + movement, self.get_column() + column_movement))

        if self.get_row() != 0:
            movement = -1
            if vp == chessboard[self.get_row() + movement][self.get_column()]:
                acceptable_moves.append((self.get_row() + movement, self.get_column()))
            elif self.get_piece_name()[0:1] != chessboard[self.get_row() + movement][self.get_column()][0:1]:
                acceptable_moves.append((self.get_row() + movement, self.get_column()))
            if self.get_column() != columns - 1:
                column_movement = 1
                if vp == chessboard[self.get_row() + movement][self.get_column() + column_movement]:
                    acceptable_moves.append((self.get_row() + movement, self.get_column() + column_movement))
                elif self.get_piece_name()[0:1] != chessboard[self.get_row() + movement][self.get_column()
                                                                                         + column_movement][0:1]:
                    acceptable_moves.append((self.get_row() + movement, self.get_column() + column_movement))
            if self.get_column() != 0:
                column_movement = -1
                if vp == chessboard[self.get_row() + movement][self.get_column() + column_movement]:
                    acceptable_moves.append((self.get_row() + movement, self.get_column() + column_movement))
                elif self.get_piece_name()[0:1] != chessboard[self.get_row() + movement][self.get_column()
                                                                                         + column_movement][0:1]:
                    acceptable_moves.append((self.get_row() + movement, self.get_column() + column_movement))

        if self.get_column() != columns - 1:
            movement = 1
            if vp == chessboard[self.get_row()][self.get_column() + movement]:
                acceptable_moves.append((self.get_row(), self.get_column() + movement))
            elif self.get_piece_name()[0:1] != chessboard[self.get_row()][self.get_column() + movement][0:1]:
                acceptable_moves.append((self.get_row(), self.get_column() + movement))

        if self.get_column() != 0:
            movement = -1
            if vp == chessboard[self.get_row()][self.get_column() + movement]:
                acceptable_moves.append((self.get_row(), self.get_column() + movement))
            elif self.get_piece_name()[0:1] != chessboard[self.get_row()][self.get_column() + movement][0:1]:
                acceptable_moves.append((self.get_row(), self.get_column() + movement))

        return acceptable_moves
