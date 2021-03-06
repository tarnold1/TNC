#__author__ = 'tarnold 10/10/2016'

from configparser import ConfigParser
import glob
import time,sys,datetime,re,os,pytest,subprocess
from sys import exit
import getpass
from collections import OrderedDict
from pyparsing import Literal, Word, Group, Dict, ZeroOrMore, alphas, nums, delimitedList
import string
import xlwt
from xlwt import Workbook, XFStyle, Borders, Pattern, Font ,easyxf
import re
from subprocess import Popen, PIPE

BinNoDict = {}
prev_col1 = {}
TestNoByBin = True
BinCounterDict = {}
testFuncDict={}
testBlockDict={}
testListArray=[]

if (sys.platform == "win32"):
    dirSeperator = "\\"
elif (sys.platform == "linux"):
    dirSeperator = "/"
else:
    dirSeperator = "\\"
    
class ParseFile(object):
    pinGGList=[]
    label_index = {}
    tnumberOffset = 1050
    temparray = ['' for i in range(9)]
    temparray2 = [[""]*2 for j in range(5)]

    def __init__(self):
        self.fileCounter=0
        self.tindex=0
        self.topline=True
        self.commentIndex=0
        
    def runDos2Unix(self,path,WCF,fileList):
            errorFlag = False
            ##print("Path:"+path)
            if (os.path.exists(WCF.resource_path("Dos2Unix.exe"))):
                Sources_Input = WCF.resource_path("Dos2Unix.exe")
                path = path.replace('/',"\\")
                for file in fileList:
                    command = Sources_Input+" "+path+file
                    ##print("Command 1:"+command)
                    p = Popen(command, shell=True, bufsize=0,stdin=PIPE, stdout=PIPE, stderr=PIPE)
            elif (os.path.exists('.'+dirSeperator+'Dos2Unix.exe')):
                path = path.replace('/',"\\")
                for file in fileList:
                    command = "Dos2Unix.exe "+path+file
                    ##print("Command 2:"+command)
                    #CREATE_NO_WINDOW = 0x08000000
                    #subprocess.call(command, creationflags=CREATE_NO_WINDOW)
                    p = Popen(command, shell=True, bufsize=0,stdin=PIPE, stdout=PIPE, stderr=PIPE)
            else:
                errorFlag = True
            return errorFlag

    def resource_path(self,relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)
        
