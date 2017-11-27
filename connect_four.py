from game import Game

class ConnectFour(Game):
    def get_initial_state(self):
        # 7 slots per row, 6 rows
        # first inner list represents the bottom row from left to right
        # return an empty board
        return [[-1] * 7 for _ in range(6)]
    
    def get_properties(self):
        '''This returns a list of numbers of constant length describing the state, or None
        This is what we'd feed into a neural net to learn about the game
        
        For example, if the game really was player 1's turn to move, it would swap all the pieces and then return the same values
        ...as if player 0 had made all the moves that player 1 did and vice versa
        
        TODO this will need to be defined better if/when we actually start using neural networks
        '''
        return [val for val in row for row in self.get_copy().state]
        
    def swap_players(self):
        '''Swap the players in a game. Does not return any value.'''
        self.state = [[Game.other_player(val) if val >=0 else -1 for val in row] for row in self.state]
        
    def get_copy(self):
        '''Return a copy of the object'''
        return ConnectFour(([row[:] for row in self.state], self.active_player))
    
    def get_hash(self):
        '''Return a unique string for the state and active player'''
        string_list = ["O", "X", " "]
        ans = string_list[self.active_player]
        for row in self.state:
            for val in row:
                ans += string_list[val]
        return ans
    
    def get_possible_actions(self):
        '''Return a list of the possible actions that can be taken by self.active_player in the self.state state
        Behavior is undefined when the game is complete
        '''
        # return which slots are open on the top
        return [i for i in range(7) if self.state[-1][i] == -1]
        
    def make_move(self, action):
        '''Change the state of the game and update the active player based on the action'''
        # the action specifies the column
        # start on the bottom row to see if there's an open space, and then move up if not
        for row in self.state:
            if row[action] == -1:
                row[action] = self.active_player
                break
        
        self.active_player = Game.other_player(self.active_player)
        
    def who_won(self):
        '''Return 0 if player 0 won, 1 if player 1 won, -1 if there was a tie, and None if the game has not finished'''
        match_amount = 4 # must be greater than 1
        columns = 7
        rows = 6
        
        ans = -1  # default to tie
        if -1 in self.state[-1]:
            ans = None  # game is not complete yet
        
        # the player we're checking to see if they won
        cur_player = None
        # upgrade: duplicate code here
        # check rows (left to right)
        for row_index in range(rows):
            for start_col_index in range(columns - match_amount + 1):
                # how many columns to shift over from the start_col_index
                for col_shift in range(match_amount):
                    if col_shift == 0:
                        cur_player = self.state[row_index][start_col_index + col_shift]
                        if cur_player == -1:
                            # no player has moved here yet
                            break
                    if self.state[row_index][start_col_index + col_shift] != cur_player:
                        # not enough in the series
                        break
                    else:
                        # found the next one in the series
                        if col_shift == match_amount - 1:
                            # found an entire match
                            return cur_player
        # check columns (bottom to top)
        for col_index in range(columns):
            for start_row_index in range(rows - match_amount + 1):
                #how many rows to shift over from the start_row_index
                for row_shift in range(match_amount):
                    if row_shift == 0:
                        cur_player = self.state[start_row_index + row_shift][col_index]
                        if cur_player == -1:
                            # no player has moved here yet
                            break
                    if self.state[start_row_index + row_shift][col_index] != cur_player:
                        # not enough in the series
                        break
                    else:
                        # found the next one in the series
                        if row_shift == match_amount - 1:
                            # found an entire match
                            return cur_player
                            
        # check top left diagonals
        # iterate up through the rows
        for row_index in range(match_amount - 1, rows):
            for start_col_index in range(columns - match_amount + 1):
                # how many columns to shift over from the start_col_index
                for shift in range(match_amount):
                    if shift == 0:
                        cur_player = self.state[row_index - shift][start_col_index + shift]
                        if cur_player == -1:
                            # no player has moved here yet
                            break
                    if self.state[row_index - shift][start_col_index + shift] != cur_player:
                        # not enough in the series
                        break
                    else:
                        # found the next one in the series
                        if shift == match_amount - 1:
                            # found an entire match
                            return cur_player
        
        # check top right diagonals
        # iterate up through the rows
        for row_index in range(rows - match_amount + 1):
            for start_col_index in range(columns - match_amount + 1):
                # how many columns to shift over from the start_col_index
                for shift in range(match_amount):
                    if shift == 0:
                        cur_player = self.state[row_index + shift][start_col_index + shift]
                        if cur_player == -1:
                            # no player has moved here yet
                            break
                    if self.state[row_index + shift][start_col_index + shift] != cur_player:
                        # not enough in the series
                        break
                    else:
                        # found the next one in the series
                        if shift == match_amount - 1:
                            # found an entire match
                            return cur_player
        return ans
        
    def __str__(self):
        return "Player {}'s turn:\n{}".format(self.active_player, "\n".join([str(row).replace("-1", "-") for row in reversed(c.state)]))
                            
if __name__ == "__main__":
    print("Getting random game!")
    c = ConnectFour.get_random_game()
    print(c)
    print(c.who_won())
    # haha this takes forever. 64! is under a googol, but not by too much, so that's expected
    print(ConnectFour().get_complexity(-1)) 