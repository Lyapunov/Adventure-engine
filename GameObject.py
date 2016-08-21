import copy
import sys
import json

# http://stackoverflow.com/questions/390250/elegant-ways-to-support-equivalence-equality-in-python-classes
class CommonEquality(object):

   def __eq__(self, other):
      return (isinstance(other, self.__class__) and self.__dict__ == other.__dict__)

   def __ne__(self, other):
      return not self.__eq__(other)

class GameEncoder(json.JSONEncoder):
   def default(self, obj):
      if isinstance( obj, GameObject ):
         return { 'obj_name': 'GameObject', 'obj_content': obj.__dict__}
      if isinstance( obj, GamePassage ):
         return { 'obj_name': 'GamePassage', 'obj_content': obj.__dict__ }
      if isinstance( obj, GameObjectUseAction ):
         return { 'obj_name': 'GameObjectUseAction', 'obj_content': obj.__dict__}
      if isinstance( obj, GamePassageRevealAction ):
         return { 'obj_name': 'GamePassageRevealAction', 'obj_content': obj.__dict__ }
      if isinstance( obj, GameObjectRevealAction ):
         return { 'obj_name': 'GameObjectRevealAction', 'obj_content': obj.__dict__ }
      if isinstance( obj, Game ):
         return [ obj.game_internal.rooms,
                  obj.game_internal.limbo,
                  obj.game_internal.passages,
                  obj.game_internal.use_actions,
                  obj.game_internal.views,
                  obj.game_internal.final_room,
                  obj.game_internal.descriptions ];
      return json.JSONEncoder.default(self, obj);

class GameDecoder(json.JSONDecoder):
   def __init__(self):
      json.JSONDecoder.__init__(self, object_hook=self.parsing)

   def parsing(self, d):
      if isinstance(d, dict) and len( d ) == 2 and 'obj_name' in d:
         if d['obj_name'] == 'GameObject': 
            retval = GameObject()
            retval.__dict__ = d['obj_content']
            return retval
         if d['obj_name'] == 'GamePassage': 
            retval = GamePassage()
            retval.__dict__ = d['obj_content']
            return retval
         if d['obj_name'] == 'GameObjectUseAction':
            retval = GameObjectUseAction()
            retval.__dict__ = d['obj_content']
            return retval
         if d['obj_name'] == 'GamePassageRevealAction':
            retval = GamePassageRevealAction()
            retval.__dict__ = d['obj_content']
            return retval
         if d['obj_name'] == 'GameObjectRevealAction':
            retval = GameObjectRevealAction()
            retval.__dict__ = d['obj_content']
            return retval
      return d;

class GameSolver:

   def solveInternal( self, game, solution ):
      if game.won():
         return True
      pathToWin = game.game_internal.find_path_between_rooms( lambda x : x == game.game_internal.final_room, game.game_internal.room.name, [], [] )
      if not pathToWin is None:
         self.do_for_all( game, solution, 'go', pathToWin )
         return self.solveInternal( game, solution )
      uses = game.game_internal.applicable_uses()
      if not uses == []:
         self.use_all( game, solution, uses )
         return self.solveInternal( game, solution )
      takes = game.game_internal.room.takable_child_names()
      if not takes == []:
         self.do_for_all( game, solution, 'take', takes )
         return self.solveInternal( game, solution )
      opens = game.game_internal.room.openable_child_names()
      if not opens == []:
         self.do_for_all( game, solution, 'open', opens )
         return self.solveInternal( game, solution )
      pathToCanAnythingToDo = game.game_internal.find_path_between_rooms( lambda x : game.game_internal.can_anything_to_do( x ), game.game_internal.room.name, [], [] )
      if not pathToCanAnythingToDo is None:
         self.do_for_all( game, solution, 'go', pathToCanAnythingToDo )
         return self.solveInternal( game, solution )
      return True

   def do_for_all( self, game, solution, command, stuffs ):
      for stuff in stuffs:
         game.do_it( command, stuff )
         solution.append( [command, stuff ] ) 

   def use_all( self, game, solution, uses ):
      for [first, second] in uses:
         game.do_it( 'use', first, second )
         solution.append( ['use', first, second ] ) 
      
   def solve( self, game, use_checker = True ):
      if use_checker and not GameSyntaxChecker().check( game ) == '':
         return None
      my_solution = []
      my_game = copy.deepcopy( game )
      won = self.solveInternal( my_game, my_solution )
      if won:
         return my_solution
      return None

