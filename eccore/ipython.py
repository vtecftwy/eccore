# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs-dev/0_01_ipython.ipynb.

# %% ../nbs-dev/0_01_ipython.ipynb 2
from __future__ import annotations
from fastcore.test import test_fail
from functools import wraps
from IPython.core.getipython import get_ipython
from IPython.display import display, Markdown, display_markdown
from pathlib import Path
from typing import Any, List, Callable, Optional
from .core import safe_path, path_to_parent_dir, is_type, CurrentMachine

import numpy as np
import pandas as pd
import sys
import subprocess
import warnings

# %% auto 0
__all__ = ['run_cli', 'nb_setup', 'install_code_on_cloud', 'display_mds', 'display_dfs', 'pandas_nrows_ncols', 'display_full_df']

# %% ../nbs-dev/0_01_ipython.ipynb 5
# TODO: replace with fastcore run

def run_cli(cmd:str = 'ls -l'   # command to execute in the cli
           ):
    """Runs a cli command from jupyter notebook and print the shell output message
    
    Uses subprocess.run with passed command to run the cli command"""
    p = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
    print(str(p.stdout, 'utf-8'))

# %% ../nbs-dev/0_01_ipython.ipynb 8
# TODO: update using the ipython functions of fastcore

def nb_setup(
    autoreload:bool = True,       # True to set autoreload in this notebook
    paths:List[str|Path] = None   # Paths to add to the path environment variable
    ):
    """Use in first cell of notebook to set autoreload, and add system paths
    
    Always add a path to the directoruy 'src' if `srs` directory exists at the same level as the `nbs` directory.

    When the notebook is not located in a tree including the name `nbs`, `src` directory is searched at the same level
    as the directory in which the notebook is located.
    """
    #  Handle paths
    #  Add src if it exists
    nbs_root = path_to_parent_dir('nbs')
    p2src = (nbs_root / '../src').resolve().absolute()
    if p2src.is_dir():
        p = str(p2src.absolute())
        if p not in sys.path:
            sys.path.insert(0, p)
            print(f"Added path: {p2src.absolute()}")
    # Add passed paths
    if paths:
        for p in paths:
            if isinstance(p, Path): p = str(p.resolve().absolute())
            if p not in sys.path:
                sys.path.insert(1, p)
                print(f"Added path: {p}")

#   Setup auto reload
    if autoreload:
        ipshell = get_ipython()
        ipshell.run_line_magic('load_ext',  'autoreload')
        ipshell.run_line_magic('autoreload', '2')
        print('Set autoreload mode')

# %% ../nbs-dev/0_01_ipython.ipynb 18
def install_code_on_cloud(
    package_name:str, # project package name, e.g. metagentools or git+https://github.com/repo.git@main
    quiet:bool=False # install quietly with Trud
):
    """pip install the project code package, when nb is running in the cloud."""
    
    machine = CurrentMachine()

    if machine.is_colab:
        CLOUD = True
        print('The notebook is running on colab.', end=' ')
        print(f'Will install {package_name}')
    elif machine.is_kaggle:
        CLOUD = True
        print('The notebook is running on kaggle.', end=' ')
        print(f'Will install {package_name}')
    elif machine.is_local:
        CLOUD = False
        print('The notebook is running locally, will not automatically install project code')
    else:
        CLOUD = True
        print('The notebook is running on a cloud VM or the machine was not registered as local')
        print(f'Will install {package_name}')

    if CLOUD:
        print(f'Installing project code {package_name}')
        cmd = f"pip install -{'qq' if quiet else ''}U {package_name}"
        run_cli(cmd)
        print((f"{package_name} is installed."))

# %% ../nbs-dev/0_01_ipython.ipynb 23
def display_mds(
    *strings:str|tuple[str] # any number of strings with text in markdown format
):
    """Display one or several strings formatted in markdown format"""
    for string in strings:
        display_markdown(Markdown(data=string))

# %% ../nbs-dev/0_01_ipython.ipynb 27
def display_dfs(*dfs:pd.DataFrame       # any number of Pandas DataFrames
               ):
    """Display one or several `pd.DataFrame` in a single cell output"""
    for df in dfs:
        display(df)

# %% ../nbs-dev/0_01_ipython.ipynb 30
class pandas_nrows_ncols:
    """Context manager that sets the max number of rows and cols to apply to any output within the context"""
    def __init__(
        self, 
        nrows:int|None=None, # max number of rows to show; show all rows if `None`
        ncols:int|None=None, # max number of columns to show; show all columns if `None`
    ):
        self.nrows = nrows
        self.ncols = ncols
    
    def __enter__(self):
        self.max_rows = pd.options.display.max_rows
        self.max_cols = pd.options.display.max_columns
        pd.options.display.max_rows = self.nrows
        pd.options.display.max_columns = self.ncols
        return self.max_rows, self.max_cols

    def __exit__(self, exc_type, exc_value, exc_tb):
        pd.options.display.max_rows = self.max_rows
        pd.options.display.max_columns = self.max_cols

# %% ../nbs-dev/0_01_ipython.ipynb 44
def display_full_df(
    df:pd.DataFrame|pd.Series,  # `DataFrame` or `Series` to display
):
    """Display a pandas `DataFrame` or `Series` showing all rows and columns"""
    if is_type(df, pd.DataFrame, raise_error=False) or is_type(df, pd.Series, raise_error=False):
        with pandas_nrows_ncols():
            display(df)
    else:
        raise TypeError(f"df must me a pandas `DataFrame` or `Series`, not a {type(df)}")
