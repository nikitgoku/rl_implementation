import numpy as np
import pickle

ROWS = 3
COLS = 3

class State:
    def __init__(self, player1, player2):
        self.board     = np.zeros((ROWS, COLS))
        self.player1   = player1
        self.player2   = player2
        self.isFin     = False
        self.boardDict = None
        self.playerSymbol   = 1

    def getDict(self):
        '''
        This function hashes the current board state to create a
        dictionary to store the state-value
        Returns: Board as a dictionary
        '''
        self.boardDict = str(self.board.reshape(COLS * ROWS))
        return self.boardDict

    def availablePositions(self):
        '''
        This function checks for the available positions on the board
        Returns: Free postion on the board as a tuple e.g., (2,1)
        '''
        positions = []
        for i in range(ROWS):
            for j in range(COLS):
                if self.board[i,j] == 0:
                    positions.append((i,j))
        return positions

    def updateState(self, position):
        '''
        This function updates the board with the player's symbol
        For e.g., symbol for player1 is 'x' and player2 is 'o'
        '''
        self.board[position] = self.playerSymbol
        
        # switch to another player
        self.playerSymbol = -1 if self.playerSymbol == 1 else 1

    # function to check if the game is finished and judge the winner
    def winner(self):
        '''
        This function checks if the game is finished or not so that the
        rewards can be distributed
        Returns; BOOL: True (stating that there's a winner)
                       False (stating that the isn't a winner yet)
        '''
        # For vertical pattern
        for i in range(ROWS):
            if sum(self.board[i, :]) == 3:
                self.isFin = True
                return 1
            if sum(self.board[i, :]) == -3:
                self.isFin = True
                return -1

        # For horizontal pattern
        for i in range(COLS):
            if sum(self.board[:, i]) == 3:
                self.isFin = True
                return 1
            if sum(self.board[:, i]) == -3:
                self.isFin = True
                return -1

        # For diagonal pattern
        sum1    = sum([self.board[i,i] for i in range(COLS)])
        sum2    = sum([self.board[i, COLS-i-1] for i in range(COLS)])
        dia_sum = max(abs(sum1), abs(sum2))

        # If the sum of these positions is 3, then the game is finished
        if dia_sum == 3:
            self.isFin = True
            if sum1 == 3 or sum2 == 3:
                return 1
            else:
                return -1

        # For the scenario where the game ties
        if len(self.availablePositions()) == 0:
            self.isFin = True
            return 0

        self.isFin = False
        return None

    # Give reward only when game ends
    # Reward is between 0 and 1
    def giveReward(self):
        res = self.winner()

        if res == 1:
            self.player1.feedReward(1)
            self.player2.feedReward(0)
        elif res == -1:
            self.player1.feedReward(0)
            self.player2.feedReward(1)
        else:
            # We can change the reward when the game ties
            # the numbers can be updated to see how the agent behaves
            self.player1.feedReward(0.4)
            self.player2.feedReward(0.8)

    def play(self, rounds=100):
        ''''
        Function where two computer players play against each other to train
        them. The training process goes as follows
        - Look for available postions
        - Choose action
        - Updating theboard state and add the action to player's states
        - Check if the game has reached the end and distribute the rewards
          accordingly
        '''
        for i in range(rounds):
            if i%1000 == 0:
                print('Rounds {}'.format(i))
            while not self.isFin:
                # Player1
                positions = self.availablePositions()
                p1_action = self.player1.chooseAction(positions, self.board, self.playerSymbol)
                self.updateState(p1_action)
                board_dict = self.getDict()
                self.player1.addState(board_dict)

                win = self.winner()
                if win is not None:
                    self.giveReward()
                    self.player1.reset()
                    self.player2.reset()
                    self.reset()
                    break
                else:
                    positions = self.availablePositions()
                    p2_action = self.player2.chooseAction(positions, self.board, self.playerSymbol)
                    self.updateState(p2_action)
                    board_dict = self.getDict()
                    self.player2.addState(board_dict)

                    win = self.winner()
                    if win is not None:
                        self.giveReward()
                        self.player1.reset()
                        self.player2.reset()
                        self.reset()
                        break

    def playWithHuman(self):
        '''
        Function where player1 is the agent and player2 is the user
        - Player1 checks for the available postions
          Takes action, updates the board state and checks for the game
          completion
        - Player2 sees the board and gives input in (row,col) format
          Updates the state on the board and checks is the game is completed
        '''
        while not self.isFin:
            # player1
            positions = self.availablePositions()
            p1_action = self.player1.chooseAction(positions, self.board, self.playerSymbol)
            self.updateState(p1_action)
            self.showBoard()

            win = self.winner()
            if win is not None:
                if win == 1:
                    print(self.player1.name, "wins!")
                else:
                    print("Game has tied!")
                self.reset()
                break
            else:
                # player2
                positions = self.availablePositions()
                p2_action = self.player2.chooseAction(positions)
                self.updateState(p2_action)
                self.showBoard()
                
                win = self.winner()
                if win is not None:
                    if win == -1:
                        print(self.player2.name, " wins!")
                    else:
                        print("Game has tied!")
                    self.reset()
                    break



    # Display the game board
    def showBoard(self):
        '''
        Function is used to display the board after every step when
        agent is playing with the human player
        '''
        # p1: x  p2: o
        for i in range(0, ROWS):
            print('-------------')
            out = '| '
            for j in range(0, COLS):
                if self.board[i, j] == 1:
                    token = 'x'
                if self.board[i, j] == -1:
                    token = 'o'
                if self.board[i, j] == 0:
                    token = ' '
                out += token + ' | '
            print(out)
        print('-------------')

    # board reset
    def reset(self):
        '''
        Function is used to reset the board to its initial state
        '''
        self.board = np.zeros((ROWS, COLS))
        self.boardHash = None
        self.isEnd = False
        self.playerSymbol = 1