class GameSyntaxChecker:
   def check_must_have_at_least_one_room( self, game ):
      return len( game.game_internal.rooms ) > 0

   def check_final_room_differs_from_starting_room( self, game ):
      if ( len( game.game_internal.rooms ) > 0 ):
         if ( game.game_internal.final_room == game.game_internal.rooms[0].name ):
             return False
      return True
      
   def check_final_room_exists( self, game ):
      if ( not game.game_internal.find_room( game.game_internal.final_room ) is None ):
         return True
      return False

   def get_all_stuffs( self, game, addrooms = 0, add_top_children = 1 ):
      retval = []
      for room in game.game_internal.rooms:
         if addrooms == 1:
            retval += [ room ]
         retval += room.descendants( add_top_children )
      for lobj in game.game_internal.limbo:
         retval += [ lobj ]
         retval += lobj.descendants( add_top_children )
      return retval

   def get_all_stuff_names( self, game, addrooms = 0, add_top_children = 1 ):
      retval = []
      for stuff in self.get_all_stuffs( game, addrooms, add_top_children ):
         retval.append( stuff.name )
      return retval

   def get_list_of_accessible_rooms( self, game ):
      first_room = game.game_internal.rooms[0].name
      return game.game_internal.accessible_room_names( first_room )

   def check_final_room_is_reachable( self, game ):
      accessible_rooms = self.get_list_of_accessible_rooms( game )
      return game.game_internal.final_room in accessible_rooms

   def check_all_room_is_reachable( self, game ):
      accessible_rooms = self.get_list_of_accessible_rooms( game )
      for room in game.game_internal.rooms:
         if not room.name in accessible_rooms:
            return False
      return True

   def check_no_multiple_passages_between_rooms( self, game ):
      ordered_edges = []
      for passage in game.game_internal.passages:
         edge = passage.get_ordered_name()
         if edge in ordered_edges:
            return False
         else:
            ordered_edges.append( edge )
      return True

   def check_all_passage_identifiers_are_unique( self, game ):
      ids = []
      for passage in game.game_internal.passages:
         identifier = passage.identifier
         if identifier in ids:
            return False
         else:
            ids.append( identifier )
      return True

   def check_passage_identifiers_are_valid_in_actions( self, game ):
      ids = []
      for passage in game.game_internal.passages:
         ids.append( passage.identifier )
      allactions = game.game_internal.use_actions + game.game_internal.views
      for passage in allactions:
         try:
            if not passage.get_passage_identifier() in ids:
               return False
         except Exception:
            sys.exc_clear()
      return True

   def check_actors_are_valid_in_actions( self, game ):
      allactions = game.game_internal.use_actions + game.game_internal.views
      stuffs = self.get_all_stuff_names( game )
      for action in allactions:
         for actor in action.get_actor_names():
            if not actor == '' and not actor in stuffs:
               return False
      return True

   def check_subjects_to_reveal_are_invisible_in_actions( self, game ):
      allactions = game.game_internal.use_actions + game.game_internal.views
      objects = self.get_all_stuffs( game )
      for action in allactions:
         subjectname_array = action.subject_to_reveal()
         if subjectname_array:
            subjectname = subjectname_array[0]
            for obj in objects:
              if obj.name == subjectname:
                 if not GameObjectAttribute.INVISIBLE in obj.get_attributes():
                    return False
      return True

   def check_there_is_exactly_one_action_for_each_invisible_object_which_reveals_it( self, game ):
      allactions = game.game_internal.use_actions + game.game_internal.views
      objects = self.get_all_stuffs( game )
      for obj in objects:
         if GameObjectAttribute.INVISIBLE in obj.get_attributes():
            counter = 0
            for action in allactions:
               subjectname_array = action.subject_to_reveal()
               for subjectname in subjectname_array:
                  if obj.name == subjectname:
                     counter += 1
            if not counter == 1:
               return False
      return True

   def check_no_actions_without_actors( self, game ):
      allactions = game.game_internal.use_actions + game.game_internal.views
      for action in allactions:
         for actor in action.get_actor_names():
            if not actor == '':
               break
         else:
            return False
      return True

   def check_no_actions_with_same_actor_twice( self, game ):
      allactions = game.game_internal.use_actions + game.game_internal.views
      for action in allactions:
         actors = action.get_actor_names()
         if actors[0] == actors[1]:
            return False
      return True

   def check_no_multiple_actions( self, game ):
      allactions = game.game_internal.use_actions + game.game_internal.views

      # First pass: if two actions have exactly the same actors, it is always bad
      actor_pairs = []
      for action in allactions:
         pair = action.get_actor_names()
         if pair in actor_pairs:
            return False
         else:
            actor_pairs.append( pair )

      # Second + third pass: if two actions have exactly one common actors, it is bad only if one of the actions remove the actor
      actors = []
      for action in allactions:
         if not action.subject_to_reveal():
            for actor in action.get_actor_names():
               if actor in actors:
                  return False
               else:
                  actors.append( actor )
      for action in allactions:
         if action.subject_to_reveal():
            for actor in action.get_actor_names():
               if actor in actors:
                  return False
      return True

   def check_no_actions_with_two_immobile_actors( self, game ):
      allactions = game.game_internal.use_actions + game.game_internal.views
      objects = self.get_all_stuffs( game )

      # First pass: if two actions have exactly the same actors, it is always bad
      for action in allactions:
         pair = action.get_actor_names()
         immobiles = 0
         for one_name in pair:
            for obj in objects:
               if obj.name == one_name:
                  if GameObjectAttribute.IMMOBILE in obj.get_attributes():
                     immobiles += 1
         if immobiles == 2:
            return False
      return True


   def check_no_two_actors_with_the_same_name( self, game ):
      stuffs = []
      for stuffname in self.get_all_stuff_names( game, 1 ):
         if stuffname in stuffs:
            return False
         else:
            stuffs.append( stuffname )
      return True

   def check_not_top_level_stuffs_cannot_have_attributes( self, game ):
      for stuff in self.get_all_stuffs( game, 0, 0 ):
         if len( stuff.get_attributes() ) > 0:
            return False
      return True

   def check( self, game ):
      if not self.check_must_have_at_least_one_room( game ):
         return "must have at least one room"

      if not self.check_final_room_differs_from_starting_room( game ):
         return "cannot start in the ending room"

      if not self.check_final_room_exists( game ):
         return 'final room does not exist'

      if not self.check_final_room_is_reachable( game ):
         return 'final room is not reachable' 

      if not self.check_no_multiple_passages_between_rooms( game ):
         return 'multiple passages between the same rooms'

      if not self.check_all_passage_identifiers_are_unique( game ):
         return 'passage identifiers are not unique'

      if not self.check_all_room_is_reachable( game ):
         return 'not all rooms are accessible'

      if not self.check_passage_identifiers_are_valid_in_actions( game ):
         return 'invalid passage identifiers in an action'

      if not self.check_actors_are_valid_in_actions( game ):
         return 'found invalid object in an action'

      if not self.check_no_two_actors_with_the_same_name( game ):
         return 'found two objects with the same name'

      if not self.check_no_actions_without_actors( game ):
         return 'found an action without actors'

      if not self.check_no_actions_with_same_actor_twice( game ):
         return 'found invalid action with the same actor twice'

      if not self.check_no_multiple_actions( game ):
         return 'found multiple actions for the same actor'

      if not self.check_not_top_level_stuffs_cannot_have_attributes( game ):
         return 'not top level stuffs cannot have attributes'

      if not self.check_subjects_to_reveal_are_invisible_in_actions( game ):
         return 'subjects of revealing actions must be invisible initially'

      if not self.check_no_actions_with_two_immobile_actors( game ):
         return "at least one of the action's actors must be mobile"

      if not self.check_there_is_exactly_one_action_for_each_invisible_object_which_reveals_it( game ):
         return 'there must be exactly one action for each invisible object which reveals it'

      return ''


