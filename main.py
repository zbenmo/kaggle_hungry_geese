from collections import defaultdict
from kaggle_environments import make
from kaggle_environments.envs.hungry_geese.hungry_geese import (
  Configuration,
  Observation,
  Action,
  translate,
)
from pprint import pprint
from collections import deque
import random

env = make("hungry_geese")

class Agent1():
  def __init__(self, configuration):
    self.configuration = Configuration(configuration)
    self.memory = deque(maxlen=3)

  def make_move(self, observation):
    _observation = Observation(observation)
    self.memory.append(_observation)
    allowed_actions = set(Action)
    if len(self.memory) > 1:
      cur_obs = self.memory[-1]
      assert cur_obs == _observation
      prev_obs = self.memory[-2]
      my_index = cur_obs.index
      I_was = prev_obs.geese[my_index][0]
      I_am = cur_obs.geese[my_index][0]
      prev_action = self._the_move(I_was, I_am)
      allowed_actions.discard(prev_action.opposite())
    return random.choice(list(allowed_actions)).name

  def _the_move(self, pos_from, pos_to):
    rows, columns = self.configuration.rows, self.configuration.columns
    return next(action for action in Action if translate(pos_from, action, columns=columns, rows=rows) == pos_to)

  #   current_score = self._evaluate_board(self._cur_observation)
  #   return 'NORTH'

  # def _evaluate_board(self, observation):
  #   my_index = observation.index
  #   lengths = [len(x) for x in observation.geese]
  #   my_length = lengths[my_index]
  #   assert sum(lengths) > 0, f'sum(lengths)={sum(lengths)}' 
  #   return my_length / sum(lengths)


dict_with_agents = dict()

def agent(observation, configuration):
  index = observation['index']
  agent_obj = dict_with_agents.get(index, None)
  if agent_obj is None:
    agent_obj = Agent1(configuration)
    dict_with_agents[index] = agent_obj
  return agent_obj.make_move(observation)  

#   print(observation) # {board: [...], mark: 1}
#   print(configuration) # {rows: 10, columns: 8, inarow: 5}

# Run an episode using the agent above vs the default random agent.
env.run([agent, "random"])
# print(env.render(mode="ansi", width=500, height=400))

pprint(env.steps)

# pprint(env.logs)