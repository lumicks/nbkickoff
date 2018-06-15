"""Create IPython Notebooks from templates, using simple variable substitution

Some simple functions for creating IPython Notebooks from template IPYNB files.
During creation, occurrences of Jinja2-like variable references in cell sources
are substituted. E.g., if your notebook template cell contains the text

    some_python_code('{{ my_variable }}')

then creating the new notebook with a template variable dictionary of

    {'my_variable': 'lorem ipsum'}

will result in the final cell containing:

    some_python_code('lorem ipsum')
"""
import os

import nbformat


def substitute_template_vars(s, template_vars):
    for k, v in template_vars.items():
        s = s.replace('{{ %s }}' % k, v)
    return s


def fill_notebook_template(notebook, template_vars):
    for cell in notebook.cells:
        cell.source = substitute_template_vars(cell.source, template_vars)


def create_notebook_from_template(template_file, target_file, template_vars=None):
    if os.path.exists(target_file):
        raise FileExistsError(f"Target notebook file '{target_file}' already exists")

    notebook = nbformat.read(template_file, nbformat.current_nbformat)

    if template_vars:
        fill_notebook_template(notebook, template_vars)

    nbformat.write(notebook, target_file, nbformat.current_nbformat)

