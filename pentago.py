'''
THIS IS THE TERMINAL VERSION OF THE GAME

RULES OF PENTAGO:
    - THE PLAYER HAS TO PLACE THE PIECE / MARBLE IN A SOCKET
    - THE PLAYER THEN HAS TO ROTATE ONE OF THE QUADRANTS BY 90 DEGREES
    - FIRST TO GET 5 PIECE / MARBLE IN A ROW WINS
'''

ROWS, COLS = 6, 6
WIN_LENGTH = 5  # no. of piece in a row to win

class Game:
    def __init__(self):
        self.board = [[0 for _ in range(ROWS)] for _ in range(COLS)]
        self.player = 1  # player 1 / 2

    def get_player(self) -> int:
        return self.player
    
    def update_player(self):
        ''' update player turn to next player '''
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

    def is_empty_slot(self, row:int, col:int) -> bool:
        ''' check if socket is empty '''
        if self.board[row][col] == 0:
            return True
        return False
    
    def is_valid_slot(self, row:int, col:int) -> bool:
        ''' check if given row & col is valid '''
        if 0 <= row <= ROWS and 0 <= col <= COLS:
            return True
        return False
    
    def insert_piece(self, row:int, col:int):
        self.board[row][col] = self.player

    def print_board(self):
        ''' print board on terminal '''
        top_row = ' ' * 2
        for i in range(COLS):
            if i == COLS // 2:
                top_row += ' ' * 2
            top_row += str(i) + ' '
        print(top_row)

        piece = ['.', 'O', 'X']
        for row in range(ROWS):
            if row == ROWS // 2:
                print(' ' * 2 + '-' * 13)

            row_str = str(row) + ' '
            for col in range(COLS):
                if col == COLS // 2:
                    row_str += '| '
                row_str += piece[self.board[row][col]] + ' '

            print(row_str)

    def rotate_board(self, quadrant:int, clockwise:bool):
        ''' 
        rotate quadrant either cw or acw, quadrants of board:
        1 | 2
        -----
        3 | 4
        '''
        row_start = 0   
        col_start = 0

        # find first row & col of quadrant
        if quadrant in [1, 2]:
            row_start = 0
        else:
            row_start = ROWS // 2

        if quadrant in [1, 3]:
            col_start = 0
        else:
            col_start = COLS // 2

        # save quadrant into arr and rotate arr
        quadrant = [[0 for _ in range(COLS//2)] for _ in range(ROWS//2)]
        for i in range(ROWS//2):
            for j in range(COLS//2):
                row = row_start + i
                col = col_start + j
                quadrant[i][j] = self.board[row][col]

        # rotate quadrant clockwise
        if clockwise:
            quadrant = list(zip(*quadrant[::-1]))

        # rotate quadrant anti-clockwise
        else:
            quadrant = list(zip(*quadrant))[::-1]

        # update board with new quadrant
        for i in range(ROWS//2):
            for j in range(COLS//2):
                row = row_start + i
                col = col_start + j
                self.board[row][col] = quadrant[i][j]
    
    def check_win(self) -> bool:
        ''' 
        check if current player has won 
        1) 5 in a row
        2) 5 in a column
        3) 5 in a diagonal
        '''
        if self.check_row() or self.check_col() or self.check_diag():
            return True
        return False
        
    def check_row(self) -> bool:
        ''' check for 5 piece in a row '''
        for row in range(ROWS):
            for col in range(COLS - WIN_LENGTH + 1):
                flag = True
                for k in range(WIN_LENGTH):
                    if self.board[row][col+k] != self.player:
                        flag = False
                        break
                if flag:
                    return True
        return False

    def check_col(self) -> bool:
        ''' check for 5 piece in a col '''
        for col in range(COLS):
            for row in range(ROWS - WIN_LENGTH + 1):
                flag = True
                for k in range(WIN_LENGTH):
                    if self.board[row+k][col] != self.player:
                        flag = False
                        break
                if flag:
                    return True
        return False

    def check_diag(self) -> bool:
        ''' check for 5 piece in a diagonal '''
        for i in range(ROWS - WIN_LENGTH + 1):
            flag1, flag2 = True, True
            for k in range(WIN_LENGTH):
                # check downwards diagonal
                if self.board[i+k][i+k] != self.player:
                    flag1 = False
                
                # check upwards diagonal
                if self.board[i+k][ROWS-1-i-k] != self.player:
                    flag2 = False

            if flag1 or flag2:
                return True
        return False

    def check_draw(self) -> bool:
        ''' check if game is in a state of draw - all socket filled and no winner '''
        # check for winner
        if self.check_win() == True:
            return False
        
        # check if all sockets filled
        for row in self.board:
            for ele in row:
                if ele == 0:   # empty socket found
                    return False
                
        return True


def main():
    print('-' * 50)
    print('WELCOME TO PENTAGO')
    print('-' * 50)
    print('RULES:')
    print('- THE PLAYER HAS TO PLACE THE PIECE / MARBLE IN A SOCKET')
    print('- THE PLAYER THEN HAS TO ROTATE ONE OF THE QUADRANTS BY 90 DEGREES')
    print('- FIRST TO GET 5 PIECE / MARBLE IN A ROW WINS')
    print('-' * 50)
    print()

    game = Game()
    game.print_board()

    while True:
        player_turn = game.get_player()
        print(f'Player {player_turn} turn')

        # get user input
        while True:
            row = int(input('Enter row: '))
            col = int(input('Enter col: '))
            if game.is_valid_slot(row, col):
                if game.is_empty_slot(row, col):
                    break
                else:
                    print("Slot is occupied, choose another slot")
            else:
                print('Invalid input, try again')

        # insert piece and check if player has won
        game.insert_piece(row, col)
        game.print_board()
        if game.check_win() == True:
            print(f'Player {player_turn} wins !!!')
            break

        # get quadrant number
        print('Quadrants:')
        print(' 1 | 2 ')
        print('-------')
        print(' 3 | 4 ')
        while True:
            quadrant = int(input('Enter quadrant to rotate: '))
            if 1 <= quadrant <= 4:
                break
            else:
                print('Invalid input, try again')

        # get direction of rotation
        print('Direction')
        print('0 - anticlockwise')
        print('1 - clockwise')
        while True:
            direction = int(input('Enter direction of rotation: '))
            if 0 <= direction <= 1:
                if direction == 0:
                    direction = False
                else:
                    direction = True
                break
            else:
                print('Invalid input')

        # rotate quadrant and check if player has won
        game.rotate_board(quadrant, direction)
        game.print_board()
        if game.check_win() == True:
            print(f'Player {player_turn} wins !!!')
            break

        # check for draw
        if game.check_draw():
            print('Both players draw')
            break

        # update turn
        game.update_player()


if __name__ == '__main__':
    main()