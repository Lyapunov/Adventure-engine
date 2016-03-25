import copy

class Game:
   def __init__( self, rooms, passages, use_actions, views ):
      self.rooms       = rooms
      self.room        = rooms[0]
      self.passages    = passages
      self.inventory   = GameObject( 'inventory', 'my inventory', [] )
      self.use_actions = use_actions
      self.views = views

   def move_between_entities( self, name, from_entity, to_entity ):
      object = from_entity.take( name )
      if ( not object is None ):
         to_entity.put( object )
         return object
      return None

   def change_subject_according_to_prototype( self, subject, prototype ):
      retval = copy.copy(prototype)
      retval.childObjects = subject.childObjects
      return retval

   def see_subject_through_views( self, subject ):
      for action in self.views:
         for tool in self.inventory.childObjects:
            if action.tool == tool.name and action.subject == subject.name:
               return self.change_subject_according_to_prototype( subject, action.prototype )
         for tool in self.room.childObjects:
            if action.tool == tool.name and action.subject == subject.name:
               return self.change_subject_according_to_prototype( subject, action.prototype )
      return subject

   def find_in_entities( self, name, entities ):
      for entity in entities:
         subject = entity.find( name ) 
         if ( not subject is None ):
            return self.see_subject_through_views( subject ), entity
      return None

   def use_one_direction( self, name_of_tool, name_of_subject ):
      tool = self.inventory.find( name_of_tool )
      if ( tool is None ):
         return None
      subject, entity = self.find( name_of_subject )
      if ( subject is None ):
         return None
      for action in self.use_actions:
         if action.tool == tool.name and action.subject == subject.name:
            self.use_actions.remove( action )
            self.destroy( name_of_tool )
            entity.take( name_of_subject )
            retval = self.change_subject_according_to_prototype( subject, action.prototype )
            entity.put( retval )
            return retval
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
      retval = self.use_one_direction( name_of_tool, name_of_subject )
      if ( not retval is None ):
         return retval
      return self.use_one_direction( name_of_subject, name_of_tool )

   def is_in_room( self, name ):
      subject = self.room.find( name )
      return subject

class GameObjectAction:
   def __init__( self, subject, tool, actionDescription, prototype ):
      self.subject           = subject
      self.tool              = tool
      self.actionDescription = actionDescription
      self.prototype         = prototype

class GameObject:
   def __init__( self, name = '', description = '', childObjects = []):
      self.name = name
      self.description = description
      self.childObjects = childObjects

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
         if child.name == name:
            self.childObjects.remove( child )
            return child
      return None 

   def put( self, child ):
      self.childObjects.append( child )

class GamePassage:
   def __init__( self, room1, room2, direction1, direction2 ):
      self.room1 = room1
      self.room2 = room2
      self.direction1 = direction1
      self.direction2 = direction2
