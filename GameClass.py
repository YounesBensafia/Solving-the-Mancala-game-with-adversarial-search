class GameClass:
    def __init__(self, state, choice):
        """
        Args:
            state (an instance of the MancalaBoard class): represent the game state.
            playerSide (dictionary):  stores the player side chosen by the human and
            the computer (player1 or player2).
        """
        self.state = state #INSTANCE OF MANCALA BOARD CLASS
        self.player = choice
        if choice == 1:
            self.playerSide = {1:2, -1:1} # HABIT TLAEB MEN A-F OU G-L4
        else:
            self.playerSide = {1:1, -1:2} 

    def gameOver(self):
        """The function gameOver(), which checks if the game has ended (i.e., all the pits of one player are 
        empty). This function will also collect all remaining seeds in the opponent s pits and place them 
        in their store"""
        
        player1_empty = all(self.state.board[pit] == 0 for pit in self.state.player_pits[1])
        player2_empty = all(self.state.board[pit] == 0 for pit in self.state.player_pits[2])
        
        if player1_empty or player2_empty:
            if player1_empty:
                for pit in self.state.player_pits[2]:
                    self.state.board[2] += self.state.board[pit]
                    self.state.board[pit] = 0
            elif player2_empty:
                for pit in self.state.player_pits[1]:
                    self.state.board[1] += self.state.board[pit]
                    self.state.board[pit] = 0
            return True 
        return False

    def findWinner(self):
        player1_score = self.state.board[1]
        player2_score = self.state.board[2]
        
        if player1_score > player2_score:
            return 'PLAYER1', player1_score
        elif player2_score > player1_score:
            return 'PLAYER2', player2_score
        else:
            return 'draw', player1_score
   
    def h1(self):
        computer_store = self.state.board[self.playerSide[1]]
        human_store = self.state.board[self.playerSide[-1]]
        return computer_store - human_store
    
    def h2(self):
        computer_store = self.state.board[self.playerSide[1]]
        computer_store2 = self.state.board[self.playerSide[-1]]  

        computer2_remaining = sum(self.state.board[pit] for pit in self.state.player_pits[self.playerSide[1]])  
        computer1_remaining = sum(self.state.board[pit] for pit in self.state.player_pits[self.playerSide[-1]])

        computer1_empty_pits = sum(1 for pit in self.state.player_pits[self.playerSide[-1]] if self.state.board[pit] == 0)
        computer2_empty_pits = sum(1 for pit in self.state.player_pits[self.playerSide[1]] if self.state.board[pit] == 0)

        # Contrôler le joueur adverse en limitant ses options
        computer2_next_move = sum(1 for pit in self.state.player_pits[self.playerSide[1]] if self.state.board[pit] != 0) 

        return (
            30 * computer_store           # Maximise les graines dans le magasin de Computer 2
            - 25 * computer_store2            # Pénalise le score de l'humain (on favorise Computer 1)
            - 10 * computer2_remaining    # Pénalise les graines restantes de Computer 2
            + 5 * computer1_remaining     # Encourage à garder des graines pour de futures opportunités
            - 15 * computer2_empty_pits   # Pénalise Computer 2 pour ses pits vides
            + 10 * computer1_empty_pits   # Réduit l'impact des pits vides de Computer 1
            - 5 * computer2_next_move     # Réduit les options pour Computer 2
            + 5 * (computer_store - computer_store2)  # Favorise un écart positif pour Computer 1
        )

        
    







    
    def evaluate(self, h):
        if h == 1:
            return GameClass.h1(self)
        else:
            return GameClass.h2(self)
    