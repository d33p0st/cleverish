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
    def __init__(self, bin_path: str):
        self.bin_path = bin_path
        self.session = PromptSession(history=InMemoryHistory())
        self.command_history = []
        self.path_completer = PathCompleter()
        self.command_completer = WordCompleter(self.command_history, ignore_case=True)
        self.ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    
    def _execute(self, command: List[str]):
        if command[0] in listdir(self.bin_path):
            command[0] = join(self.bin_path, command[0])

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError:
            pass
        except (KeyboardInterrupt, EOFError):
            pass
        except Exception:
            pass
    
    def _strip_ansi(self, text):
        return self.ansi_escape.sub('', text)

    def _add_to_history(self, command: str):
        stripped_command = self._strip_ansi(command.strip())
        if stripped_command and (not self.command_history or self.command_history[-1] != stripped_command):
            self.command_history.append(stripped_command)
    
    def _get_completer(self):
        return merge_completers([WordCompleter(self.command_history), self.path_completer])
    
    def start_shell(self, prompt: HTML, stop: List[str]):
        print(f"\n{f.GREEN}Emulator Enabled.{f.RESET} use \'/stop\', \'stop\', or \'deactivate\' to exit.")
        print(f"{f.YELLOW}NOTE{f.RESET}: This emulator is meant for pip, python, cleverish and any bins installed in the environment only.")
        
        # add stop commands in history.
        # and a few custom
        custom = [
            'clever init','clever shell', 'clever add', 
            'clever install', 'clever help', 'pip install', 
            'pip uninstall', 'python -m pip install --upgrade pip',
            'python -m', 'clear'
        ]
        for stop_command in stop + custom:
            self._add_to_history(stop_command)

        while True:
            try:
                self.session.completer = self._get_completer()

                user_input = self.session.prompt(prompt, auto_suggest=AutoSuggestFromHistory())

                if user_input.strip().lower() in stop:
                    print(f"{f.GREEN}exit.{f.RESET}")
                    break

                self._add_to_history(user_input)
                self._execute(user_input.split())
            except (KeyboardInterrupt, EOFError):
                print(f"{f.GREEN}exit.{f.RESET}")
                break

class TerminalEmulator:
    def __init__(self, env: str, bin_path: str) -> None:
        self.env = env
        self.bin_path = bin_path
    
    @property
    def start(self) -> None:
        stop_keywords = ['/stop', 'stop', 'deactivate', 'exit', 'quit', ':q']

        shell = _InteractiveShell(self.bin_path)
        shell.start_shell(HTML(f'(<ansiblue>{self.env})</ansiblue> <ansigreen>> </ansigreen>'), stop_keywords)
        
        