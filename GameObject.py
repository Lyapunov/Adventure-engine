import copy

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

   def check_final_room_is_reachable( self, game ):
      if ( len( game.game_internal.passages ) != 0 ):
         return True
      return False

   def check( self, game ):
      if not self.check_must_have_at_least_one_room( game ):
         return "must have at least one room"

      if not self.check_final_room_differs_from_starting_room( game ):
         return "cannot start in the ending room"

      if not self.check_final_room_exists( game ):
         return 'final room does not exist'

      if not self.check_final_room_is_reachable( game ):
         return 'final room is not reachable' 

      return ''


class Game:
   def __init__(  self, rooms, passages, use_actions, views, final_room ):
      self.game_internal = GameInternal( rooms, passages, use_actions, views, final_room )

   # === Reading the status of the game board ===

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

   def use( self, subjectname, toolname = '' ):
      return self.game_internal.use( subjectname, toolname )

   def drop( self, name ):
      return self.game_internal.drop( name )

   def take( self, name ):
      return self.game_internal.take( name )

   def move( self, direction ):
      return self.game_internal.move( direction )

class GameInternal:
   def __init__( self, rooms, passages, use_actions, views, final_room ):
      self.rooms       = rooms
      if ( len(rooms) > 0 ):
         self.room        = rooms[0] 
      else:
         self.room        = None
      self.passages    = passages
      self.inventory   = GameObject( 'inventory', '', [], [] )
      self.use_actions = use_actions
      self.views       = views
      self.won_        = 0
      self.final_room  = final_room

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

   def see_subject_through_views( self, subject ):
      for action in self.views:
         for tool in self.inventory.childObjects:
            if action.applicable( subject.name, tool.name ):
               return action.view_through_prototype( subject )
         for tool in self.room.childObjects:
            if action.applicable( subject.name, tool.name ):
               return action.view_through_prototype( subject )
      return subject

   def find_in_entities( self, name, entities ):
      for entity in entities:
         subject = entity.find( name ) 
         if ( not subject is None ):
            return self.see_subject_through_views( subject ), entity
      return None, None

   def find_room( self, name ):
      for room in self.rooms:
         if room.name == name:
            return room
      else:
         return None

   def use_internal( self, subjectname, toolname ):
      if ( subjectname == '' ):
         return None
      subject, entity = self.find( subjectname )
      if ( subject is None ):
         return None
      if ( toolname == '' ):
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

   def take( self, name ):
      return self.move_between_entities( name, self.room, self.inventory )

   def drop( self, name ):
      return self.move_between_entities( name, self.inventory, self.room )

   def has( self, name ):
      subject = self.inventory.find( name )
      return subject

   def look( self ):
      return self.see_subject_through_views( self.room ).description

   def find( self, name ):
      return self.find_in_entities( name, [ self.inventory, self.room ] )

   def use( self, subjectname, toolname = '' ):
      retval = self.use_internal( subjectname, toolname )
      if ( not retval is None ):
         return retval
      return self.use_internal( toolname, subjectname )

   def directions( self ):
      retval = []
      for passage in self.passages:
         tmp = passage.get_out_passage_from_room( self.room.name ) 
         if not tmp is None:
            retval.append( tmp )
      return retval

   def move( self, direction ):
      topology = self.directions()
      for [room_direction, room_name] in topology:
         if room_direction == direction:
            self.setting_current_room( room_name )
            return self.room
      return None  

   def stuffs( self ):
      retval = []

      for subject in self.room.children():
         appearance = self.room.find( subject.name ) 
         if ( not appearance is None ):
            retval.append( appearance.name )
      return retval

   def winning( self ):
      self.won_ = 1

   def won( self ):
      return self.won_

class GameObjectUseAction:
   def __init__( self, subjectname, toolname, actionDescription, prototype ):
      self.subjectname       = subjectname
      self.toolname          = toolname
      self.actionDescription = actionDescription
      self.prototype         = prototype

   def applicable( self, subjectname, toolname ):
      return self.subjectname == subjectname and self.toolname == toolname

   def view_through_prototype( self, subject ):
      subject.childObjects = subject.childObjects + self.prototype.childObjects
      self.prototype.childObjects = []
      retval = copy.copy(self.prototype)
      retval.childObjects = subject.childObjects
      return retval

   def doIt( self, game ):
      game.use_actions.remove( self )
      game.move_between_entities( self.toolname, game.inventory, None )
      subject, entity = game.find( self.subjectname )
      entity.take( subject.name )
      retval = self.view_through_prototype( subject )
      entity.put( retval )
      return retval

class GamePassageRevealAction:
   def __init__( self, subjectname, toolname, actionDescription, identifier ):
      self.subjectname       = subjectname
      self.toolname          = toolname
      self.actionDescription = actionDescription
      self.identifier        = identifier

   def applicable( self, subjectname, toolname ):
      return self.subjectname == subjectname and self.toolname == toolname

   def view_through_prototype( self, subject ):
      raise Exception('Cannot use passage action as a view, it modifies the world')
 
   def doIt( self, game ):
      for passage in game.passages:
         if passage.identifier == self.identifier:
            passage.make_visible()

class GameObjectAttribute:
   IMMOBILE  = 'immobile'
   INVISIBLE = 'invisible'

class GameObject:

   def __init__( self, name = '', description = '', attributes = [], cobs = []):
      self.name = name
      self.description  = description
      self.attributes   = attributes
      self.childObjects = cobs

   def make_equal_to( self, other ):
      self.name         = other.name
      self.description  = other.description
      self.childObjects = other.childObjects

   def look( self ):
      return self.description

   # todo: refactor with take if you will be more experienced
   def find( self, name ):
      for child in self.childObjects:
         if child.name == name:
            return child
      return None 

   def children( self ):
      return self.childObjects

   def take( self, name ):
      for child in self.childObjects:
         if child.name == name and not GameObjectAttribute.IMMOBILE in child.attributes :
            self.childObjects.remove( child )
            return child
      return None 

   def put( self, child ):
      self.childObjects.append( child )

class GamePassage:
   def __init__( self, identifier, room_name1, room_name2, direction1, direction2, attributes = [] ):
      self.identifier = identifier
      self.room_name1 = room_name1
      self.room_name2 = room_name2
      self.direction1 = direction1
      self.direction2 = direction2
      self.attributes = attributes

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

