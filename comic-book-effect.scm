(define (script-fu-comic-book-effect image drawable)
  (let* (
         (width (car (gimp-image-width image)))
         (height (car (gimp-image-height image)))
         (cyan-layer (car (gimp-layer-new image width height RGBA-IMAGE "Cyan" 100 NORMAL-MODE)))
         (magenta-layer (car (gimp-layer-new image width height RGBA-IMAGE "Magenta" 100 NORMAL-MODE)))
         (yellow-layer (car (gimp-layer-new image width height RGBA-IMAGE "Yellow" 100 NORMAL-MODE)))
         (black-layer (car (gimp-layer-new image width height RGBA-IMAGE "Black" 100 NORMAL-MODE)))
         )
    
    (gimp-image-insert-layer image cyan-layer 0 0)
    (gimp-image-insert-layer image magenta-layer 0 0)
    (gimp-image-insert-layer image yellow-layer 0 0)
    (gimp-image-insert-layer image black-layer 0 0)
    
    (plug-in-newsprint RUN-NONINTERACTIVE image cyan-layer 8 15 0 0 0)
    (plug-in-newsprint RUN-NONINTERACTIVE image magenta-layer 8 45 0 0 0)
    (plug-in-newsprint RUN-NONINTERACTIVE image yellow-layer 8 0 0 0 0)
    (plug-in-newsprint RUN-NONINTERACTIVE image black-layer 8 75 0 0 0)
    
    (set! drawable (car (gimp-image-merge-visible-layers image CLIP-TO-IMAGE)))
    
    (gimp-displays-flush)
  )
)

(script-fu-register
  "script-fu-comic-book-effect"
  "CMYK Halftone"
  "Apply a CMYK halftone effect to an image"
  "Your Name"
  "Your Name"
  "2023"
  "*"
  SF-IMAGE      "Image"      0
  SF-DRAWABLE   "Drawable"   0
  SF-ADJUSTMENT "Dot Size"   '(8 1 64 1 10 0 0)
  SF-ADJUSTMENT "Cyan Angle"    '(15 0 360 1 10 0 0)
  SF-ADJUSTMENT "Magenta Angle" '(45 0 360 1 10 0 0)
  SF-ADJUSTMENT "Yellow Angle"  '(0 0 360 1 10 0 0)
  SF-ADJUSTMENT "Black Angle"   '(75 0 360 1 10 0 0)
)

(script-fu-menu-register "script-fu-cmyk-halftone" "<Image>/Filters/Halftone")