class Game(CommonEquality):
   def __init__( self, args ):
#      print json.dumps( [ args ], cls=GameEncoder );
      rooms, limbo, passages, use_actions, views, final_room, descriptions = args

      self.game_internal = GameInternal( rooms, limbo, passages, use_actions, views, final_room, descriptions )
      self.commands = { 'use'  : self.game_internal.use,
                        'drop' : self.game_internal.drop,
                        'take' : self.game_internal.take,
                        'go'   : self.game_internal.go,
                        'open' : self.game_internal.open }

   def __str__( self ):
#     return "GameObjectUseAction( '%s', '%s', '%s' )" % ( self.subjectname, self.toolname, self.resultname );
      return json.dumps( self, cls=GameEncoder );

   def __repr__( self ):
#     return "GameObjectUseAction( '%s', '%s', '%s' )" % ( self.subjectname, self.toolname, self.resultname );
      return json.dumps( self, cls=GameEncoder );

   def get_blueprints( self ):
      return self.game_internal.get_blueprints(); 

   # === Reading the status of the game board ===

   def current_room( self ):
      return self.game_internal.current_room()

   def look( self ):
      return self.game_internal.look()

   def directions( self ):
      return self.game_internal.directions()

   def has( self, name ):
      return self.game_internal.has( name )

   def stuffs( self ):
      return self.game_internal.stuffs()

   def won( self ):
      return self.game_internal.won()

   # === Manipulating the game board ===

   def do_it( self, command, arg1, arg2 = '' ):
      if not command in self.commands:
         raise Exception('Invalid command')
      else:
         retval = self.commands[command]( arg1, arg2 )
      self.game_internal.view_refresh()
      return retval

