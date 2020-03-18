import constraints as CON
import structures as S
import hydra

# Constraints for the world.
constraints = [
  CON.NoCourseLevelConstraint(100),
  CON.HasCourseLevelConstraint(200, 100)
]


def advance(a_world):
  """Advance the GA one timestep.

  For each timestep, I'm given a world structure, I run the GA, update
  everything, and return a new world."""

  return a_world

def make_initial_world(cfg):
  pass

# Using Facebook's Hydra for configuration.
# http://bit.ly/2Ufz7dI
@hydra.main(config_path="config.yaml")
def main (cfg):
  a_world = make_initial_world(cfg)
  for t in range(cfg.world.terms):
    the_new_world = advance(a_world)
    a_world = the_new_world
  # Show the results.

# Run.
if __name__ == "__main__":
  main()