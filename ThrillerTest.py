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
      return None

   def drop( self, name ):
      object = self.inventory.take( name )
      if ( not object is None ):
         self.world.put( object )
         return object
      return None

   def has( self, name ):
      object = self.inventory.find( name )
      return object

   def use( self, name_of_tool, name_of_actor ):
      tool = self.inventory.find( name_of_tool )
      if ( tool is None ):
         return None
      actor = self.world.find( name_of_actor )
      if ( actor is None ):
         return None
      print actor.name
      print tool.name
      for action in self.actions:
         if action.tool == tool.name and action.actor == actor.name:
            tool = self.inventory.take( name_of_tool )
            actor = self.world.take( name_of_actor )
            retval = self.world.put( action.prototype )
            self.actions.remove( action )
            return action.prototype
      return None

   def is_in_world( self, name ):
      return self.world.find( name )

class ThrillerTest(unittest.TestCase):
   def setUp( self ):
      self.game = Game( GameObject( 'room','dark room', [ GameObject( 'candle' ), GameObject('match'), GameObject('bird'), GameObject('stone') ] ),
                        GameObject( 'inventory', 'my inventory', [] ),
                        [ GameObjectAction( 'candle', 'match', 'light the candle with the match', GameObject('burning candle') ),
                          GameObjectAction( 'bird', 'stone',   'hit the bird with the stone', GameObject('injured bird') ) ] );

   def test_look_in_room(self):
      text = self.game.world.look()
      assert( text == 'dark room' )

   def test_take_and_drop_existing_object(self):
      name_of_existing_object = 'candle'
      object = self.game.take( name_of_existing_object )
      assert ( not object is None )
      assert ( not self.game.has( 'candle' ) is None )
      assert ( self.game.is_in_world( 'candle' ) is None )
      object = self.game.drop( name_of_existing_object )
      assert ( not object is None )
      assert ( self.game.has( 'candle' ) is None )
      assert ( not self.game.is_in_world( 'candle' ) is None )

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
      assert ( not object1 is None )
      assert ( self.game.is_in_world( 'bird' ) is None )
      assert ( self.game.has( 'stone' ) is None )
      assert ( not self.game.is_in_world( 'injured bird' ) is None )
      object2 = self.game.use( 'stone', 'bird' )
      assert ( object2 is None )

   def test_put_burning_candle_to_inventory_to_light_room(self):
      self.game.inventory.put( GameObject( 'burning candle' ) )

if __name__ == '__main__' :
   unittest.main()

