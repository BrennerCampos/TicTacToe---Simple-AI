
import random

sample=('O', 'O', ' ', ' ', 'X', ' ', ' ', 'X', 'X')
start=(' ',' ',' ', ' ', ' ', ' ',' ',' ',' ')

#basic functions:
# given a board, has anybody won?
# win returns: X, O, ' ' (game isn't over), or '-' tie
def win(b):
	if b[0]==b[1] and b[1]==b[2] and b[0]!=' ':
		return b[0]
	if b[3]==b[4] and b[4]==b[5] and b[3]!=' ':
		return b[3]
	if b[6]==b[7] and b[7]==b[8] and b[6]!=' ':
		return b[6]
	if b[0]==b[3] and b[3]==b[6] and b[0]!=' ':
		return b[0]
	if b[1]==b[4] and b[4]==b[7] and b[1]!=' ':
		return b[1]
	if b[2]==b[5] and b[5]==b[8] and b[2]!=' ':
		return b[2]
	if b[0]==b[4] and b[4]==b[8] and b[0]!=' ':
		return b[0]
	if b[2]==b[4] and b[4]==b[6] and b[2]!=' ':
		return b[2]
	if not ' ' in b:
		return '-'
	return ' '

# print out a board
def printboard(brd):
	print( brd[0],"|",brd[1],"|",brd[2])
	print( "---------")
	print( brd[3],"|",brd[4],"|",brd[5])
	print( "---------")
	print( brd[6],"|",brd[7],"|",brd[8])
	print()

#('O', 'O', ' ', ' ', 'X', ' ', ' ', 'X', 'X')
# go through every place in the board
# if there's a space, play in it, and add it to my moves
def allmoves(board, player):
    moves=[]    #my list of possible moves
    for i in range(len(board)):
        if board[i]==" ":
            child=board         #I can do this because board is tuple
            child=list(child[:i]) + [player] + list(child[i+1:])
            child=tuple(child)
            moves.append(child)
    return moves

#swaps player
def otherplayer(player):
    if player=="X":
        return "O"
    return "X"

#score gives a value to the board from the point of view of the player
def score(board,player):
    winner=win(board)
    if winner==player:
        return 10
    if winner==otherplayer(player):
        return -10
    if winner=="-":
        return -5
    #game is ongoing? score 0
    return 0

# basic random player
#def randomplayer(board,player):

   # move = moves[random.randrange(0,len(moves)) ]
    #return move

# greedy player
#one who goes for the win
# if it can't win, play random
    # it should select a set of moves with the best score, and choose one randomly from it

def greedyplayer(board,player):
    #get all my moves
    moves=allmoves(board,player)
    # go through my moves and score them
    for i in range(len(moves)):
        value = score(moves[i],player)
        #put the score as a tuple in front of  the move
        moves[i] = (value,moves[i])
    # now I can sort them: biggest value first
    moves.sort(reverse=True)
    # get a sublist of all the moves that are best
    index=0
    topscore=moves[0][0]
    while index<len(moves) and moves[index][0]==topscore:
        index=index+1
    moves=moves[:index]
    #moves now contains only my best moves (however many there are)
    #pick one randomly and return
    move = moves [ random.randrange(0,len(moves)) ]
    return move[1]      #cut off the score and just return move

# one depth minimax
# look at all my moves, then all opponents, no further
#  behavior?  go for the win.  if no win, will block opponent
def minimax_onedepth(board,player):
    #get all my moves
    moves=allmoves(board,player)
    # go through all my moves to score them
    for i in range(len(moves)):
        value = score(moves[i],player)
        #end game? don't go further, use the score
        if value!=0:
            moves[i]=(value,moves[i])
        else:
            # need to look at opponent
            #get a list of all countermoves
            countermoves = allmoves(moves[i],otherplayer(player))
            #score them
            for j in range(len(countermoves)):
                # put the score at front of move so I can sort
                countermoves[j]=(score(countermoves[j],player), countermoves[j])
            #rank them: but this time with the min first
            countermoves.sort(reverse=False)
            #get the score of the lowest move
            worstscore = countermoves[0][0]
            #now use that score to value my move
            moves[i]=(worstscore,moves[i])

    #now pick the best of the worst
    moves.sort(reverse=True)
    # get a sublist of all the moves that are best
    index=0
    topscore=moves[0][0]
    while index<len(moves) and moves[index][0]==topscore:
        index=index+1
    moves=moves[:index]
    #moves now contains only my best moves (however many there are)
    #pick one randomly and return
    move = moves [ random.randrange(0,len(moves)) ]
    return move[1]      #cut off the score and just return move

# make a game that will play two random players against each other
def game():
    board=start
    printboard(board)
    player="X"
    #keep going until game over
    while win(board)==" ":
        #find all the possible moves
        moves = allmoves(board,player)
        #pick one at random
        board = minimax_onedepth(board,player)
        printboard(board)
        input()     #pause for keystroke
        player = otherplayer(player)

    print("the winner is",win(board))

game()
