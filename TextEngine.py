#!/usr/bin/python2.7

import json
import os.path
import sys

from GameObject import Game
from GameObject import GameDecoder
from GameObject import GameSyntaxChecker

def main(argv):
   if len(argv) != 2:
      print "USAGE:", os.path.basename( argv[0] ), "<game dat file>"
      return
   gamefile = argv[1]
   print "Opening file", gamefile
   print
   game = None;
   try:
      with open(gamefile,'r') as myfile:
         game_blueprints = myfile.read().replace('\n','')
         game = Game( GameDecoder().decode( game_blueprints ) )
   except IOError as e:
      print "I/O error({0}): {1}".format(e.errno, e.strerror)
      return
   except Exception as e:
      print "Could not parse game file."
      return
   result = GameSyntaxChecker().check( game );
   if result != "":
      print "Error: ", result;
      return

   looked = {}
   while True:

      if not game.current_room() in looked:
         print game.look()
         looked[game.current_room()] = True
      else: 
         print "You are in a", game.current_room()

      if game.won():
         break

      if len( game.stuffs() ) > 0:
          print "The following objects are in the room:", 
          for stuff in game.stuffs():
             print stuff,
          print "."
      if len( game.directions() ) > 0 :
          print "You can go to the following directions:",
          for dirdesc in game.directions():
             print dirdesc[0],
          print "."

      input_fields = []
      while len(input_fields) <= 0:
         input_fields = raw_input('>').split(); # better than split('')

      if len(input_fields) > 3:
         print "You cannot do that."

      input_fields += ['',''] # to set a default value for not given params in an easy way

      if input_fields[1] == '' and input_fields[2] == '':
         if input_fields[0] in [ 'quit', 'exit' ]:
            break 
         if input_fields[0] in [ 'inventory' ]:
            if len( game.inventory() ) > 0:
               print 'You have the following items:',
               for item in game.inventory():
                  print item,
               print
            else:
               print 'You have no items.'
            continue

      try:
         game.do_it( input_fields[0], input_fields[1], input_fields[2] )
      except Exception:
         print "You cannot do that."


if __name__ == "__main__":
    main(sys.argv)
