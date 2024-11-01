# Overview

`cleverish` is a dependency and environment handler for `python` projects. Inspired from `Cargo` (from `Rust` programming language), `cleverish` brings a few greatly attractive features like the [__`clever shell`__](#clever-shell). `cleverish` aims to handle all dependency problems so that you don't have to rattle your brain for it.

## Table of Contents

- [__Features__](#features)
  - [Initialization](#initialization)
  - [The clever shell](#the-clever-shell)
  - [Integration of dot-lock file and toml file](#integration-of-dot-lock-and-toml-file)
  - [Attention to detail](#attention-to-detail)
  - [Building and Uploading](#building-and-uploading)
- [__Usage__](#usage)
- [__Use cases__](#use-cases)
- [__Upcoming Features__](#upcoming-features)
- [__Contributing__](#contributing)

## Features

`cleverish` brings a ton of features engineered with great attention to detail. Still, I wont claim it's perfect, This is still in beta and I am working on it still, improving it's decision making and working which in turn will improve the user comfort.

- #### Initialization

  `cleverish` as inspired from `Cargo`, can initialize empty projects with structure complying with [Python Packaging Index(PYPI)](https://pypi.org "Python Packaging Index")

  ```bash
  $ clever init
  ```

  Initializing a project creates a virtual environment for that particular project where all the dependencies will be added and maintained.

  All arguments and descriptions are provided in [__Usage__](#usage)

- #### The Clever Shell

  As the name mentions, it is a __`clever shell`__. It is a python wrapped terminal which helps execute commands in the virtual environment created for the project.

  > For example, you have a globally installed python and pip. But the virtual environment has it's own python and pip and any executable bins of libraries that you install for that particular virtual environment. Using the __`clever shell`__, when you call for a bin or simply python, it will be called from the virtual environment if the bin exists, and if it doesn't exist, then it will look globally.  
  Overall, using the __`clever shell`__ is the safest practice while interacting with the project and its dependencies.
  
  ```bash
  $ clever shell
  ```

  Apart from safe and valid execution of commands, __`clever shell`__ has `command history`, `auto-suggestion` and `free cursor movement`.

  Other descriptive features are provided in [__Usage__](#usage)

- #### Integration of dot-lock and toml file

  `cleverish` works with a set of configurations that are saved in a `clever.toml` file in the same directory as your project (same as `pyproject.toml`).

  Having this configuration file makes it easy to configure it based on user needs.

  `cleverish` maintains a dot-lock file (`clever.lock`) which keeps track of all dependencies and their requirements. This file is not for user intervention, it is generated and updated by `cleverish`.

- #### Attention to detail

  `cleverish` is made with a lot of attention to detail which can be seen in it's working. 

  > For example, if a library is installed in your virtual environment and you don't know the version And you want to install it again, this time, say, `>=v2.0.0`. `cleverish` will find out the version of the currently installed library and checks if it matches the description, if it does, it will skip, else it will install.

  This avoids repeated installation of the same library.

  Apart from this, several more details are handled by `cleverish` and therefore it provides a smooth user experience.

- #### Building and Uploading

  With `cleverish` you can build and upload your projects to [__Python Packaging Index__](https://pypi.orge "PYPI"). You will need an API key from the website and need to paste it in the terminal or you can create a `.pypirc` file in your home directory as per given below.

  `.pypirc`
  ```toml
  [pypi]
    username = __token__
    password = <paste your api token here>
  ```

## Usage

- __`Init`__

  Initializing a new project with clever comes with a few benefits, such as, defining if you are creating a package or just a simple project.

  The base command is `clever init`. However there are a few sub arguments for it such as `package` and `name`.

  Let us see them all.

  - `clever init`

    This will create the following directory structure.

    ```console
    project_name/
        | 
        | - .project_name/
        |       | 
        |       | - bin/
        |       |    |
        |       |    | - activate
        |       |    | - activate.csh
        |       |    | - activate.fish
        |       |    | - Activate.ps1
        |       |    | - pip
        |       |    | - pip3 # based on root python version
        |       |    | - pip3.13 # based on root python version
        |       |    | - build
        |       |    | - twine
        |       |    | - * and a few other bins * to start you off.
        |       |
        |       | - include/ # will contain python executable
        |       |
        |       | - lib/ # will contain libraries
        |       |
        |       | - pyvenv.cfg
        |
        |- src/
        |   |
        |   |- __init__.py
        |
        | - pyproject.toml
        | - clever.toml
        | - clever.lock
    ```

    where .project_name is the virtual environment name.

  - `clever init package`

    This command will create a package inside `src` directory

    ```console
    ...
    | - src/
    |   | - project_name/
    |   |       | - __init__.py
    ...
    ```

  - `clever init package name <some_name>`

    This will change the default `package_name` to `some_name`

    ```console
    ...
    | - src/
    |   | - some_name/
    |   |       | - __init__.py
    ...
    ```

    > The presence of `name` argument will automatically set the `package` argument as True. i.e, `clever init name <some_name>` will have the same effect.

- __`clever shell`__

  The `clever shell` will be automatically opened after `clever init`, however it's usage depends on the user.

  The use of `clever shell` is recommended for calling the environment `python`, `pip` and other bins installed in it.

  To open the shell,

  ```bash
  $ clever shell
  ```

  To exit, enter any of these: [`exit`, `quit`, `deactivate`, `ctrl+c`, `ctrl+d`, `:q`] and hit enter.

- __`clever install`__

  Suppose you have already mentioned a few dependencies in the `clever.toml`, using this command, those dependencies will be installed.

  In other cases, if any installation you did using pip and did not add in the toml file, using this command will add it into the `.lock` and `clever.toml` file.

  Any dependency already present will be skipped.

  There is no sub-arguments for this command (__`YET!`__)

- __`clever add <package-name>`__

  This command is for adding new or updating existing dependencies.

  if version is not provided: `clever add modstore`, the latest version will be installed. However, if the library already exists, it will skip it.

  If a library is installed, say, modstore v1.1.1, and you want to install version v1.0.0. using `clever add modstore==1.0.0` will install v1.0.0. However, if you use `clever add modstore==1.1.1`, it will be skipped as it is already installed in the virtual environment.

  `cleverish` will check the toml file and the dot-lock file and system installations to tally the currently present and user requested dependency versions, and then make a decision on whether to skip it or install it. If will only install if necessary.

  The toml file and dot-lock file will be updated automatically upon using this command.

  > __Important:__  
  This command supports multiple packages at once and therefore the command: `clever add modstore, wrapper-bar, numpy, pandas` is valid. Any number of packages can be provided at once.

- `clever build`

  This command uses the `build` library of python to build the project into `sdist`(.tar.gz) and `wheel`(.whl). The build will be available in the folder `project_name/dist/`.

  > __Important:__  
  If you are using maturin to create Python/Rust mix project or similar(using something other than setup-tools backend), then do not use this command. Use the related build command, for example, in case of maturin, it is `maturin build`.  

  >__NOTE:__ You need to install maturin in the virtual environment using `clever add maturin` and then call `maturin build`. All this can be done in the __`clever shell`__. ;)

- `clever upload <distribution-folder>`

  Using this command, dist packages can be upload to the [__Python Packaging Index__](https://pypi.org "PYPI").

  Let us take an example. You built the project using `clever build` and now it is available under `./dist`

  Therefore, the command to upload it to `pypi` will be  
  ```bash
  $ clever upload dist
  ```

- `clever help`

  For a list of commands and sub commands and their usage,
  use `clever help`. The arguments have shorter counterparts, use `clever help` to find out.

## Use cases

Now typically this is ideal for pure python projects currently. Future updates will include other language support such as Python/Rust mix projects.

- For people who work on multiple projects at the same time, like me, `cleverish` is a great fit to maintain virtual environment and dependencies of different projects separate and iron clad.

- `Clever Shell` provides a locked environment to run commands which prevents breaking dependencies upon accidental mistakes or typos and even saves from accidentally calling libraries outside the project scope.

- Support for VSCode, Once using `clever init`, the virtual environment can be selected in `vscode` which will then help in environment specific hinting and code suggestions.

- Overall saving time and effort.

## Upcoming Features

There are a lot of upcoming features on my mind, like..

- Extending the `clever shell` functionalities
- Adding sub-arguments for `clever install`
- Adding support for Mix Python projects in `build`, `init` and `upload` arguments
- Adding a `test` argument for testing (might even check docstring codes, if found)
- Customize `init` argument for more specific initializing options
- and a few secrets :D

## Contributing

Contributions are welcome for this project. Please submit any issues or PRs and I will get back to it asap.

- [__GitHub__](https://github.com/d33p0st/cleverish)
- [__Issues__](https://github.com/d33p0st/cleverish/issues)
- [__Pull Requests__](https://github.com/d33p0st/cleverish/pulls)

Thank you for your interest in contributing! `cleverish` aims to shorten the time it takes to create projects and the ease of use. We welcome contributions of all kinds, including bug reports, feature requests, documentation improvements, and more.

Find the Code of Conduct [here](CODE_OF_CONDUCT.md). If you are seeing this page on `PYPI`, go to the repository using the `GitHub` link listed above and see `CODE_OF_CONDUCT.md`

Find the Contribution Instructions [here](CONTRIBUTING.md). If you are seeing this page on `PYPI`, go to the repository using the `GitHub` link listed above and see `CONTRIBUTING.md`