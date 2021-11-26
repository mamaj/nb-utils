import re
from base64 import b64decode
from io import BytesIO

import nbformat
import numpy as np
from PIL import Image


def read_nb(file_path):
    return nbformat.read(file_path, as_version=nbformat.NO_CONVERT)


def iter_cell(nb, clue=None, cell_type='any'):
    CELL_TYPES = ['markdown', 'code']
    if cell_type == 'any':
        cell_type = CELL_TYPES
    else:
        assert cell_type in CELL_TYPES, f'{cell_type} not in {CELL_TYPES}'
        cell_type = [cell_type]

    clue = clue or ''
    return (
        cell
        for cell in nb['cells']
        if cell['cell_type'] in cell_type and clue in cell['source']
    )


def filter_between(str, before, after):
    if not str:
        return None

    pattern = re.escape(before) + '(.*?)' + re.escape(after)
    if ans := re.search(pattern, str, flags=re.S):
        return ans.group(1)


def filter_code(code, remove_comment=True, remove_indent=True):
    if not code:
        return None

    result = []
    for line in code.split('\n'):
        if remove_comment:
            line = line.split('#')[0]
        if remove_indent:
            line = line.strip()
        if line:
            result.append(line)
    return '\n'.join(result)


def search_nb(nb_path, cell_clue, before, after, remove_comment=True, remove_indent=True):
    nb = read_nb(nb_path)
    result = []
    for cell in iter_cell(nb, cell_clue):
        code = cell['source']
        code = filter_between(code, before, after)
        code = filter_code(code, remove_comment=remove_comment,
                           remove_indent=remove_indent)
        if code:
            result.append(code)
    return result


def b64_to_image(img_b64):
    return Image.open(BytesIO(b64decode(img_b64)))


def whiten_backgroud(image):
    new_image = Image.new("RGBA", image.size, "WHITE")
    new_image.paste(image, (0, 0), image)
    return new_image.convert('RGB')


def get_cell_b64images(cell):
    images = []
    if outputs := cell.get('outputs'):
        for output in outputs:
            if output['output_type'] == 'display_data' and 'image/png' in output['data']:
                img = output['data']['image/png']
                images.append(img)
    return images


def vstack_imgs(images):
    if not images:
        return []
    min_shape = sorted([(np.sum(i.size), i.size) for i in images])[0][1]
    images_resized = [img.resize(min_shape) for img in images]
    imgs_comb = np.vstack(images_resized)
    return Image.fromarray(imgs_comb)


def get_cell_images(cell, concat=False, remove_transparency=False):
    images = get_cell_b64images(cell)
    if not images:
        return None

    images = [b64_to_image(img) for img in images]

    if remove_transparency:
        images = [whiten_backgroud(img) for img in images]

    if concat:
        images = vstack_imgs(images)

    return images
