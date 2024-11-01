from os import (
    listdir,
    getcwd,
    makedirs,
    name as osname,
    environ,
    unlink,
    system as run,
    popen as get_output_of
)

if osname != 'nt':
    from os import geteuid

from os.path import join, basename, exists, dirname
from typing import Union, Tuple, List, Dict
from pathlib import Path
from colorama import Fore as _
from packaging import version
from packaging.specifiers import SpecifierSet, InvalidSpecifier
import subprocess, sys, venv, ctypes, requests

from .exceptions import NonEmptyDirectory
from .utils import Tomler, ConfigurationInterpreter, TerminalEmulator
from .utils.dotlock import DotLock

class _ConstantTextContents:

    HELP = f"""{_.GREEN},-----------,{_.RESET} ,------------------,
{_.GREEN}|{_.RESET} Help Text {_.GREEN}|{_.RESET}-| {_.BLUE}Cleverish{_.RESET} v{_.RED}0.0.2{_.RESET} |
{_.GREEN}'-----------'{_.RESET} '------------------'

Credits: Soumyo Deep Gupta (d33p0st (GitHub)) 2024
License: MIT

Syntax: {_.BLUE}clever{_.RESET} [OPTIONS] [OPTION-VALUES] [SUB OPTIONS]

{_.YELLOW}[OPTIONS]{_.RESET}
help (-h)            :  Show this help text and exit.

init (-i)            :  Initialize an empty project.
      {_.YELLOW}[SUB OPTIONS]{_.RESET} (When using init, these can be used with it)
      force (-f)     :  If the current directory is non-empty, init
                        will raise NonEmptyDirectory Error. To force
                        it, use this flag.
    
      package (-pkg) :  Use this flag if you want to create a package
                        type project (src/<package_name>/__init__.py)
                        else it will be (src/__init__.py) type structure.
    
      name (-n)      :  Set the package name. If not provided, enclosing
                        directory name will be used as package name.
                        NOTE: If (-pkg) flag is not given but (-n) is given
                        (-pkg) flag will be auto-added.

add (-a)             :  Add a dependency.
      Syntax: {_.BLUE}clever{_.RESET} add <package-name-1> <package-2> ...

install (-in)        : Install all dependencies if not, update dot-lock
                       and toml file with any shadow installed packages
                       (packges that are installed but not added through
                       cleverish.)

      Syntax: {_.BLUE}clever{_.RESET} install

shell (-sh)          : Activates the clever shell. with current project
                       virtual environment. All bins like `pip` or `python`
                       or any newly installed libs that contains callable
                       bins, if called through clever shell will be searched
                       in the project environment first and then global.

build (-b)           : Build the project based on pyproject.toml and clever.toml
                       leveraging the packages locked in dot-lock file.
            
upload (-u)          : Upload the package to PYPI.

      Syntax: {_.BLUE}clever{_.RESET} upload <dist-folder-name-or-path>
"""

    PYPROJECT_TOML = """# Generated using Cleverish

[build-system]
requires = ["setuptools>=42", "wheel"] # Auto generated with cleverish, you can change it as per your needs
build-backend = "setuptools.build_meta" # Auto generated with cleverish, you can change it as per your needs
    
[project]
name = "{}"
version = "0.0.1"
description = "Auto Generated Text using Cleverish"
readme = { file = "README.md", content-type = "text/markdown"}
license = { file = "LICENSE" }
"""

    DEMO_CLEVERISH_TOML = """
[config]
environment_name = \'{}\'

[requirements]
dependency_directory = 'deps'
get-automatically = false
list = []
"""

