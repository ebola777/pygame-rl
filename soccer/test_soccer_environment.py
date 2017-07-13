# Test modules
import pytest

# Testing targets
import soccer


class SoccerEnvironmentTest:
  env = soccer.SoccerEnvironment()

  def test_init(self):
    # The soccer positions should be non-empty
    assert len(self.env.soccer_pos.walkable) > 0
    assert len(self.env.soccer_pos.goals) > 0

  def test_reset(self):
    # Reset the environment
    observation = self.env.reset()
    # Get the state
    state = self.env.state
    # Check the initial observation
    assert observation.state == state
    assert observation.action is None
    assert observation.reward == pytest.approx(0.0)
    assert observation.next_state is None
    # The initial state should not be terminal
    assert not state.is_terminal()
    # The player agent positions should be on the left to the computer agent
    player_pos = state.get_agent_pos(0)
    computer_pos = state.get_agent_pos(1)
    assert player_pos[0] < computer_pos[0]
    # Either agent has the ball
    player_has_ball = state.get_agent_ball(0)
    computer_has_ball = state.get_agent_ball(1)
    assert player_has_ball != computer_has_ball
    # The time step should be 0
    assert state.time_step == 0

  def test_take_action(self):
    # Take each action
    expected_time_step = 0
    for action in self.env.actions:
      observation = self.env.take_action(action)
      expected_time_step += 1
      # Check the observation
      assert observation.state is None
      assert observation.action == action
      assert observation.reward >= -1.0 and observation.reward <= 1.0
      assert observation.next_state.time_step == expected_time_step

  def test_renderer(self):
    self.env.render()
    # The renderer should contain the environment
    assert self.env.renderer.env_state == self.env
    # The renderer display should have been quitted
    assert self.env.renderer.display_quitted

  def test_get_moved_pos(self):
    pos = [0, 0]
    # Check the moved positions of each action
    assert self.env.get_moved_pos(pos, 'MOVE_RIGHT') == [1, 0]
    assert self.env.get_moved_pos(pos, 'MOVE_UP') == [0, -1]
    assert self.env.get_moved_pos(pos, 'MOVE_LEFT') == [-1, 0]
    assert self.env.get_moved_pos(pos, 'MOVE_DOWN') == [0, 1]
    assert self.env.get_moved_pos(pos, 'STAND') == pos

  def test_get_pos_distance(self):
    pos1 = [0, 0]
    pos2 = [3, 4]
    # Check the Euclidean distance
    assert self.env.get_pos_distance(pos1, pos2) == pytest.approx(5.0)
