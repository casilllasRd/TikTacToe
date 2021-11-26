import random 

# Player Inputs 
def turnInput(board):
    move = input('\nPick a number on the board: ')
    try: 
        move = int(move)
        if move in board:
            return move
        else: 
            print('\nThat move is not available.')
    except ValueError:
        print('\nNot a valid input. ')
    return turnInput(board)

def promptPlayer(prompt, yes, no):
    question = input(prompt)
    if question == yes:
        return True
    elif question == no:
        return False
    else:
        print('Not a valid input.')
        return promptPlayer(prompt, yes, no)

# final state checks
def rowWin(board):
    row1 = [board[i] for i in range(0, 3)]
    row2 = [board[i] for i in range(3, 6)]
    row3 = [board[i] for i in range(6, 9)]

    check1 = len(set(row1)) == 1
    check2 = len(set(row2)) == 1
    check3 = len(set(row3)) == 1

    if check1 or check2 or check3:
        return True
    else: 
        return False

def columnWin(board):
    column1 = [board[i] for i in range(0, 7, 3)]
    column2 = [board[i] for i in range(1, 8, 3)]
    column3 = [board[i] for i in range(2, 9, 3)]

    check1 = len(set(column1)) == 1
    check2 = len(set(column2)) == 1
    check3 = len(set(column3)) == 1

    if check1 or check2 or check3:
        return True
    else: 
        return False

def diagWin(board):
    diag1 = [board[i] for i in range(0, 9, 4)]
    diag2 = [board[i] for i in range(2, 7, 2)]

    check1 = len(set(diag1)) == 1
    check2 = len(set(diag2)) == 1

    if check1 or check2:
        return True
    else:
        return False

def playerWin(board):
    if rowWin(board) or columnWin(board) or diagWin(board):
        return True
    else:
        return False

def catscratch(board):
    check = len(set(board)) == 2
    if check and not playerWin(board):
        return True
    else:
        return False

def gameOver(board):
    if playerWin(board):
        return True
    else:
        return catscratch(board)

# AI functionality 
def checkOpenCells(board):
    peices = {'X', 'O'}
    options = list(set(board) - peices)
    return options

def compRandomTurn(board):
    options = checkOpenCells(board)
    move = random.choice(options)
    return move

def maximize(board):
    maxValue = -10**2
    maxIndex = 0
    options = checkOpenCells(board)
    for choice in options:
        nextBoard = [i for i in board]
        nextBoard[choice - 1] = 'O'
        if gameOver(nextBoard):
            if catscratch(nextBoard):
                if 0 > maxValue:
                    maxValue = 0
                    maxIndex = choice
            else:
                maxValue = 1
                maxIndex = choice
        else:
            minValue = minimize(nextBoard)
            if minValue > maxValue:
                maxValue = minValue  
                maxIndex = choice
    return [maxValue, maxIndex]

def minimize(board):
    minValue = 10**2
    options = checkOpenCells(board)
    for choice in options:
        nextBoard = [i for i in board]
        nextBoard[choice - 1] = 'X'
        if gameOver(nextBoard):
            if catscratch(nextBoard):
                if 0 < minValue:
                    minValue = 0
            else:
                minValue = -1
        else: 
            maxValue = maximize(nextBoard)[0]
            if maxValue < minValue:
                minValue = maxValue
    return minValue

# displays 
def displayBoard(board):
    frame = str(board[0]) + '|' + str(board[1]) + '|' + str(board[2]) + '\n' +\
            '-+-+-' + '\n' +\
            str(board[3]) + '|' + str(board[4]) + '|' + str(board[5]) + '\n' +\
            '-+-+-' + '\n' +\
            str(board[6]) + '|' + str(board[7]) + '|' + str(board[8]) 
    return frame

def leaderboard(player1, player2, ties, games):
    P1 = 'Player One Wins: '
    P2 = 'Player Two Wins: '
    T = 'Ties: '
    G = 'Total Games: '
    dash = '-'*(len(P1) + 2)
    frame = P1 + str(player1) + '\n' +\
            dash + '\n' +\
            P2 + str(player2) + '\n' +\
            dash + '\n' +\
            T  + str(ties)    + '\n' +\
            dash + '\n' +\
            G  + str(games)   + '\n'
    return frame

# game functionality 
def playGame(turnCount):
    Board = [i for i in range(1, 10)]
    single = promptPlayer('\nSingle player or Double player? (1 or 2) ', '1', '2')
    if single:
        diff = promptPlayer('\nDifficulty Level Randy (Easy) or Tasha (Hard)? (R or T) ', 'R', 'T')
    while not gameOver(Board):
        print()
        print(displayBoard(Board), '\n')
        if turnCount % 2 == 0:
            print("\nPlayer One's Turn")
            turn = turnInput(Board)
            Board[turn - 1] = 'X'
        elif single:
            if diff:
                turn = compRandomTurn(Board)
                print('\nComputer Chose: ', turn)
                Board[turn - 1] = 'O'
            else: 
                turn = maximize(Board)[1]
                print('\nComputer Chose: ', turn)
                Board[turn - 1] = 'O'
        else:
            print("\nPlayer Two's Turn")
            turn = turnInput(Board)
            Board[turn - 1] = 'O'
        turnCount += 1
    print(displayBoard(Board), '\n')
    if catscratch(Board):
        print('Catscratch :(')
        return 0
    if turnCount % 2 == 1:
        print('Player One Wins!')
        return 1
    else: 
        print('Player Two Wins!')
        return 2

# main function 
def main():
    playAgain = True
    player1 = 0
    player2 = 0
    ties = 0
    games = 0
    while playAgain:
        result = playGame(games)
        if result == 1:
            player1 += 1
        elif result == 2:
            player2 += 1
        else:
            ties += 1
        games += 1
        print(leaderboard(player1, player2, ties, games), '\n')
        playAgain = promptPlayer('\nWould you like to play again? (y or n) ', 'y', 'n')
        print()


main()