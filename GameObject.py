class Game:
   def __init__( self, world, inventory, use_actions, view_actions ):
      self.world = world
      self.inventory = inventory
      self.use_actions = use_actions
      self.view_actions = view_actions

   def move_between_entities( self, name, from_entity, to_entity ):
      object = from_entity.take( name )
      if ( not object is None ):
         to_entity.put( object )
         return object
      return None

   def take( self, name ):
      return self.move_between_entities( name, self.world, self.inventory )

   def drop( self, name ):
      return self.move_between_entities( name, self.inventory, self.world )

   def destroy( self, name ):
      self.world.take( name )
      self.inventory.take( name )
      return None 

   def has( self, name ):
      object = self.inventory.find( name )
      return object

   def find( self, name ):
      object = self.inventory.find( name )
      if ( not object is None ):
         return object
      object = self.world.find( name )
      if ( not object is None ):
         return object
      return None

   def use( self, name_of_tool, name_of_actor ):
      retval = self.use_one_direction( name_of_tool, name_of_actor )
      if ( not retval is None ):
         return retval
      return self.use_one_direction( name_of_actor, name_of_tool )

   def use_one_direction( self, name_of_tool, name_of_actor ):
      tool = self.inventory.find( name_of_tool )
      if ( tool is None ):
         return None
      actor = self.find( name_of_actor )
      if ( actor is None ):
         return None
      for action in self.use_actions:
         if action.tool == tool.name and action.actor == actor.name:
            self.destroy( name_of_tool )
            self.destroy( name_of_actor )
            self.use_actions.remove( action )
            retval = self.world.put( action.prototype )
            return action.prototype
      return None

   def is_in_world( self, name ):
      return self.world.find( name )

class GameObjectAction:
   def __init__( self, actor, tool, actionDescription, prototype ):
      self.actor             = actor
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

