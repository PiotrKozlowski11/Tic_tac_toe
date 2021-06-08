Simple Tic Tac Toe game using pygame addon.
Classic game uses two players: each player can be occupied by human or one of the AI difficulties. Easy diffuculty: makes random moves up to the end of the game.
Medium: makes random moves up to the point where there are “size – 1”occupied tiles by one of the players. In such situation AI will go for the win or block the enemy. 
Hard: uses minimax algorithm with alpha beta prunning.
There is also possibility to adjust size of the board. When hard difficulty is selected size is limitied to “6” due to time required to make calculations for each move.
TODO in future:
•	Add possibility to adjust resolution of game
•	Decrease calculations required for minimax algorithm by checking first places where there are occupied tiles and there is still possibility to win in each of rows, columns or by crossing win.
