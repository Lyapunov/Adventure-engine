import copy

class Game:
   def __init__( self, rooms, passages, use_actions, views ):
      self.rooms       = rooms
      self.room        = rooms[0]
      self.passages    = passages
      self.inventory   = GameObject( 'inventory', '', [], [] )
      self.use_actions = use_actions
      self.views = views

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
      # If we try to take it, it can trigger actions, it is like using on itself. Think about trying to take a mine.
      self.use( name )
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
            self.room = self.find_room( room_name )
            return self.room
      return None  

   def is_in_room( self, name ):
      subject = self.room.find( name )
      return subject

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
   def __init__( self, subjectname, toolname, actionDescription, roomname, direction ):
      self.subjectname       = subjectname
      self.toolname          = toolname
      self.actionDescription = actionDescription
      self.roomname          = roomname
      self.direction         = direction

   def applicable( self, subjectname, toolname ):
      return self.subjectname == subjectname and self.toolname == toolname

   def view_through_prototype( self, subject ):
      raise Exception('Cannot use passage action as a view, it modifies the world')
 
   def doIt( self, game ):
      for passage in game.passages:
         tmp = passage.get_out_passage_from_room( self.roomname, 0 ) 
         if not tmp is None:
            outdirection, outroomname = tmp 
            if outdirection == self.direction:
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

   def take( self, name ):
      for child in self.childObjects:
         if child.name == name and not GameObjectAttribute.IMMOBILE in child.attributes :
            self.childObjects.remove( child )
            return child
      return None 

   def put( self, child ):
      self.childObjects.append( child )

class GamePassage:
   def __init__( self, room_name1, room_name2, direction1, direction2, attributes = [] ):
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

