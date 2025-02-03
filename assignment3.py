import sys

def make_list(input_file):
    #create a list from the input file
    board = []
    for line in input_file:
        line = line.split()
        board.append(line)

    return board


def find_neighbors(board, i, j):
    #finds all neighboring cells with the same value in the board
    value = board[i][j]
    neighbors = []

    def check(board, r, c, value):
        bool = True
        value_check = 0
        while bool == True:
            bool = False
            for a in neighbors:

                r, c = a[0], a[1]

                num = 0
                if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == value:
                    #check all four directions
                    if 0 <= r - 1 < len(board) and ((r - 1, c) not in neighbors and board[r - 1][c] == value):
                        neighbors.append((r - 1, c))  # up
                        num += 1
                        value_check += 1
                        bool = True
                    if 0 <= r + 1 < len(board) and ((r + 1, c) not in neighbors and board[r + 1][c] == value):
                        neighbors.append((r + 1, c))  #down
                        num += 1
                        value_check += 1
                        bool = True
                    if 0 <= c - 1 < len(board[0]) and ((r, c - 1) not in neighbors and board[r][c - 1] == value):
                        neighbors.append((r, c - 1))  #left
                        num += 1
                        value_check += 1
                        bool = True
                    if 0 <= c + 1 < len(board[0]) and ((r, c + 1) not in neighbors and board[r][c + 1] == value):
                        neighbors.append((r, c + 1))  #right
                        num += 1
                        value_check += 1
                        bool = True
                    if value_check > 0:
                        board[r][c] = " "  #mark the cell as processed
        if value_check == 0:
            value = 0
        return (neighbors, board, value)

    neighbors.append((i, j))
    neighbors, board, value = check(board, i, j, value)
    return [neighbors, value]


def str_board(board):
    #prints the table in the appropriate format
    for row in board:
        row_str = ' '.join(map(str, row))
        print(row_str)
    print()


def deleting_empty_cells(board):
    #delete all empty cells and rows/columns from the board
    while True:
        bool = False
        for i in range(len(board) - 1):
            for j in range(len(board[0])):
                if board[i][j] != " " and board[i + 1][j] == " ":
                    board[i + 1][j], board[i][j] = board[i][j], board[i + 1][j]
                    bool = True

        if not bool:
            break

    #delete empty rows
    empty_row_list = []
    for row in board:
        if all(value == " " for value in row):
            empty_row_list.append(row)

    if len(empty_row_list) != 0:
        new_board = []
        for row in board:
            if row not in empty_row_list:
                new_board.append(row)
        board = new_board

    # delete empty cols
    rotated_board = list(zip(*board))

    empty_col_list = []
    for col in rotated_board:
        if all(value == " " for value in col):
            empty_col_list.append(col)

    if len(empty_col_list) != 0:
        new_rotated_board = []
        for col in rotated_board:
            if col not in empty_col_list:
                new_rotated_board.append(col)
        rotated_board = new_rotated_board

        board = [list(col) for col in zip(*rotated_board)]

    return board


def last_control(board, i, j):
    #check if the game is over by verifying if any moves are left
    def chec(board, r, c):
        value = board[r][c]
        return ((
                        (r <= len(board) - 1 and board[r + 1][c] == value) or

                        (c <= len(board[0]) - 1 and board[r][c + 1] == value)) and board[r][c] != ' ')

    game_over = True  #assume game over by default

    for i in range(len(board) - 1):
        for j in range(len(board[0]) - 1):
            if chec(board, i, j):
                game_over = False  #if any cell has a same-value neighbor, continue the game
                break  #exit the inner loop

        if not game_over:
            break  #exit the outer loop if game is not over

    return game_over


def main(input_file):
    #main function to run the game
    boolen = True
    board = make_list(input_file)
    str_board(board)
    score = 0
    print("Your score is: {}\n".format(score))

    def game(board, score):
        x, y = map(int, input("Please enter a row and a column number: ").split())
        print()
        x, y = x - 1, y - 1
        if x > len(board) - 1 or y > len(board[0]) - 1 or x < 0 or y < 0:
            print("Please enter a correct size!\n")
            game(board, score)
            return (True, board, score)

        neighbors, value = find_neighbors(board, x, y)
        if value == 0:
            print("No movement happened try again\n")
            str_board(board)
            print("Your score is: {}\n".format(score))
            return (True, board, score)
        if value != 0:
            board = deleting_empty_cells(board)
            score += int(value) * len(neighbors)
            str_board(board)
            print("Your score is: {}\n".format(score))
            if last_control(board, x, y):
                print("Game over")
                return (False, board, score)
            else:
                return (True, board, score)

    while boolen != False:
        boolen, board, score = game(board, score)  #keep playing until the game is over



input_file = open("input.txt", "r")
main(input_file)
input_file.close()
