# nbkickoff

Launch an IPython Notebook from a template notebook file.


## Requirements

Tested with:

* Jupyter Notebook 5.5 (or higher)
* Python 3.6

Should also work with other Python 3.x versions.


## Installation

For general use, you can install `nbkickoff` using _pip_:

    pip install nbkickoff

To upgrade to the latest version:

    pip install -U nbkickoff

For local development:

    git clone https://github.com/lumicks/nbkickoff.git
    cd nbkickoff
    pip install -e .


## Usage

Invoke using either the full:

    python -m nbkickoff TEMPLATEFILE TARGETFILE [VAR=VALUE [VAR2=VALUE ...]]

Or, if the corresponding entry point script is on the `PATH`, the shorter version:

    nbkickoff TEMPLATEFILE TARGETFILE [VAR=VALUE [VAR2=VALUE ...]]

Here, `TEMPLATEFILE` is an IPython Notebook file that functions as a template. This file is copied to `TARGETFILE` (which must not exist yet), after which all variables in the notebook's cells are substituted with their corresponding values.

So, if your template notebook contains a cell with the text:

    my_python_var = '{{ foo }}'

and you invoke `nbkickoff` using:

    nbkickoff template.ipynb my_notebook.ipynb foo=bar

Then your shiny new notebook will have a cell containing:

    my_python_var = 'bar'

If a suitable Jupyter server process is already running, `nbkickoff` opens the new notebook in the existing server. Otherwise, a new Jupyter server process is started. This behavior is based on that of the [_nbopen_ tool](https://github.com/takluyver/nbopen/), with the notable change that `nbkickoff` always returns immediately; any newly spawned Jupyter server process is detached.

