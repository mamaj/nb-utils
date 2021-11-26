from base64 import b64decode
from io import BytesIO

import numpy as np
from PIL import Image


def b64_to_image(img_b64):
    return Image.open(BytesIO(b64decode(img_b64)))


def whiten_backgroud(image):
    new_image = Image.new("RGBA", image.size, "WHITE")
    new_image.paste(image, (0, 0), image)
    return new_image.convert('RGB')


def vstack_imgs(images):
    if not images:
        return []
    min_shape = sorted([(np.sum(i.size), i.size) for i in images])[0][1]
    images_resized = [img.resize(min_shape) for img in images]
    imgs_comb = np.vstack(images_resized)
    return Image.fromarray(imgs_comb)
