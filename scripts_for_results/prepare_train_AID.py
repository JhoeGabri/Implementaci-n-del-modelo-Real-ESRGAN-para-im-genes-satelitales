import os
import shutil
import re

def copy_images(source_directory, destination_directory, num_images=100):
    # Path to the AID directory
    aid_path = os.path.join(source_directory, '../datasets', 'AID')

    # Path to the new AID dataset directory
    aid_dataset_path = os.path.join(source_directory, '../datasets', destination_directory)

    # Check if AID directory exists
    if not os.path.exists(aid_path):
        print(f"The directory {aid_path} does not exist.")
        return

    # Create the new AID dataset directory if it does not exist
    if not os.path.exists(aid_dataset_path):
        os.makedirs(aid_dataset_path)

    # Initialize a counter for the total number of copied images
    total_copied_images = 0

    # Regex pattern to match filenames with numeric suffix
    pattern = re.compile(r'_(\d+)\.(png|jpg|jpeg|bmp|gif)$')

    # Iterate over each subdirectory in the AID directory
    for subdir in os.listdir(aid_path):
        subdir_path = os.path.join(aid_path, subdir)

        # Check if it's a directory
        if os.path.isdir(subdir_path):
            # Get list of image files in the subdirectory
            images = [file for file in os.listdir(subdir_path) if
                      os.path.isfile(os.path.join(subdir_path, file)) and pattern.search(file.lower())]

            # Sort images based on the numeric suffix
            images_sorted = sorted(images, key=lambda x: int(pattern.search(x).group(1)))

            # Copy the first num_images images to the new AID dataset directory
            for image in images_sorted[:num_images]:
                source_image_path = os.path.join(subdir_path, image)
                destination_image_path = os.path.join(aid_dataset_path, f"{subdir}_{image}")
                shutil.copy(source_image_path,      destination_image_path)
                total_copied_images += 1      

            print(f"Copied {min(num_images, len(images_sorted))} images from {subdir} to {aid_dataset_path}")

    print(f"Total copied images: {total_copied_images}")


if __name__ == "__main__":
    # Specify the directory where the script is located
    base_directory = os.path.dirname(os.path.abspath(__file__))

    # Specify the number of images to copy
    num_images_to_copy = 100

    # Call the function to copy images
    copy_images(base_directory, 'AID_train', num_images_to_copy)