class DriverConfiguration:
    def __init__(self) -> None:
        self._forceful_initialization: bool = False
        self._package_name: Union[str, None] = None
        self._package: bool = False
        self._ws: bool = False
        self._tomler: Tomler
        self._to_add: Union[str, List[str], None,] = None
        self._upload_directory: Union[str, None] = None
    
    def set_force(self, value: bool) -> None:
        self.forceful_initialization = value
    
    def set_package_name(self, value: Union[str, None]) -> None:
        self.package_name = value
    
    def set_package_status(self, value: bool) -> None:
        self.package = value
    
    def set_tomler(self, value: Tomler) -> None:
        self._tomler = value
    
    def set_to_add(self, value: Union[str, List[str], None]) -> None:
        self._to_add = value
    
    def set_upload_directory(self, value: Union[str, None]) -> None:
        self._upload_directory = value
    
    def set_without_shell(self, value: bool) -> None:
        self._ws = value
    
    @property
    def forceful_initialization(self) -> bool:
        return self._forceful_initialization
    
    @forceful_initialization.setter
    def forceful_initialization(self, force: bool) -> None:
        self._forceful_initialization = force
    
    @forceful_initialization.deleter
    def forceful_initialization(self) -> None:
        self.forceful_initialization = False
    
    @property
    def package_name(self) -> Union[str, None]:
        return self._package_name
    
    @package_name.setter
    def package_name(self, name: Union[str, None]) -> None:
        self._package_name = name
        if self._package_name:
            self.package = True
    
    @package_name.deleter
    def package_name(self) -> None:
        self.package_name = None
    
    @property
    def package(self) -> bool:
        return self._package
    
    @package.setter
    def package(self, pkg: bool) -> None:
        self._package = pkg
    
    @package.deleter
    def package(self) -> None:
        self.package = False
    
    @property
    def tomler(self) -> Tomler:
        return self._tomler
    
    @tomler.setter
    def tomler(self, tomler: Tomler) -> None:
        self._tomler = tomler
    
    @tomler.deleter
    def tomler(self) -> None:
        self._tomler = None
    
    @property
    def to_add(self) -> Union[str, List[str], None]:
        return self._to_add
    
    @to_add.setter
    def to_add(self, value: Union[str, List[str], None]) -> None:
        self._to_add = value
    
    @to_add.deleter
    def to_add(self) -> None:
        self._to_add = None
    
    @property
    def upload_directory(self) -> Union[str, None]:
        return self._upload_directory
    
    @upload_directory.setter
    def upload_directory(self, value: Union[str, None]) -> None:
        self._upload_directory = value
    
    @upload_directory.deleter
    def upload_directory(self) -> None:
        self._upload_directory = None
    
    @property
    def without_shell(self) -> bool:
        return self._ws
    
    @without_shell.setter
    def without_shell(self, v: bool) -> None:
        self._ws = v
    
    @without_shell.deleter
    def without_shell(self) -> None:
        self._ws = False

class _DriverMethods:
    @staticmethod
    def create_init_file_at(location: str) -> None:
        with open(join(location, '__init__.py'), 'w+') as reference:
            reference.write("# Init File - Auto Generated Through Cleverish.")
    
    @staticmethod
    def create_pyproject_toml_at(location: str, name: str) -> None:
        with open(join(location, 'pyproject.toml'), 'w+') as reference:
            reference.write(_ConstantTextContents.PYPROJECT_TOML.replace("{}", name))
    
    @staticmethod
    def create_cleverish_toml_at(location: str, name: str) -> None:
        with open(join(location, 'clever.toml'), 'w+') as reference:
            reference.write(_ConstantTextContents.DEMO_CLEVERISH_TOML.replace("{}", name))

