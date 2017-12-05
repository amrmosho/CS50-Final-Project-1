import random
import useful_functions as useful

#tests player1 against player2 and prints the results for player1 
def test_against(players, game_class, rounds=50, games_per_round=1000, comment=2, pct_increment=2, round_amt=0):
    lows = [games_per_round+1]*3
    highs = [-1]*3
    overall = [0]*3
    for i in range(rounds):
        results = [0]*3 #[losses, ties, wins] for the player
        for game_num in range(games_per_round):
            if comment > 3:
                print("Testing game {}/{}".format((game_num+1), games_per_round))
            game = game_class()
            game.active_player = random.choice([0, 1])
            while game.who_won() is None:
                players[game.active_player].make_move(game)
                if comment > 5:
                    print(game)
            
            # update the results; this works because players[0] is always the player we care about
            results[game.who_won()] += 1
            if comment > 3:
                if comment > 4:
                    print(game)
                print("Results so far in round:\n{}".format(results))
                
        if comment > 2:
            print("Results of one round:\n{}".format(results))
            
        if pct_increment > 0 and comment > 1:
            useful.print_percent(i, rounds, increment_amt = pct_increment, round_amt=round_amt)
            
        for j, testVal in enumerate(results):
            lows[j] = min(lows[j], testVal)
            highs[j] = max(highs[j], testVal)
            overall[j]+=testVal
    ranges = [highs[i]-lows[i] for i in range(3)]
    avgs = [overall[i]*1.0/rounds for i in range(3)] #the *1.0 makes it so it doesn't use integer division 
    if comment > 0:
        print("Lows: {}".format(lows))
        print("Highs: {}".format(highs))
        print("Ranges: {}".format(ranges))
        print("Averages: {}".format(avgs))
    return (lows, highs, ranges, avgs)
    
if __name__ == "__main__":
    from tic_tac_toe import TicTacToe
    from connect_four import ConnectFour
    from players import RandomPlayer, HumanPlayer
    from basic_monte_carlo_player import BasicMonteCarloPlayer
    # TODO something is wrong with this; it's not flipping the players results correctly
    # significant difference: 74 - 15, no ties.
    # test_against((BasicMonteCarloPlayer(30, 1), BasicMonteCarloPlayer(30)), ConnectFour, 100, 100, comment=4)
    # no significant difference: 29 - 28 - 2
    # test_against((BasicMonteCarloPlayer(40, 1), BasicMonteCarloPlayer(30, 1)), ConnectFour, 1, 100, comment=4)
    # significant: 71 - 6 - 2 (Mainly lost when it had a perfect trap set up that was blocked by an opponent, then it gave up easy wins; should be fixed with minimax)
    # personal note: it is so much fun and kinda hilarious to watch this better player completely out-play the worse one, especially knowing that I have been beaten by the worse one multiple times
    # test_against((BasicMonteCarloPlayer(5, 3), BasicMonteCarloPlayer(30)), ConnectFour, 1, 100, comment=6)
    test_against((HumanPlayer(), BasicMonteCarloPlayer(30)), ConnectFour, 1, 100, comment=6)