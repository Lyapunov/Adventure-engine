import unittest

from GameObject import Game
from GameObject import GameObject
from GameObject import GameObjectAttribute
from GameObject import GameObjectUseAction
from GameObject import GamePassageRevealAction
from GameObject import GamePassage
from GameObject import GameSyntaxChecker

class ThrillerTest(unittest.TestCase):

   def setUp( self ):
      # Test game1, just to start with something
      self.game1 = Game( [ GameObject( 'dark room','dark room', [], [ GameObject( 'table', '', [GameObjectAttribute.IMMOBILE], [] ), 
                                                                      GameObject( 'candle' ),
                                                                      GameObject( 'match' ),
                                                                      GameObject( 'bird' ),
                                                                      GameObject( 'stone' ) ] ),
                           GameObject( 'bathroom', 'bathroom' , [], [ GameObject( 'cabinet', '', [GameObjectAttribute.IMMOBILE], [ GameObject( 'knife' ) ] ) ] ),
                           GameObject( 'secret room' ) ],
                         [ GamePassage( 11, 'dark room', 'bathroom'   , 'N', 'S' ),
                           GamePassage( 12, 'dark room', 'secret room', 'W', 'E',  [GameObjectAttribute.INVISIBLE] ),  ],
                         [ GameObjectUseAction( 'candle', 'match', 'lighting candle', GameObject('burning candle') ),
                           GameObjectUseAction( 'bird',   'stone', 'hitting bird',    GameObject('injured bird') ),
                           GamePassageRevealAction( 'picture', '', 'finding new passage', 12 ) ],
                         [ GameObjectUseAction( 'dark room', 'burning candle', '',
                                GameObject('light room', 'light room', [], [ GameObject( 'picture', '', [GameObjectAttribute.IMMOBILE] ) ] ) ) ],
                         'secret room' );
      assert ( self.game1.look() == 'dark room' )
      assert ( self.game1.has( 'burning candle' ) is None )
      assert ( self.game1.has( 'candle' ) is None )
      assert ( self.game1.has( 'match' )  is None )
      assert ( 'candle' in self.game1.stuffs() )
      assert ( 'match' in self.game1.stuffs() )
      assert ( 'table' in self.game1.stuffs() )
      assert ( self.game1.directions() == [['N', 'bathroom']] )
      assert ( self.game1.won() == 0 )
 
   def test_syntax_checker_wrong_game_1(self):
      # there is no room
      game_internal = Game( [], [], [], [], '' )
      assert ( GameSyntaxChecker().check( game_internal )  == 'must have at least one room' )

   def test_syntax_checker_wrong_game_2(self):
      # starting in the ending room
      game_internal = Game( [ GameObject( 'room1', 'room1', [], []) ], [], [], [], 'room1' )
      assert ( GameSyntaxChecker().check( game_internal )  == 'cannot start in the ending room' )

   def test_syntax_checker_wrong_game_3(self):
      # starting in the ending room
      game_internal = Game( [ GameObject( 'room1', 'room1', [], []) ], [], [], [], 'final room' )
      assert ( GameSyntaxChecker().check( game_internal )  == 'final room does not exist' )

   def test_syntax_checker_wrong_game_4(self):
      game_internal = Game( [ GameObject( 'starting room' ), GameObject( 'final room' ) ], [], [], [], 'final room' )
      assert ( GameSyntaxChecker().check( game_internal )  == 'final room is not reachable' )

   def test_syntax_checker_wrong_game_5(self):
      game_internal = Game( [ GameObject( 'roomA' ), GameObject( 'roomB' ),
                              GameObject( 'roomC' ), GameObject( 'roomD' ) ],
                            [ GamePassage(11, 'roomA', 'roomB', 'N', 'S' ),
                              GamePassage(12, 'roomC', 'roomD', 'N', 'S' ) ],
                            [], [], 'roomD' )
      assert ( GameSyntaxChecker().check( game_internal )  == 'final room is not reachable' )

   def test_syntax_checker_wrong_game_6(self):
      game_internal = Game( [ GameObject( 'roomA' ), GameObject( 'roomB' ),
                              GameObject( 'roomC' ), GameObject( 'roomD' ) ],
                            [ GamePassage(11, 'roomA', 'roomB', 'N', 'S' ),
                              GamePassage(12, 'roomB', 'roomC', 'N', 'S' ) ],
                            [], [], 'roomD' )
      assert ( GameSyntaxChecker().check( game_internal )  == 'final room is not reachable' )

   def test_syntax_checker_wrong_game_7(self):
      game_internal = Game( [ GameObject( 'roomA' ), GameObject( 'roomB' ),
                              GameObject( 'roomC' ), GameObject( 'roomD' ),
                              GameObject( 'roomE' ), GameObject( 'roomF' ) ],
                            [ GamePassage(11, 'roomA', 'roomB', 'N', 'S' ),
                              GamePassage(12, 'roomA', 'roomE', 'E', 'W' ),
                              GamePassage(13, 'roomE', 'roomB', 'N', 'E' ),
                              GamePassage(14, 'roomD', 'roomE', 'N', 'S' ),
                              GamePassage(15, 'roomC', 'roomF', 'E', 'W' ) ],
                            [], [], 'roomF' )
      assert ( GameSyntaxChecker().check( game_internal )  == 'final room is not reachable' )

   def test_syntax_checker_wrong_game_8(self):
      game_internal = Game( [ GameObject( 'roomA' ), GameObject( 'roomB' ) ],
                            [ GamePassage(11, 'roomA', 'roomB', 'N', 'S' ),
                              GamePassage(12, 'roomA', 'roomB', 'W', 'S' ) ], [], [], 'roomB' )
      assert ( GameSyntaxChecker().check( game_internal )  == 'multiple passages between the same rooms' )

   def test_syntax_checker_wrong_game_9(self):
      game_internal = Game( [ GameObject( 'roomA' ), GameObject( 'roomB' ) ],
                            [ GamePassage(11, 'roomA', 'roomB', 'N', 'S' ),
                              GamePassage(12, 'roomB', 'roomA', 'W', 'S' ) ], [], [], 'roomB' )
      assert ( GameSyntaxChecker().check( game_internal )  == 'multiple passages between the same rooms' )

   def test_syntax_checker_wrong_game_10(self):
      game_internal = Game( [ GameObject( 'roomA' ), GameObject( 'roomB' ), GameObject( 'roomC' ) ],
                            [ GamePassage(11, 'roomA', 'roomB', 'N', 'S' ),
                              GamePassage(11, 'roomB', 'roomC', 'W', 'S' ) ], [], [], 'roomC' )
      assert ( GameSyntaxChecker().check( game_internal )  == 'passage identifiers are not unique' )

   def test_syntax_checker_wrong_game_11(self):
      game_internal = Game( [ GameObject( 'roomA' ), GameObject( 'roomB' ),
                              GameObject( 'roomC' ), GameObject( 'roomD' ) ],
                            [ GamePassage(11, 'roomA', 'roomB', 'N', 'S' ),
                              GamePassage(12, 'roomC', 'roomD', 'N', 'S' ) ],
                            [], [], 'roomB' )
      assert ( GameSyntaxChecker().check( game_internal )  == 'not all rooms are accessible' )
 
   def test_syntax_checker_wrong_game_12(self):
      game_internal = Game( [ GameObject( 'roomA','roomA', [], [ GameObject( 'button', '', [GameObjectAttribute.IMMOBILE], [] ) ] ),
                              GameObject( 'roomB' ) ],
                            [ GamePassage(11, 'roomA', 'roomB', 'N', 'S', [GameObjectAttribute.INVISIBLE] ) ],
                            [ GamePassageRevealAction( 'button', '', 'opening door', 13 ) ],
                            [],
                            'roomB' )
      assert ( GameSyntaxChecker().check( game_internal )  == 'invalid passage identifiers in an action' )

   def test_syntax_checker_wrong_game_13(self):
      game_internal = Game( [ GameObject( 'roomA','roomA', [], [ GameObject( 'button1', '', [GameObjectAttribute.IMMOBILE], [] ),
                                                                 GameObject( 'button2', '', [GameObjectAttribute.IMMOBILE], [] ) ] ),
                              GameObject( 'roomB' ) ],
                            [ GamePassage(11, 'roomA', 'roomB', 'N', 'S', [GameObjectAttribute.INVISIBLE] ) ],
                            [ GamePassageRevealAction( 'button', '', 'opening door', 11 ) ],
                            [],
                            'roomB' )
      verdict = GameSyntaxChecker().check( game_internal )
      assert ( verdict  == 'found invalid object in an action' )

   def test_syntax_checker_wrong_game_14(self):
      game_internal = Game( [ GameObject( 'roomA','roomA', [], [ GameObject( 'button1', '', [GameObjectAttribute.IMMOBILE], [] ),
                                                                 GameObject( 'button1', '', [GameObjectAttribute.IMMOBILE], [] ) ] ),
                              GameObject( 'roomB' ) ],
                            [ GamePassage(11, 'roomA', 'roomB', 'N', 'S', [GameObjectAttribute.INVISIBLE] ) ],
                            [ GamePassageRevealAction( 'button1', '', 'opening door', 11 ) ],
                            [],
                            'roomB' )
      verdict = GameSyntaxChecker().check( game_internal )
      assert ( verdict  == 'found two objects with the same name' )

   def test_syntax_checker_wrong_game_15(self):
      game_internal = Game( [ GameObject( 'roomA' ), GameObject( 'roomC' ),
                              GameObject( 'roomB' ), GameObject( 'roomC' ) ],
                            [ GamePassage(11, 'roomA', 'roomB', 'N', 'S' ),
                              GamePassage(12, 'roomB', 'roomC', 'N', 'S' ) ],
                            [], [], 'roomC' )
      verdict = GameSyntaxChecker().check( game_internal )
      assert ( verdict  == 'found two objects with the same name' )

   def test_syntax_checker_wrong_game16(self):
      # Minimal game 2: there is a closed door, if you touch it, it opens and you can go through the passage and you win .. 
      game_internal = Game( [ GameObject( 'starting room', '', [], [ GameObject( 'door', '', [GameObjectAttribute.IMMOBILE] ) ] ),
                              GameObject( 'ending room' ) ],
                            [ GamePassage( 11, 'starting room', 'ending room' , 'N', 'S',  [GameObjectAttribute.INVISIBLE] ) ],
                            [ GamePassageRevealAction( '', '', 'opening door', 11 ) ],
                            [],
                            'ending room')
      verdict = GameSyntaxChecker().check( game_internal )
      assert ( verdict  == 'found an action without actors' )

   def test_syntax_checker_wrong_game17(self):
      # Minimal game 2: there is a closed door, if you touch it, it opens and you can go through the passage and you win .. 
      game_internal = Game( [ GameObject( 'starting room', '', [], [ GameObject( 'door', '', [GameObjectAttribute.IMMOBILE] ) ] ),
                              GameObject( 'ending room' ) ],
                            [ GamePassage( 11, 'starting room', 'ending room' , 'N', 'S',  [GameObjectAttribute.INVISIBLE] ) ],
                            [ GamePassageRevealAction( 'door', 'door', 'opening door', 11 ) ],
                            [],
                            'ending room')
      verdict = GameSyntaxChecker().check( game_internal )
      assert ( verdict  == 'found invalid action with the same actor twice' )

   def test_syntax_checker_wrong_game_18(self):
      game_internal = Game( [ GameObject( 'roomA','roomA', [], [ GameObject( 'button1', '', [GameObjectAttribute.IMMOBILE], [] ),
                                                                 GameObject( 'button2', '', [GameObjectAttribute.IMMOBILE], [] ) ] ),
                              GameObject( 'roomB' ) ],
                            [ GamePassage(11, 'roomA', 'roomB', 'N', 'S', [GameObjectAttribute.INVISIBLE] ) ],
                            [ GamePassageRevealAction( 'button1', '', 'opening door', 11 ),
                              GamePassageRevealAction( 'button1', '', 'opening door', 11 ) ],
                            [],
                            'roomB' )
      verdict = GameSyntaxChecker().check( game_internal )
      assert ( verdict  == 'found multiple actions on the same two actors' )

   def test_syntax_checker_wrong_game_19(self):
      game_internal = Game( [ GameObject( 'roomA','roomA', [], [ GameObject( 'button1', '', [GameObjectAttribute.IMMOBILE], [] ),
                                                                 GameObject( 'button2', '', [GameObjectAttribute.IMMOBILE], [] ) ] ),
                              GameObject( 'roomB' ) ],
                            [ GamePassage(11, 'roomA', 'roomB', 'N', 'S', [GameObjectAttribute.INVISIBLE] ) ],
                            [ GamePassageRevealAction( 'button1', '', 'opening door', 11 ),
                              GamePassageRevealAction( '', 'button1', 'hacking door', 11 ) ],
                            [],
                            'roomB' )
      verdict = GameSyntaxChecker().check( game_internal )
      assert ( verdict  == 'found multiple actions on the same two actors' )

   def test_syntax_checker_good_game1(self):
      # minimal valid game
      game_internal = Game( [ GameObject( 'starting room' ), GameObject( 'final room' ) ],
                            [ GamePassage( 11, 'starting room', 'final room', 'N', 'S' ) ], [], [], 'final room' )
      assert ( GameSyntaxChecker().check( game_internal )  == '' )

   def test_syntax_checker_good_game2(self):
      # Minimal game 2: there is a closed door, if you touch it, it opens and you can go through the passage and you win .. 
      game_internal = Game( [ GameObject( 'starting room', '', [], [ GameObject( 'door', '', [GameObjectAttribute.IMMOBILE] ) ] ),
                              GameObject( 'ending room' ) ],
                            [ GamePassage( 11, 'starting room', 'ending room' , 'N', 'S',  [GameObjectAttribute.INVISIBLE] ) ],
                            [ GamePassageRevealAction( 'door', '', 'opening door', 11 ) ],
                            [],
                            'ending room')
      verdict = GameSyntaxChecker().check( game_internal )
      assert ( verdict  == '' )


   def test_syntax_checker_good_game_3(self):
      # testing whether final room is accessible
      game_internal = Game( [ GameObject( 'roomA' ), GameObject( 'roomB' ),
                              GameObject( 'roomC' ), GameObject( 'roomD' ),
                              GameObject( 'roomE' ), GameObject( 'roomF' ) ],
                            [ GamePassage(11, 'roomA', 'roomB', 'N', 'S' ),
                              GamePassage(12, 'roomA', 'roomE', 'E', 'W' ),
                              GamePassage(13, 'roomD', 'roomC', 'E', 'W' ),
                              GamePassage(14, 'roomE', 'roomB', 'N', 'E' ),
                              GamePassage(15, 'roomD', 'roomE', 'N', 'S' ),
                              GamePassage(16, 'roomC', 'roomF', 'E', 'W' ) ],
                            [],
                            [],
                            'roomF' )
      assert ( GameSyntaxChecker().check( game_internal )  == '' )

   def test_take_and_drop_existing_object(self):
      subject = self.game1.take( 'candle' )
      assert ( not subject is None )
      assert ( not self.game1.has( 'candle' ) is None )
      assert ( not 'candle' in self.game1.stuffs() )

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
      assert ( not 'bird' in self.game1.stuffs() )
      assert ( self.game1.has( 'stone' ) is None )
      assert ( 'injured bird' in self.game1.stuffs() )

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
      assert ( 'injured bird' in self.game1.stuffs() )

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
      assert( not 'candle' in self.game1.stuffs() )

   def test_recognizing_a_new_object_through_a_view_and_it_becomes_permanent(self):
      self.game1.take( 'match' )
      object1 = self.game1.use( 'candle', 'match' )
      self.game1.take('burning candle')
      assert( self.game1.look() == 'light room' )

      self.game1.move('N')
      self.game1.drop('burning candle')
      self.game1.move('S')
      assert( self.game1.look() == 'dark room' )
      assert( 'picture' in self.game1.stuffs() )

   def test_finding_a_new_passage(self):
      self.test_recognizing_a_new_object_through_a_view_and_it_becomes_permanent()
      assert( 'picture' in self.game1.stuffs() )

      self.game1.use('picture')
      assert ( self.game1.directions() == [['N', 'bathroom'], ['W', 'secret room']] )

   def test_winning_the_game(self):
      self.test_finding_a_new_passage()     
      self.game1.move('W')
      assert ( self.game1.won() == 1 )

if __name__ == '__main__' :
   unittest.main()

