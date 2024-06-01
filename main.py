import pygame
from enums import Pieces
import os

# TODO
# Castles
# Turns
# check for check
# allow only moves that stop the check

COLOR_LIGHT = (245, 245, 220)
COLOR_DARK = (148, 69, 48)
COLOR_MOVE_HIGHLIGHT = (137, 137, 137, 80)

SQUARE_SIZE = 100
TRANSPARENT = (0, 0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((8 * SQUARE_SIZE, 8 * SQUARE_SIZE))
pygame.display.set_caption("Chess")

IMAGES = [0,
          pygame.image.load(os.path.join("res", "pieces", "Chess_plt45.png")),
          pygame.image.load(os.path.join("res", "pieces", "Chess_blt45.png")),
          pygame.image.load(os.path.join("res", "pieces", "Chess_nlt45.png")),
          pygame.image.load(os.path.join("res", "pieces", "Chess_rlt45.png")),
          pygame.image.load(os.path.join("res", "pieces", "Chess_qlt45.png")),
          pygame.image.load(os.path.join("res", "pieces", "Chess_klt45.png")),

          pygame.image.load(os.path.join("res", "pieces", "Chess_pdt45.png")),
          pygame.image.load(os.path.join("res", "pieces", "Chess_bdt45.png")),
          pygame.image.load(os.path.join("res", "pieces", "Chess_ndt45.png")),
          pygame.image.load(os.path.join("res", "pieces", "Chess_rdt45.png")),
          pygame.image.load(os.path.join("res", "pieces", "Chess_qdt45.png")),
          pygame.image.load(os.path.join("res", "pieces", "Chess_kdt45.png"))]


def get_nearest_center(pos):
    rank = int(pos[0] / 100)
    row = int(pos[1] / 100)

    return [rank, row]

class Castle_Check:
    def __init__(self):
        self.can_white_castle_queenside = True
        self.can_white_castle_kingside = True
        self.can_black_castle_queenside = True
        self.can_black_castle_kingside = True

    def check_for_castle(self, board, color, side) -> bool:
        """

        :param board: the current board configuration
        :param color: the color of the king that tries to castle 1 = white, -1 = black
        :param side: the side that the king tries to castle 1 = Kingside, -1 = Queenside
        :return: is the castle operation possible
        """

        if color == 1:
            rank = 7
        else:
            rank = 0

        if side == 1:  # Kingside
            if color == 1 and not self.can_white_castle_kingside:
                return False
            elif color == -1 and not self.can_black_castle_kingside:
                return False

            if board[5][rank] == Pieces.EMPTY and board[6][rank] == Pieces.EMPTY:
                return True
            else:
                return False

        if side == -1:  # Queenside
            if color == 1 and not self.can_white_castle_queenside:
                return False
            elif color == -1 and not self.can_black_castle_queenside:
                return False

            if board[1][rank] == Pieces.EMPTY and board[2][rank] == Pieces.EMPTY and board[3][rank] == Pieces.EMPTY:
                return True
            else:
                return False

    def check_for_lost_castle_right(self, piece, orig_pos):
        if piece == Pieces.KING_WHITE:
            self.can_white_castle_kingside, self.can_white_castle_queenside = False, False
        elif piece == Pieces.ROOK_WHITE:
            if orig_pos[1] == 0:
                self.can_white_castle_queenside = False
            elif orig_pos[1] == 7:
                self.can_white_castle_kingside = False
        elif piece == Pieces.KING_BLACK:
            self.can_black_castle_kingside, self.can_black_castle_queenside = False, False
        elif piece == Pieces.ROOK_BLACK:
            if orig_pos[1] == 0:
                self.can_black_castle_queenside = False
            elif orig_pos[1] == 7:
                self.can_black_castle_kingside = False

    def get_castle_direction(self, piece, orig_pos, new_pos) -> int:
        if piece == Pieces.KING_BLACK or piece == Pieces.KING_WHITE:
            if 2 <= new_pos[0] - orig_pos[0] <= 3:  # kingside
                if new_pos[1] == 0:  # --> black castled
                    self.can_black_castle_kingside = False
                else:  # --> white castled
                    self.can_white_castle_kingside = False
                return 1
            elif 2 <= orig_pos[0] - new_pos[0] <= 4:  # queenside
                if new_pos[1] == 0:  # --> black castled
                    self.can_black_castle_queenside = False
                else:  # --> white castled
                    self.can_white_castle_queenside = False
                return -1
        return 0


class Game_Control:
    def __init__(self, board):
        self.running = True
        self.board = board

        self.active_piece = None
        self.orig_pos = None
        self.legal_moves = None

        self.double_pawn_move = None

        self.render_promotion_select = False
        self.promotion_square = None

        self.queen_select_hitbox = None
        self.rook_select_hitbox = None
        self.bishop_select_hitbox = None
        self.knight_select_hitbox = None

        self.castle_check = Castle_Check()

    def update(self):
        while self.running:
            self.handle_events()

            self.board.draw_board()
            self.draw_active_piece()

            if self.render_promotion_select:
                self.draw_promotion_select()

            pygame.display.update()

    def draw_promotion_select(self):
        if self.queen_select_hitbox.y == 0:  # at the top of the board --> white pawn promoted
            screen.blit(pygame.transform.scale(IMAGES[Pieces.QUEEN_WHITE], (50, 50)), self.queen_select_hitbox)
            screen.blit(pygame.transform.scale(IMAGES[Pieces.ROOK_WHITE], (50, 50)), self.rook_select_hitbox)
            screen.blit(pygame.transform.scale(IMAGES[Pieces.BISHOP_WHITE], (50, 50)), self.bishop_select_hitbox)
            screen.blit(pygame.transform.scale(IMAGES[Pieces.KNIGHT_WHITE], (50, 50)), self.knight_select_hitbox)
        elif self.queen_select_hitbox.y == 700:  # at the 7th rank --> black promoted
            screen.blit(pygame.transform.scale(IMAGES[Pieces.QUEEN_BLACK], (50, 50)), self.queen_select_hitbox)
            screen.blit(pygame.transform.scale(IMAGES[Pieces.ROOK_BLACK], (50, 50)), self.rook_select_hitbox)
            screen.blit(pygame.transform.scale(IMAGES[Pieces.BISHOP_BLACK], (50, 50)), self.bishop_select_hitbox)
            screen.blit(pygame.transform.scale(IMAGES[Pieces.KNIGHT_BLACK], (50, 50)), self.knight_select_hitbox)

    def draw_active_piece(self):
        if self.active_piece is not None:
            for move in self.legal_moves:  # draw move highlight markers
                if self.board.is_empty([move[0], move[1]]):
                    pygame.draw.circle(screen, COLOR_MOVE_HIGHLIGHT, (move[0] * 100 + 50, move[1] * 100 + 50), 10, 0)
                else:
                    pygame.draw.circle(screen, COLOR_MOVE_HIGHLIGHT, (move[0] * 100 + 50, move[1] * 100 + 50), 49, 3)

            pos = pygame.mouse.get_pos()
            screen.blit(IMAGES[self.active_piece], (pos[0] - 50, pos[1] - 50))

    def handle_events(self):
        ev = pygame.event.get()

        for event in ev:
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.render_promotion_select:
                    square = get_nearest_center(pygame.mouse.get_pos())
                    if not self.board.is_empty(square):
                        self.active_piece = self.board.board[square[0]][square[1]]
                        self.board.board[square[0]][square[1]] = 0
                        self.legal_moves = self.calculate_legal_moves(self.active_piece, square)
                        self.orig_pos = square

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.active_piece is not None and not self.render_promotion_select:
                    self.place_piece(get_nearest_center(pygame.mouse.get_pos()))
                elif self.render_promotion_select:
                    self.handle_promotion_select(pygame.mouse.get_pos())

    def handle_promotion_select(self, pos):
        x_pos = int(self.queen_select_hitbox.x / 100)
        y_pos = int(self.queen_select_hitbox.y / 100)

        if self.queen_select_hitbox.y == 0:  # at the top of the board --> white pawn promoted
            if self.queen_select_hitbox.collidepoint(pos):
                self.board.board[x_pos][y_pos] = Pieces.QUEEN_WHITE
                self.render_promotion_select = False
            elif self.rook_select_hitbox.collidepoint(pos):
                self.board.board[x_pos][y_pos] = Pieces.ROOK_WHITE
                self.render_promotion_select = False
            elif self.bishop_select_hitbox.collidepoint(pos):
                self.board.board[x_pos][y_pos] = Pieces.BISHOP_WHITE
                self.render_promotion_select = False
            elif self.knight_select_hitbox.collidepoint(pos):
                self.board.board[x_pos][y_pos] = Pieces.KNIGHT_WHITE
                self.render_promotion_select = False
        elif self.queen_select_hitbox.y == 700:  # at the 7th rank --> black promoted
            if self.queen_select_hitbox.collidepoint(pos):
                self.board.board[x_pos][y_pos] = Pieces.QUEEN_BLACK
                self.render_promotion_select = False
            elif self.rook_select_hitbox.collidepoint(pos):
                self.board.board[x_pos][y_pos] = Pieces.ROOK_BLACK
                self.render_promotion_select = False
            elif self.bishop_select_hitbox.collidepoint(pos):
                self.board.board[x_pos][y_pos] = Pieces.BISHOP_BLACK
                self.render_promotion_select = False
            elif self.knight_select_hitbox.collidepoint(pos):
                self.board.board[x_pos][y_pos] = Pieces.KNIGHT_BLACK
                self.render_promotion_select = False

    def place_piece(self, square):
        if square in self.legal_moves:
            self.board.board[square[0]][square[1]] = self.active_piece
            self.check_for_en_passent(self.active_piece, square)
            self.check_for_double_pawn_move(self.active_piece, square)
            self.check_for_promote(self.active_piece, square)
            self.handle_castle(square)
        else:
            self.board.board[self.orig_pos[0]][self.orig_pos[1]] = self.active_piece
        self.active_piece = None

    def handle_castle(self, square):
        self.castle_check.check_for_lost_castle_right(self.active_piece, self.orig_pos)
        castle_dir = self.castle_check.get_castle_direction(self.active_piece, self.orig_pos, square)
        if castle_dir == 1:  # Kingside
            if square[1] == 0:  # --> black castled
                self.board.board[7][0] = Pieces.EMPTY
                self.board.board[6][0] = Pieces.KING_BLACK
                self.board.board[5][0] = Pieces.ROOK_BLACK
            else:
                self.board.board[7][7] = Pieces.EMPTY
                self.board.board[6][7] = Pieces.KING_WHITE
                self.board.board[5][7] = Pieces.ROOK_WHITE

        if castle_dir == -1:  # Queenside
            if square[1] == 0:  # --> black castled
                self.board.board[0][0] = Pieces.EMPTY
                self.board.board[1][0] = Pieces.EMPTY
                self.board.board[2][0] = Pieces.KING_BLACK
                self.board.board[3][0] = Pieces.ROOK_BLACK
            else:
                self.board.board[0][7] = Pieces.EMPTY
                self.board.board[1][7] = Pieces.EMPTY
                self.board.board[2][7] = Pieces.KING_WHITE
                self.board.board[3][7] = Pieces.ROOK_WHITE

    def check_for_double_pawn_move(self, piece, square):
        if piece == Pieces.PAWN_WHITE and square[1] - self.orig_pos[1] == -2:
            self.double_pawn_move = square[0]
        elif piece == Pieces.PAWN_BLACK and square[1] - self.orig_pos[1] == 2:
            self.double_pawn_move = square[0]
        else:
            self.double_pawn_move = None

    def check_for_en_passent(self, piece, square):
        if piece == Pieces.PAWN_WHITE:
            if square[0] == self.double_pawn_move and self.board.board[square[0]][square[1] + 1] == Pieces.PAWN_BLACK:
                self.board.board[square[0]][square[1] + 1] = Pieces.EMPTY
        elif piece == Pieces.PAWN_BLACK:
            if square[0] == self.double_pawn_move and self.board.board[square[0]][square[1] - 1] == Pieces.PAWN_WHITE:
                self.board.board[square[0]][square[1] - 1] = Pieces.EMPTY

    def check_for_promote(self, piece, square):
        if (piece == Pieces.PAWN_WHITE and square[1] == 0) or (piece == Pieces.PAWN_BLACK and square[1] == 7):
            self.board.board[square[0]][square[1]] = Pieces.EMPTY

            self.queen_select_hitbox = pygame.Rect(square[0] * 100, square[1] * 100, 50, 50)
            self.rook_select_hitbox = pygame.Rect(square[0] * 100 + 50, square[1] * 100, 50, 50)
            self.bishop_select_hitbox = pygame.Rect(square[0] * 100, square[1] * 100 + 50, 50, 50)
            self.knight_select_hitbox = pygame.Rect(square[0] * 100 + 50, square[1] * 100 + 50, 50, 50)

            self.render_promotion_select = True

    def is_square_protected(self, square, color) -> bool:
        if color == 1:  # WHITE PIECE

            # check for black knight
            moves = [[square[0] - 1, square[1] - 2], [square[0] + 1, square[1] - 2], [square[0] + 2, square[1] - 1],
                     [square[0] + 2, square[1] + 1], [square[0] + 1, square[1] + 2], [square[0] - 1, square[1] + 2],
                     [square[0] - 2, square[1] - 1], [square[0] - 2, square[1] + 1]]

            # filtering moves that are outside the board
            moves = [move for move in moves if 0 <= move[0] <= 7 and 0 <= move[1] <= 7]

            for move in moves:
                if self.board.board[move[0]][move[1]] == Pieces.KNIGHT_BLACK:
                    return True

            # check for black pawns
            moves = [[square[0] - 1, square[1] - 1], [square[0] + 1, square[1] - 1]]

            # filtering moves that are outside the board
            moves = [move for move in moves if 0 <= move[0] <= 7 and 0 <= move[1] <= 7]

            for move in moves:
                if self.board.board[move[0]][move[1]] == Pieces.PAWN_BLACK:
                    return True

            # check for black King
            moves = [[square[0] - 1, square[1] - 1], [square[0], square[1] - 1], [square[0] + 1, square[1] - 1],
                     [square[0] - 1, square[1]], [square[0] + 1, square[1]],
                     [square[0] - 1, square[1] + 1], [square[0], square[1] + 1], [square[0] + 1, square[1] + 1]]

            # filtering moves that are outside the board
            moves = [move for move in moves if 0 <= move[0] <= 7 and 0 <= move[1] <= 7]

            for move in moves:
                if self.board.board[move[0]][move[1]] == Pieces.KING_BLACK:
                    return True

            # check for black bishop or queen
            pos = square.copy()
            while pos[0] < 7 and pos[1] < 7:  # bottom right
                pos[0] += 1
                pos[1] += 1
                if self.board.board[pos[0]][pos[1]] != Pieces.EMPTY:
                    if self.board.board[pos[0]][pos[1]] == Pieces.QUEEN_BLACK or \
                            self.board.board[pos[0]][pos[1]] == Pieces.BISHOP_BLACK:
                        return True
                    else:
                        break

            pos = square.copy()
            while pos[0] < 7 and pos[1] > 0:  # top right
                pos[0] += 1
                pos[1] -= 1
                if self.board.board[pos[0]][pos[1]] != Pieces.EMPTY:
                    if self.board.board[pos[0]][pos[1]] == Pieces.QUEEN_BLACK or \
                            self.board.board[pos[0]][pos[1]] == Pieces.BISHOP_BLACK:
                        return True
                    else:
                        break

            pos = square.copy()
            while pos[0] > 0 and pos[1] > 0:  # top left
                pos[0] -= 1
                pos[1] -= 1
                if self.board.board[pos[0]][pos[1]] != Pieces.EMPTY:
                    if self.board.board[pos[0]][pos[1]] == Pieces.QUEEN_BLACK or \
                            self.board.board[pos[0]][pos[1]] == Pieces.BISHOP_BLACK:
                        return True
                    else:
                        break

            pos = square.copy()
            while pos[0] > 0 and pos[1] < 7:  # bottom left
                pos[0] -= 1
                pos[1] += 1
                if self.board.board[pos[0]][pos[1]] != Pieces.EMPTY:
                    if self.board.board[pos[0]][pos[1]] == Pieces.QUEEN_BLACK or \
                            self.board.board[pos[0]][pos[1]] == Pieces.BISHOP_BLACK:
                        return True
                    else:
                        break

            # check for Black rook or queen
            pos = square.copy()
            while pos[1] < 7:  # dowm
                pos[1] += 1
                if self.board.board[pos[0]][pos[1]] != Pieces.EMPTY:
                    if self.board.board[pos[0]][pos[1]] == Pieces.QUEEN_BLACK or \
                            self.board.board[pos[0]][pos[1]] == Pieces.ROOK_BLACK:
                        return True
                    else:
                        break

            pos = square.copy()
            while pos[1] > 0:  # up
                pos[1] -= 1
                if self.board.board[pos[0]][pos[1]] != Pieces.EMPTY:
                    if self.board.board[pos[0]][pos[1]] == Pieces.QUEEN_BLACK or \
                            self.board.board[pos[0]][pos[1]] == Pieces.ROOK_BLACK:
                        return True
                    else:
                        break

            pos = square.copy()
            while pos[0] < 7:  # right
                pos[0] += 1
                if self.board.board[pos[0]][pos[1]] != Pieces.EMPTY:
                    if self.board.board[pos[0]][pos[1]] == Pieces.QUEEN_BLACK or \
                            self.board.board[pos[0]][pos[1]] == Pieces.ROOK_BLACK:
                        return True
                    else:
                        break

            pos = square.copy()
            while pos[0] > 0:  # left
                pos[0] -= 1
                if self.board.board[pos[0]][pos[1]] != Pieces.EMPTY:
                    if self.board.board[pos[0]][pos[1]] == Pieces.QUEEN_BLACK or \
                            self.board.board[pos[0]][pos[1]] == Pieces.ROOK_BLACK:
                        return True
                    else:
                        break
        elif color == -1:  # Black Piece
            # check for White knight
            moves = [[square[0] - 1, square[1] - 2], [square[0] + 1, square[1] - 2], [square[0] + 2, square[1] - 1],
                     [square[0] + 2, square[1] + 1], [square[0] + 1, square[1] + 2], [square[0] - 1, square[1] + 2],
                     [square[0] - 2, square[1] - 1], [square[0] - 2, square[1] + 1]]

            # filtering moves that are outside the board
            moves = [move for move in moves if 0 <= move[0] <= 7 and 0 <= move[1] <= 7]

            for move in moves:
                if self.board.board[move[0]][move[1]] == Pieces.KNIGHT_WHITE:
                    return True

            # check for white pawns
            moves = [[square[0] - 1, square[1] - 1], [square[0] + 1, square[1] - 1]]

            # filtering moves that are outside the board
            moves = [move for move in moves if 0 <= move[0] <= 7 and 0 <= move[1] <= 7]

            for move in moves:
                if self.board.board[move[0]][move[1]] == Pieces.PAWN_WHITE:
                    return True

            # check for white King
            moves = [[square[0] - 1, square[1] - 1], [square[0], square[1] - 1], [square[0] + 1, square[1] - 1],
                     [square[0] - 1, square[1]], [square[0] + 1, square[1]],
                     [square[0] - 1, square[1] + 1], [square[0], square[1] + 1], [square[0] + 1, square[1] + 1]]

            # filtering moves that are outside the board
            moves = [move for move in moves if 0 <= move[0] <= 7 and 0 <= move[1] <= 7]

            for move in moves:
                if self.board.board[move[0]][move[1]] == Pieces.KING_WHITE:
                    return True

            # check for white bishop or queen
            pos = square.copy()
            while pos[0] < 7 and pos[1] < 7:  # bottom right
                pos[0] += 1
                pos[1] += 1
                if self.board.board[pos[0]][pos[1]] != Pieces.EMPTY:
                    if self.board.board[pos[0]][pos[1]] == Pieces.QUEEN_WHITE or \
                            self.board.board[pos[0]][pos[1]] == Pieces.BISHOP_WHITE:
                        return True

            pos = square.copy()
            while pos[0] < 7 and pos[1] > 0:  # top right
                pos[0] += 1
                pos[1] -= 1
                if self.board.board[pos[0]][pos[1]] != Pieces.EMPTY:
                    if self.board.board[pos[0]][pos[1]] == Pieces.QUEEN_WHITE or \
                            self.board.board[pos[0]][pos[1]] == Pieces.BISHOP_WHITE:
                        return True

            pos = square.copy()
            while pos[0] > 0 and pos[1] > 0:  # top left
                pos[0] -= 1
                pos[1] -= 1
                if self.board.board[pos[0]][pos[1]] != Pieces.EMPTY:
                    if self.board.board[pos[0]][pos[1]] == Pieces.QUEEN_WHITE or \
                            self.board.board[pos[0]][pos[1]] == Pieces.BISHOP_WHITE:
                        return True

            pos = square.copy()

            while pos[0] > 0 and pos[1] < 7:  # bottom left
                pos[0] -= 1
                pos[1] += 1
                if self.board.board[pos[0]][pos[1]] != Pieces.EMPTY:
                    if self.board.board[pos[0]][pos[1]] == Pieces.QUEEN_WHITE or \
                            self.board.board[pos[0]][pos[1]] == Pieces.BISHOP_WHITE:
                        return True

            # check for White rook or queen
            pos = square.copy()
            while pos[1] < 7:  # dowm
                pos[1] += 1
                if self.board.board[pos[0]][pos[1]] != Pieces.EMPTY:
                    if self.board.board[pos[0]][pos[1]] == Pieces.QUEEN_WHITE or \
                            self.board.board[pos[0]][pos[1]] == Pieces.ROOK_WHITE:
                        return True

            pos = square.copy()
            while pos[1] > 0:  # up
                pos[1] -= 1
                if self.board.board[pos[0]][pos[1]] != Pieces.EMPTY:
                    if self.board.board[pos[0]][pos[1]] == Pieces.QUEEN_WHITE or \
                            self.board.board[pos[0]][pos[1]] == Pieces.ROOK_WHITE:
                        return True

            pos = square.copy()
            while pos[0] < 7:  # right
                pos[0] += 1
                if self.board.board[pos[0]][pos[1]] != Pieces.EMPTY:
                    if self.board.board[pos[0]][pos[1]] == Pieces.QUEEN_WHITE or \
                            self.board.board[pos[0]][pos[1]] == Pieces.ROOK_WHITE:
                        return True

            pos = square.copy()
            while pos[0] > 0:  # left
                pos[0] -= 1
                if self.board.board[pos[0]][pos[1]] != Pieces.EMPTY:
                    if self.board.board[pos[0]][pos[1]] == Pieces.QUEEN_WHITE or \
                            self.board.board[pos[0]][pos[1]] == Pieces.ROOK_WHITE:
                        return True
        return False

    def calculate_legal_moves(self, piece, square):
        if piece == Pieces.KING_WHITE or piece == Pieces.KING_BLACK:  # King
            if piece == Pieces.KING_WHITE:
                color = 1
            else:
                color = -1
            moves = [[square[0] - 1, square[1] - 1], [square[0], square[1] - 1], [square[0] + 1, square[1] - 1],
                     [square[0] - 1, square[1]], [square[0] + 1, square[1]],
                     [square[0] - 1, square[1] + 1], [square[0], square[1] + 1], [square[0] + 1, square[1] + 1]]

            # filtering moves that are outside the board
            moves = [move for move in moves if 0 <= move[0] <= 7 and 0 <= move[1] <= 7]

            # filtering not empty squares
            moves = [move for move in moves if self.board.get_color(move) != color]

            # #filtering protected squares
            moves = [move for move in moves if not self.is_square_protected(move, color)]

            if self.castle_check.check_for_castle(self.board.board, color, 1):
                moves.append([6, square[1]])
                moves.append([7, square[1]])

            if self.castle_check.check_for_castle(self.board.board, color, -1):
                moves.append([0, square[1]])
                moves.append([1, square[1]])
                moves.append([2, square[1]])

            return moves

        elif piece == Pieces.QUEEN_WHITE or piece == Pieces.QUEEN_BLACK:  # Queen
            if piece == Pieces.QUEEN_WHITE:
                color = 1
            else:
                color = -1
            moves = []

            # Rook Movement
            pos = square.copy()
            while pos[1] < 7:  # dowm
                pos[1] += 1
                if self.board.board[pos[0]][pos[1]] != Pieces.EMPTY:
                    if self.board.get_color([pos[0], pos[1]]) == color:
                        break
                    else:
                        moves.append(pos.copy())
                        break
                moves.append(pos.copy())

            pos = square.copy()
            while pos[1] > 0:  # up
                pos[1] -= 1
                if self.board.board[pos[0]][pos[1]] != Pieces.EMPTY:
                    if self.board.get_color([pos[0], pos[1]]) == color:
                        break
                    else:
                        moves.append(pos.copy())
                        break
                moves.append(pos.copy())

            pos = square.copy()
            while pos[0] < 7:  # right
                pos[0] += 1
                if self.board.board[pos[0]][pos[1]] != Pieces.EMPTY:
                    if self.board.get_color([pos[0], pos[1]]) == color:
                        break
                    else:
                        moves.append(pos.copy())
                        break
                moves.append(pos.copy())

            pos = square.copy()
            while pos[0] > 0:  # left
                pos[0] -= 1
                if self.board.board[pos[0]][pos[1]] != Pieces.EMPTY:
                    if self.board.get_color([pos[0], pos[1]]) == color:
                        break
                    else:
                        moves.append(pos.copy())
                        break
                moves.append(pos.copy())

            # bishop movement
            pos = square.copy()
            while pos[0] < 7 and pos[1] < 7:  # bottom right
                pos[0] += 1
                pos[1] += 1
                if self.board.board[pos[0]][pos[1]] != Pieces.EMPTY:
                    if self.board.get_color([pos[0], pos[1]]) == color:
                        break
                    else:
                        moves.append(pos.copy())
                        break
                moves.append(pos.copy())

            pos = square.copy()
            while pos[0] < 7 and pos[1] > 0:  # top right
                pos[0] += 1
                pos[1] -= 1
                if self.board.board[pos[0]][pos[1]] != Pieces.EMPTY:
                    if self.board.get_color([pos[0], pos[1]]) == color:
                        break
                    else:
                        moves.append(pos.copy())
                        break
                moves.append(pos.copy())

            pos = square.copy()
            while pos[0] > 0 and pos[1] > 0:  # top left
                pos[0] -= 1
                pos[1] -= 1
                if self.board.board[pos[0]][pos[1]] != Pieces.EMPTY:
                    if self.board.get_color([pos[0], pos[1]]) == color:
                        break
                    else:
                        moves.append(pos.copy())
                        break
                moves.append(pos.copy())

            pos = square.copy()

            while pos[0] > 0 and pos[1] < 7:  # bottom left
                pos[0] -= 1
                pos[1] += 1
                if self.board.board[pos[0]][pos[1]] != Pieces.EMPTY:
                    if self.board.get_color([pos[0], pos[1]]) == color:
                        break
                    else:
                        moves.append(pos.copy())
                        break
                moves.append(pos.copy())

            return moves

        elif piece == Pieces.ROOK_BLACK or piece == Pieces.ROOK_WHITE:
            if piece == Pieces.ROOK_WHITE:
                color = 1
            else:
                color = -1

            moves = []

            # Rook Movement
            pos = square.copy()
            while pos[1] < 7:  # dowm
                pos[1] += 1
                if self.board.board[pos[0]][pos[1]] != Pieces.EMPTY:
                    if self.board.get_color([pos[0], pos[1]]) == color:
                        break
                    else:
                        moves.append(pos.copy())
                        break
                moves.append(pos.copy())

            pos = square.copy()
            while pos[1] > 0:  # up
                pos[1] -= 1
                if self.board.board[pos[0]][pos[1]] != Pieces.EMPTY:
                    if self.board.get_color([pos[0], pos[1]]) == color:
                        break
                    else:
                        moves.append(pos.copy())
                        break
                moves.append(pos.copy())

            pos = square.copy()
            while pos[0] < 7:  # right
                pos[0] += 1
                if self.board.board[pos[0]][pos[1]] != Pieces.EMPTY:
                    if self.board.get_color([pos[0], pos[1]]) == color:
                        break
                    else:
                        moves.append(pos.copy())
                        break
                moves.append(pos.copy())

            pos = square.copy()
            while pos[0] > 0:  # left
                pos[0] -= 1
                if self.board.board[pos[0]][pos[1]] != Pieces.EMPTY:
                    if self.board.get_color([pos[0], pos[1]]) == color:
                        break
                    else:
                        moves.append(pos.copy())
                        break
                moves.append(pos.copy())

            return moves

        elif piece == Pieces.BISHOP_BLACK or piece == Pieces.BISHOP_WHITE:
            if piece == Pieces.BISHOP_WHITE:
                color = 1
            else:
                color = -1

            moves = []

            # bishop movement
            pos = square.copy()
            while pos[0] < 7 and pos[1] < 7:  # bottom right
                pos[0] += 1
                pos[1] += 1
                if self.board.board[pos[0]][pos[1]] != Pieces.EMPTY:
                    if self.board.get_color([pos[0], pos[1]]) == color:
                        break
                    else:
                        moves.append(pos.copy())
                        break
                moves.append(pos.copy())

            pos = square.copy()
            while pos[0] < 7 and pos[1] > 0:  # top right
                pos[0] += 1
                pos[1] -= 1
                if self.board.board[pos[0]][pos[1]] != Pieces.EMPTY:
                    if self.board.get_color([pos[0], pos[1]]) == color:
                        break
                    else:
                        moves.append(pos.copy())
                        break
                moves.append(pos.copy())

            pos = square.copy()
            while pos[0] > 0 and pos[1] > 0:  # top left
                pos[0] -= 1
                pos[1] -= 1
                if self.board.board[pos[0]][pos[1]] != Pieces.EMPTY:
                    if self.board.get_color([pos[0], pos[1]]) == color:
                        break
                    else:
                        moves.append(pos.copy())
                        break
                moves.append(pos.copy())

            pos = square.copy()

            while pos[0] > 0 and pos[1] < 7:  # bottom left
                pos[0] -= 1
                pos[1] += 1
                if self.board.board[pos[0]][pos[1]] != Pieces.EMPTY:
                    if self.board.get_color([pos[0], pos[1]]) == color:
                        break
                    else:
                        moves.append(pos.copy())
                        break
                moves.append(pos.copy())

            return moves

        elif piece == Pieces.KNIGHT_BLACK or piece == Pieces.KNIGHT_WHITE:
            if piece == Pieces.KNIGHT_WHITE:
                color = 1
            else:
                color = -1

            moves = [[square[0] - 1, square[1] - 2], [square[0] + 1, square[1] - 2], [square[0] + 2, square[1] - 1],
                     [square[0] + 2, square[1] + 1], [square[0] + 1, square[1] + 2], [square[0] - 1, square[1] + 2],
                     [square[0] - 2, square[1] - 1], [square[0] - 2, square[1] + 1]]

            # filtering moves that are outside the board
            moves = [move for move in moves if 0 <= move[0] <= 7 and 0 <= move[1] <= 7]

            # filtering not empty squares
            moves = [move for move in moves if self.board.is_empty(move) or self.board.get_color(move) != color]

            return moves

        elif piece == Pieces.PAWN_BLACK:
            moves = [[square[0], square[1] + 1]]

            if square[1] == 1 and self.board.is_empty([square[0], square[1] + 2]):  # 2 spacs from start space
                moves.append([square[0], square[1] + 2])

            if not self.board.is_empty([square[0], square[1] + 1]):
                moves = []

            if self.double_pawn_move is not None:  # En Passent
                if square[1] == 4 and (
                        square[0] + 1 == self.double_pawn_move or square[0] - 1 == self.double_pawn_move):
                    moves.append([self.double_pawn_move, square[1] + 1])

            if square[0] < 7:
                if self.board.get_color([square[0] + 1, square[1] + 1]) == 1:  # captures
                    moves.append([square[0] + 1, square[1] + 1])
            if square[0] > 0:
                if self.board.get_color([square[0] - 1, square[1] + 1]) == 1:
                    moves.append([square[0] - 1, square[1] + 1])

            return moves

        elif piece == Pieces.PAWN_WHITE:
            moves = [[square[0], square[1] - 1]]

            if square[1] == 6 and self.board.is_empty([square[0], square[1] - 2]):  # two spaces form start space
                moves.append([square[0], square[1] - 2])

            if not self.board.is_empty([square[0], square[1] - 1]):
                moves = []

            if self.double_pawn_move is not None:  # En Passent
                if square[1] == 3 and (
                        square[0] + 1 == self.double_pawn_move or square[0] - 1 == self.double_pawn_move):
                    moves.append([self.double_pawn_move, square[1] - 1])

            if square[0] < 7:
                if self.board.get_color([square[0] + 1, square[1] - 1]) == -1:  # captures
                    moves.append([square[0] + 1, square[1] - 1])
            if square[0] > 0:
                if self.board.get_color([square[0] - 1, square[1] - 1]) == -1:
                    moves.append([square[0] - 1, square[1] - 1])

            return moves


class Board:
    def __init__(self):
        # # starting position
        # self.board = [
        #     [Pieces.ROOK, Pieces.KNIGHT, Pieces.BISHOP, Pieces.QUEEN, Pieces.KING, Pieces.BISHOP, Pieces.KNIGHT,
        #      Pieces.ROOK],
        #     [Pieces.PAWN] * 8,
        #     [Pieces.EMPTY] * 8,
        #     [Pieces.EMPTY] * 8,
        #     [Pieces.EMPTY] * 8,
        #     [Pieces.EMPTY] * 8,
        #     [Pieces.PAWN] * 8,
        #     [Pieces.ROOK, Pieces.KNIGHT, Pieces.BISHOP, Pieces.QUEEN, Pieces.KING, Pieces.BISHOP, Pieces.KNIGHT,
        #      Pieces.ROOK]]

        self.board = [
            [Pieces.EMPTY] * 8,
            [Pieces.EMPTY] * 8,
            [Pieces.EMPTY] * 8,
            [Pieces.EMPTY] * 8,
            [Pieces.EMPTY] * 8,
            [Pieces.EMPTY] * 8,
            [Pieces.EMPTY] * 8,
            [Pieces.EMPTY] * 6 + [Pieces.BISHOP_WHITE, Pieces.KNIGHT_WHITE]]

    def read_fen_string(self, fen):
        x_pos = 0
        y_pos = 0

        piece = ["r", "n", "b", "q", "k", "p"]

        for c in fen:
            if c == "r":
                self.board[x_pos][y_pos] = Pieces.ROOK_BLACK
            elif c == "n":
                self.board[x_pos][y_pos] = Pieces.KNIGHT_BLACK
            elif c == 'b':
                self.board[x_pos][y_pos] = Pieces.BISHOP_BLACK
            elif c == "q":
                self.board[x_pos][y_pos] = Pieces.QUEEN_BLACK
            elif c == "k":
                self.board[x_pos][y_pos] = Pieces.KING_BLACK
            elif c == "p":
                self.board[x_pos][y_pos] = Pieces.PAWN_BLACK

            elif c == "R":
                self.board[x_pos][y_pos] = Pieces.ROOK_WHITE
            elif c == "N":
                self.board[x_pos][y_pos] = Pieces.KNIGHT_WHITE
            elif c == 'B':
                self.board[x_pos][y_pos] = Pieces.BISHOP_WHITE
            elif c == "Q":
                self.board[x_pos][y_pos] = Pieces.QUEEN_WHITE
            elif c == "K":
                self.board[x_pos][y_pos] = Pieces.KING_WHITE
            elif c == "P":
                self.board[x_pos][y_pos] = Pieces.PAWN_WHITE

            elif c.isnumeric():
                x_pos += int(c)
            elif c == "/":
                y_pos += 1
                x_pos = 0

            if c.lower() in piece:
                x_pos += 1

            if c == " ":
                break

    def is_empty(self, square):
        return self.board[square[0]][square[1]] == 0

    def get_color(self, square):
        if Pieces.PAWN_WHITE <= self.board[square[0]][square[1]] <= Pieces.KING_WHITE:
            return 1  # white
        elif Pieces.PAWN_BLACK <= self.board[square[0]][square[1]] <= Pieces.KING_BLACK:
            return -1  # black
        else:
            return 0

    def draw_board(self):
        for y in range(8):  # draw board
            for x in range(8):
                pygame.draw.rect(screen, (COLOR_LIGHT if (x + y) % 2 == 0 else COLOR_DARK),
                                 pygame.Rect(x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        for y in range(8):  # draw pieces
            for x in range(8):
                val = self.board[x][y]
                if val > 0:
                    screen.blit(IMAGES[val], (x * 100, y * 100))


if __name__ == "__main__":
    chess_board = Board()
    chess_board.read_fen_string("r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1")
    game = Game_Control(chess_board)
    game.update()
