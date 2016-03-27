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
      return None

   def find_room( self, name ):
      for room in self.rooms:
         if room.name == name:
            return room
      else:
         return None

   def use_internal( self, name_of_tool, name_of_subject ):
      tool = self.inventory.find( name_of_tool )
      if ( tool is None ):
         return None
      subject, entity = self.find( name_of_subject )
      if ( subject is None ):
         return None
      for action in self.use_actions:
         if action.applicable( subject.name, tool.name ):
            return action.doIt( self )
      return None

   def take( self, name ):
      return self.move_between_entities( name, self.room, self.inventory )

   def drop( self, name ):
      return self.move_between_entities( name, self.inventory, self.room )

   def destroy( self, name ):
      self.room.take( name )
      self.inventory.take( name )
      return None 

   def has( self, name ):
      subject = self.inventory.find( name )
      return subject

   def look( self ):
      return self.see_subject_through_views( self.room ).description

   def find( self, name ):
      return self.find_in_entities( name, [ self.inventory, self.room ] )

   def use( self, name_of_tool, name_of_subject ):
      retval = self.use_internal( name_of_tool, name_of_subject )
      if ( not retval is None ):
         return retval
      return self.use_internal( name_of_subject, name_of_tool )

   def directions( self ):
      retval = []
      for passage in self.passages:
         if passage.room_name1 == self.room.name and not GameObjectAttribute.INVISIBLE in passage.attributes:
            retval.append( [ passage.direction1, passage.room_name2 ] )
         if passage.room_name2 == self.room.name and not GameObjectAttribute.INVISIBLE in passage.attributes:
            retval.append( [ passage.direction2, passage.room_name1 ] )
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
      game.destroy( self.toolname )
      subject, entity = game.find( self.subjectname )
      entity.take( subject.name )
      retval = self.view_through_prototype( subject )
      entity.put( retval )
      return retval

class GameObjectPassageAction:
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
      return retval

class GameObjectAttribute:
   IMMOBILE  = 'immobile'
   INVISIBLE = 'invisible'

class GameObject:

   def __init__( self, name = '', description = '', attributes = [], cobs = []):
      self.name = name
      self.description  = description
      self.attributes   = attributes
      self.childObjects = cobs

   def makeEqualTo( self, other ):
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
