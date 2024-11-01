from .arguments import PathWays
from .utils import Tomler
from .drivers import DriverConfiguration, Drivers

from colorama import init as colorama, Fore as _
from argpi import FetchType
import sys

def clever():

    # color initialization
    colorama()
    
    function_pathways = PathWays()

    # register for each argument
    # create a configuration maintainer
    driver_configuration = DriverConfiguration()

    ###### HELP ########
    function_pathways.register('help', Drivers.help)

    ###### INIT Functionality goes here ##########

    ## get if force
    function_pathways.register('force', driver_configuration.set_force, False, FetchType.SINGULAR, True)

    ## get if package Name provided, if provided automatically set package to True too
    function_pathways.register('name', driver_configuration.set_package_name, True, FetchType.SINGULAR)
    
    ## get if package_name not given but it is a package.
    function_pathways.register('package', driver_configuration.set_package_status, False, FetchType.SINGULAR, True)

    ## do init
    function_pathways.register('init', Drivers.init, False, FetchType.SINGULAR, driver_configuration)
    # If this skips, go to the next functionality.

    ### This Following check is mandatory for all other commands. ####
    # Check this if anything except init.
    if not Drivers.clever_toml():
        print(f"{_.RED}Cleverish{_.RESET}: cleverish.toml file not present in current directory.")
        sys.exit(1)
    
    driver_configuration.set_tomler(Tomler())
    
    ######## Shell Functionality goes here. ######

    function_pathways.register('shell', Drivers.shell, False, FetchType.SINGULAR, driver_configuration)

    ######## Install dependencies ###############

    function_pathways.register('install', Drivers.user_install_dependencies, False, FetchType.SINGULAR, driver_configuration)

    ######## Add Functionality goes here ##########

    # have to get the package_name to add.
    function_pathways.register('add', driver_configuration.set_to_add, True, FetchType.TILL_LAST)
    
    # add them now
    function_pathways.register('add', Drivers.add, False, FetchType.SINGULAR, driver_configuration)

    ########### BUILD Functionality ############

    function_pathways.register('build', Drivers.build, False, FetchType.SINGULAR, driver_configuration)

    ########### UPLOAD Functionality ##############

    function_pathways.register('upload', driver_configuration.set_upload_directory, True, FetchType.SINGULAR)

    function_pathways.register('upload', Drivers.upload, False, FetchType.SINGULAR, driver_configuration)
