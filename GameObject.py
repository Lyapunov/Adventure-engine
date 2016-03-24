
class GameObjectAction:
   def __init__( self, main, manipulator, actionDescription, prototype ):
      self.main              = main
      self.manipulator       = manipulator
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

   def use( self, manipulator, actions ):
      for action in actions:
         if action.main == self and manipulator == action.manipulator:
            actions.remove(action)
            self.makeEqualTo( action.prototype ) 
            return action.actionDescription
      return None
