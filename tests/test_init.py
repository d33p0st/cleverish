from os import system, chdir, getcwd, makedirs, popen, name
from os.path import exists, join
from shutil import rmtree
from pathlib import Path
import tempfile

def test_init():
    # create a temp dir
    with tempfile.TemporaryDirectory() as tempdir:
        # change to temp dir
        current = getcwd()
        makedirs(join(tempdir, 'test'))
        chdir(join(tempdir, 'test'))

        # use simple init
        system("clever init -ws")

        assert exists(join(getcwd(), '.test'))
        assert exists(join(getcwd(), '.git'))
        assert exists(join(getcwd(), 'src'))
        assert exists(join(getcwd(), 'pyproject.toml'))
        assert exists(join(getcwd(), 'clever.toml'))

        # delete the dir
        chdir(tempdir)
        rmtree(join(tempdir, 'test'))

        # create again and move
        makedirs(join(tempdir, 'test'))
        chdir(join(tempdir, 'test'))

        # test init name
        system('clever init name testing -ws')

        assert exists(join(getcwd(), '.testing'))
        assert exists(join(getcwd(), '.git'))
        assert exists(join(getcwd(), 'src'))
        assert exists(join(getcwd(), 'src', 'testing'))
        assert exists(join(getcwd(), 'pyproject.toml'))
        assert exists(join(getcwd(), 'clever.toml'))

        # delete the dir
        chdir(tempdir)
        rmtree(join(tempdir, 'test'))

        # create again and move
        makedirs(join(tempdir, 'test'))
        chdir(join(tempdir, 'test'))

        system('clever init package -ws')

        # test init package
        assert exists(join(getcwd(), '.test'))
        assert exists(join(getcwd(), '.git'))
        assert exists(join(getcwd(), 'src'))
        assert exists(join(getcwd(), 'src', 'test'))
        assert exists(join(getcwd(), 'pyproject.toml'))
        assert exists(join(getcwd(), 'clever.toml'))

        ### NOW CHECK FOR INSTALLATIONS OF build, twine\
        pip_path = Path(f'./.test') / ('bin' if name != 'nt' else 'Scripts') / 'pip'
        data = popen(f'{pip_path} list --format=freeze').read()

        if 'twine' in data and 'build' in data:
            assert True
        else:
            assert False

        # change to current
        chdir(current)
        # exits here