#!/bin/bash
cp ../index.html .
cp ../PointAndClickEngine.html .
cp ../spritesheet.png .

# Not dev mode and using sprite sheet

sed -i 's/devMode = 1/devMode = 0/g' PointAndClickEngine.html
sed -i 's/useSpriteSheet = 0/useSpriteSheet = 1/g' PointAndClickEngine.html

zip demo.zip GraphicEngine.html spritesheet.png index.html

rm index.html
rm PointAndClickEngine.html
rm spritesheet.png