class Drivers:
    @staticmethod
    def has_admin_priviledge() -> bool:
        if osname != 'nt':
            return geteuid() == 0
        else:
            try:
                return ctypes.windll.shell32.IsUserAnAdmin()
            except AttributeError:
                return False
    
    @staticmethod
    def relaunch_with_admin_priviledge() -> None:
        if osname != 'nt':
            try:
                subprocess.check_call(['sudo'] + sys.argv)
            except subprocess.CalledProcessError:
                print(f"{_.RED}Failed{_.RESET} to run with sudo.\nRun the following to run it as root.\n{_.YELLOW}sudo{_.RESET} " + ' '.join(sys.argv))
                sys.exit(1)
        else:
            try:
                ctypes.windll.shell32.shellExecute(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            except Exception:
                print(f"{_.RED}Failed{_.RESET} to elevate priviledge automatically. Run it in administrator cmd/powershell.")
                sys.exit(1)
        
        sys.exit(0)
    
    @staticmethod
    def clever_toml() -> bool:
        files = listdir(getcwd())
        return 'clever.toml' in files or 'Clever.toml' in files

    @staticmethod
    def help() -> None:
        print(_ConstantTextContents.HELP)
        sys.exit(0)
    
    @staticmethod
    def init(config: DriverConfiguration) -> None:
        # # Initiate root if not root.
        # if not Drivers.has_admin_priviledge():
        #     Drivers.relaunch_with_admin_priviledge()

        # Get Contents of the current directory if not force
        if not config.forceful_initialization:
            files_in_current_directory = listdir(getcwd())
            
            if '.git' in files_in_current_directory:
                files_in_current_directory.remove('.git')
            
            if files_in_current_directory:
                raise NonEmptyDirectory(NonEmptyDirectory.NOT_EMPTY.format(getcwd()) + " Init Failed.")
        
        # create src
        makedirs(join(getcwd(), 'src'), exist_ok=True)

        package_name = None

        # create a directory under src if package else just create __init__.py
        if not config.package:
            # Not a package
            _DriverMethods.create_init_file_at(join(getcwd(), 'src'))
        else:
            # IT is a package.
            # check if name is provided
            package_name: str
            if config.package_name:
                package_name = config.package_name
                # Create the package name dir
                makedirs(join(getcwd(), 'src', config.package_name), exist_ok=True)
                # create init file inside
                _DriverMethods.create_init_file_at(join(getcwd(), 'src', config.package_name))
            else:
                # If name not provided,
                # get name of the current dir.
                package_name = basename(getcwd())
                # create the package name dir
                makedirs(join(getcwd(), 'src', package_name), exist_ok=True)
                _DriverMethods.create_init_file_at(join(getcwd(), 'src', package_name))
        
        # src -> ?Package_name_dir? -> __init__.py COMPLETE HERE

        # create a pyproject.toml
        _DriverMethods.create_pyproject_toml_at(getcwd(), package_name if package_name else basename(getcwd()))

        # create demo cleverish.toml
        _DriverMethods.create_cleverish_toml_at(getcwd(), package_name if package_name else basename(getcwd()))

        # If not a git repository, run git init
        if not exists(join(getcwd(), '.git')):
            try:
                subprocess.check_call(['git', 'init'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                print(f"{_.RED}Git repository at this location cannot be created.{_.RESET} Create manually if needed.")
        
        print(f"{_.GREEN}Succesfully created{_.RESET} empty project at current directory.")

        # tomler needs to be created and added to config for env
        new_config = DriverConfiguration()
        new_config.set_force(config.forceful_initialization)
        new_config.set_package_name(config.package_name)
        new_config.set_package_status(config.package)
        new_config.tomler = Tomler()
        new_config.set_without_shell(config.without_shell)
        Drivers.create_environment(config=new_config) # create env too
        sys.exit(0)
    
    @staticmethod
    def create_environment(config: DriverConfiguration) -> None:
        print(f"{_.YELLOW}Creating Environment...{_.RESET}", end='\r')
        # get tomler
        tomler = config.tomler
        interpreted_tomler = ConfigurationInterpreter.interpret(tomler)

        # create environment
        env_path = Path(f'./.{interpreted_tomler.environment_name}')
        if not env_path.exists() or config.forceful_initialization:
            venv.create(env_path, with_pip=True)
        else:
            print("                                                  ", end='\r')
            print(f"{_.YELLOW}Environment Exists{_.RESET}")
            print(f"Run: {_.BLUE}clever{_.RESET} shell")
            sys.exit(0)
        
        if osname == 'nt':
            activator = env_path / 'Scripts' / 'activate'
        else:
            activator = env_path / 'bin' / 'activate'
        
        print(f"{_.GREEN}Environment created as per configuration.{_.RESET}")

        print(f"{_.YELLOW}Installing requirements (if any) ...{_.RESET}", end='\r')

        skipped, total = Drivers.install_dependencies(config, False, ['build', 'twine'], []) # later on add cleverish
        print(f"                                                                  ", end='\r')
        
        if skipped == total:
            print(f"{_.RED}Failed{_.RESET} to install dependencies.")
        elif skipped > 0:
            print(f"requirements {_.GREEN}Installed{_.RESET} {_.YELLOW}(partially){_.RESET}")
            print(f"{_.YELLOW}Skipped{_.RESET} {skipped} dependencies.")
        else:
            print(f"requirements {_.GREEN}Installed{_.RESET}")

        if not config.without_shell:
            TerminalEmulator(env=interpreted_tomler.environment_name, bin_path=dirname(str(activator))).start
    
    @staticmethod
    def shell(config: DriverConfiguration) -> None:
        itomler = ConfigurationInterpreter.interpret(config.tomler)
        env_path = Path(f'./.{itomler.environment_name}')
        
        if not env_path.exists():
            print(f"({_.BLUE}{itomler.environment_name}{_.RESET}) {_.RED}Environment Does Not Exist{_.RESET}")
            print(f"Run: {_.BLUE}clever{_.RESET} init")
            print(f"For more information: {_.BLUE}clever{_.RESET} help")
            sys.exit(1)
        
        if osname == 'nt':
            bin_p = env_path / 'Scripts'
        else:
            bin_p = env_path / 'bin'
        
        TerminalEmulator(env=itomler.environment_name, bin_path=bin_p).start
    
    @staticmethod
    def get_all_versions(name: str) -> List[str]:
        url = f"https://pypi.org/pypi/{name}/json"
        try:
            response = requests.get(url)
            try:
                response.raise_for_status()
            except requests.HTTPError:
                print(f"{_.RED}Failed{_.RESET} to resolve dependency for {name}.")
                sys.exit(1)
            data = response.json()
            return sorted(data["releases"].keys(), key=version.parse, reverse=True)
        except requests.exceptions.RequestException:
            print(f"{_.RED}Failed{_.RESET} to resolve dependency for {name}.")
            sys.exit(1)
    
    @staticmethod
    def get_latest_compatible_version(name: str, constraint: str) -> Union[str, None]:
        available = Drivers.get_all_versions(name)
        try:
            compatible = [v for v in available if version.parse(v) in SpecifierSet(constraint)]
        except InvalidSpecifier:
            print(f"{_.RED}Invalid Specifier{_.RESET}: \'{constraint}\' for {name}.")
            sys.exit(1)
        
        return compatible[0] if compatible else None

    @staticmethod
    def resolve_dependencies(dependencies: List[Dict[str, str]]) -> List[Dict[str, str]]:
        resolved = []
        for dep in dependencies:
            name = dep.get('name', None)
            constraint = dep.get('version', None)
            if not name:
                resolved.append(dep) # will be skipped later in "install_dependencies"
                continue

            if not constraint:
                resolved.append(dep) # name but no version. will be handled in "install_dependencies"
                continue

            specific_v = Drivers.get_latest_compatible_version(name, constraint)
            resolved.append({"name": name, "version": specific_v})
        return resolved

    @staticmethod
    def install_dependencies(config: DriverConfiguration, explicit: bool = True, extras: List[str] = [], user_given: List[str] = []) -> Tuple[int, int]:
        itomler = ConfigurationInterpreter.interpret(config.tomler)
        if not exists(join(getcwd(), 'clever.lock')):
            dependencies = Drivers.resolve_dependencies(itomler.requirements_list)
            for x in dependencies:
                user_given.append(x['name'])
        else:
            dependencies = DotLock.load()
        
        for x in extras:
            dependencies.append({"name": x})
        
        env_path = Path(f'./.{itomler.environment_name}') / "bin" if osname != 'nt' else Path(f'./.{itomler.environment_name}') / "Scripts"
        pip_path = env_path / 'pip'
        py_path = env_path / 'python'

        skip_count = 0
        for dependency in dependencies:
            name = dependency.get('name', None)
            version = dependency.get('version', None)

            if not name:
                skip_count += 1
                continue

            list_of_i = get_output_of(f"{pip_path} list --format=freeze").readlines()
            v_to_check = None
            for i in range(len(list_of_i)):
                if name in list_of_i[i]:
                    list_of_i[i] = list_of_i[i].replace('\n', '')
                    v_to_check = list_of_i[i].split('==')[1]
                    break
            
            # if not pip and (either (current_installed_version != version) or (no current_installed_version))
            if name != 'pip' and ((v_to_check and v_to_check != version) or (not v_to_check)):
                icommand = f"{pip_path} install {name}" + ("" if version is None else f"=={version}")

                try:
                    subprocess.run(icommand.split(), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    if explicit:
                        print(f"{_.GREEN}Added{_.RESET} {name}.")
                except subprocess.CalledProcessError:
                    print(f"{_.RED}Failed{_.RESET} to install {name}. {_.YELLOW}Skipping{_.RESET}")
                    skip_count += 1
                    continue
            elif {"name": "pip", "version": Drivers.get_all_versions('pip')[0]} not in dependencies:
                try:
                    subprocess.run(f"{py_path} -m pip install --upgrade pip".split(), check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                    print(f"{_.GREEN}Upgraded{_.RESET} pip -> {Drivers.get_all_versions('pip')[0]}")
                except subprocess.CalledProcessError:
                    print(f"{_.RED}Failed{_.RESET} to upgrade pip. {_.GREEN}An upgrade is available{_.RESET}")
                    sys.exit(0)
            else:
                skip_count += 1
        
        # get list of installed versions from pip
        list_of_installed = get_output_of(f"{pip_path} list --format=freeze").readlines()
        dependency_list_complete = []

        for i in range(len(list_of_installed)):
            list_of_installed[i] = list_of_installed[i].replace('\n', '')
            name, version = tuple(list_of_installed[i].split('=='))
            if name not in user_given:
                continue
            dependency_list_complete.append(
                {
                    "name": name,
                    "version": version,
                    "dependencies": Drivers._find_required_dependencies(pip_path, [name])
                }
            )

        DotLock.create(dependencies=dependency_list_complete)
        
        tomler = config.tomler
        itomler = ConfigurationInterpreter.interpret(tomler)
        current_requirement_menu = tomler.fetch_entry('requirements')
        current_requirement_menu['list'] = dependency_list_complete
        tomler.add_or_modify_entry('requirements', current_requirement_menu)

        return skip_count, len(dependencies)
    
    @staticmethod
    def user_install_dependencies(config: DriverConfiguration) -> Tuple[int, int]:
        return Drivers.install_dependencies(config, True, [], [x['name'] for x in ConfigurationInterpreter.interpret(config.tomler).requirements_list])

    @staticmethod
    def _strip(string: str) -> str:
        return string.strip()
    
    @staticmethod
    def _find_required_dependencies(pip_path: Path, to_check: List[str]) -> List[str]:
        # consider all the packages provided are already installed.
        deps = []
        for each in to_check:
            data = get_output_of(f'{pip_path} show {each}').readlines()
            for line in data:
                if 'Requires' in line:
                    line = line.replace('\n', '')
                    line = line.split(':')[1].strip()
                    if line != '':
                        deps_here = list(map(Drivers._strip, line.split(',')))
                        for dep in deps_here:
                            if dep not in deps:
                                deps.append(dep)

        return deps

    @staticmethod
    def _resolve_package_name_and_divide(name: str) -> Tuple[str, Union[str, None]]:
        v = None
        if "=" not in name:
            v = None
        else:
            n = ''
            for i in range(len(name)):
                if name[i].isalpha():
                    n += name[i]
                else:
                    v = name[i:]
                    break
            name = n
        
        return name, v
    
    @staticmethod
    def _remove_signs_from_version(version: str) -> str:
        while not version[0].isnumeric():
            version = version[1:]
        return version
    
    @staticmethod
    def add(config: DriverConfiguration) -> None:
        packages: List[str] = config.to_add
        tomler = config.tomler
        itomler = ConfigurationInterpreter.interpret(tomler)

        list_from_toml = itomler.requirements_list

        to_install = []
        ignored = []
        shadow_installed = []

        # packages are the ones i need to add
        for package in packages:
            pkg_name, pkg_version = Drivers._resolve_package_name_and_divide(package)
            
            # none_check
            there_is_none = pkg_version is None

            if pkg_version is not None:
                pkg_version = Drivers._remove_signs_from_version(pkg_version)
            

            # in the list from toml, check if the current package to install,
            # is already installed or not
            breaker = False
            found_in_toml = False
            for element_from_toml in list_from_toml:
                
                # if already installed
                # check if versions are same or not
                if element_from_toml['name'] == pkg_name:
                    # if the name is found, but given pkg version is None,
                    if there_is_none:
                        ignored.append((pkg_name, pkg_version, f'{pkg_name} present.'))
                        breaker = True
                        break
                    
                    # try to get version from the toml
                    version_from_toml = element_from_toml.get('version', None)

                    # If version found in toml and check if pkg_to_install does not have the version same as the version in the toml
                    # if they dont, i need to install it
                    if version_from_toml is not None and version_from_toml != pkg_version:
                        to_install.append((pkg_name, pkg_version))
                    
                    elif version_from_toml is not None and version_from_toml == pkg_version:
                        # if version found in toml and if pkg to install has the version same as
                        # the toml version then it needs to be ignore, it is already installed
                        ignored.append((pkg_name, pkg_version, 'present'))

                    elif version_from_toml is None:
                        # If version is not there in the toml.
                        # Try to find it from the env_pip freeze list

                        pip_path = Path(f'./.{itomler.environment_name}') / ('bin' if osname != 'nt' else 'Scripts') / 'pip'

                        # get output of
                        # pip list --format=freeze
                        list_from_freeze = get_output_of(f'{pip_path} list --format=freeze').readlines()

                        # from the pip list (currently installed), check if the list contains version which
                        # i want to install.
                        found = False
                        for element_from_freeze in list_from_freeze:
                            # if the package name is in the element (package_name==version) (format)
                            if pkg_name in element_from_freeze:
                                found = True
                                a, version_from_freeze = Drivers._resolve_package_name_and_divide(element_from_freeze.replace('\n', ''))

                                # check if the version from freeze is the same as i want to install
                                if version_from_freeze == pkg_version:
                                    # if same, ignore it
                                    ignored.append((pkg_name, pkg_version, 'present'))
                                else:
                                    to_install.append((pkg_name, pkg_version))
                                
                                break
                        
                        # If not found in the freeze list, add it for install
                        if not found:
                            to_install.append((pkg_name, pkg_version))
                    
                    breaker = True
                    break
            
            if there_is_none and breaker:
                continue
                # Continue if package version is not provided
                # and breaker is triggered, meaning found
                
            # Breaker will be only true if name is found and version is found
            # and decision is made on ignorance or installation
            if breaker:
                break
            else:
                # If breaker is false then decision is not made.
                # does not exist and needs to be installed.

                # OK Here it is possible that it was not found in toml but is installed.
                # maybe it was installed by pip installed.

                pip_path = Path(f'./.{itomler.environment_name}') / ('bin' if osname != 'nt' else 'Scripts') / 'pip'

                # get output of
                # pip list --format=freeze
                list_from_freeze = get_output_of(f'{pip_path} list --format=freeze').readlines()

                # from the pip list (currently installed), check if the list contains version which
                # i want to install.
                found = False
                for element_from_freeze in list_from_freeze:
                    # if the package name is in the element (package_name==version) (format)
                    if pkg_name in element_from_freeze:

                        found = True
                        a, version_from_freeze = Drivers._resolve_package_name_and_divide(element_from_freeze.replace('\n', ''))
                        version_from_freeze = Drivers._remove_signs_from_version(version_from_freeze)

                        # If the pkg_version is None
                        # and there is one installed using pip
                        if pkg_version is None:
                            # IT means it is shadown installed. needs to be added
                            shadow_installed.append((pkg_name, version_from_freeze))
                            break

                        # check if the version from freeze is the same as i want to install
                        if version_from_freeze == pkg_version:
                            # if same, still, it is present in pip but not in toml
                            shadow_installed.append((pkg_name, version_from_freeze))
                        else:
                            # through pip it was known that it is present, but the pkg_version is given different than
                            # what is installed. Therefore, install it.
                            to_install.append((pkg_name, pkg_version))
                        
                        # since found, break it.
                        break
                
                # if not found, install it.
                if not found:
                    to_install.append((pkg_name, pkg_version))

        # For each package to install.
        for package in to_install:
            # if installation is done.
            if Drivers.add_installation(package[0], package[1], config):
                # check the list from tomler
                found = False
                # in the list from toml
                for i in range(len(list_from_toml)):
                    # if the entry exists
                    if list_from_toml[i]['name'] == package[0]:
                        # change the version
                        list_from_toml[i]['version'] = package[1]
                        found = True
                        break
                
                # If found, then version is changed/added, move on to next package
                if found:
                    continue
                else:
                    # If not found
                    # just add an entry
                    list_from_toml.append({"name": package[0], "version": package[1]})
            else:
                # If installation fails, add it in the ignored.
                ignored.append((package[0], package[1], 'failed'))

        for i in range(len(shadow_installed)):
            data = {"name": shadow_installed[i][0], "version": shadow_installed[i][1]}
            if not data in list_from_toml:
                list_from_toml.append(data)
            ignored.append(([shadow_installed[i][0], shadow_installed[i][1], 'present']))

        # Update the list from toml with propert version
        for x in list_from_toml:
            x['version'] = Drivers.get_version_from_freeze(x['name'], pip_path = Path(f'./.{itomler.environment_name}') / ('bin' if osname != 'nt' else 'Scripts') / 'pip')
            x['dependencies'] = Drivers._find_required_dependencies(pip_path, [x['name']])

        # update toml file
        requirements_dict: Dict = tomler.fetch_entry('requirements')
        requirements_dict['list'] = list_from_toml
        tomler.add_or_modify_entry('requirements', requirements_dict)

        # CREATE DOTLOCK
        DotLock.create(list_from_toml)

        # skipped status
        print(f"{_.RED if len(ignored) > 0 else _.GREEN}Skipped{_.RESET} {len(ignored)} : \n"+ '\n'.join(list(map(str, ignored))))
    
    @staticmethod
    def get_version_from_freeze(name: str, pip_path: Path) -> Union[str, None]:
        data = get_output_of(f"{pip_path} list --format=freeze").readlines()

        for line in data:
            if name in line:
                line = line.replace('\n', '')
                __, version = Drivers._resolve_package_name_and_divide(line)
                return Drivers._remove_signs_from_version(version)
        
        return None


    @staticmethod
    def add_installation(name: str, version: Union[str, None], config: DriverConfiguration) -> bool:
        tomler = config.tomler
        tomler.load_configuration

        itomler = ConfigurationInterpreter.interpret(tomler)
        pip_path = Path(f'./.{itomler.environment_name}') / ('bin' if osname != 'nt' else 'Scripts') / 'pip'

        command = f"{pip_path} install {name}" + (f"=={version}" if version else '')

        print(f"{_.YELLOW}Installing{_.RESET} {name}" + (f"=={version}" if version else "" + " ..."), end='\r')
        try:
            subprocess.run(command.split(), check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            print(f"                                                                         ", end='\r')
            print(f"{_.GREEN}Installed{_.RESET} {name}" + (f"=={version}." if version else "."))
            return True
        except subprocess.CalledProcessError:
            print("                                                          ", end='\r')
            print(f"{_.RED}Failed{_.RESET} to install {name}" + (f"=={version}" if version else ""))
            return False
    
    @staticmethod
    def build(config: DriverConfiguration) -> None:
        itomler = ConfigurationInterpreter.interpret(config.tomler)

        py_path = Path(f'./.{itomler.environment_name}') / ('bin' if osname != 'nt' else 'Scripts') / 'python'
        command = f"{py_path} -m build"
        print(f"{_.YELLOW}Building.{_.RESET}", end='\r')
        try:
            subprocess.run(command.split(), check=True, stdout=subprocess.DEVNULL)
            print(f"                            ", end='\r')
            print(f"{_.GREEN}Built.{_.RESET} ./dist")
        except subprocess.CalledProcessError:
            print("                           ", end='\r')
            print(f"Build {_.RED}Failure{_.RESET}")
            sys.exit(1)

        sys.exit(0)
    
    @staticmethod
    def upload(config: DriverConfiguration) -> None:
        upload_dir = config.upload_directory
        if upload_dir is None:
            print(f"Please provide a {_.RED}Upload Directory Path{_.RESET}.\nFor help run: {_.BLUE}clever{_.RESET} help")
            sys.exit(1)
        
        twine_path = Path(f'./.{ConfigurationInterpreter.interpret(config.tomler).environment_name}') / ('bin' if osname != 'nt' else 'Scripts') / 'twine'
        command = f"{twine_path} upload --verbose {upload_dir}/*"
        try:
            subprocess.run(command.split(), check=True)
            print(f"{_.GREEN}Done.{_.RESET}")
        except subprocess.CalledProcessError:
            print(f"{_.RED}Failed{_.RESET} to upload packages to PYPI.")
            sys.exit(1)
        
        sys.exit(0)