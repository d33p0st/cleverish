from colorama import Fore as f
from os.path import join
from os import listdir
from typing import List
import subprocess, re

from prompt_toolkit import PromptSession, HTML
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter, PathCompleter, Completer, merge_completers

class _InteractiveShell:
    """Interactive Shell Wrap"""
    def __init__(self, bin_path: str) -> None:
        """`create shell wrapper object`"""
        ...
    
    def _execute(self, command: List[str]) -> None:
        """`run command`"""
        ...
    
    def _strip_ansi(self, text: str) -> str:
        """`stripped ansi`"""
        ...
    
    def _get_completer(self) -> Completer:
        """merge and return completers"""
        ...
    
    def start_shell(self, prompt: HTML, stop: List[str]) -> None:
        """start the interactive shell.
        
        #### Parameters

        - `prompt`: This is <class 'prompt_toolkit.HTML'>
        - `stop`: List of stop keywords
        """
        ...

class TerminalEmulator:
    """`Terminal Emulator for Enviroment`"""
    def __init__(self, env: str, bin_path: str) -> None:
        """Create a Terminal Emulator Object"""
        ...
    
    @property
    def start(self) -> None:
        """`Start`"""
        ...