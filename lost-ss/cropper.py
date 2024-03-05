import os
from PIL import Image

def crop_custom(image_path, output_path):
    """Crops the image to the middle 80% of its height and left 85% of its width and saves it to output_path."""
    with Image.open(image_path) as img:
        width, height = img.size

        # Calculate new dimensions
        new_width = int(width * 0.87)
        new_height = int(height * 0.65)

        # Calculate coordinates to crop the image
        left = 0
        top = ((height - new_height) // 2) * 0.6
        right = left + new_width
        bottom = top + new_height

        cropped_image = img.crop((left, top, right, bottom))
        cropped_image.save(output_path)

def process_folder(input_folder, output_folder):
    """Crops all images in the input_folder and saves them to output_folder."""
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            image_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            crop_custom(image_path, output_path)
            print(f"Processed and saved {filename} to {output_folder}")

# Replace these paths with the actual paths
input_folder = 'images'
output_folder = 'cropped_images'

process_folder(input_folder, output_folder)