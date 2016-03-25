import unittest

from GameObject import Game
from GameObject import GameObject
from GameObject import GameObjectAction
from GameObject import GamePassage

class ThrillerTest(unittest.TestCase):
   def setUp( self ):
      self.game = Game( [ GameObject( 'dark room','dark room', [ GameObject( 'candle' ), GameObject('match'), GameObject('bird'), GameObject('stone') ] ),
                          GameObject( 'bathroom','bathroom', [ GameObject( 'mirror' ) ] ) ],
                        [ GamePassage( 'dark room', 'bathroom', 'N', 'S' ) ],
                        [ GameObjectAction( 'candle', 'match', 'lighting candle', GameObject('burning candle') ),
                          GameObjectAction( 'bird', 'stone', 'hitting bird', GameObject('injured bird') ) ],
                        [ GameObjectAction( 'dark room', 'burning candle', '', GameObject('light room', 'light room') ) ] );

   def test_take_and_drop_existing_object(self):
      name_of_existing_object = 'candle'
      object = self.game.take( name_of_existing_object )
      assert ( not object is None )
      assert ( not self.game.has( 'candle' ) is None )
      assert ( self.game.is_in_room( 'candle' ) is None )
      object = self.game.drop( name_of_existing_object )
      assert ( not object is None )
      assert ( self.game.has( 'candle' ) is None )
      assert ( not self.game.is_in_room( 'candle' ) is None )

   def test_trying_take_not_existing_object(self):
      name_of_not_existing_object = 'banana'
      object = self.game.take( name_of_not_existing_object )
      assert ( object is None )
      assert ( self.game.has( name_of_not_existing_object ) is None )

   def test_action_hit_the_bird_with_the_stone(self):
      self.game.take( 'stone' )
      object1 = self.game.use( 'stone', 'bird' )
      assert ( not object1 is None )
      assert ( self.game.is_in_room( 'bird' ) is None )
      assert ( self.game.has( 'stone' ) is None )
      assert ( not self.game.is_in_room( 'injured bird' ) is None )
      object2 = self.game.use( 'stone', 'bird' )
      assert ( object2 is None )

   def test_action_hit_the_bird_with_the_stone_but_both_are_in_inventory(self):
      self.game.take( 'stone' )
      self.game.take( 'bird' )
      object1 = self.game.use( 'stone', 'bird' )
      assert ( not self.game.has( 'injured bird' ) is None )

   def test_action_hit_the_bird_with_the_stone_but_use_params_are_reversed(self):
      self.game.take( 'stone' )
      object1 = self.game.use( 'bird', 'stone' )
      assert ( not self.game.is_in_room( 'injured bird' ) is None )

   def test_room_goes_light_from_dark_if_we_burn_the_candle(self):
      assert ( self.game.look() == 'dark room'  )
      assert ( self.game.has( 'candle' ) is None )
      assert ( self.game.has( 'match' ) is None )
      self.game.take( 'candle' )
      self.game.take( 'match' )
      assert ( not self.game.has( 'candle' ) is None )
      assert ( not self.game.has( 'match' ) is None )
      object1 = self.game.use( 'candle', 'match' )
      assert ( not object1 is None )
      assert ( self.game.look() == 'light room' )

   def test_moving_between_rooms(self):
      assert ( self.directions != ['N'] );
      self.game.move('N')
      self.game.look() == 'other room'

if __name__ == '__main__' :
   unittest.main()

