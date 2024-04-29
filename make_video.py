import cv2
import numpy as np
import os

def adjust_image_colors(image):
    # Convert to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Reduce saturation
    hsv_image[:, :, 1] = hsv_image[:, :, 1] * 0.8 
    
    # Convert back to BGR
    adjusted_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

    # Apply a warm white balance (simulating a yellowed effect)
    adjusted_image[:, :, 0] = cv2.add(adjusted_image[:, :, 0], 30)  # more blue
    adjusted_image[:, :, 2] = cv2.add(adjusted_image[:, :, 2], 30)  # more red

    return adjusted_image

def create_video(image_folder, output_file, target_length, fps=30):
    target_cell_size = 1400
    border = 30
    shift = 200
    
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (target_cell_size, target_cell_size))

    # Load images
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    
    # limit to 40 images
    # images = images[0:40]
    
    images.sort()  # Sort to maintain order

    # Prepare the extended canvas
    resized_width = int((target_cell_size - (border * 3)) / 2) 
    resized_height = int((target_cell_size - (border * 3)) / 2) 
    num_images = len(images)
    column_height = (num_images) * (resized_height + border) // 2 + border  # Adjusted calculation
    full_image = np.zeros((column_height, target_cell_size, 3), dtype=np.uint8)

    # Place images in the full_image array
    y_offset = border
    for i, img_name in enumerate(images):
        print(i, img_name)
        img_path = os.path.join(image_folder, img_name)
        img = cv2.imread(img_path)
        if img is None:
            continue

        # Resize image
        img = cv2.resize(img, (resized_width, resized_height), interpolation=cv2.INTER_AREA)

        # Adjust image color
        if img_name.endswith('A.png') or img_name.endswith('B.png') or img_name.endswith('C.png') or img_name.endswith('D.png') or img_name.endswith('E.png') or img_name.endswith('F.png'):
            img = adjust_image_colors(img)

        # Calculate the proper offsets for each column
        x_offset = border if i % 2 == 0 else resized_width + 2 * border  # Adjust for two columns
        # Ensure we do not exceed the full_image bounds
        if y_offset + resized_height > column_height:
            break
        full_image[y_offset:y_offset + resized_height, x_offset:x_offset + resized_width] = img
        y_offset += shift if i % 2 == 0 else resized_height + border - shift  # Increment y_offset after placing an image

    # Calculate the required scroll rate to achieve the target video length
    total_scroll_distance = column_height - target_cell_size
    total_number_of_frames = target_length * fps
    scroll_rate = total_scroll_distance / total_number_of_frames if total_number_of_frames else 1

    # scroll_fraction = 0
    int_scroll_rate = int(scroll_rate)
    # Scroll through the full_image to create frames
    for i in range(0, column_height - target_cell_size, int_scroll_rate):
        # scroll_fraction += scroll_rate - int_scroll_rate
        # offset = 0 if scroll_fraction < 1 else 1
        # if scroll_fraction >= 1:
        #     scroll_fraction -= 1
         
        # frame = full_image[i:i+target_cell_size+offset, :]
        frame = full_image[i:i+target_cell_size, :]
        out.write(frame)

    # Release everything when done
    out.release()
    print(f'Video saved as {output_file}')

import cv2
import numpy as np

def rotate_and_crop_video(input_file, output_file, fps=30):
    # Open the original video
    cap = cv2.VideoCapture(input_file)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Define codec and create a new VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (1024, 1024))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Rotate frame
        M = cv2.getRotationMatrix2D((frame.shape[1] // 2, frame.shape[0] // 2), -20, 1)  # Negative angle for clockwise rotation
        rotated = cv2.warpAffine(frame, M, (frame.shape[1], frame.shape[0]))

        # Crop the center
        start_x = (rotated.shape[1] - 1024) // 2
        start_y = (rotated.shape[0] - 1024) // 2
        cropped = rotated[start_y:start_y + 1024, start_x:start_x + 1024]

        out.write(cropped)

    # Release everything when done
    cap.release()
    out.release()
    print(f'Video saved as {output_file}')

# Usage
create_video('./video-assets/final', 'output1.mp4', 268)
rotate_and_crop_video('output1.mp4', 'output2.mp4')
