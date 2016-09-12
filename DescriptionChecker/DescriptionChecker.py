#!/usr/bin/python2.7

import json
import os.path
import sys
sys.path.append("../PyLib")

from GameObject import Game
from GameObject import GameDecoder
from GameObject import GameSyntaxChecker
from GameObject import GameSolver

def main(argv):
   if len(argv) != 2:
      print "USAGE:", os.path.basename( argv[0] ), "<game dat file>"
      return
   gamefile = argv[1]
   exit_commands = [ 'quit', 'exit' ]
   inventory_commands = [ 'inventory' ];
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
      print e
      return
   result = GameSyntaxChecker().check( game );
   if result != "":
      print "Error: ", result;
      return
   else:
      print "Game description in",gamefile,"is error-free."
   solution =  GameSolver().solve( game )
   print
   print "The solution is:"
   print solution

if __name__ == "__main__":
    main(sys.argv)
