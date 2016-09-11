# FloRETs

##Introduction

My **r**oom **e**scape-game **t**ools are in this repo. To make easier myself creating
simple point and click andventure games, I wanted to have the following stuffs:
* Inventing JSON descripton for simple room escape games about rooms, objects, possible
  actions.
* **DescriptionChecker**, which is able to test whether the JSON description has no 
  coneptual errors and contradictions, there is one and only one solution, you cannot 
  get lost and cannot die.
* **TextEngine**, which runs the JSON description as a text adventure game in command
  line.
* A **PointAndClickEngine** which is for running the JSON description as a point and 
  click adventure game in browser. I added a minimal editor to the game code, to make
  easier to place objects. If variable *devMode = 1*, then pressing key 'p' brings
  to editor mode, and the positions of objects and corridors can be changed.

Codes are in Python and in JavaScript.

## Demo game

Click to the image to try the demo game, which was created with these tools.
[![image of demogame](demo_game.png)](http://critic-fire-81205.bitballoon.com/)

## Development step by step