class GameInternal(CommonEquality):
   def __init__( self, rooms, limbo, passages, use_actions, views, final_room, descriptions ):
      self.rooms        = rooms
      self.limbo        = limbo 
      if ( len(rooms) > 0 ):
         self.room        = rooms[0] 
      else:
         self.room        = None
      self.passages     = passages
      self.inventory    = GameObject( 'inventory', [], [] )
      self.use_actions  = use_actions
      self.views        = views
      self.won_         = 0
      self.final_room   = final_room
      self.descriptions = descriptions
      self.blueprints = [ copy.deepcopy( self.rooms ),
                          copy.deepcopy( self.limbo ),
                          copy.deepcopy( self.passages ),
                          copy.deepcopy( self.use_actions ),
                          copy.deepcopy( self.views ),
                          copy.deepcopy( self.final_room ),
                          copy.deepcopy( self.descriptions ) ]

   def current_room( self ):
      return self.room.name

   def get_blueprints( self ):
      return self.blueprints;

   def find_in_limbo_and_remove( self, name ):
      retval = None
      for lobj in self.limbo:
         if lobj.name == name:
            retval = lobj
            break
      else:
         raise Exception('Cannot find the result object of the use action in the game.')
      self.limbo.remove( retval )
      return retval

   def setting_current_room( self, room_name ):
      self.room = self.find_room( room_name )
      if ( room_name == self.final_room ):
         self.winning()

   def move_between_entities( self, name, from_entity, to_entity ):
      subject = from_entity.take( name )
      if ( not subject is None ):
         if ( not to_entity is None ):
            to_entity.put( subject )
         return subject
      return None

   def view_refresh( self ):
      sorrounding_objects = [] + self.inventory.childObjects + self.room.childObjects
      for action in self.views:
         # cheating to make it faster
         subject, entity = self.find( action.subjectname )
         tool,    entity = self.find( action.toolname )
         if not subject is None and not tool is None and action.applicable( subject.name, tool.name ):
            action.showIt( self )

   def find_in_entities( self, name, entities ):
      for entity in entities:
         attempt = entity.find( name ) 
         if not attempt is None:
            return attempt, entity
      return None, None

   def find_room( self, name ):
      for room in self.rooms:
         if room.name == name:
            return room
      else:
         return None

   def open( self, name, other ):
      if other != '':
         raise Exception('Command takes has only one argument')
         return None

      subject, entity = self.find( name )
      if subject is None:
         return False
      for child in subject.children(): 
         entity.put(subject.take( child.name ) )
      return True
         
   def use_internal( self, subjectname, toolname ):
      if subjectname == '':
         return None
      subject, entity = self.find( subjectname )
      if subject is None:
         return None
      if toolname == '':
         for action in self.use_actions:
            if action.applicable( subject.name, '' ):
               return action.doIt( self )
         return None
      else:
         tool = self.inventory.find( toolname )
         if ( tool is None ):
            return None
         for action in self.use_actions:
            if action.applicable( subject.name, tool.name ):
               return action.doIt( self )
         return None

   def take( self, name, other ):
      if other != '':
         raise Exception('Command takes has only one argument')
         return None
      return self.move_between_entities( name, self.room, self.inventory )

   def drop( self, name, other ):
      if other != '':
         raise Exception('Command takes has only one argument')
         return None
      return self.move_between_entities( name, self.inventory, self.room )

   def has( self, name ):
      subject = self.inventory.find( name )
      return subject

   def look( self ):
      if self.room.get_hash_name() in self.descriptions:
         return self.descriptions[self.room.get_hash_name()]
      return ''

   def find( self, name ):
      return self.find_in_entities( name, [ self.inventory, self.room ] )

   def use( self, subjectname, toolname = '' ):
      retval = self.use_internal( subjectname, toolname )
      if ( not retval is None ):
         return retval
      return self.use_internal( toolname, subjectname )

   def directionsInternal( self, room_name, visibility = 1 ):
      retval = []
      for passage in self.passages:
         tmp = passage.get_out_passage_from_room(room_name, visibility)
         if not tmp is None:
            retval.append( tmp )
      return retval

   def find_path_between_rooms( self, endfunc, current_room = '', way = [], rooms = [] ):
      if current_room == '':
         return self.find_path_between_rooms( endfunc, self.room.name, way, rooms )
      if endfunc( current_room ):
         return way
      for [ direction, room_name ] in self.directionsInternal( current_room, 1 ):
         if not room_name in rooms:
            whatIfPath = self.find_path_between_rooms( endfunc, room_name, way + [ direction ], rooms + [ current_room ] )
            if not whatIfPath is None:
               return whatIfPath
      return None

   def accessible_room_names( self, first_room = '' ):
      # Preparations
      if ( len( self.rooms ) == 0 ):
         return []
      visited_room_names = []
      candidate_list = []
      if first_room == '':
         candidate_list.apped( self.room.name )
      else:
         candidate_list.append( first_room )

      # visiting rooms
      while len( candidate_list ) > 0:
         candidate = candidate_list.pop()
         if not candidate in visited_room_names:
            visited_room_names.append( candidate )
            for [i,j] in self.directionsInternal( candidate, 0 ):
               candidate_list.append( j )

      # retval
      return visited_room_names

   def can_anything_to_do( self, roomname ):
      myroom = self.find_room( roomname )
      return not self.applicable_views( roomname ) == [] or not self.applicable_uses( roomname ) == [] or not myroom.takable_child_names() == [] or not myroom.openable_child_names() == []

   def get_subject_names_and_tool_names( self, roomname = '', visibility_matters = True ):
      if roomname == '':
         myroom = self.room
      else:
         myroom = self.find_room( roomname )
         
      subjectnames = []
      toolnames = ['']
      for child in myroom.children():
         if not ( visibility_matters and GameObjectAttribute.INVISIBLE in child.attributes ):
            subjectnames.append( child.name ) 
      for child in self.inventory.children():
         subjectnames.append( child.name )
         toolnames.append( child.name )

      return subjectnames, toolnames

   def applicable_uses( self, roomname = '' ):
      subjectnames, toolnames = self.get_subject_names_and_tool_names( roomname )

      uses = []
      for action in self.use_actions:
         pair = action.get_actor_names()
         if action.subjectname in subjectnames and action.toolname in toolnames and action.applicable( action.subjectname, action.toolname ):
            uses.append( pair ) 
         elif action.toolname in subjectnames and action.subjectname in toolnames and action.applicable( action.toolname, action.subjectname ):
            uses.append( pair ) 

      return uses

   def applicable_views( self, roomname = '' ):
      subjectnames, toolnames = self.get_subject_names_and_tool_names( roomname, False )

      views = []
      for action in self.views:
         pair = action.get_actor_names()
         if action.subjectname in subjectnames and action.toolname in toolnames:
            views.append( pair ) 

      return views

   def directions( self ):
      return self.directionsInternal( self.room.name )

   def go( self, direction, other ):
      if other != '':
         raise Exception('Command takes has only one argument')
         return None

      topology = self.directions()
      for [room_direction, room_name] in topology:
         if room_direction == direction:
            self.setting_current_room( room_name )
            return self.room
      return None  

   def stuffs( self ):
      retval = []
      for subject in self.room.children():
         if not GameObjectAttribute.INVISIBLE in subject.attributes:
            appearance = self.room.find( subject.name ) 
            if ( not appearance is None ):
               retval.append( appearance.name )
      return retval

   def winning( self ):
      self.won_ = 1

   def won( self ):
      return self.won_

