import unittest
from tilovanta import Game
class Tests(unittest.TestCase):
 def test_reachable(self):
  for i in range(100):self.assertTrue(Game(i).reachable())
 def test_boundary(self):
  g=Game(1);self.assertFalse(g.move(-1,0));self.assertEqual(g.moves,0)
 def test_gap(self):
  g=Game();g.board[1,9]=' ';g.move(1,0);self.assertTrue(g.dead);self.assertFalse(g.move(1,0))
 def test_hazard(self):
  g=Game();g.board[1,9]='!';g.move(1,0);self.assertTrue(g.dead)
 def test_jump(self):
  g=Game();g.board[1,9]='!';g.board[2,9]='.';g.move(1,0,True);self.assertEqual(g.pos,(2,9));self.assertFalse(g.dead)
 def test_win(self):
  g=Game();g.pos=(8,0);g.move(1,0);self.assertTrue(g.won)
 def test_seed(self):self.assertEqual(Game(42).board,Game(42).board)
 def test_direction(self):self.assertRaises(ValueError,Game().move,1,1)
if __name__=='__main__':unittest.main()
