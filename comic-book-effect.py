from PIL import Image
import numpy as np
import math

def apply_halftone(image, angles, size):
    cmyk_image = image.convert('CMYK')
    cmyk_channels = cmyk_image.split()
    halftone_channels = []

    for channel, angle in zip(cmyk_channels, angles):
        print(channel, angle)
        channel_array = np.array(channel, dtype=np.float32) / 255.0
        height, width = channel_array.shape
        halftone_array = np.zeros((height, width), dtype=np.float32)

        angle_rad = math.radians(angle)
        cos_angle = math.cos(angle_rad)
        sin_angle = math.sin(angle_rad)

        for y in range(0, height, size):
            for x in range(0, width, size):
                x_offset = int(x * cos_angle - y * sin_angle) % size
                y_offset = int(x * sin_angle + y * cos_angle) % size
                cell_mean = np.mean(channel_array[y:y+size, x:x+size])
                dot_size = int(cell_mean * size) * 2
                
                for i in range(size):
                    for j in range(size):
                        if (i - y_offset) ** 2 + (j - x_offset) ** 2 <= (dot_size // 2) ** 2:
                            halftone_array[y+i, x+j] = 1.0

        halftone_channels.append(Image.fromarray((halftone_array * 255).astype(np.uint8)))

    halftone_image = Image.merge('CMYK', halftone_channels).convert('RGB')
    return halftone_image

# Load the source PNG image
source_image = Image.open('video-assets/shark-net.png')

# Define the halftone angles for each CMYK channel (in degrees)
angles = [15, 45, 0, 75]  # [Cyan, Magenta, Yellow, Black]

# Define the size of the halftone pattern
size = 8

# Apply CMYK halftone effect
halftone_image = apply_halftone(source_image, angles, size)

# Save the halftone image as PNG
halftone_image.save('video-assets/final/shark-net.png')