class Players:
    def __init__(self, name, exp_rate=0.3):
        # initializing a dictionary 'state_values' to store the state-value 
        # pair; the learning rate 'alpha' can be updated
        self.name         = name
        self.states       = []
        self.alpha        = 0.2
        self.exp_rate     = exp_rate
        self.gamma        = 0.9
        self.states_value = {}

    def chooseAction(self, positions, current_game, symbol):
        '''
        We are using the epsilon-greedy method to balance the exploration
        and exploitation; only 30% (exp_rate=0.3) of the time our agent will
        take random actions
        '''
        if np.random.uniform(0,1) <= self.exp_rate:
            idx    = np.random.choice(len(positions))
            action = positions[idx]
        else:
            # Here we hash the next board state and choose the action that
            # returns the max value of the next state
            max = -999
            for p in positions:
                next_game     = current_game.copy()
                next_game[p]  = symbol
                next_gameDict = self.getDict(next_game)

                value = 0 if self.states_value.get(next_gameDict) is None else self.states_value.get(next_gameDict)

                if value >= max:
                    max    = value
                    action = p
        
        return action

    def feedReward(self, reward):
        # Applying the value iteration to update the value estimation of the states
        for state in reversed(self.states):
            if self.states_value.get(state) is None:
                self.states_value[state] = 0
            self.states_value[state] += self.alpha*(self.gamma*reward - self.states_value[state])

            reward = self.states_value[state]

    def getDict(self, board):
        boardDict = str(board.reshape(COLS*ROWS))
        return boardDict

    def addState(self, state):
        self.states.append(state)

    def reset(self):
        self.states = []

    def savePolicy(self):
        '''
        Function to save the policy which can be used to play against
        human players
        '''
        fwrite = open('policy_'+str(self.name), 'wb')
        pickle.dump(self.states_value, fwrite)
        fwrite.close()

    def loadPolicy(self, file):
        '''
        Function to load the learned policy
        '''
        fread = open(file, 'rb')
        self.states_value = pickle.load(fread)
        fread.close()


class HumanPlayer:
    # Human will choose actions accordingly to the
    # input, which will be the position in (row,col) format
    def __init__(self, name):
        self.name = name

    def chooseAction(self, positions):
        while True:
            row = int(input("Input your action row:"))
            col = int(input("Input your action col:"))
            action = (row, col)
            if action in positions:
                return action

    def addState(self, state):
        pass

    # Humans don't need any reward, they're just happy creating such agents
    def feedReward(self, reward):
        pass

    def reset(self):
        pass


if __name__ == "__main__":
    p1 = Players("p1")
    p2 = Players("p2")

    state = State(p1, p2)
    print("training...")
    state.play(50000)

    p1.savePolicy()
    p2.savePolicy()
    p1.loadPolicy('policy_p1')

    p1 = Players("computer", exp_rate=0)
    p1.loadPolicy("policy_p1")

    p2 = HumanPlayer("human")

    state = State(p1, p2)
    state.playWithHuman()
    