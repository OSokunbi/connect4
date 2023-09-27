import os
import time
import random

grid = [["⚫", "⚫", "⚫", "⚫", "⚫", "⚫", "⚫"],
        ["⚫", "⚫", "⚫", "⚫", "⚫", "⚫", "⚫"],
        ["⚫", "⚫", "⚫", "⚫", "⚫", "⚫", "⚫"],
        ["⚫", "⚫", "⚫", "⚫", "⚫", "⚫", "⚫"],
        ["⚫", "⚫", "⚫", "⚫", "⚫", "⚫", "⚫"],
        ["⚫", "⚫", "⚫", "⚫", "⚫", "⚫", "⚫"]]

def printBoard():
    for i in grid:
        for j in i:
            print(j, end="")
        print()

p1 = "🔵"
p2 = "🔴"

mark = ""
ply1 = True

def clear(seconds=0.05):
    time.sleep(seconds)
    os.system('clear')

def pickPos(col_picked, player):
    global ply1
    clear()
    if ply1:
        mark = p1
    else:
        mark = p2

    def empty(col_picked):
        rowNum = 5
        while rowNum >= 0:
            if grid[rowNum][col_picked] == "⚫":
                return rowNum
            rowNum -= 1

    row = empty(col_picked)
    grid[row][col_picked] = mark
    ply1 = not ply1
    printBoard()

def checkWinner(state):
    for i in range(6):
        for j in range(4):
            if state[i][j] != "⚫" and state[i][j] == state[i][j+1] == state[i][j+2] == state[i][j+3]:
                return True

    for i in range(3):
        for j in range(7):
            if state[i][j] != "⚫" and state[i][j] == state[i+1][j] == state[i+2][j] == state[i+3][j]:
                return True

    for i in range(3):
        for j in range(4):
            if state[i][j] != "⚫" and state[i][j] == state[i+1][j+1] == state[i+2][j+2] == state[i+3][j+3]:
                return True

    for i in range(3):
        for j in range(3, 7):
            if state[i][j] != "⚫" and state[i][j] == state[i+1][j-1] == state[i+2][j-2] == state[i+3][j-3]:
                return True

    return False

def evaluate(state):
    if checkWinner(state):
        if p2 in state[2][2]: 
            return 1000
        elif p1 in state[2][2]: 
            return -1000
                
    computer_score = 0
    player_score = 0

    for row in state:
        for i in range(4):
            window = row[i:i + 4]
            computer_score += window.count(p2)
            player_score += window.count(p1)

    for col in range(7):
        for i in range(3):
            window = [state[i][col], state[i + 1][col], state[i + 2][col], state[i + 3][col]]
            computer_score += window.count(p2)
            player_score += window.count(p1)

    for i in range(3):
        for j in range(4):
            window = [state[i][j], state[i + 1][j + 1], state[i + 2][j + 2], state[i + 3][j + 3]]
            computer_score += window.count(p2)
            player_score += window.count(p1)

    for i in range(3):
        for j in range(3, 7):
            window = [state[i][j], state[i + 1][j - 1], state[i + 2][j - 2], state[i + 3][j - 3]]
            computer_score += window.count(p2)
            player_score += window.count(p1)

    return computer_score - player_score  

def minimax(state, depth, maximizing_player, alpha, beta):
    if depth == 0 or checkWinner(state):
        if maximizing_player:
            return evaluate(state)  
        else:
            return -evaluate(state)  

    valid_moves = [col for col in range(7) if state[0][col] == "⚫"]
    
    if maximizing_player:
        max_eval = float("-inf")
        for col in valid_moves:
            new_state = makeMove(state, col, p2)  
            eval = minimax(new_state, depth - 1, False, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  
        return max_eval
    else:
        min_eval = float("inf")
        for col in valid_moves:
            new_state = makeMove(state, col, p1) 
            eval = minimax(new_state, depth - 1, True, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  
        return min_eval

def makeMove(state, col, player):
    new_state = [row[:] for row in state]
    row = 0
    while row < 6 and new_state[row][col] == "⚫":
        row += 1
    new_state[row - 1][col] = player
    return new_state

def computerMove():
    valid_moves = [col for col in range(7) if grid[0][col] == "⚫"]
    if valid_moves:
        for col in valid_moves:
            new_state = makeMove(grid, col, p1)
            if checkWinner(new_state):
                pickPos(col, p2)  
                return

            new_state = makeMove(grid, col, p1)
            if checkWinner(new_state):
                pickPos(col, p2) 
                return

            new_state = makeMove(grid, col, p1)
            if checkWinner(new_state):
                pickPos(col, p2)  
                return

            new_state = makeMove(grid, col, p1)
            if checkWinner(new_state):
                pickPos(col, p2) 
                return

        for col in valid_moves:
            new_state = makeMove(grid, col, p2)
            
            if checkWinner(new_state):
                pickPos(col, p2) 
                return

        best_move = None
        best_score = float("-inf")
        for col in valid_moves:
            new_state = makeMove(grid, col, p2)
            score = minimax(new_state, 4, False, float("-inf"), float("inf"))
            if score > best_score:
                best_score = score
                best_move = col
        pickPos(best_move, p2)



play = True

player1 = input("Enter Player 1 Name > ")
player2 = "Computer"

clear()

turn = False
player = player1

printBoard()

while play:
    if turn:
        player = player2
        computerMove() 
    else:
        player = player1
        pos = int(input("Pick a column > "))
        pickPos(pos, player)  

    clear()
    printBoard()

    if checkWinner(grid):
        play = False
        if turn:
            print(player2, "has won!")
        else:
            print(player1, "has won!")

    turn = not turn

