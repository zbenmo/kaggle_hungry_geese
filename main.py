from collections import defaultdict
from kaggle_environments import make
from kaggle_environments.envs.hungry_geese.hungry_geese import (
  Configuration
)
from pprint import pprint

env = make("hungry_geese")

class Agent1():
  def __init__(self, configuration):
    self.configuration = Configuration(configuration)

  def make_move(self, observation):
    return 'NORTH'


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
print(env.render(mode="ansi", width=500, height=400))

pprint(env.steps)
# # Print schemas from the specification.
# pprint(env.specification.observation)
# pprint(env.specification.configuration)
# pprint(env.specification.action)
