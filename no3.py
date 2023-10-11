import math
import copy 
## Problem: Tic-Tac-Toe game
# 'x' = 1 
# 'o' = -1
# empty = 0
# state: [[0,0,1],[0,-1,0],[0,0,0]]
# 'x' starts first
# The one who makes a row, a column, 
# or a diagonal of the same type wins

class TicTacToe:
    # initialize game with some state
    def __init__(self, state=[[0, 0, 0], [0, 0, 0], [0, 0, 0]]):
        self.state = state

    # make a real move: set val to the cell
    # with coordinates [row, col]
    def make_move(self, row, col, val):
        #if statement to check if a cell at the specific row and col is empty
        #if it is empty, then the move can be made by filling the cell with the val
        if self.state[row][col] == 0:
            self.state[row][col] = val
            #True = move made, False = invalid move, move not made
            return True
        return False

    # check if the terminal node   
    def terminal_node(self):
        # result of the game
        # win1 = +10, win2 = -10, tie=0
        result = 0
        isGameOver = False

        # check if there is an empty cell
        emptyCells = False
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    emptyCells = True

        # check rows if there is a winner
        isWinner = False
        for i in range(3):
            sum_p1 = 0
            sum_p2 = 0
            for j in range(3):
                if self.state[i][j] == 1:
                    sum_p1 += 1
                if self.state[i][j] == -1:
                    sum_p2 += -1
            if (sum_p1 == 3) or (sum_p2 == -3):
                isWinner = True
                if (sum_p1 == 3):
                    result = 10
                if (sum_p2 == -3):
                    result = -10

        # check cols if there is a winner
        for j in range(3):
            sum_p1 = 0
            sum_p2 = 0
            for i in range(3):
                if self.state[i][j] == 1:
                    sum_p1 += 1
                if self.state[i][j] == -1:
                    sum_p2 += -1
            if (sum_p1 == 3) or (sum_p2 == -3):
                isWinner = True
                if (sum_p1 == 3):
                    result = 10
                if (sum_p2 == -3):
                    result = -10

        # check diagonals if there is a winner
        sum_p1 = 0
        sum_p2 = 0
        for i in range(3):
            if self.state[i][i] == 1:
                sum_p1 += 1
            if self.state[i][i] == -1:
                sum_p2 += -1
        if (sum_p1 == 3) or (sum_p2 == -3):
            isWinner = True
            if (sum_p1 == 3):
                result = 10
            if (sum_p2 == -3):
                result = -10

        sum_p1 = 0
        sum_p2 = 0
        for i in range(3):
            if self.state[i][2 - i] == 1:
                sum_p1 += 1
            if self.state[i][2 - i] == -1:
                sum_p2 += -1
        if (sum_p1 == 3) or (sum_p2 == -3):
            isWinner = True
            if (sum_p1 == 3):
                result = 10
            if (sum_p2 == -3):
                result = -10

        isGameOver = isWinner or not emptyCells
        return {"gameover": isGameOver, "result": result}
    
    # find the children of the given state
    # returns the coordinates (x,y) of empty cells  
    def expand_state(self):
        children = []
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    child = [i, j]
                    children.append(child)
        return children

    #function for the computer's moves
    def computer(self):
        bestMove = None
        bestScore = -math.inf
        #traverse through each row and column (every cell)
        for i in range(3):
            for j in range(3):
                #if the cell is empty (val == 0)
                if self.state[i][j] == 0:
                    #-1 is the computer move value
                    self.state[i][j] = -1
                    #the computer thinks of a move (not making a move yet) and evaluate the score
                    #depth = 0, alpha = -inf, beta = inf, isMaxPlayer = False
                    currentScore = self.alphabeta(0, -math.inf, math.inf, False)
                    self.state[i][j] = 0
                    #if the current thought of move score is better than the bestScore so far,
                    #make the current score the best score, and the position of the move the best move
                    if currentScore > bestScore:
                        bestScore = currentScore
                        bestMove = [i, j]
        #once the best possible move is found (True)
        if bestMove:
            #the computer makes its move
            self.state[bestMove[0]][bestMove[1]] = -1

    #function for the alpha-beta algorithm inspired by sir zhandos' function, but modified to suit the code better
    def alphabeta(self, depth, alpha, beta, isMaxPlayer):
        #instead of count_terminal, the terminal_node() returns the current state of the game in the variable
        terminal = self.terminal_node()
        #if the terminal is game over it checks who wins
        if terminal["gameover"]:
            #user wins so return 1
            if terminal["result"] == 1:
                return 1
            #computer wins so return -1
            elif terminal["result"] == -1:
                return -1
            #no one wins (tie) so return 0
            else:
                return 0

        if isMaxPlayer:# player maximizes his score
            v_max = -math.inf
            #traverse through each row and column (every cell)
            for i in range(3):
                for j in range(3):
                    #if cell is empty, it thinks of a move, tracks the max score (v_max) and alpha
                    if self.state[i][j] == 0:
                        #possible player move 
                        self.state[i][j] = 1
                        #recursively call alphabeta
                        v = self.alphabeta(depth + 1, alpha, beta, False)
                        self.state[i][j] = 0
                        #get vmax and alpha
                        v_max = max(v_max, v)
                        alpha = max(alpha, v)
                        #once beta becomes <= alpha, break from the loop bcs alphabeta is done
                        if beta <= alpha:
                            break
            return v_max
        
        else:# player minimizes his score
            v_min = math.inf
            #traverse through each row and column (every cell)
            for i in range(3):
                for j in range(3):
                    #if cell is empty, it thinks of a move that the computer can make, tracks the vmin and beta
                    if self.state[i][j] == 0:
                        #possible computer move
                        self.state[i][j] = -1
                        #recursively call alphabeta
                        v = self.alphabeta(depth + 1, alpha, beta, True)
                        self.state[i][j] = 0
                        #get vmin and beta
                        v_min = min(v_min, v)
                        beta = min(beta, v)
                        #once beta becomes <= alpha, break from the loop bcs alphabeta is done
                        if beta <= alpha:
                            break
            return v_min

    #function to make a game grid or a 3x3 table for the tictactoe
    def grid(self):
        #traverse through each row and column (every cell)
        for i in range(3):
            for j in range(3):
                #if empty cell value, just leave it blank
                if self.state[i][j] == 0:
                    print(" ", end=' ')
                #if its a cell with a player's move value, print X as player symbol
                elif self.state[i][j] == 1:
                    print("X", end=' ')
                #if its a cell with a computers's move value, print O as computer symbol
                else:
                    print("O", end=' ')
                #if the column position is <2 char spaces, print a column divider
                if j < 2:
                    print("|", end=' ')
            print()
            #if the row position is <2 lines, print a row divider
            if i < 2:
                print("---------")

#main function to run the program
def main():    
    game = TicTacToe()
    playerTurn = True
    print("=========== Tic Tac Toe vs Computer! ===========")
    game.grid()

    #while the game is not over 
    while not game.terminal_node()["gameover"]:
        if playerTurn:
            #row and col both -1 bcs i use 1-3 values instead of 0-2 for user input moves
            row = int(input("Input row (1/2/3):")) - 1
            col = int(input("Input column (1/2/3):")) - 1
            if game.make_move(row, col, 1):
                playerTurn = not playerTurn
        else:
            print("Its the computer's turn to make a move!")
            game.computer()
            playerTurn = not playerTurn
        print("Current Positions:")
        game.grid()

    #if the game is over and we get the result value
    #10 = player wins
    #-10 = computer wins
    #else, because there would be no more empty cells and no winner, its a tie
    if game.terminal_node()["result"] == 10:
        print("You won the game! Great job!")
        print("Final Positions:")
        game.grid()
        print("=================================")
    elif game.terminal_node()["result"] == -10:
        print("Game Over! The computer won >:)")
        print("=================================")
    else:
        print("You tied with the computer!")
        print("=================================")

main()


