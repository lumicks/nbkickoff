#!/usr/bin/env python3

from .__about__ import (__summary__, __title__)
import logging
import os
from pathlib import Path
import sys
import webbrowser

import subprocess
CREATE_NEW_CONSOLE = 0x10

from notebook import notebookapp
from notebook.utils import url_path_join, url_escape
from notebook.extensions import install_nbextension_python, enable_nbextension_python

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

def enable_interactive():
    """Enable notebook interactive widgets and plots"""
    install_nbextension_python(module="ipympl", sys_prefix=True)
    install_nbextension_python(module="widgetsnbextension", sys_prefix=True)

    enable_nbextension_python(module="ipympl", sys_prefix=True)
    enable_nbextension_python(module="widgetsnbextension", sys_prefix=True)


def kickoff(template_file, target_file, variables):
    enable_interactive()
    create_notebook_from_template(template_file, target_file, variables)
    open_notebook(target_file)


def main():
    import argparse

    def parse_template_var(s):
        if '=' not in s:
            raise argparse.ArgumentTypeError('Invalid template variable specification: ' + s)
        parts = s.split('=', 1)
        return {parts[0]: parts[1]}

    class DictMergeAction(argparse.Action):
        def __call__(self, p, namespace, values, option_string=None):
            current_dict = dict()
            if hasattr(namespace, self.dest) and getattr(namespace, self.dest) is not None:
                current_dict = getattr(namespace, self.dest)
            for v in values:
                current_dict = {**current_dict, **v}
            setattr(namespace, self.dest, current_dict)

    parser = argparse.ArgumentParser(prog=__title__, description=__summary__)
    parser.add_argument('template', help='Template notebook file')
    parser.add_argument('target', help='Target notebook file to create')
    parser.add_argument('variable', action=DictMergeAction, type=parse_template_var, nargs='*',
                        help='Template variable in the format NAME=VALUE')
    args = parser.parse_args()
    kickoff(args.template, args.target, args.variable)


if __name__ == '__main__':
    main()

