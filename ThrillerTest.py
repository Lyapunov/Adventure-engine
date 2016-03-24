import unittest

from GameObject import GameObject
from GameObject import GameObjectAction

class Game:
   def __init__( self, world, inventory, actions ):
      self.world = world
      self.inventory = inventory
      self.actions = actions

class ThrillerTest(unittest.TestCase):
   def setUp( self ):
      self.game = Game( GameObject( 'room','dark room', [ GameObject( 'candle' ), GameObject('match') ] ),
                        GameObject( 'inventory', 'my inventory', [] ),
                        [ GameObjectAction( GameObject('candle'), GameObject('match'), 'you light the candle with the match', GameObject('burning candle') ) ] );

   def test_look_in_room(self):
      text = self.game.world.look()
      assert( text == 'dark room' )

   def test_take_candle(self):
      object = self.game.world.take('candle')
      assert ( not object is None and object.name == 'candle' )

   def test_put_knife_in_inventory(self):
      object = GameObject( 'knife' )
      self.game.inventory.put( object )
      assert ( not self.game.inventory.take('knife') is None )

   def test_use_bird_on_stone(self):
      bird  = GameObject( 'bird' )
      stone = GameObject( 'stone' )
      burning_stone = GameObject( 'injured bird' )
      actionDescription = 'you hit the bird with the stone';
      action = GameObjectAction( bird, stone, actionDescription, burning_stone )
      self.game.actions.append( action )
      assert ( stone.use( bird, self.game.actions ) is None )
      assert ( bird.name == 'bird' )
      assert ( bird.use( stone, self.game.actions ) == actionDescription )
      assert ( bird.name == 'injured bird' )
      assert ( not action in self.game.actions )

   def test_put_burning_candle_to_inventory_to_light_room(self):
      self.game.inventory.put( GameObject( 'burning candle' ) )

if __name__ == '__main__' :
   unittest.main()

