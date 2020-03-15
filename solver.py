board = [
    [0,0,0,0,3,0,6,0,0],
    [6,0,2,8,0,0,0,5,1],
    [0,1,5,7,0,0,0,0,0],
    [0,0,0,0,0,5,7,2,0],
    [8,0,0,0,2,6,0,0,3],
    [4,0,3,0,0,0,0,0,9],
    [0,4,0,0,0,9,0,0,0],
    [0,0,0,0,7,0,9,4,0],
    [0,9,0,0,1,0,2,8,7]
]

# board = [
#     [7,8,0,4,0,0,1,2,0],
#     [6,0,0,0,7,5,0,0,9],
#     [0,0,0,6,0,1,0,7,8],
#     [0,0,7,0,4,0,2,6,0],
#     [0,0,1,0,5,0,9,3,0],
#     [9,0,4,0,6,0,0,0,5],
#     [0,7,0,3,0,0,0,1,2],
#     [1,2,0,0,0,7,4,0,0],
#     [0,4,9,2,0,6,0,0,7]
# ]

def disp_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("----------------------")
        for j in range(len(board[0])):
            if j%3 == 0 and j != 0:
                print("|",end=' ')
            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]),end=' ')

def check_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i,j) #row,col

    return None

def plausible(board,num,pos):
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False
        
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    x_coord = pos[1]//3
    y_coord = pos[0]//3

    for i in range(y_coord*3,y_coord*3 + 3):
        for j in range(x_coord*3,x_coord*3 + 3):
            if board[i][j] == num and (i,j) == pos:
                return False
    
    return True

def solve(board):
    pos = check_empty(board)

    if not pos:
        return True
    else:
        row,col = pos
    for i in range(1,10):
        if plausible(board,i,(row,col)):
            board[row][col] = i

            if solve(board):
                return True
            
            board[row][col] = 0

    return False

disp_board(board)
solve(board)
print("_______________________")
disp_board(board)