###################################################################################################################
############################################ Create UPG Configuraton File #########################################
###################################################################################################################
    def writeUpgConfig(self,progName,package,binning,binningUno,testflow,levels,timing,specs,testgroup,UPGConfig_Output):

        upgConfig1 = """
###############################################################################
# File: configuration_UPG.cfg
# Configuration file for the Unison Program Generator
# Generated by the MPP Program on Date: %s
###############################################################################

# The directory name for the new test program
# The top level una file will be the same as the directory name
###############################################################################
PROJECT_NAME        %s

# The main input files defining the new test program
# File paths for the config files can be absolute or relative to this .cfg file
###############################################################################
# Definition for the adapterboard(s) and pingroup(s)
# PACKAGE_FILE must be an XLS or XLSX file
# As an alternative, you may use CSV files instead of a PACKAGE_FILE, 
# however, the CSV has to be broken into multiple files.
# If you don't use PACKAGE_FILE, you must have a PINTYPE_FILE, PINGROUP_FILE
# and at least one ADAPTERBOARD_FILE
PACKAGE_FILE    %s
# 
# Alternate CSV package files
# PINTYPE_FILE        pintypes.csv
# PINGROUP_FILE       Package.csv
# First ADAPTERBOARD_FILE found is used as the Active Adapterboard
# ADAPTERBOARD_FILE   Board_Dual.csv
# ADAPTERBOARD_FILE   Board_Single.csv

# Optional limits file(s) - the format is a standard Unison limits csv file
# Multiple limits files may be specified by repeating the LIMITS_CSV_FILE
# directive. The first limit file listed will be assigned as the program's
# active limit table.
#LIMITS_CSV_FILE        limits.csv

# The binning definition file
# Must be an XLS, XLSX, or CSV file
BINNING_FILE    %s

# The test flow definition file
# Must be an XLS, XLSX, or CSV file
TEST_FLOW_FILE      %s
# Flow apparence - snake shape per default - only LINEAR or SNAKE
FLOW_GRAPH_TYPE SNAKE

#Optional levels file
TEST_LEVELS_FILE    %s

# The subdirectories to use for various generated program files.
# IMPORTANT:
# The paths are always relative and cannot be absolute paths for the *_DIR directives!
#
# They are relative to either:
# 1) Inside the optional -d project_dir if upg is invoked with the -d option.
#     (Meaning if you use '-d /MyAbsolutePath' when invoking upg
#      and if you have a PROGRAM_DIR of Program then you will have:
#      /MyAbsolutePath/Program/ directory containing your .una and non-pattern .uno files)
# 2) Inside the current working directory where upg was invoked (not where upg is installed) 
#    if the -d option was not used.
#     (Meaning if you run upg while your current working directory is /u/me/
#      and your PROGRAM_DIR is Program then you will have:
#      /u/me/Program/ directory containing your .una and non-pattern .uno files)
# 
# If these directives are left out, then appropriate files for those
# directories are placed in './', relative to the above.
#
# The same directory can be used for multiple options, if desired.
# Example:
# PROGRAM_DIR   Program
# LIMITS_DIR    Program
###############################################################################
# Used for the .una and non-pattern .uno files
PROGRAM_DIR             Program
# Used as the base directory for all application libraries (each library will 
# have a subdirectory in this directory
LIBRARIES_DIR           Libraries
# Used for limit files
LIMITS_DIR              Limits
# Used for pattern source files (ascii .uno files)
PATTERN_SOURCE_DIR      Patterns/PatternSource
# Used for compiled pattern binary files (.upf files)
PATTERN_BINARY_DIR      Patterns/PatternBinary
# Used for any applications library doxygen documentation
LIBRARY_DOC_DIR         Docs
# Used for various support scripts 
SUPPORT_DIR             Support

# Keyword must be present for 'legacy' U4 programs
# If U4_MODE keyword is commented out or not present, newer Unison syntax is used
# which requires a newer package file syntax.
# 
# Some keywords are only necessary in U4_MODE:
# DIGITAL_PIN_TYPE is only necessary in U4_MODE (ignored otherwise)
# PROGRAM_MODEL is only necessary in U4_MODE (ignored otherwise)
# PATTERN_MAP_DIR is only allowed in U4_MODE (errors in non-U4_MODE)
#
# If U4_MODE is commented or not present, then SYSTEM_TYPE must be supplied
# See SYSTEM_TYPE below
###############################################################################
# U4_MODE

# SYSTEM_TYPE is required if not in U4_MODE
# Not required in U4_MODE (ignored)
#
# Valid SYSTEM_TYPES are: DMDX, DMD, XSERIES (XSERIES includes EX, LX, MX, & PAX)
###############################################################################
SYSTEM_TYPE DMDX

# DIGITAL_PIN_TYPE is only necessary in U4_MODE
# The digital pin cards type, specify FX or D96
# Optional keyword, it defaults to FX when not present
# Used in compiling patterns using the -d option of upc
###############################################################################
# DIGITAL_PIN_TYPE    D96

# PROGRAM_MODEL is only necessary in U4_MODE
# The digital programming model, specify MSDI or VLSI
# Optional keyword, it defaults to MSDI when not present
###############################################################################
# PROGRAM_MODEL           VLSI

# PATTERN_MAP_DIR is only allowed in U4_MODE
# The patterns to include in the program. In order to include 
# patterns, you use the PATTERN_MAP_DIR directive and point 
# to a directory (relative to this config file or an absolute path). 
# The directory name is used for the name of the PatternMap object 
# in Unison. Inside the directory, all .uno files are put into the
# PatternMap under a default pattern group. The default pattern group 
# name will be '<PatternMap_name>_group'. All subdirectories inside 
# the PATTERN_MAP_DIR are used as PatternGroup names and all .uno files in 
# these subdirectories are added to the PatternMap under this PatternGroup. 
# Note: PatternGroups are not used in MSDI, so subdirectory names are 
# ignored.
#
# Example:
# To create a PatternMap named 'MyPatternMap' that has 3 
# PatternGroups (named MyPatGrp1 & MyPatGrp2 & a default) each with 2 patterns, 
# the following directory structure would be used:
#
# MyPatternMap/
#   MyPatternFile1.uno      <- assigned to MyPatternMap_group PatternGroup
#   MyPatternFile2.uno      <- assigned to MyPatternMap_group PatternGroup
#   MyPatGrp1/               
#       MyPattern1_1.uno    <-- assigned to MyPatGrp1 PatternGroup
#       MyPattern1_2.uno    <-- assigned to MyPatGrp1 PatternGroup
#   MyPatGrp2/
#       MyPattern2_1.uno    <-- assigned to MyPatGrp2 PatternGroup
#       MyPattern2_2.uno    <-- assigned to MyPatGrp2 PatternGroup
# 
#
# Then, you would use the following directive (assuming MyPatternMap 
# directory is one directory up from this config file)
# 
# PATTERN_MAP_DIR   ../MyPatternMap
#
# Patterns in the directory (and subdirectories) are copied into the program's 
# PATTERN_SOURCE_DIR for use in the program.
#
# Multiple PATTERN_MAP_DIR directives may be used to create
# multiple PatternMaps, if required. However, the first map
# defined is used as the program's default pattern map.
#
# Note: In current version of UnisonProgramGenerator, you must use the INCLUDE_OBJECT_FILE
# directive below to include a file with pattern support objects (waveform tables, etc)
# in order for the program to compile these patterns properly.
#
# Note: Although the PatternGroup is referenced in the PatternMap (based
# on directory names), the PatternGroup is NOT created and must be included 
# through an external file along with waveforms, timing, and signal headers
# (as mentioned above).
###############################################################################
#PATTERN_MAP_DIR   relative_path/to/directory
#PATTERN_MAP_DIR   /absolute_path/to/directory

# External Reference files to include in program
# 
# If you have complete existing Unison object files that you wish to 
# include into your program, they may be included through the INCLUDE_OBJECT_FILE
# directive. 
#
# If you merely want to link in an external object file without making a 
# local copy into your program, follow the filepath with the DO_NOT_COPY 
# directive modifier. Files with DO_NOT_COPY must have absolute paths.
# 
#
# Example:
# You have a global file for your company that defines objects that are
# used for every program in your company and it is such that you don't 
# want to make a copy so that you will always point to the latest version, 
# you can include (and not copy) the file like this:
#
# INCLUDE_OBJECT_FILE   /absolute_path/to/global_standard/file.uno   DO_NOT_COPY
#
# Example:
# You have a file that you want to copy into your program and reuse objects:
# 
# INCLUDE_OBJECT_FILE   filepath
#
# Multiple object files may be included by repeating the INCLUDE_OBJECT_FILE
# directive.
###############################################################################
#INCLUDE_OBJECT_FILE    /absolute_path/to/file.uno  DO_NOT_COPY
#INCLUDE_OBJECT_FILE    /absolute_path/to/file.uno
#INCLUDE_OBJECT_FILE    relative_path/to/file.uno
INCLUDE_OBJECT_FILE    %s
INCLUDE_OBJECT_FILE    %s
INCLUDE_OBJECT_FILE    %s
# Adjust .una to include this .uno file.
#INCLUDE_OBJECT_FILE    %s
#INCLUDE_OBJECT_FILE Global_Specs.uno

# Optional keyword to specify a package to create doxygen help
# File path can be relative from this config file or absolute
###############################################################################
#DOXYGEN_FILE        doxygen_input.tgz

# The library files to add to the test program
# Multiple different libraries may be specified by using multiple LIBRARY_NAME
# statements. All LIBRARY_X statements following a LIBRARY_NAME will apply to 
# one library until a new LIBRARY_NAME is encountered, which starts a new 
# library.
#
# If a LIBRARY_COPY is FALSE, then the library will not have a program-local
# copy made. All SOURCE and INCLUDE files must be absolute path if LIBRARY_COPY
# is FALSE. If LIBRARY_COPY is TRUE, then a local copy of the files will be 
# made and the SOURCE and INCLUDE files can be absolute or relative (to this 
# config file) path.
#
# Local library files will be stored in the program under 
# LIBRARY_DIRECTORY/LIBRARY_NAME directory
###############################################################################
#LIBRARY_NAME        DemoLib

# COPY is optional. It defaults to TRUE if not specified
#LIBRARY_COPY        TRUE

# Source code files can be absolute or relative (unless LIBRARY_COPY is FALSE)
#LIBRARY_SOURCE      relative_path/from_this_config_file/source1.cpp
#LIBRARY_SOURCE      /absolute_path/to_source_file/source2.cpp

# Header files can be absolute or relative (unless LIBRARY_COPY is FALSE)
# (No need to include system resource files here, only application library files)
#LIBRARY_INCLUDE     relative_path/from_this_config_file/include1.h
#LIBRARY_INCLUDE     /absolute_path/to_source_file/include2.h

# Specify any dependencies this library has on other libraries
# Multiple dependencies are allowed, just add more LIBRARY_DEPENDENCY lines
# LIBRARY_DEPENDENCY  DependencyLib  
# Example Dependency on a pre-compiled library (not a Unison ApplicationLibrary object)
# LIBRARY_DEPENDENCY  libLTXCCoreMethods.un.so

# Next library
#LIBRARY_NAME        DemoLib2
#LIBRARY_COPY        TRUE
#LIBRARY_SOURCE      relative_path/from_this_config_file_2/source1.cpp
#LIBRARY_SOURCE      /absolute_path/to_source_file_2/source2.cpp
#LIBRARY_INCLUDE     relative_path/from_this_config_file_2/include1.h
#LIBRARY_DEPENDENCY  DemoLib

# Define the datalog streams
# If DLOG0 and DLOG1 are missing, a default setup will be created
###############################################################################
# Keyword       Method      Mode                Filter          Frequency   Destination
# DLOG0/DLOG9   ASCII/STDF  BUFFERED/IMMEDIATE  DEFAULT/ON/OFF  LOT/WAFER   Filename or empty
#DLOG0         ASCII       BUFFERED            DEFAULT         LOT
#DLOG1         STDF        BUFFERED            OFF             LOT         ${LTXHOME}/testers/${LTX_TESTER}/dlog/${ObjName}_${Device}_${LotId}_${WaferId}_${DlogSetupTime}.std

    """
        timeGenerated = datetime.datetime.now().strftime("%b %d %Y at %H:%M")
        try:
            fo = open(UPGConfig_Output, "a+",buffering=2)
            if (os.path.exists(UPGConfig_Output)):
                doNothing = 1
            fo.write(upgConfig1 %(timeGenerated,progName,package,binning,testflow,levels,timing,specs,testgroup,binningUno))
            fo.close()
        except:
            pass



        

