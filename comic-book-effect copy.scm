(define (script-fu-comic-book-effect input-path output-path)
  (let* ((image (car (gimp-file-load RUN-NONINTERACTIVE input-path input-path)))
         (drawable (car (gimp-image-get-active-layer image))))

    ;; Apply the Newsprint filter with spot function set to circles
    (plug-in-newsprint RUN-NONINTERACTIVE
                       image drawable
                       8                       ; pixelSize - size of the print dot
                       1                       ; colorspace (1 for CMYK)
                       100                     ; black pullout percentage
                       45                      ; blackAng - angle for black ink
                       0                       ; spot function for black (change if needed)
                       15                      ; cyanAng - angle for cyan ink
                       0                       ; spot function for cyan (change if needed)
                       75                      ; magentaAng - angle for magenta ink
                       0                       ; spot function for magenta (change if needed)
                       0                       ; yellowAng - angle for yellow ink
                       0                       ; spot function for yellow (change if needed)
                       1)                     ; turbulence

    ;; Change saturation
    (gimp-hue-saturation drawable
                         0  ; ALL channels
                         0  ; Hue
                         0  ; Lightness
                         -50) ; Saturation increase

    ;; Save the image
    (gimp-file-save RUN-NONINTERACTIVE image drawable output-path output-path)
    (gimp-image-delete image)))

(script-fu-register
 "script-fu-comic-book-effect"
 "Apply Comic Book effect"
 "Opens an image, applies a newsprint and saturation effect, then saves it with a new name."
 "SqueeGlitterFox"
 "SqueeGlitterFox"
 "2023"
 "*"
 SF-STRING "Input Path" ""
 SF-STRING "Output Path" "")

(script-fu-menu-register "script-fu-comic-book-effect" "<Image>/Filters/Batch Tools/")
