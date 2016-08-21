#!/usr/bin/python2.7

import json
import os.path
import sys

from GameObject import Game
from GameObject import GameDecoder

def main(argv):
   if len(argv) != 2:
      print "USAGE:", os.path.basename( argv[0] ), "<game dat file>"
      return
   gamefile = argv[1]
   print "Opening file", gamefile
   print
   try:
      with open(gamefile,'r') as myfile:
         game_blueprints = myfile.read().replace('\n','')
         game = Game( GameDecoder().decode( game_blueprints ) )
         looked = {}

         if not game.current_room() in looked:
            print game.look()
            looked[game.current_room()] = True
         else: 
            print "You are in a", game.current_room()
         print "You can go to the following directions:",
         for dirdesc in game.directions():
            print dirdesc[0],
         print "."
   except IOError as e:
      print "I/O error({0}): {1}".format(e.errno, e.strerror)

#  game_from_text = Game( GameDecoder().decode( self.game1_text_blueprints ) )

if __name__ == "__main__":
    main(sys.argv)
