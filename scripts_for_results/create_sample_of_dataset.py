import os
import random
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# Directorios donde están almacenadas las imágenes de entrenamiento y validación

# train_dir = '../datasets/DIV2K/DIV2K_train_HR'
# val_dir = '../datasets/DIV2K/DIV2K_valid_HR'

train_dir = '../datasets/AID/AID_train'
val_dir = '../datasets/AID/AID_validation'


# Función para obtener rutas aleatorias de imágenes del mismo tamaño
def get_random_image_paths_same_size(directory, num_images):
    image_paths = [os.path.join(directory, img) for img in os.listdir(directory)]
    random.shuffle(image_paths)

    # Filtrar imágenes que tengan el mismo tamaño
    selected_images = []
    for img_path in image_paths:
        with Image.open(img_path) as img:
            if len(selected_images) == 0:
                target_size = img.size
            if img.size == target_size:
                selected_images.append(img_path)
            if len(selected_images) >= num_images:
                break

    return selected_images


# Función para cargar y redimensionar imágenes manteniendo la proporción
def load_and_resize_image(image_path, target_size=(256, 256)):
    image = Image.open(image_path)
    image.thumbnail(target_size, Image.LANCZOS)
    # Crear una nueva imagen con el tamaño de destino y fondo blanco
    new_image = Image.new("RGB", target_size, (255, 255, 255))
    # Pegar la imagen redimensionada en el centro de la nueva imagen
    new_image.paste(image, ((target_size[0] - image.size[0]) // 2,
                            (target_size[1] - image.size[1]) // 2))
    return np.array(new_image)


# Función para crear un mosaico de imágenes
def create_image_mosaic(image_paths, mosaic_shape=(2, 4), figsize=(14, 7)):
    fig, axes = plt.subplots(mosaic_shape[0], mosaic_shape[1], figsize=figsize)
    axes = axes.flatten()

    for ax in axes:
        ax.axis('off')

    for i, img_path in enumerate(image_paths):
        image = load_and_resize_image(img_path)
        axes[i].imshow(image)

    # Ajustar los espacios entre las subtramas para que no haya espacios
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.margins(0, 0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())

    # Eliminar bordes adicionales
    plt.gcf().set_size_inches(figsize)
    plt.gcf().tight_layout(pad=0)
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    plt.show()


# Obtener rutas aleatorias de imágenes de entrenamiento y validación
num_images_per_set = 4
train_image_paths = get_random_image_paths_same_size(train_dir, num_images_per_set)
val_image_paths = get_random_image_paths_same_size(val_dir, num_images_per_set)

# Crear mosaico conjunto de imágenes
print("Mosaico conjunto de imágenes:")
combined_image_paths = train_image_paths + val_image_paths

# Imprimir las rutas de las imágenes seleccionadas
for path in combined_image_paths:
    print(path)

create_image_mosaic(combined_image_paths)
