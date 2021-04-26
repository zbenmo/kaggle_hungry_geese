# from collections import defaultdict
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
# import random
from functools import partial
import click

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
        values_smooth[cell] = values[cell] * 0.9 + sum(values[n] for n in neighbors) / len(neighbors) * 0.1
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

@click.group()
def main():
  pass

@main.command()
def play():
  env = make("hungry_geese")

  # Run an episode using the agent above vs the default random agent.
  env.run([agent, agent, agent, agent]), # "random"])
  # print(env.render(mode="ansi", width=500, height=400))

  # pprint(env.steps)

  # pprint(env.logs)

@main.command()
def show_board():
  env = make("hungry_geese")

  # Run an episode using the agent above vs the default random agent.
  env.run([agent, agent, agent, agent]), # "random"])
  print(env.render(mode="ansi", width=500, height=400))
  last_step = env.steps[-1]
  # pprint(last_step)
  index = max(range(len(last_step)), key=lambda i: last_step[i]['reward'])
  agent_obj = dict_with_agents.get(index, None)
  board_values = agent_obj._find_values_of_cells()
  for row in range(7):
    print()
    row_to_print = []
    for col in range(11):
      pos = row * 11 + col
      row_to_print.append(board_values[pos])
    print(' '.join(map(lambda x: f'{x:4.2f}', row_to_print)))
  print()

@main.command()
def show_possible_next_moves():
  step = [{'action': 'NORTH',
                      'info': {},
                      'observation': {'food': [62, 44],
                                      'geese': [[56], [73], [75], [25]],
                                      'index': 0,
                                      'remainingOverageTime': 60,
                                      'step': 0},
                      'reward': 0,
                      'status': 'ACTIVE'},
                    {'action': 'NORTH',
                      'info': {},
                      'observation': {'index': 1, 'remainingOverageTime': 60},
                      'reward': 0,
                      'status': 'ACTIVE'},
                    {'action': 'NORTH',
                      'info': {},
                      'observation': {'index': 2, 'remainingOverageTime': 60},
                      'reward': 0,
                      'status': 'ACTIVE'},
                    {'action': 'NORTH',
                      'info': {},
                      'observation': {'index': 3, 'remainingOverageTime': 60},
                      'reward': 0,
                      'status': 'ACTIVE'}]
  env = make("hungry_geese", steps=[step])


  print(env.render(mode="ansi", width=500, height=400))

  print("before")
  pprint(env.state)

  print()
  env.step(['NORTH', 'NORTH', 'NORTH', 'NORTH'])
  print(env.render(mode="ansi", width=500, height=400))

  print("after")
  pprint(env.state)

if __name__ == '__main__':
  main()