class GameObjectUseAction(CommonEquality):
   def __init__( self, subjectname='', toolname='', resultname='' ):
      self.subjectname       = subjectname
      self.toolname          = toolname
      self.resultname        = resultname

   def __str__( self ):
      return "GameObjectUseAction( '%s', '%s', '%s' )" % ( self.subjectname, self.toolname, self.resultname );

   def __repr__( self ):
      return "GameObjectUseAction( '%s', '%s', '%s' )" % ( self.subjectname, self.toolname, self.resultname );

   def subject_to_reveal( self ):
      return []

   def get_result_name( self ):
      return resultname

   def get_actor_names( self ):
      if self.subjectname < self.toolname:
         return [ self.subjectname, self.toolname ]
      else:
         return [ self.toolname, self.subjectname ]

   def applicable( self, subjectname, toolname ):
      return self.subjectname == subjectname and self.toolname == toolname

   def showIt( self, game ):
      game.views.remove( self )
      game.move_between_entities( self.toolname, game.inventory, None )
      subject, entity = game.find( self.subjectname )
      if not subject is None:
         entity.take( subject.name )
         retval = game.find_in_limbo_and_remove( self.resultname )
         entity.put( retval )
         return retval
      return None

   def doIt( self, game ):
      game.use_actions.remove( self )
      game.move_between_entities( self.toolname, game.inventory, None )
      subject, entity = game.find( self.subjectname )
      if not subject is None:
         entity.take( subject.name )
         retval = game.find_in_limbo_and_remove( self.resultname )
         entity.put( retval )
         return retval
      return None

