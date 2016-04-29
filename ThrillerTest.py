import unittest

from GameObject import Game
from GameObject import GameObject
from GameObject import GameObjectAttribute
from GameObject import GameObjectUseAction
from GameObject import GameObjectRevealAction
from GameObject import GamePassageRevealAction
from GameObject import GamePassage
from GameObject import GameSyntaxChecker
from GameObject import GameSolver

class ThrillerTest(unittest.TestCase):

   # TODO: (IDEA) descriptions and images, the entire view should be a completely separated layer,
   #       which just portrays the game objects according to their attributes

   def setUp( self ):
      # Test game1, just to start with something
      self.game1 = Game( [ GameObject( 'dark room','dark room', [], [ GameObject( 'table',   '', [GameObjectAttribute.IMMOBILE], [] ), 
                                                                      GameObject( 'candle' ),
                                                                      GameObject( 'match' ),
                                                                      GameObject( 'bird' ),
                                                                      GameObject( 'stone' ),
                                                                      GameObject( 'picture', '', [GameObjectAttribute.IMMOBILE, GameObjectAttribute.INVISIBLE] ) ] ),
                           GameObject( 'bathroom', 'bathroom' , [], [ GameObject( 'cabinet', '', [GameObjectAttribute.IMMOBILE], [ GameObject( 'knife' ) ] ) ] ),
                           GameObject( 'secret room' ) ],
                         [ GamePassage( 11, 'dark room', 'bathroom'   , 'N', 'S' ),
                           GamePassage( 12, 'dark room', 'secret room', 'W', 'E',  [GameObjectAttribute.INVISIBLE] ),  ],
                         [ GameObjectUseAction( 'candle', 'match', 'lighting candle', GameObject('burning candle') ),
                           GameObjectUseAction( 'bird',   'stone', 'hitting bird',    GameObject('injured bird') ),
                           GamePassageRevealAction( 'picture', '',               'finding new passage'          , 12 ) ],
                         [ GameObjectRevealAction(  'picture', 'burning candle', 'the light reveals the picture' ) ],
                         'secret room' );
      assert ( self.game1.look() == 'dark room' )
      assert ( self.game1.has( 'burning candle' ) is None )
      assert ( self.game1.has( 'candle' ) is None )
      assert ( self.game1.has( 'match' )  is None )
      assert ( 'candle' in self.game1.stuffs() )
      assert ( 'match' in self.game1.stuffs() )
      assert ( 'table' in self.game1.stuffs() )
      assert ( not 'picture' in self.game1.stuffs() )
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
      assert ( verdict  == 'found multiple actions for the same actor' )

   def test_syntax_checker_wrong_game_19(self):
      game_internal = Game( [ GameObject( 'roomA','roomA', [], [ GameObject( 'button1', '', [GameObjectAttribute.IMMOBILE], [] ),
                                                                 GameObject( 'button2', '', [GameObjectAttribute.IMMOBILE], [] ) ] ),
                              GameObject( 'roomB' ) ],
                            [ GamePassage(11, 'roomA', 'roomB', 'N', 'S', [GameObjectAttribute.INVISIBLE] ) ],
                            [ GamePassageRevealAction( 'button1', '', 'opening door', 11 ),
                              GameObjectUseAction( '', 'button1', 'breaking button', GameObject( 'broken button' ) ) ],
                            [],
                            'roomB' )
      verdict = GameSyntaxChecker().check( game_internal )
      assert ( verdict  == 'found multiple actions for the same actor' )

   def test_syntax_checker_wrong_game_20(self):
      game_internal = Game( [ GameObject( 'roomA','roomA', [], [ GameObject( 'handle1', '', [GameObjectAttribute.IMMOBILE], [] ),
                                                                 GameObject( 'handle2', '', [GameObjectAttribute.IMMOBILE], [] ),
                                                                 GameObject( 'crowbar' ) ] ),
                              GameObject( 'roomB' ) ],
                            [ GamePassage(11, 'roomA', 'roomB', 'N', 'S', [GameObjectAttribute.INVISIBLE] ) ],
                            [ GamePassageRevealAction( 'handle1', 'crowbar', 'opening door', 11 ),
                              GameObjectUseAction( 'handle2', 'crowbar', 'breaking handle', GameObject( 'broken handle' ) ) ],
                            [],
                            'roomB' )
      verdict = GameSyntaxChecker().check( game_internal )
      assert ( verdict  == 'found multiple actions for the same actor' )

   def test_syntax_checker_wrong_game_21(self):
      game_internal = Game( [ GameObject( 'roomA','roomA', [], [ GameObject( 'handle1', '', [GameObjectAttribute.IMMOBILE], [] ),
                                                                 GameObject( 'handle2', '', [GameObjectAttribute.IMMOBILE], [] ),
                                                                 GameObject( 'crowbar' ) ] ),
                              GameObject( 'roomB' ) ],
                            [ GamePassage(11, 'roomA', 'roomB', 'N', 'S', [GameObjectAttribute.INVISIBLE] ) ],
                            [ GamePassageRevealAction( 'handle1', 'crowbar', 'opening door', 11 ),
                              GameObjectUseAction( 'handle2', 'crowbar', 'breaking handle', GameObject( 'handle1' ) ) ],
                            [],
                            'roomB' )
      verdict = GameSyntaxChecker().check( game_internal )
      assert ( verdict  == 'found two objects with the same name' )

   def test_syntax_checker_wrong_game22(self):
      # Minimal game 2: there is a closed door, if you touch it, it opens and you can go through the passage and you win .. 
      game_internal = Game( [ GameObject( 'starting room', '', [], [ GameObject( 'door', '', [GameObjectAttribute.IMMOBILE] ),
                                                                     GameObject( 'box',  '', [GameObjectAttribute.IMMOBILE], 
                                                                        [GameObject( 'key', '', [GameObjectAttribute.IMMOBILE] ) ] ) ] ),
                              GameObject( 'ending room' ) ],
                            [ GamePassage( 11, 'starting room', 'ending room' , 'N', 'S',  [GameObjectAttribute.INVISIBLE] ) ],
                            [ GamePassageRevealAction( 'door', 'key', 'opening door', 11 ) ],
                            [],
                            'ending room')
      verdict = GameSyntaxChecker().check( game_internal )
      assert ( verdict  == 'not top level stuffs cannot have attributes' )

   def test_syntax_checker_wrong_game23(self):
      # Minimal game 2: there is a closed door, if you touch it, it opens and you can go through the passage and you win .. 
      game_internal = Game( [ GameObject( 'starting room', '', [], [ GameObject( 'door', '', [GameObjectAttribute.IMMOBILE] ),
                                                                     GameObject( 'keypart1' ),
                                                                     GameObject( 'box',  '', [GameObjectAttribute.IMMOBILE], [GameObject( 'keypart2' ) ] ) ] ),
                              GameObject( 'ending room' ) ],
                            [ GamePassage( 11, 'starting room', 'ending room' , 'N', 'S',  [GameObjectAttribute.INVISIBLE] ) ],
                            [ GamePassageRevealAction( 'door', 'key', 'opening door', 11 ),
                              GameObjectUseAction( 'keypart1', 'keypart2', '', GameObject( 'key', '', [GameObjectAttribute.INVISIBLE] ) ) ],
                            [],
                            'ending room')
      verdict = GameSyntaxChecker().check( game_internal )
      assert ( verdict  == 'not top level stuffs cannot have attributes' )

   def test_syntax_checker_wrong_game24(self):
      game_internal = Game( [ GameObject( 'starting room', '', [], [ GameObject( 'key', '', [GameObjectAttribute.INVISIBLE] ) ] ),
                              GameObject( 'middle room'  , '', [], [ GameObject( 'burning candle' ),
                                                                     GameObject( 'door', '', [GameObjectAttribute.IMMOBILE] ) ] ),
                              GameObject( 'ending room' ) ],
                            [ GamePassage( 11, 'middle room',   'ending room' , 'N', 'S',  [GameObjectAttribute.INVISIBLE] ),
                              GamePassage( 12, 'starting room', 'middle room' , 'N', 'S' ) ],
                            [ GamePassageRevealAction( 'door', 'key',           'opening door', 11 ) ],
                            [ GameObjectRevealAction( 'burning candle', 'key',  'finding a key') ],
                            'ending room')
      verdict = GameSyntaxChecker().check( game_internal )
      assert ( verdict  == 'subjects of revealing actions must be invisible initially' )

   def test_syntax_checker_wrong_game25(self):
      # Minimal game: there is a closed door, if you touch it, it opens and you can go through the passage and you win .. 
      game_internal = Game( [ GameObject( 'starting room', '', [], [ GameObject( 'door', '', [GameObjectAttribute.IMMOBILE] ),
                                                                     GameObject( 'key' , '', [GameObjectAttribute.IMMOBILE] ) ] ),
                              GameObject( 'ending room' ) ],
                            [ GamePassage( 11, 'starting room', 'ending room' , 'N', 'S',  [GameObjectAttribute.INVISIBLE] ) ],
                            [ GamePassageRevealAction( 'door', 'key', 'opening door', 11 ) ],
                            [],
                            'ending room')
      verdict = GameSyntaxChecker().check( game_internal )
      assert ( verdict  == "at least one of the action's actors must be mobile" )

   def test_syntax_checker_wrong_game26(self):
      game_internal = Game( [ GameObject( 'starting room', '', [], [ GameObject( 'door', '', [GameObjectAttribute.IMMOBILE, GameObjectAttribute.INVISIBLE] ),
                                                                     GameObject( 'key' ) ] ),
                              GameObject( 'ending room' ) ],
                            [ GamePassage( 11, 'starting room', 'ending room' , 'N', 'S',  [GameObjectAttribute.INVISIBLE] ) ],
                            [ GamePassageRevealAction( 'door', 'key', 'opening door', 11 ) ],
                            [],
                            'ending room')
      verdict = GameSyntaxChecker().check( game_internal )
      assert ( verdict  == 'there must be exactly one action for each invisible object which reveals it' )

   def test_syntax_checker_good_game1(self):
      # minimal valid game
      game_internal = Game( [ GameObject( 'starting room' ), GameObject( 'final room' ) ],
                            [ GamePassage( 11, 'starting room', 'final room', 'N', 'S' ) ], [], [], 'final room' )
      assert ( GameSyntaxChecker().check( game_internal )  == '' )
      assert ( GameSolver().solve( game_internal )  == [ [ 'go', 'N' ] ] )


   def test_syntax_checker_good_game_2(self):
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
      assert ( GameSolver().solve( game_internal )  == [ [ 'go', 'N' ], [ 'go', 'E' ], [ 'go', 'S' ], [ 'go', 'E' ], [ 'go', 'E' ] ] )

   def test_syntax_checker_good_game3(self):
      # Minimal game: there is a closed door, if you touch it, it opens and you can go through the passage and you win .. 
      game_internal = Game( [ GameObject( 'starting room', '', [], [ GameObject( 'door', '', [GameObjectAttribute.IMMOBILE] ) ] ),
                              GameObject( 'ending room' ) ],
                            [ GamePassage( 11, 'starting room', 'ending room' , 'N', 'S',  [GameObjectAttribute.INVISIBLE] ) ],
                            [ GamePassageRevealAction( 'door', '', 'opening door', 11 ) ],
                            [],
                            'ending room')
      verdict = GameSyntaxChecker().check( game_internal )
      assert ( verdict  == '' )
      assert ( GameSolver().solve( game_internal ) == [['use', '', 'door'], ['go', 'N']] )

   def test_syntax_checker_good_game4(self):
      # Minimal game: there is a closed door, if you touch it, it opens and you can go through the passage and you win .. 
      game_internal = Game( [ GameObject( 'starting room', '', [], [ GameObject( 'door', '', [GameObjectAttribute.IMMOBILE] ),
                                                                     GameObject( 'key' ) ] ),
                              GameObject( 'ending room' ) ],
                            [ GamePassage( 11, 'starting room', 'ending room' , 'N', 'S',  [GameObjectAttribute.INVISIBLE] ) ],
                            [ GamePassageRevealAction( 'door', 'key', 'opening door', 11 ) ],
                            [],
                            'ending room')
      verdict = GameSyntaxChecker().check( game_internal )
      assert ( verdict  == '' )
      assert ( GameSolver().solve( game_internal ) == [['take', 'key'], ['use', 'door', 'key'], ['go', 'N']] )

   def test_syntax_checker_good_game5(self):
      # Minimal game: there is a closed door, if you touch it, it opens and you can go through the passage and you win .. 
      game_internal = Game( [ GameObject( 'starting room', '', [], [ GameObject( 'door', '', [GameObjectAttribute.IMMOBILE] ),
                                                                     GameObject( 'box',  '', [GameObjectAttribute.IMMOBILE], [GameObject( 'key' ) ] ) ] ),
                              GameObject( 'ending room' ) ],
                            [ GamePassage( 11, 'starting room', 'ending room' , 'N', 'S',  [GameObjectAttribute.INVISIBLE] ) ],
                            [ GamePassageRevealAction( 'door', 'key', 'opening door', 11 ) ],
                            [],
                            'ending room')
      verdict = GameSyntaxChecker().check( game_internal )
      assert ( verdict  == '' )
      solution = GameSolver().solve( game_internal )
      assert ( solution == [['open', 'box'], ['take', 'key'], ['use', 'door', 'key'], ['go', 'N']] )

   def test_syntax_checker_good_game6(self):
      # Minimal game: there is a closed door, if you touch it, it opens and you can go through the passage and you win .. 
      game_internal = Game( [ GameObject( 'starting room' ),
                              GameObject( 'middle room', '', [], [ GameObject( 'door', '', [GameObjectAttribute.IMMOBILE] ),
                                                                   GameObject( 'box',  '', [GameObjectAttribute.IMMOBILE], [GameObject( 'key' ) ] ) ] ),
                              GameObject( 'ending room' ) ],
                            [ GamePassage( 11, 'middle room',   'ending room' , 'N', 'S',  [GameObjectAttribute.INVISIBLE] ),
                              GamePassage( 12, 'starting room', 'middle room' , 'N', 'S' ) ],
                            [ GamePassageRevealAction( 'door', 'key', 'opening door', 11 ) ],
                            [],
                            'ending room')
      verdict = GameSyntaxChecker().check( game_internal )
      assert ( verdict  == '' )
      solution = GameSolver().solve( game_internal )
      assert ( solution == [['go', 'N'],['open', 'box'], ['take', 'key'], ['use', 'door', 'key'], ['go', 'N']] )

   def test_syntax_checker_good_game7(self):
      game_internal = Game( [ GameObject( 'starting room', '', [], [ GameObject( 'key', '', [GameObjectAttribute.INVISIBLE] ) ] ),
                              GameObject( 'middle room'  , '', [], [ GameObject( 'door', '', [GameObjectAttribute.IMMOBILE] ),
                                                                     GameObject( 'box',  '', [GameObjectAttribute.IMMOBILE], [GameObject( 'burning candle' ) ] ) ] ),
                              GameObject( 'ending room' ) ],
                            [ GamePassage( 11, 'middle room',   'ending room' , 'N', 'S',  [GameObjectAttribute.INVISIBLE] ),
                              GamePassage( 12, 'starting room', 'middle room' , 'N', 'S' ) ],
                            [ GamePassageRevealAction( 'door', 'key',            'opening door', 11 ) ],
                            [ GameObjectRevealAction(  'key',  'burning candle', 'finding a key') ],
                            'ending room')
      verdict = GameSyntaxChecker().check( game_internal )
      assert ( verdict  == '' )
      solution = GameSolver().solve( game_internal )

   def test_take_and_drop_existing_object(self):
      subject = self.game1.do_it( 'take',  'candle' )
      assert ( not subject is None )
      assert ( not self.game1.has( 'candle' ) is None )
      assert ( not 'candle' in self.game1.stuffs() )

      subject = self.game1.do_it( 'drop',  'candle' )
      assert ( not subject is None )
      assert ( self.game1.has( 'candle' ) is None )

   def test_trying_take_not_existing_object(self):
      subject = self.game1.do_it( 'take',  'banana' )
      assert ( subject is None )
      assert ( self.game1.has( 'banana' ) is None )

   def test_trying_take_immobile_object(self):
      subject = self.game1.do_it( 'take',  'table' )
      assert ( subject is None )
      assert ( self.game1.has( 'table' ) is None )

   def test_action_hit_the_bird_with_the_stone(self):
      self.game1.do_it( 'take',  'stone' )
      object1 = self.game1.do_it( 'use', 'stone', 'bird' )
      assert ( not object1 is None )
      assert ( not 'bird' in self.game1.stuffs() )
      assert ( self.game1.has( 'stone' ) is None )
      assert ( 'injured bird' in self.game1.stuffs() )

      object2 = self.game1.do_it( 'use', 'stone', 'bird' )
      assert ( object2 is None )

   def test_action_hit_the_bird_with_the_stone_but_both_are_in_inventory(self):
      self.game1.do_it( 'take', 'stone' )
      self.game1.do_it( 'take', 'bird' )
      object1 = self.game1.do_it( 'use', 'stone', 'bird' )
      assert ( not self.game1.has( 'injured bird' ) is None )

   def test_action_hit_the_bird_with_the_stone_but_use_params_are_reversed(self):
      self.game1.do_it( 'take', 'stone' )
      self.game1.do_it( 'use',  'bird', 'stone' )
      assert ( 'injured bird' in self.game1.stuffs() )

   def test_room_goes_light_from_dark_if_we_burn_the_candle_without_taking_it_first(self):
      self.game1.do_it( 'take', 'match' )
      self.game1.do_it( 'use',  'candle', 'match' )

      # Note: the look triggers the appearance of the revealed object! TODO: making it automatic after use
      assert( not 'candle' in self.game1.stuffs() )
      assert( 'burning candle' in self.game1.stuffs() )
      assert( 'picture' in self.game1.stuffs() )

   def test_room_goes_light_from_dark_if_we_burn_the_candle_with_taking_it_first(self):
      self.game1.do_it( 'take', 'candle' )
      self.game1.do_it( 'take', 'match' )
      self.game1.do_it( 'use',  'candle', 'match' )

      assert ( not self.game1.has( 'burning candle' ) is None )
      assert( 'picture' in self.game1.stuffs() )

   def test_moving_between_rooms(self):
      self.game1.do_it( 'go', 'N')
      assert( self.game1.look() == 'bathroom' )
      assert ( self.game1.directions() == [['S', 'dark room']] )

      self.game1.do_it( 'go', 'S')
      assert( self.game1.look() == 'dark room' )

   def test_opening_objects(self):
      self.game1.do_it( 'go', 'N')
      assert( not 'knife' in self.game1.stuffs() )
      assert ( self.game1.do_it( 'open',  'cabinet' ) )
      assert( 'knife' in self.game1.stuffs() )

   def test_moving_between_rooms_and_carrying_object(self):
      subject = self.game1.do_it( 'take', 'candle')
      self.game1.do_it( 'go', 'N')
      self.game1.do_it( 'drop', 'candle')
      self.game1.do_it( 'go', 'S')
      assert( self.game1.look() == 'dark room' )
      assert( not 'candle' in self.game1.stuffs() )

   def test_recognizing_a_new_object_through_a_view_and_it_becomes_permanent(self):
      self.game1.do_it( 'take',  'match' )
      object1 = self.game1.do_it( 'use', 'candle', 'match' )
      self.game1.do_it( 'take', 'burning candle')
      self.game1.do_it( 'go', 'N')
      self.game1.do_it( 'drop', 'burning candle')
      self.game1.do_it( 'go', 'S')
      assert( self.game1.look() == 'dark room' )
      assert( 'picture' in self.game1.stuffs() )

   def test_finding_a_new_passage(self):
      self.test_recognizing_a_new_object_through_a_view_and_it_becomes_permanent()
      assert( 'picture' in self.game1.stuffs() )

      self.game1.do_it( 'use','picture')
      assert ( self.game1.directions() == [['N', 'bathroom'], ['W', 'secret room']] )

   def test_winning_the_game(self):
      self.test_finding_a_new_passage()     
      self.game1.do_it( 'go', 'W')
      assert ( self.game1.won() == 1 )

   def test_solver_on_full_game(self):
      verdict = GameSyntaxChecker().check( self.game1 )
      assert ( verdict  == '' )
      solution = GameSolver().solve( self.game1 )
      assert ( solution == [ ['take', 'candle'], ['take', 'match'], ['take', 'bird'], ['take', 'stone'], ['use', 'candle', 'match'],
                             ['use', 'bird', 'stone'], ['use', '', 'picture'], ['go', 'W']] )

   # TODO: GameObjectRevealAction, mobile, immobile, possible at all?

if __name__ == '__main__' :
   unittest.main()

