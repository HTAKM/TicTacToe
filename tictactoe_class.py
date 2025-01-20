PLAYER_X = 1
PLAYER_O = -1

class TicTacToe:
    def __init__(self):
        self.game_state = [0 for i in range(9)]
        self.player = PLAYER_X
    
    def initialize_game_state(self):
        """
        Initialize the game. Player for placing X is default as the first one.
        """

        self.player = PLAYER_X
        self.game_state = [0 for i in range(9)]

    def player_move(self, pos):
        self.game_state[pos] = self.player
    
    def next_turn(self):
        """
        Set the current player to the next player.
        """

        self.player = PLAYER_X if self.player == PLAYER_O else PLAYER_O
    
    def is_x_turn(self):
        """
        Determine whether it is the default player's turn. i.e. player who places X
        """

        return self.player == PLAYER_X

    def is_winner(self) -> bool:
        """
        Check if the current player is the winner.
        """

        return any(self.player == self.game_state[i] == self.game_state[j] == self.game_state[k]
            for i,j,k in [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)])

    def print_player(self):
        """
        Print the current player as text.
        """

        return "Player X" if self.player == PLAYER_X else "Player O"

def obtain_click_pos(game_coor, click_coor) -> int:
    """
    Find the position in the game screen where the player has clicked. 
    If the position is not in the game region, -1 is returned.
    The position is determined in top to bottom, left to right.
    """

    trans_coor = ((click_coor[0]-game_coor[0]) // 100, (click_coor[1]-game_coor[1]) // 100)
    if 0 <= trans_coor[0] < 3 and 0 <= trans_coor[1] < 3:
        return trans_coor[0] + trans_coor[1] * 3
    return -1