class GamePassageRevealAction(CommonEquality):
   def __init__( self, subjectname='', toolname='', identifier='' ):
      self.subjectname       = subjectname
      self.toolname          = toolname
      self.identifier        = identifier

   def __str__( self ):
      return "GamePassageRevealAction( '%s', '%s', '%s' )" % ( self.subjectname, self.toolname, self.identifier );

   def __repr__( self ):
      return "GamePassageRevealAction( '%s', '%s', '%s' )" % ( self.subjectname, self.toolname, self.identifier );

   def subject_to_reveal( self ):
      return [ '@#passage#@' ] # although it looks strange, the real subject is a passage which is not an ordinary object TODO: find a better name, remove this woraround

   def get_actor_names( self ):
      if self.subjectname < self.toolname:
         return [ self.subjectname, self.toolname ]
      else:
         return [ self.toolname, self.subjectname ]

   def get_passage_identifier( self ):
      return self.identifier

   def applicable( self, subjectname, toolname ):
      return self.subjectname == subjectname and self.toolname == toolname

   def showIt( self, game ):
      raise Exception('Cannot use passage action as a view, it modifies the world')
 
   def doIt( self, game ):
      for passage in game.passages:
         if passage.identifier == self.identifier:
            passage.make_visible()

class GameObjectRevealAction(CommonEquality):
   def __init__( self, subjectname='', toolname='' ):
      self.subjectname       = subjectname
      self.toolname          = toolname

   def __str__( self ):
      return "GameObjectRevealAction( '%s', '%s' )" % ( self.subjectname, self.toolname );

   def __repr__( self ):
      return "GameObjectRevealAction( '%s', '%s' )" % ( self.subjectname, self.toolname );

   def subject_to_reveal( self ):
      return [ self.subjectname ]

   def get_actor_names( self ):
      if self.subjectname < self.toolname:
         return [ self.subjectname, self.toolname ]
      else:
         return [ self.toolname, self.subjectname ]

   def get_passage_identifier( self ):
      return self.identifier

   def applicable( self, subjectname, toolname ):
      return self.subjectname == subjectname and self.toolname == toolname

   def showIt( self, game ):
      game.views.remove( self ) # optimization
      tool,    entity = game.find( self.toolname )
      subject, entity = game.find( self.subjectname )
      if not tool is None and not subject is None and not subject.is_visible():
         subject.make_visible()
         return subject
      return None
 
   def doIt( self, game ):
      raise Exception('Cannot use game object reveal action with use.')

