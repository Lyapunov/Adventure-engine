import unittest

from GameObject import GameObject
from GameObject import GameObjectAction

class Game:
   def __init__( self, world, inventory, actions ):
      self.world = world
      self.inventory = inventory
      self.actions = actions
   def take( self, name ):
      object = self.world.take( name )
      if ( not object is None ):
         self.inventory.put( object )
         return object
   def has( self, name ):
      object = self.inventory.find( name )
      return object
   def use( self, name1, name2 ):
      pass 
   def is_in_world( self, name ):
      return self.world.find( name )

class ThrillerTest(unittest.TestCase):
   def setUp( self ):
      self.game = Game( GameObject( 'room','dark room', [ GameObject( 'candle' ), GameObject('match'), GameObject('bird'), GameObject('stone') ] ),
                        GameObject( 'inventory', 'my inventory', [] ),
                        [ GameObjectAction( GameObject('candle'), GameObject('match'), 'light the candle with the match', GameObject('burning candle') ),
                          GameObjectAction( GameObject('bird'), GameObject('stone'),   'hit the bird with the stone', GameObject('injured bird') ) ] );

   def test_look_in_room(self):
      text = self.game.world.look()
      assert( text == 'dark room' )

   def test_take_existing_object(self):
      name_of_existing_object = 'candle'
      object = self.game.take( name_of_existing_object )
      assert ( not object is None )
      assert ( not self.game.has( 'candle' ) is None )

   def test_take_not_existing_object(self):
      name_of_not_existing_object = 'banana'
      object = self.game.take( name_of_not_existing_object )
      assert ( object is None )
      assert ( self.game.has( name_of_not_existing_object ) is None )

   def test_put_knife_on_the_world(self):
      object = GameObject( 'knife' )
      self.game.inventory.put( object )
      assert ( not self.game.inventory.take('knife') is None )

   def test_action_hit_the_bird_with_the_stone(self):
      self.game.take( 'stone' )
      object1 = self.game.use( 'stone', 'bird' )
      assert ( object1 is not None )
      assert ( self.game.is_in_world( 'bird' ) is None )
      assert ( not self.game.is_in_world( 'injured bird' ) is None )
      object2 = self.game.use( 'stone', 'bird' )
      assert ( object2 is not None )

   def test_put_burning_candle_to_inventory_to_light_room(self):
      self.game.inventory.put( GameObject( 'burning candle' ) )

if __name__ == '__main__' :
   unittest.main()

