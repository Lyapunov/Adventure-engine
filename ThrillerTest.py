import unittest

from GameObject import Game
from GameObject import GameObject
from GameObject import GameObjectAction
from GameObject import GamePassage

class ThrillerTest(unittest.TestCase):
   def setUp( self ):
      self.game1 = Game( [ GameObject( 'dark room','dark room', [ GameObject( 'candle' ), GameObject('match'), GameObject('bird'), GameObject('stone') ] ),
                           GameObject( 'bathroom', 'bathroom' , [ GameObject( 'mirror' ) ] ) ],
                         [ GamePassage( 'dark room', 'bathroom', 'N', 'S' ) ],
                         [ GameObjectAction( 'candle', 'match', 'lighting candle', GameObject('burning candle') ),
                           GameObjectAction( 'bird', 'stone', 'hitting bird', GameObject('injured bird') ) ],
                         [ GameObjectAction( 'dark room', 'burning candle', '', GameObject('light room', 'light room', [ GameObject( 'picture' ) ] ) ) ] );

   def test_take_and_drop_existing_object(self):
      name_of_existing_object = 'candle'
      object = self.game1.take( name_of_existing_object )
      assert ( not object is None )
      assert ( not self.game1.has( 'candle' ) is None )
      assert ( self.game1.is_in_room( 'candle' ) is None )
      object = self.game1.drop( name_of_existing_object )
      assert ( not object is None )
      assert ( self.game1.has( 'candle' ) is None )
      assert ( not self.game1.is_in_room( 'candle' ) is None )

   def test_trying_take_not_existing_object(self):
      name_of_not_existing_object = 'banana'
      object = self.game1.take( name_of_not_existing_object )
      assert ( object is None )
      assert ( self.game1.has( name_of_not_existing_object ) is None )

   def test_action_hit_the_bird_with_the_stone(self):
      self.game1.take( 'stone' )
      object1 = self.game1.use( 'stone', 'bird' )
      assert ( not object1 is None )
      assert ( self.game1.is_in_room( 'bird' ) is None )
      assert ( self.game1.has( 'stone' ) is None )
      assert ( not self.game1.is_in_room( 'injured bird' ) is None )
      object2 = self.game1.use( 'stone', 'bird' )
      assert ( object2 is None )

   def test_action_hit_the_bird_with_the_stone_but_both_are_in_inventory(self):
      self.game1.take( 'stone' )
      self.game1.take( 'bird' )
      object1 = self.game1.use( 'stone', 'bird' )
      assert ( not self.game1.has( 'injured bird' ) is None )

   def test_action_hit_the_bird_with_the_stone_but_use_params_are_reversed(self):
      self.game1.take( 'stone' )
      object1 = self.game1.use( 'bird', 'stone' )
      assert ( not self.game1.is_in_room( 'injured bird' ) is None )

   def test_room_goes_light_from_dark_if_we_burn_the_candle(self):
      assert ( self.game1.look() == 'dark room'  )
      assert ( self.game1.has( 'candle' ) is None )
      assert ( self.game1.has( 'match' ) is None )
      self.game1.take( 'candle' )
      self.game1.take( 'match' )
      assert ( not self.game1.has( 'candle' ) is None )
      assert ( not self.game1.has( 'match' ) is None )
      object1 = self.game1.use( 'candle', 'match' )
      assert ( not object1 is None )
      assert ( self.game1.look() == 'light room' )

   def test_moving_between_rooms_and_carrying_object(self):
      assert ( self.game1.directions() == [['N', 'bathroom']] )
      assert( not self.game1.take('candle') is None )
      self.game1.move('N')
      assert( self.game1.look() == 'bathroom' )
      assert( self.game1.take('candle') is None )
      self.game1.drop('candle')
      assert ( self.game1.directions() == [['S', 'dark room']] )
      self.game1.move('S')
      assert( self.game1.look() == 'dark room' )
      assert( self.game1.take('candle') is None )
      self.game1.move('N')
      assert( not self.game1.take('candle') is None )

   def test_recognizing_a_new_object_through_a_view_and_it_becomes_permanent(self):
      self.game1.take( 'match' )
      assert( self.game1.look() == 'dark room' )
      assert( self.game1.take( 'picture' ) is None )
      object1 = self.game1.use( 'candle', 'match' )
      assert( self.game1.look() == 'light room' )
      self.game1.take('burning candle')
      self.game1.move('N')
      self.game1.drop('burning candle')
      self.game1.move('S')
      assert( self.game1.look() == 'dark room' )
      assert( not self.game1.take( 'picture' ) is None )

if __name__ == '__main__' :
   unittest.main()

