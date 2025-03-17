from rembg import remove
from PIL import Image
import io

def remove_background(image: bytes):
    """
    Удаляет фон с изображения

    :param image: Входное изображение
    :type image: bytes
    :return: Обработанное изображение с удаленным фоном
    :rtype: PIL.Image
    """
    input_image = Image.open(image).convert("RGBA")
    output_image = remove(input_image)

    return output_image


def replace_background(photo_bytes: bytes):
    """
    Заменяет фон на загруженном изображении (с использованием шаблона из backgrounds/)
    
    :param photo_bytes: Изображение, на котором нужно заменить фон
    :type photo_bytes: bytes
    :return: Изображение с замененным фоном
    :rtype: PIL.Image
    """
    background = Image.open("backgrounds/ex1.png").convert("RGBA")
    image = Image.open(io.BytesIO(photo_bytes)).convert("RGBA")

    width, height = image.size
    background = background.resize((width, height))

    new_background = background.copy()
    new_background.paste(image, (0, 0), image)

    return new_background
