#!/bin/bash

# get absolute path for the current directory
DIRECTORY=$(cd `dirname $0` && pwd)

FILES_PATH="$DIRECTORY/video-assets/"

# get directory listing from FILES_PATH for *.png files
FILES=$(ls $FILES_PATH*.png)

# loop through each file in FILES
for FILE in $FILES
do
  # get the filename from the full path
  FILE=$(basename $FILE)

  INPUT_PATH="$DIRECTORY/video-assets/$FILE"
  OUTPUT_PATH="$DIRECTORY/video-assets/final/$FILE"
  MOVE_PATH="$DIRECTORY/video-assets/orig/$FILE"

  echo "Processing file: $INPUT_PATH"
  echo "Saving to: $OUTPUT_PATH"

  # Run GIMP with batch commands
  flatpak run org.gimp.GIMP -idf -b "(
      let* (
        (image (car (gimp-file-load RUN-NONINTERACTIVE \"$INPUT_PATH\" \"$INPUT_PATH\"))) 
        (drawable (car (gimp-image-get-active-layer image)))
      )
      (gimp-brightness-contrast drawable -40 60)
      ; (gimp-drawable-hue-saturation drawable 0 -15 20 -60 100) ;all
      (gimp-drawable-hue-saturation drawable 0 0 20 -30 100) ;all
      (gimp-levels-stretch drawable)
      (plug-in-newsprint RUN-NONINTERACTIVE image drawable 8 1 0 15 0 15 0 75 0 0 0 15) 
      (gimp-file-save RUN-NONINTERACTIVE image drawable \"$OUTPUT_PATH\" \"$OUTPUT_PATH\")
      (gimp-image-delete image)
    )" \
    -b "(gimp-quit 0)"
done
