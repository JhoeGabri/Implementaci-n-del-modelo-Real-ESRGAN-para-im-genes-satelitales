import cv2
from skimage.metrics import peak_signal_noise_ratio, structural_similarity, mean_squared_error

def compare_images(image1_path, image2_path):
    try:
        # Load the images
        img1 = cv2.imread(image1_path, cv2.IMREAD_COLOR)
        img2 = cv2.imread(image2_path, cv2.IMREAD_COLOR)

        # Convert images to RGB (OpenCV loads images in BGR format)
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

        # Calculate PSNR
        psnr = peak_signal_noise_ratio(img1, img2)

        # Calculate SSIM
        ssim = structural_similarity(img1, img2, channel_axis=-1, win_size=7)

        # Calculate MSE
        mse = mean_squared_error(img1, img2)

        # Print the metrics
        print(f'PSNR: {psnr:.2f}')
        print(f'SSIM: {ssim:.4f}')
        print(f'MSE: {mse:.2f}')

    except Exception as e:
        print(f"Error comparing images: {str(e)}")

# Rutas a las dos imágenes que deseas comparar
image1_path = '../datasets/DIV2K/DIV2K_result_70K/0801x2_out.png'
image2_path = '../datasets/DIV2K/DIV2K_result_70K/0801x2_out.png'

# Llama a la función para comparar las imágenes
compare_images(image1_path, image2_path)
