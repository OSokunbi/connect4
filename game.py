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
    # Check horizontal
    for i in range(6):
        for j in range(4):
            if state[i][j] != "⚫" and state[i][j] == state[i][j+1] == state[i][j+2] == state[i][j+3]:
                return True

    # Check vertical
    for i in range(3):
        for j in range(7):
            if state[i][j] != "⚫" and state[i][j] == state[i+1][j] == state[i+2][j] == state[i+3][j]:
                return True

    # Check diagonal (up-right)
    for i in range(3):
        for j in range(4):
            if state[i][j] != "⚫" and state[i][j] == state[i+1][j+1] == state[i+2][j+2] == state[i+3][j+3]:
                return True

    # Check diagonal (up-left)
    for i in range(3):
        for j in range(3, 7):
            if state[i][j] != "⚫" and state[i][j] == state[i+1][j-1] == state[i+2][j-2] == state[i+3][j-3]:
                return True

    return False

def evaluate(state):
    # Evaluate the current game state for the computer
    # Assign positive scores for favorable states and negative scores for unfavorable states

    # Check for winning positions
    if checkWinner(state):
        if p2 in state[2][2]:  # If the computer wins, assign a high score
            return 1000
        elif p1 in state[2][2]:  # If the player wins, assign a low score
            return -1000

    # Evaluate based on the number of connected pieces
    computer_score = 0
    player_score = 0

    # Check horizontally
    for row in state:
        for i in range(4):
            window = row[i:i + 4]
            computer_score += window.count(p2)
            player_score += window.count(p1)

    # Check vertically
    for col in range(7):
        for i in range(3):
            window = [state[i][col], state[i + 1][col], state[i + 2][col], state[i + 3][col]]
            computer_score += window.count(p2)
            player_score += window.count(p1)

    # Check diagonally (up-right)
    for i in range(3):
        for j in range(4):
            window = [state[i][j], state[i + 1][j + 1], state[i + 2][j + 2], state[i + 3][j + 3]]
            computer_score += window.count(p2)
            player_score += window.count(p1)

    # Check diagonally (up-left)
    for i in range(3):
        for j in range(3, 7):
            window = [state[i][j], state[i + 1][j - 1], state[i + 2][j - 2], state[i + 3][j - 3]]
            computer_score += window.count(p2)
            player_score += window.count(p1)

    # Score difference
    return computer_score - player_score  

def minimax(state, depth, maximizing_player, alpha, beta):
    if depth == 0 or checkWinner(state):
        if maximizing_player:
            # Evaluate game state for computer
            return evaluate(state)  
        else:
            # Evaluate game state for player
            return -evaluate(state)  

    valid_moves = [col for col in range(7) if state[0][col] == "⚫"]
    
    if maximizing_player:
        max_eval = float("-inf")
        for col in valid_moves:
            # Simulate the move
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
            new_state = makeMove(state, col, p1)  # Simulate the move
            eval = minimax(new_state, depth - 1, True, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha-Beta pruning
        return min_eval

def makeMove(state, col, player):
    # Create a new state with the given move
    new_state = [row[:] for row in state]
    row = 0
    while row < 6 and new_state[row][col] == "⚫":
        row += 1
    new_state[row - 1][col] = player
    return new_state

def computerMove():
    valid_moves = [col for col in range(7) if grid[0][col] == "⚫"]
    if valid_moves:
        # Block winning player moves
        for col in valid_moves:
            # Check horizontally
            new_state = makeMove(grid, col, p1)
            if checkWinner(new_state):
                pickPos(col, p2)  
                return

            # Check vertically
            new_state = makeMove(grid, col, p1)
            if checkWinner(new_state):
                pickPos(col, p2) 
                return

            # Check diagonally (left to right)
            new_state = makeMove(grid, col, p1)
            if checkWinner(new_state):
                pickPos(col, p2)  
                return

            # Check diagonally (right to left)
            new_state = makeMove(grid, col, p1)
            if checkWinner(new_state):
                pickPos(col, p2) 
                return

        for col in valid_moves:
            # Simulate move
            new_state = makeMove(grid, col, p2)
            
            # Check if can win with this move
            if checkWinner(new_state):
                pickPos(col, p2)  # Make a winning move if available
                return

        # If neither player can win immediately or be blocked, pick a move based on minimax
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
        computerMove()  # Computer's turn
    else:
        player = player1
        pos = int(input("Pick a column > "))
        pickPos(pos, player)  # Human's turn

    clear()
    printBoard()

    if checkWinner(grid):
        play = False
        if turn:
            print(player2, "has won!")
        else:
            print(player1, "has won!")

    turn = not turn

