import unittest

from GameObject import Game
from GameObject import GameObject
from GameObject import GameObjectAttribute
from GameObject import GameObjectUseAction
from GameObject import GamePassageRevealAction
from GameObject import GamePassage

class ThrillerTest(unittest.TestCase):
   def setUp( self ):
      self.game1 = Game( [ GameObject( 'dark room','dark room', [], [ GameObject( 'table', '', [GameObjectAttribute.IMMOBILE], [] ), 
                                                                      GameObject( 'candle' ),
                                                                      GameObject( 'match' ),
                                                                      GameObject( 'bird' ),
                                                                      GameObject( 'stone' ) ] ),
                           GameObject( 'bathroom', 'bathroom' , [], [ GameObject( 'cabinet', '', [GameObjectAttribute.IMMOBILE], [ GameObject( 'knife' ) ] ) ] ) ],
                         [ GamePassage( 'dark room', 'bathroom', 'N', 'S' ),
                           GamePassage( 'dark room', 'secret room', 'W', 'E',  [GameObjectAttribute.INVISIBLE] ),  ],
                         [ GameObjectUseAction( 'candle',    'match',          'lighting candle',     GameObject('burning candle') ),
                           GameObjectUseAction( 'bird',      'stone',          'hitting bird',        GameObject('injured bird') ),
                           GamePassageRevealAction( 'picture', '', 'finding new passage', 'dark room', 'W' ) ],
                         [ GameObjectUseAction( 'dark room', 'burning candle', '',                    GameObject('light room', 'light room', [], [ GameObject( 'picture', '', [GameObjectAttribute.IMMOBILE] ) ] ) ) ] );
      assert ( self.game1.look() == 'dark room' )
      assert ( self.game1.has( 'burning candle' ) is None )
      assert ( self.game1.has( 'candle' ) is None )
      assert ( self.game1.has( 'match' )  is None )
      assert ( self.game1.is_in_room( 'picture' ) is None )
      assert ( not self.game1.is_in_room( 'candle' ) is None )
      assert ( not self.game1.is_in_room( 'match' ) is None )
      assert ( not self.game1.is_in_room( 'table' ) is None )
      assert ( self.game1.directions() == [['N', 'bathroom']] )
      assert ( self.game1.won() == 0 )

   def test_take_and_drop_existing_object(self):
      subject = self.game1.take( 'candle' )
      assert ( not subject is None )
      assert ( not self.game1.has( 'candle' ) is None )
      assert ( self.game1.is_in_room( 'candle' ) is None )

      subject = self.game1.drop( 'candle' )
      assert ( not subject is None )
      assert ( self.game1.has( 'candle' ) is None )

   def test_trying_take_not_existing_object(self):
      subject = self.game1.take( 'banana' )
      assert ( subject is None )
      assert ( self.game1.has( 'banana' ) is None )

   def test_trying_take_immobile_object(self):
      subject = self.game1.take( 'table' )
      assert ( subject is None )
      assert ( self.game1.has( 'table' ) is None )

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

   def test_room_goes_light_from_dark_if_we_burn_the_candle_first(self):
      self.game1.take( 'match' )
      assert ( not self.game1.has( 'match' )  is None )

      object1 = self.game1.use( 'candle', 'match' )
      assert ( self.game1.has( 'match' ) is None )

      self.game1.take('burning candle')
      assert ( not self.game1.has( 'burning candle' ) is None )
      assert ( self.game1.look() == 'light room' )

   def test_room_goes_light_from_dark_if_we_burn_the_candle_second(self):
      self.game1.take( 'candle' )
      self.game1.take( 'match' )
      assert ( not self.game1.has( 'candle' ) is None )
      assert ( not self.game1.has( 'match' )  is None )

      object1 = self.game1.use( 'candle', 'match' )
      assert ( not object1 is None )
      assert ( not self.game1.has( 'burning candle' ) is None )
      assert ( self.game1.look() == 'light room' )

   def test_moving_between_rooms(self):
      self.game1.move('N')
      assert( self.game1.look() == 'bathroom' )
      assert ( self.game1.directions() == [['S', 'dark room']] )

      self.game1.move('S')
      assert( self.game1.look() == 'dark room' )

   def test_moving_between_rooms_and_carrying_object(self):
      subject = self.game1.take('candle')
      self.game1.move('N')
      self.game1.drop('candle')
      self.game1.move('S')
      assert( self.game1.look() == 'dark room' )
      assert( self.game1.is_in_room('candle') is None )

   def test_recognizing_a_new_object_through_a_view_and_it_becomes_permanent(self):
      self.game1.take( 'match' )
      object1 = self.game1.use( 'candle', 'match' )
      self.game1.take('burning candle')
      assert( self.game1.look() == 'light room' )

      self.game1.move('N')
      self.game1.drop('burning candle')
      self.game1.move('S')
      assert( self.game1.look() == 'dark room' )
      assert( not self.game1.is_in_room( 'picture' ) is None )

   def test_finding_a_new_passage(self):
      self.test_recognizing_a_new_object_through_a_view_and_it_becomes_permanent()
      assert( not self.game1.is_in_room( 'picture' ) is None )

      self.game1.take('picture')
      assert ( self.game1.directions() == [['N', 'bathroom'], ['W', 'secret room']] )

if __name__ == '__main__' :
   unittest.main()

