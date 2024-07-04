from PIL import Image, ImageDraw, ImageFont
from random import randrange
import os

font = ImageFont.truetype('../fonts/Poppins-Medium.ttf', 40)


def procesar_imagen(imagen_path, coords, ancho, margen=8):
    # Cargar la imagen
    imagen = Image.open(imagen_path)

    aspect_ratio = imagen.width / imagen.height
    target_width = ancho - margen * 2

    new_height = target_width / (aspect_ratio + 1)
    new_width = target_width - new_height

    new_width = int(round(new_width))
    new_height = int(round(new_height))

    imagen = imagen.resize((new_width, new_height))
    draw = ImageDraw.Draw(imagen)

    if (len(coords) == 0):
        size = 110
        x = randrange(0, int(new_width / 2) - size)
        y = randrange(0, int(new_height / 2) - size)
        coords.append((x, y, x + size, y + size))

        x = randrange(int(new_width / 2), new_width - size)
        y = randrange(0, int(new_height / 2) - size)
        coords.append((x, y, x + size, y + size))

        x = randrange(0, int(new_width / 2) - size)
        y = randrange(int(new_height / 2), new_height - size)
        coords.append((x, y, x + size, y + size))

        x = randrange(0, int(new_width / 2) - size)
        x = randrange(int(new_width / 2), new_width - size)
        coords.append((x, y, x + size, y + size))

    # Crear subimágenes recortadas según las coordenadas proporcionadas
    recuadros = []
    for i, coord in enumerate(coords):
        # Recortar la subimagen
        recuadro = imagen.crop(coord)
        recuadros.append(recuadro)
        # Dibujar el recuadro en la imagen original
        draw.rectangle([(coord[0] - 1, coord[1] - 1), (coord[2] + 1, coord[3] + 1)], outline="black",
                       width=int(margen / 2) + 2)
        draw.rectangle(coord, outline="yellow", width=int(margen / 2))
        # draw.text((coord[0] - 30, coord[1] - 5), str(i), 'black', font, stroke_width=2)
        # draw.text((coord[0] - 30, coord[1] - 5), str(i), 'yellow', font)

    return imagen, recuadros


def crear_imagen_compuesta(recuadros, margen=0):
    # Determinar el tamaño de cada recuadro y de la imagen compuesta
    ancho, alto = recuadros[0].size
    ancho_compuesto = 2 * ancho + margen
    alto_compuesto = 2 * alto + margen

    # Crear una nueva imagen compuesta
    imagen_compuesta = Image.new('RGB', (ancho_compuesto, alto_compuesto), 'white')

    # Pegar los recuadros en la imagen compuesta
    imagen_compuesta.paste(recuadros[0], (0, 0))
    imagen_compuesta.paste(recuadros[1], (ancho + margen, 0))
    imagen_compuesta.paste(recuadros[2], (0, alto + margen))
    imagen_compuesta.paste(recuadros[3], (ancho + margen, alto + margen))

    return imagen_compuesta


def crear_imagen_compuesta_compuesta(imagen, imagen_compuesta, title, ancho, margen=5):
    imagen_compuesta_compuesta = Image.new('RGB', (ancho, 60 + imagen.height + margen * 2), 'white')
    draw = ImageDraw.Draw(imagen_compuesta_compuesta)

    draw.text((margen, margen), title, 'black', font)

    imagen_compuesta_compuesta.paste(imagen, (margen, 60 + margen))

    imagen_compuesta = imagen_compuesta.resize((imagen.height, imagen.height))
    draw = ImageDraw.Draw(imagen_compuesta)
    x = int(imagen_compuesta.width / 2)
    y = int(imagen_compuesta.height / 2)
    draw.line([(x, 0), (x, imagen_compuesta.height)], 'white', 5)
    draw.line([(0, y), (imagen_compuesta.width, y)], 'white', 5)

    imagen_compuesta_compuesta.paste(imagen_compuesta, (imagen.width + margen * 2, 60 + margen))

    return imagen_compuesta_compuesta


def guardar_resultados(imagen_compuesta, output_folder):
    # Crear directorio para guardar los resultados de esta imagen
    # os.makedirs(output_folder, exist_ok=True)

    # Guardar la imagen compuesta
    imagen_compuesta.save(output_folder + '_imagen_compuesta.png')


