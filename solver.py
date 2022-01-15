def findempty(board):
    # range of each row
    for i in range(len(board)):
        # range of each column
        for j in range(len(board[0])):
            if board[i][j] == 0:
                # return row and column
                return (i, j)
    return None
def valid(board, num, pos):
    # Check row
    for i in range(len(board[0])):
        # Check if each element in row is equal to the number that has just been inserted
        # if position trying to be checked is the position we just inserted a number in, ignore
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    # Check cube
    # assign box_x to column selected in that cube
    box_x = pos[1] // 3
    # assign box_y to row selected in that cube
    box_y = pos[0] // 3

    # assign the index of the cube selected, using *3 because we used //3 for assigning
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i,j) != pos:
                return False
    return True

def solve(board):
    # assign find to an empty position
    find = findempty(board)
    # if find does not find value return True
    if not find:
        return True
    # if find does find value, assign the values to row and col
    else:
        row, col = find
    # range 1 - 9
    for i in range(1,10):
        # if board is valid
        if valid(board, i, (row, col)):
            # assign i to position
            board[row][col] = i
            # recursively find solution, keep trying until True or 1-9 has been tried and return False
            if solve(board):
                return True
            board[row][col] = 0
    return False