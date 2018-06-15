#!/usr/bin/env python3

from .__about__ import __summary__
import logging
import os
from pathlib import Path
import shutil
import sys
import webbrowser

import subprocess
CREATE_NEW_CONSOLE = 0x10

from notebook import notebookapp
from notebook.utils import url_path_join, url_escape

from .template import create_notebook_from_template


def is_relative_to(path, root_path):
    try:
        relpath = path.relative_to(root_path)
        return True
    except ValueError:
        return False


def find_running_server(notebook_file):
    notebook_path = Path(notebook_file).resolve(strict=True)
    servers = [s for s in notebookapp.list_running_servers()
               if is_relative_to(notebook_path, Path(s['notebook_dir']))]
    if servers:
        return max(servers, key=lambda s: len(Path(s['notebook_dir']).parts))
    else:
        return None


def launch_detached_process(*args):
    if sys.platform == 'win32':
        subprocess.Popen(args, close_fds=True, creationflags=CREATE_NEW_CONSOLE)
    else:
        os.spawnv(os.P_NOWAIT, args[0], args)


def open_notebook(notebook_file):
    """Open the given IPython Notebook file in an existing or a new Jupyter Notebook server"""
    server = find_running_server(notebook_file)
    if server:
        logging.info(f"Using existing Jupyter server at {server['url']} (serving from {server['notebook_dir']})")
        rel_path = Path(notebook_file).resolve(strict=True).relative_to(Path(server['notebook_dir']))
        url = url_path_join(server['url'], 'notebooks', url_escape(rel_path.as_posix()))

        nbapp = notebookapp.NotebookApp.instance()
        nbapp.load_config_file()
        browser = webbrowser.get(nbapp.browser or None)
        browser.open_new_tab(url)
    else:
        logging.info("Starting new Jupyter server to serve notebook file")
        launch_detached_process(sys.executable, '-m', 'notebook', '--NotebookApp.open_browser=True', notebook_file)


def kickoff(template_file, target_file):
    create_notebook_from_template(template_file, target_file, {})
    open_notebook(target_file)


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__summary__)
    parser.add_argument('-t', '--template', required=True, help='Template notebook file')
    parser.add_argument('-f', '--file', required=True, help='Target notebook file to create')
    args = parser.parse_args()
    kickoff(args.template, args.file)


if __name__ == '__main__':
    main()
