from collections import defaultdict
from kaggle_environments import make
from kaggle_environments.envs.hungry_geese.hungry_geese import (
  Configuration,
  Observation,
  Action,
  translate,
  row_col,
  adjacent_positions,
)
from pprint import pprint
from collections import deque
import random
from functools import partial

env = make("hungry_geese")

class Agent1():
  def __init__(self, configuration):
    self.configuration = Configuration(configuration)
    self.memory = deque(maxlen=3)
    columns = self.configuration.columns
    rows = self.configuration.rows
    self.row_col = partial(row_col, columns=columns)
    self.translate = partial(translate, columns=columns, rows=rows)
    self.adjacent_positions = partial(adjacent_positions, columns=columns, rows=rows)

  def make_move(self, observation):
    self.memory.append(Observation(observation))
    allowed_actions = set(Action)
    cur_obs = self.memory[-1]
    if len(self.memory) > 1:
      prev_obs = self.memory[-2]
      my_index = cur_obs.index
      I_was = prev_obs.geese[my_index][0]
      I_am = cur_obs.geese[my_index][0]
      prev_action = self._the_move(I_was, I_am)
      allowed_actions.discard(prev_action.opposite())

    board_values = self._find_values_of_cells()

    cur_pos = cur_obs.geese[cur_obs.index][0]

    moves_to_value = {
      move: board_values[self.translate(cur_pos, move)]
      for move in allowed_actions
    }

    # return random.choice(list(allowed_actions)).name

    return max(moves_to_value, key=moves_to_value.get).name

  def _the_move(self, pos_from, pos_to):
    return next(action for action in Action if self.translate(pos_from, action) == pos_to)

  def _find_values_of_cells(self):
    rows, columns = self.configuration.rows, self.configuration.columns
    values = {
      cell: 0
      for cell in range(rows * columns)
    }
    cur_obs = self.memory[-1]
    for food_position in cur_obs.food:
      values[food_position] = 10
    for geese in cur_obs.geese:
      for bp in geese:
        values[bp] = -10

    for _ in range(8):
      values_smooth = {}
      for cell in values.keys():
        neighbors = self.adjacent_positions(cell)
        values_smooth[cell] = values[cell] * 0.8 + sum(values[n] for n in neighbors) * 0.2
      values = values_smooth

    return values

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
env.run([agent, agent, agent, agent]), # "random"])
# print(env.render(mode="ansi", width=500, height=400))

pprint(env.steps)

# pprint(env.logs)