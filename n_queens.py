import random


#make a random n-queens board
#index=column value=row
def make_random_board(n):
    board = []
    for col in range(n):
        row_choice = random.randint(0, n - 1)
        board.append(row_choice)
    return board


#count attacking queen pairs
#we want this number as low as possible
def get_conflicts(board):
    n = len(board)
    conflict_total = 0

    #compare each pair one time
    for c1 in range(n):
        r1 = board[c1]
        for c2 in range(c1 + 1, n):
            r2 = board[c2]

            #same row
            if r1 == r2:
                conflict_total += 1

            #same diagonal
            if abs(r1 - r2) == abs(c1 - c2):
                conflict_total += 1

    return conflict_total


#generate neighbors by moving one queen in one column
#this returns a list of nieghbor boards
def get_all_neighbors(board):
    n = len(board)
    neighbors = []

    #try changing each column
    for col in range(n):
        original_row = board[col]

        #try every row except the current one
        for new_row in range(n):
            if new_row == original_row:
                continue

            temp_board = board.copy()
            temp_board[col] = new_row
            neighbors.append(temp_board)

    return neighbors


#pick a random neighbor quickly
#useful later for stochastc ideas
def get_random_neighbor(board):
    n = len(board)

    col = random.randint(0, n - 1)
    original_row = board[col]

    #pick a new row that is different
    new_row = random.randint(0, n - 1)
    while new_row == original_row:
        new_row = random.randint(0, n - 1)

    temp_board = board.copy()
    temp_board[col] = new_row

    return temp_board