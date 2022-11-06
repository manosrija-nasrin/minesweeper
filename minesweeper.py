import random
import re

# Creating a board object to represent the minesweeper board
# This is so that when we code up the game, we can just say "create a new board object"
# and dig on that board, or "render this game for this object"


class Board:
    def __init__(self, dim_size, num_bombs):
        # keep track of these parameters because we might find them helpful later on
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # get the board
        self.board = self.make_new_board()
        self.assign_values_to_board()

        # initialize a set to keep track of which locations we've uncovered
        # we will put (row,col) tuples into these sets
        self.dug = set()

    def make_new_board(self):
        # construct a new board based on the dim size and num bombs
        # we should construct the list of lists here (or whatever representation you prefer,
        # but since we have a 2-D board, list of lists is most natural)

        # generate a new board
        board = [[None for _ in range(self.dim_size)]
                 for _ in range(self.dim_size)]
        # this creates an array like this:
        # [[None, None, ..., None],
        #  [None, None, ..., None],
        #  [...                  ],
        #  [None, None, ..., None]]
        # we can see how this represents a board!

        # plant the bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            bomb_position = random.randint(0, self.dim_size**2 - 1)
            row = bomb_position // self.dim_size
            col = bomb_position % self.dim_size
            if board[row][col] == '*':
                # we have already planted a bomb here, keep going
                continue

            board[row][col] = '*'   # plant the bomb
            bombs_planted += 1

        return board

    def assign_values_to_board(self):
        # now that we have the bombs planted, let's assign a number 0-8 for all the empty spaces, which
        # represents how many neighboring bombs there are. we can precompute these and it'll save us some
        # effort checking what's around the board later on :)
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):
        # let's iterate through each of the neighboring positions and sum number of bombs
        # top left: (row-1, col-1)
        # top middle: (row-1, col)
        # top right: (row-1, col+1)
        # left: (row, col-1)
        # right: (row, col+1)
        # bottom left: (row+1, col-1)
        # bottom middle: (row+1, col)
        # bottom right: (row+1, col+1)

        # ps we need to make sure we don't go out of bounds!!

        num_nbr_bombs = 0
        for r in range(max(0, row - 1), min(row + 1, self.dim_size - 1) + 1):
            for c in range(max(0, col - 1), min(col + 1, self.dim_size - 1) + 1):
                if r == row and c == col:   # current position, do nothing
                    continue
                if self.board[r][c] == '*':
                    num_nbr_bombs += 1
        return num_nbr_bombs

    def dig(self, row, col):
        # dig at that location!
        # return True if successful dig, False if bomb dug

        # a couple of scenarios to consider:
        # hit a bomb -> game over
        # dig at a location with neighboring bombs -> finish dig
        # dig at a location with no neighboring bombs -> recursively dig neighbors!

        self.dug.add((row, col))  # cell dug

        # base case: hit a bomb and return False
        # or dig at a location with nbr_bombs and return True
        if self.board[row][col] == '*':     # uh oh, a bomb :(
            return False
        # a non-zero number of neighbouring bombs
        elif self.board[row][col] > 0:
            return True

        # self.board[row][col] == 0
        # recursively dig around the cell
        for r in range(max(0, row - 1), min(row + 1, self.dim_size - 1) + 1):
            for c in range(max(0, col - 1), min(col + 1, self.dim_size - 1) + 1):
                if (r, c) in self.dug:
                    continue  # don't dig where you've already dug
                self.dig(r, c)

        # if our initial dig in the loop didn't hit a bomb, we shouldn't hit a bomb here
        return True     # dig successful

    def __str__(self):
        # return a string that shows the board to the player
        # note: this part is kinda hard to get the formatting right, you don't have to do it the same way
        # i did
        # you can also just copy and paste from the implementation
        # this part is not that important to understanding the logic of the code :)

        # first let's create a new array that represents what the user would see
        visible_board = [[None for _ in range(
            self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '

        # put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key=len)
                )
            )

        # print the csv strings

        # row header
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        # rows of visible_board
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                # string formatting using % - alignment
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            # stringing the column entries together
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)

        # concatenating everything
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep


def play(dim_size=10, num_bombs=10):
    # Step 1: create the board and plant the bombs
    board = Board(dim_size, num_bombs)
    # Step 2: show the user the board and ask for where they want to dig
    # Step 3a: if the location is a bomb, then show game over message
    # Step 3b: if the location is not a bomb, dig recursively until one of the squares is next to a bomb
    # Step 4: repeat steps 2 and 3a/b until there are no more places to dig, then show victory
    while len(board.dug) < board.dim_size**2 - num_bombs:
        print(board)    # display board
        # 0,0 or 0, 0 or 0,        0
        user_input = re.split(
            ',(\\s)*', input("Where would you like to dig? Input as row,col: "))    # 0,3
        row, col = int(user_input[0]), int(user_input[-1])
        if row not in range(0, board.dim_size) or col not in range(0, board.dim_size):
            print("Invalid location. Try again.")
            continue

        elif (row, col) in board.dug:
            # already dug
            print("You have already dug this cell. Try another.")
            continue

        # if it's valid, we dig
        safe = board.dig(row, col)
        if not safe:
            # dug a bomb ahhhhhhhh
            break  # (game over rip)

    if safe:
       # all cells dug successfully
        print("CONGRATS! YOU WON!!")
    else:
        # bomb dug :(
        print("SORRY. GAME OVER. :(")
    # reveal the whole board
    board.dug = [(r, c) for r in range(board.dim_size)
                 for c in range(board.dim_size)]
    print(board)


if __name__ == '__main__':  # good practice :)
    play()
