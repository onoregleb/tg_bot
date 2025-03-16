from rembg import remove
from PIL import Image
import io

def remove_background(image: bytes):
    input_image = Image.open(image).convert("RGBA")
    output_image = remove(input_image)

    return output_image


def replace_background(photo_bytes: bytes):
    background = Image.open("backgrounds/ex1.png")
    image = Image.open(io.BytesIO(photo_bytes)).convert("RGBA")

    width, height = image.size
    new_background = Image.new("RGBA", (width, height), background)

    new_background.paste(image, (0, 0), image)

    return new_background
