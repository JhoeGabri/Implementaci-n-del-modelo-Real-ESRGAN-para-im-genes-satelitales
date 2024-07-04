import os
import cv2
import numpy as np
import csv
import matplotlib.pyplot as plt
from skimage.metrics import peak_signal_noise_ratio, structural_similarity, mean_squared_error


def calculate_metrics(result_dir, gt_dir):
    results = []

    for filename in os.listdir(result_dir):
        if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
            result_path = os.path.join(result_dir, filename)

            # Intenta encontrar el archivo GT en formato PNG primero, luego en JPG
            gt_filename_base = filename.replace('_ESRNET', '').replace('.png', '').replace('.jpg', '').replace(
                '.jpeg', '') #cambiar
            gt_path_png = os.path.join(gt_dir, gt_filename_base + '.png')
            gt_path_jpg = os.path.join(gt_dir, gt_filename_base + '.jpg')
            gt_path_jpeg = os.path.join(gt_dir, gt_filename_base + '.jpeg')

            if os.path.exists(gt_path_png):
                gt_path = gt_path_png
            elif os.path.exists(gt_path_jpg):
                gt_path = gt_path_jpg
            elif os.path.exists(gt_path_jpeg):
                gt_path = gt_path_jpeg
            else:
                print(f"Ground truth image not found for {filename}")
                continue

            result_img = cv2.imread(result_path, cv2.IMREAD_COLOR)
            gt_img = cv2.imread(gt_path, cv2.IMREAD_COLOR)

            result_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
            gt_img = cv2.cvtColor(gt_img, cv2.COLOR_BGR2RGB)

            psnr = peak_signal_noise_ratio(gt_img, result_img)
            ssim = structural_similarity(gt_img, result_img, channel_axis=-1, win_size=7)
            mse = mean_squared_error(gt_img, result_img)

            results.append({
                'filename': filename,
                'PSNR': psnr,
                'SSIM': ssim,
                'MSE': mse
            })

    return results


def save_metrics_to_csv(metrics, dataset_name):
    metrics_folder = f"metrics_{dataset_name}"
    os.makedirs(metrics_folder, exist_ok=True)
    output_csv = os.path.join(metrics_folder, f"{dataset_name}_metrics_report.csv")

    with open(output_csv, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['filename', 'PSNR', 'SSIM', 'MSE'])
        writer.writeheader()
        for result in metrics:
            writer.writerow(result)


def plot_metrics(metrics, dataset_name):
    psnr_values = [res['PSNR'] for res in metrics]
    ssim_values = [res['SSIM'] for res in metrics]
    mse_values = [res['MSE'] for res in metrics]

    x = np.arange(len(metrics))

    fig, axs = plt.subplots(3, 1, figsize=(12, 18), sharex=True)

    axs[0].bar(x, psnr_values, color='skyblue')
    axs[0].axhline(y=np.mean(psnr_values), color='r', linestyle='-', linewidth=2)
    axs[0].set_title('PSNR per Image')
    axs[0].set_ylabel('PSNR (dB)')

    axs[1].bar(x, ssim_values, color='lightgreen')
    axs[1].axhline(y=np.mean(ssim_values), color='r', linestyle='-', linewidth=2)
    axs[1].set_title('SSIM per Image')
    axs[1].set_ylabel('SSIM')

    axs[2].bar(x, mse_values, color='salmon')
    axs[2].axhline(y=np.mean(mse_values), color='r', linestyle='-', linewidth=2)
    axs[2].set_title('MSE per Image')
    axs[2].set_ylabel('MSE')

    plt.xlabel('Image Index')  # Change xlabel to something generic

    plt.tight_layout()

    metrics_folder = f"metrics_{dataset_name}"
    os.makedirs(metrics_folder, exist_ok=True)
    output_plot = os.path.join(metrics_folder, f"{dataset_name}_metrics_plot.png")
    plt.savefig(output_plot)

    plt.show()


def print_extreme_cases(metrics, metric_name, top_n=3):
    sorted_metrics = sorted(metrics, key=lambda x: x[metric_name])
    worst_cases = sorted_metrics[:top_n]
    best_cases = sorted_metrics[-top_n:]

    result = ""
    result += f"\nTop {top_n} images with highest {metric_name}:\n"
    for idx, case in enumerate(reversed(best_cases), 1):
        result += f"{idx}. {case['filename']}: {metric_name}={case[metric_name]:.4f}\n"

    result += f"\nTop {top_n} images with lowest {metric_name}:\n"
    for idx, case in enumerate(worst_cases, 1):
        result += f"{idx}. {case['filename']}: {metric_name}={case[metric_name]:.4f}\n"

    return result


def save_average_and_extremes_to_txt(metrics, dataset_name):
    metrics_folder = f"metrics_{dataset_name}"
    os.makedirs(metrics_folder, exist_ok=True)
    output_txt = os.path.join(metrics_folder, f"{dataset_name}_metrics_summary.txt")

    with open(output_txt, mode='w') as file:
        file.write("Average Metrics:\n")
        file.write(f"Average PSNR: {np.mean([m['PSNR'] for m in metrics]):.4f}\n")
        file.write(f"Average SSIM: {np.mean([m['SSIM'] for m in metrics]):.4f}\n")
        file.write(f"Average MSE: {np.mean([m['MSE'] for m in metrics]):.4f}\n\n")

        file.write("Extreme Cases:\n")
        file.write(print_extreme_cases(metrics, 'PSNR'))
        file.write(print_extreme_cases(metrics, 'SSIM'))
        file.write(print_extreme_cases(metrics, 'MSE'))


if __name__ == "__main__":

    # result_dir = '../datasets/AID/AID_generated_chainner_900K_x3' #cambiar
    # gt_dir = '../datasets/AID/AID_HR_validation'
    # dataset_name = 'AID_Chainner_x3' #cambiar

    result_dir = '../datasets/DIV2K/DIV2K_ESRNET_generated_chainner_900K_x2' #cambiar
    gt_dir = '../datasets/DIV2K/DIV2K_valid_HR'
    dataset_name = 'DIV2K_RESRNET_900K_Chainner_x2' #cambiar

    metrics = calculate_metrics(result_dir, gt_dir)
    save_metrics_to_csv(metrics, dataset_name)

    average_psnr = np.mean([m['PSNR'] for m in metrics])
    average_ssim = np.mean([m['SSIM'] for m in metrics])
    average_mse = np.mean([m['MSE'] for m in metrics])

    print("\nAverage metrics:")
    print(f"Average PSNR: {average_psnr}")
    print(f"Average SSIM: {average_ssim}")
    print(f"Average MSE: {average_mse}")

    plot_metrics(metrics, dataset_name)
    save_average_and_extremes_to_txt(metrics, dataset_name)