class GameObjectAttribute:
   IMMOBILE  = 'immobile'
   INVISIBLE = 'invisible'

class GameObject(CommonEquality):

   def __init__( self, name = '', attributes = [], cobs = []):
      self.name = name
      self.attributes   = attributes
      self.childObjects = cobs

   def __str__( self ):
      return "GameObject( '%s', %s, %s )" % ( self.name, self.attributes, self.childObjects );

   def __repr__( self ):
      return "GameObject( '%s', %s, %s )" % ( self.name, self.attributes, self.childObjects );

   def get_hash_name( self ):
      return 'go#' + self.name

   def make_equal_to( self, other ):
      self.name         = other.name
      self.childObjects = other.childObjects

   def is_visible( self ):
      if GameObjectAttribute.INVISIBLE in self.attributes:
         return False
      return True

   def make_visible( self ):
      if GameObjectAttribute.INVISIBLE in self.attributes:
         self.attributes.remove( GameObjectAttribute.INVISIBLE )

   def get_attributes( self ):
      return self.attributes

   # todo: refactor with take if you will be more experienced
   def find( self, name ):
      for child in self.childObjects:
         if child.name == name:
            return child
      return None

   def children( self ):
      return self.childObjects

   def takable_child_names( self ):
      retval = []
      for child in self.childObjects:
         if not GameObjectAttribute.IMMOBILE in child.attributes and not GameObjectAttribute.INVISIBLE in child.attributes:
            retval.append( child.name )
      return retval

   def openable_child_names( self ):
      retval = []
      for child in self.childObjects:
         if not child.childObjects == []:
            retval.append( child.name )
      return retval

   def descendants( self, add_top_children = 1 ):
      retval = []
      if add_top_children:
         retval += self.children()
      for child in self.children():
         retval += child.children()
      return retval

   def take( self, name ):
      for child in self.childObjects:
         if child.name == name and not GameObjectAttribute.IMMOBILE in child.attributes and not GameObjectAttribute.INVISIBLE in child.attributes :
            self.childObjects.remove( child )
            return child
      return None 

   def put( self, child ):
      if not child is None:
         self.childObjects.append( child )

class GamePassage(CommonEquality):
   def __init__( self, identifier='', room_name1='', room_name2='', direction1='', direction2='', attributes = [] ):
      self.identifier = identifier
      self.room_name1 = room_name1
      self.room_name2 = room_name2
      self.direction1 = direction1
      self.direction2 = direction2
      self.attributes = attributes

   def __str__( self ):
      return "GamePassage( '%s', '%s', '%s', '%s', '%s', %s )" % ( self.identifier, self.room_name1, self.room_name2, self.direction1, self.direction2, self.attributes );

   def __repr__( self ):
      return "GamePassage( '%s', '%s', '%s', '%s', '%s', %s )" % ( self.identifier, self.room_name1, self.room_name2, self.direction1, self.direction2, self.attributes );

   def get_ordered_name( self ):
      if ( self.room_name1 < self.room_name2 ):
         return [self.room_name1, self.room_name2]
      else:
         return [self.room_name2, self.room_name1]

   def make_visible( self ):
      self.attributes.remove( GameObjectAttribute.INVISIBLE )

   def get_out_passage_from_room( self, roomname, visibility = 1 ):
      if ( visibility and GameObjectAttribute.INVISIBLE in self.attributes ):
         return None
      else:
         if self.room_name1 == roomname:
            return [ self.direction1, self.room_name2 ]
         if self.room_name2 == roomname:
            return [ self.direction2, self.room_name1 ]

