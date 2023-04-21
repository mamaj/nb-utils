import nbformat

from .utils import image_utils
from .utils import image_utils


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


def search_nb(nb_path, cell_clue=None, before=None, after=None, remove_comment=True, remove_indent=True):
    nb = read_nb(nb_path)
    result = []
    for cell in iter_cell(nb, cell_clue):
        code = cell['source']
        code = image_utils.filter_between(code, before, after)
        code = image_utils.filter_code(code, remove_comment=remove_comment,
                                     remove_indent=remove_indent)
        if code:
            result.append(code)
    return result


def get_cell_b64images(cell):
    images = []
    if outputs := cell.get('outputs'):
        for output in outputs:
            if output['output_type'] == 'display_data' and 'image/png' in output['data']:
                img = output['data']['image/png']
                images.append(img)
    return images


def get_cell_images(cell, concat=False, remove_transparency=False):
    images = get_cell_b64images(cell)
    if not images:
        return None

    images = [image_utils.b64_to_image(img) for img in images]

    if remove_transparency:
        images = [image_utils.whiten_backgroud(img) for img in images]

    if concat:
        images = image_utils.vstack_imgs(images)

    return images
