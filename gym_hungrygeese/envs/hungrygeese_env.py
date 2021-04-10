import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
from kaggle_environments import make

class HungryGeeseEnv(gym.Env):
    
    def __init__(self, opponents=['random','greedy'], debug=False):
        super(HungryGeeseEnv, self).__init__()
        self.opponents = opponents
        self.env = make("hungry_geese") #, debug=self.debug)
        self.config = self.env.configuration
        self.trainer = self.env.train([None, *opponents])
        
        self.action_space = spaces.Discrete(4)        
        self.observation_space = spaces.Box(low=0, high=255
                                            , shape=(self.config.rows, self.config.columns, 3)
                                            , dtype=np.uint8) 
        self.reward_range = (-1, 1000)  #TODO why this range?
        
    def step(self, action):
        my_action = self.transform_action(action)
        
        #opponent_actions = self.transform_actions(action[1:])  #TODO 
        #self.obs = self.env.step([my_action, *opponent_actions])  #TODO      
        self.obs = self.trainer.step(my_action)  #TODO           
        x_obs = self.transform_step_observation(self.obs, self.config)
        # x_reward = self.obs[0].reward
        # done = (self.obs[0]["status"] != "ACTIVE")
        # info = self.obs[0]["info"]
        x_reward = self.obs[1]
        done = self.obs[2]
        info = self.obs[3]

        return x_obs, x_reward, done, info
        
    def reset(self):
        self.obs = self.trainer.reset()
        x_obs = self.transform_observation(self.obs, self.config)
        return x_obs
    
    def transform_actions(self, actions):
        _actions = []
        for action in actions:
            _actions.append(self.transform_action(action))
        return _actions
        
    def transform_action(self, action):
        if action == 0:
            return "NORTH"
        if action == 1:
            return "EAST"
        if action == 2:
            return "WEST"
        if action == 3:
            return "SOUTH"
        
    def _transform_observations(self, obs, config):
        my_board = np.zeros((config.columns * config.rows * 1), dtype = np.uint8)
        their_board = np.zeros((config.columns * config.rows * 1), dtype = np.uint8)
        food_board = np.zeros((config.columns * config.rows * 1), dtype = np.uint8)
        for goose in obs[0].observation.geese[0]:
            my_board[goose] = 255
        my_board = my_board.reshape((config.rows, config.columns, 1))

        for goose in obs[0].observation.geese[1:]:
            their_board[goose] = 255
        their_board = their_board.reshape((config.rows, config.columns, 1))

        for goose in obs[0].observation.food:
            food_board[goose] = 255
        food_board = food_board.reshape((config.rows, config.columns, 1))
        board = np.concatenate([my_board, their_board, food_board], axis = -1)
        return board

    def transform_step_observation(self, obs, config):
        my_board = np.zeros((config.columns * config.rows * 1), dtype = np.uint8)
        their_board = np.zeros((config.columns * config.rows * 1), dtype = np.uint8)
        food_board = np.zeros((config.columns * config.rows * 1), dtype = np.uint8)

        for goose_cell in obs[0].geese[0]:
            my_board[goose_cell] = 255
        my_board = my_board.reshape((config.rows, config.columns, 1))

        for goose in obs[0].geese[1:]:
            for goose_cell in goose:
                their_board[goose_cell] = 255
        their_board = their_board.reshape((config.rows, config.columns, 1))
        
        for food_cell in obs[0].food:
            food_board[food_cell] = 255
        food_board = food_board.reshape((config.rows, config.columns, 1))
        board = np.concatenate([my_board, their_board, food_board], axis = -1)
        return board

    def transform_observation(self, obs, config):
        my_board = np.zeros((config.columns * config.rows * 1), dtype = np.uint8)
        their_board = np.zeros((config.columns * config.rows * 1), dtype = np.uint8)
        food_board = np.zeros((config.columns * config.rows * 1), dtype = np.uint8)

        for goose_cell in obs.geese[0]:
            my_board[goose_cell] = 255
        my_board = my_board.reshape((config.rows, config.columns, 1))

        for goose in obs.geese[1:]:
            for goose_cell in goose:
                their_board[goose_cell] = 255
        their_board = their_board.reshape((config.rows, config.columns, 1))
        
        for food_cell in obs.food:
            food_board[food_cell] = 255
        food_board = food_board.reshape((config.rows, config.columns, 1))
        board = np.concatenate([my_board, their_board, food_board], axis = -1)
        return board