def crear_imagen_compuesta_compuesta_compuesta(path_original, path_resultado, path_esperado, output_folder, coords=[],
                                               ancho=1200, margen=10):
    imagen, recuadros = procesar_imagen(path_original, coords, ancho)
    imagen_compuesta = crear_imagen_compuesta(recuadros)
    imagen_compuesta_compuesta_original = crear_imagen_compuesta_compuesta(imagen, imagen_compuesta, 'Low Resolution',
                                                                           ancho)

    imagen, recuadros = procesar_imagen(path_resultado, coords, ancho)
    imagen_compuesta = crear_imagen_compuesta(recuadros)
    imagen_compuesta_compuesta_resultado = crear_imagen_compuesta_compuesta(imagen, imagen_compuesta, 'Generated',
                                                                            ancho)

    imagen, recuadros = procesar_imagen(path_esperado, coords, ancho)
    imagen_compuesta = crear_imagen_compuesta(recuadros)
    imagen_compuesta_compuesta_esperada = crear_imagen_compuesta_compuesta(imagen, imagen_compuesta, 'High Resolution',
                                                                           ancho)

    altura = imagen_compuesta_compuesta_original.height + imagen_compuesta_compuesta_resultado.height + imagen_compuesta_compuesta_esperada.height

    imagen_compuesta_compuesta_compuesta = Image.new('RGB', (ancho, altura + margen * 2), 'white')
    imagen_compuesta_compuesta_compuesta.paste(imagen_compuesta_compuesta_original, (0, 0))
    imagen_compuesta_compuesta_compuesta.paste(imagen_compuesta_compuesta_resultado,
                                               (0, margen + imagen_compuesta_compuesta_original.height))
    imagen_compuesta_compuesta_compuesta.paste(imagen_compuesta_compuesta_esperada, (
    0, margen + imagen_compuesta_compuesta_original.height + margen + imagen_compuesta_compuesta_resultado.height))

    imagen_compuesta_compuesta_compuesta.show()

    nombre_imagen = os.path.splitext(os.path.basename(path_original))[0]
    output_folder_imagen = os.path.join(output_folder, nombre_imagen)
    guardar_resultados(imagen_compuesta_compuesta_compuesta, output_folder_imagen)

# Directorio donde se guardarán los resultados
output_folder = 'resultados'


# coords_gato = [
#     (220, 40, 330, 150),
#     (1000, 250, 1110, 360),
#     (360, 600, 470, 710),
#     (540, 690, 650, 800)
# ]
#
# coords_lago = [
#     (590, 190, 700, 300),
#     (1000, 180, 1110, 290),
#     (550, 480, 660, 590),
#     (740, 480, 850, 590)
# ]

# coords_escuela = [
#     (225, 300, 335, 410),
#     (775, 130, 885, 240),
#     (360, 530, 470, 640),
#     (630, 900, 740, 1010)
# ]

# coords_playa = [
#     (225, 300, 335, 410),
#     (775, 130, 885, 240),
#     (360, 530, 470, 640),
#     (630, 900, 740, 1010)
# ]
#
coords_estatua = [
    (560, 300, 670, 410),
    (700, 325, 810, 435),
    (530, 475, 640, 585),
    (725, 630, 835, 740)
]
#
# coords_pinguino = [
#     (30, 115, 140, 225),
#     (390, 180, 500, 290),
#     (55, 985, 165, 1095),
#     (400, 835, 510, 945)
# ]

# crear_imagen_compuesta_compuesta_compuesta('../datasets/DIV2K/DIV2K_valid_LR_bicubic/0838x2.png', '../datasets/DIV2K/DIV2K_result_chainner_70K_RealEsrgan/0838x2.png', '../datasets/DIV2K/DIV2K_valid_HR/0838.png',output_folder,coords_gato, 2040, 5)

#crear_imagen_compuesta_compuesta_compuesta('../datasets/DIV2K/DIV2K_valid_LR_x2/0868_downscale_x2.png', '../datasets/DIV2K/DIV2K_generated_chainner_900K_x2/0868_generated_x2.png', '../datasets/DIV2K/DIV2K_valid_HR/0868.png',output_folder, coords_estatua, 2040, 5)

# crear_imagen_compuesta_compuesta_compuesta('../datasets/AID/AID_LR_validation_x2/Beach_beach_115_sliced_x2.png', '../datasets/AID/AID_generated_chainner_900K_x2/Beach_beach_115_generated_x2.png', '../datasets/AID/AID_HR_validation/Beach_beach_115.jpg',output_folder, coords_playa, 2040, 5)