import socket
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
filename = "aquatic-net-1.png"
input_path = f"{current_directory}/video-assets/{filename}"
output_path = f"{current_directory}/video-assets/final/{filename}"

print("current_directory:", current_directory)
print("input_path:", input_path)
print("output_path:", output_path)

if not os.path.exists(input_path):
    raise FileNotFoundError(f"Input file not found: {input_path}")

if not os.path.exists(os.path.dirname(output_path)):
    raise FileNotFoundError(f"Output directory not found: {os.path.dirname(output_path)}")

def send_command(command):
    """Send a command to the GIMP Script-Fu server and retrieve the response."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 10008))  # IP and port of the GIMP Script-Fu server
        print("Connection Established")
        s.sendall((command + '\n').encode('utf-8'))
        print("Command Sent")
        response = s.recv(4096)  # Increased buffer size to ensure full response is read
        print("Received Response")
        return response.decode('utf-8')

def main():
    # Load the image
    print("Loading image...")    
    load_command = f'(gimp-file-load RUN-NONINTERACTIVE "{input_path}" "{input_path}")'
    print(load_command)
    image_id = send_command(load_command).strip()
    print("Image loaded.", image_id)

    # Apply the newsprint filter in CMYK
    print("Applying newsprint filter...")
    newsprint_command = f'(plug-in-newsprint RUN-NONINTERACTIVE {image_id} CMYK 0.001 "circle" 8.00 75 1.000 "circle" 8.00 0 "circle" 8.00 45 "circle" 8.00 15)'
    print(newsprint_command)
    send_command(newsprint_command)
    print("Newsprint filter applied.")

    # Reduce saturation
    print("Reducing saturation...")
    saturation_command = f'(gimp-hue-saturation RUN-NONINTERACTIVE {image_id} 0 0 -30)'  # Adjust to -30% to achieve 0.7 of original
    print(saturation_command)
    send_command(saturation_command)
    print("Saturation reduced.")

    # Save the image
    print("Saving image...")
    save_command = f'(gimp-file-save RUN-NONINTERACTIVE 1 {image_id} "{output_path}" "{filename}")'
    print(save_command)
    send_command(save_command)
    print("Image saved.")

    # Close image
    close_command = f'(gimp-image-delete {image_id})'
    print(close_command)
    send_command(close_command)

if __name__ == '__main__':
    main()
