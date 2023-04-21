# nb-utils

Utility functions for extracting parts of a code cell, and images in cell outputs from Jupyter Notebook (`ipynb`) files.

✅ Useful for auto grading Jupyter notebook submissions!

## Requirements

`python 3.8+`  
`numpy`  
`nbformat`  
`pillow`

## Usage

```python
nb = read_nb('path/to/ipynb')

# get an iterator over cell dictionaries:
iter_cell(nb, cell_type='code') 

# Alternatively, you may add a part of the code you are looking for in a cell:
clue = 'parts of the code'
iter_cell(nb, clue, cell_type='code')


# or search in cells containing `cell_clue` return code between `before` and `after`:
search_nb(nb_path, cell_clue, before, after, remove_comment=True, remove_indent=True):

# get PIL images of a cell 
get_cell_images(cell, concat=False, remove_transparency=False)

```
