import os
import shutil
import re


def copy_images_for_validation(source_directory, destination_directory, start_index=101, num_images=20):
    # Path to the AID directory
    aid_path = os.path.join(source_directory, '../datasets', 'AID')

    # Path to the new AID validation directory
    aid_validation_path = os.path.join(source_directory, '../datasets', destination_directory)

    # Check if AID directory exists
    if not os.path.exists(aid_path):
        print(f"The directory {aid_path} does not exist.")
        return

    # Create the new AID validation directory if it does not exist
    if not os.path.exists(aid_validation_path):
        os.makedirs(aid_validation_path)

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

            # Copy the images from start_index to start_index + num_images
            for image in images_sorted[start_index - 1:start_index - 1 + num_images]:
                source_image_path = os.path.join(subdir_path, image)
                destination_image_path = os.path.join(aid_validation_path, f"{subdir}_{image}")
                shutil.copy(source_image_path, destination_image_path)
                total_copied_images += 1

            print(
                f"Copied {min(num_images, len(images_sorted[start_index - 1:start_index - 1 + num_images]))} images from {subdir} to {aid_validation_path}")

    print(f"Total copied images for validation: {total_copied_images}")


if __name__ == "__main__":
    # Specify the directory where the script is located
    base_directory = os.path.dirname(os.path.abspath(__file__))

    # Specify the starting index and the number of images to copy
    start_index = 101
    num_images_to_copy = 20

    # Call the function to copy images for validation
    copy_images_for_validation(base_directory, 'AID_validation', start_index, num_images_to_copy)
