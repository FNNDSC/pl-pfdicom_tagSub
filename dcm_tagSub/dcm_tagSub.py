#
# pfdicom_tagsub ds ChRIS plugin app
#
# (c) 2021 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

from chrisapp.base import ChrisApp
import os
import re
import json
# import the pfdicom_tagSub module
from pfdicom_tagSub import  pfdicom_tagSub
import  pudb
import  sys

Gstr_title = r"""

        __    _ _                      _                        _     
       / _|  | (_)                    | |                      | |    
 _ __ | |_ __| |_  ___ ___  _ __ ___  | |_ __ _  __ _ ___ _   _| |__  
| '_ \|  _/ _` | |/ __/ _ \| '_ ` _ \ | __/ _` |/ _` / __| | | | '_ \ 
| |_) | || (_| | | (_| (_) | | | | | || || (_| | (_| \__ \ |_| | |_) |
| .__/|_| \__,_|_|\___\___/|_| |_| |_| \__\__,_|\__, |___/\__,_|_.__/ 
| |                                ______        __/ |                
|_|                               |______|      |___/                 

"""

Gstr_synopsis = """


    NAME

       dcm_tagsub.py 

    SYNOPSIS

        python dcm_tagSub.py                                            \\
            [-h] [--help]                                               \\
            [--json]                                                    \\
            [--man]                                                     \\
            [--meta]                                                    \\
            [--savejson <DIR>]                                          \\
            [-v <level>] [--verbosity <level>]                          \\
            [-e|--extension <DICOMextension>]                           \\
            [-O|--outputDir <outputDir>]                                \\
            [-F|--tagFile <JSONtagFile>]                                \\
            [-T|--tagStruct <JSONtagStructure>]                         \\
            [-n|--tagInfo <delimited_parameters>]                       \\
            [-s|--splitToken <split_token>]                             \\
            [-k|--splitKeyValue <keySplit>]                             \\
            [-o|--outputFileStem <outputFileStem>]                      \\
            [--outputLeafDir <outputLeafDirFormat>]                     \\
            [--threads <numThreads>]                                    \\
            [--version]                                                 \\
            <inputDir>                                                  \\
            <outputDir> 

    BRIEF EXAMPLE

        docker run -it --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing  \\
        fnndsc/pl-pfdicom_tagsub dcm_tagSub                                 \\
        --tagStruct '
        {
            "PatientName":              "%_name|patientID_PatientName",
            "PatientID":                "%_md5|7_PatientID",
            "AccessionNumber":          "%_md5|8_AccessionNumber",
            "PatientBirthDate":         "%_strmsk|******01_PatientBirthDate",
            "re:.*hysician":            "%_md5|4_#tag",
            "re:.*stitution":           "#tag",
            "re:.*ddress":              "#tag"
        }
        ' --threads 0 -v 2 -e .dcm                                           \\
        /incoming /outgoing
        
         -- OR equivalently --
        docker run -it --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing  \\
        fnndsc/pl-pfdicom_tagsub dcm_tagSub                                 \\
            -e dcm                                                          \\
            --splitToken ","                                                \\
            --splitKeyValue "="                                             \\
            --tagInfo '
                PatientName         =  %_name|patientID_PatientName,
                PatientID           =  %_md5|7_PatientID,
                AccessionNumber     =  %_md5|8_AccessionNumber,
                PatientBirthDate    =  %_strmsk|******01_PatientBirthDate,
                re:.*hysician       =  %_md5|4_#tag,
                re:.*stitution      =  #tag,
                re:.*ddress         =  #tag
            ' --threads 0 --printElapsedTime                                \\
             /incoming /outgoing
            
        will replace the explicitly named tags as shown:
        * the ``PatientName`` value will be replaced with a Fake Name,
          seeded on the ``PatientID``;
        * the ``PatientID`` value will be replaced with the first 7 characters
          of an md5 hash of the ``PatientID``;
        * the ``AccessionNumber``  value will be replaced with the first 8
          characters of an md5 hash of the `AccessionNumber`;
        * the ``PatientBirthDate`` value will set the final two characters,
          i.e. the day of birth, to ``01`` and preserve the other birthdate
          values;
        * any tags with the substring ``hysician`` will have their values
          replaced with the first 4 characters of the corresponding tag value
          md5 hash;
        * any tags with ``stitution`` and ``ddress`` substrings in the tag
          contents will have the corresponding value simply set to the tag
          name.
        NOTE:
        Spelling matters! Especially with the substring bulk replace, please
        make sure that the substring has no typos, otherwise the target tags
        will most probably not be processed

    DESCRIPTION

        'dcm_tagSub' is a customizable and friendly DICOM tag substitutor.
        As part of the "pf*" suite of applications, it is geared to IO as
        directories. Input DICOM trees are reconstructed in an output
        directory, preserving directory structure. Each node tree contains
        a copy of the original DICOM with a user-specified tag list changed
        in the output.

    ARGS

        [-h] [--help]
        If specified, show help message and exit.
        
        [--json]
        If specified, show json representation of app and exit.
        
        [--man]
        If specified, print (this) man page and exit.

        [--meta]
        If specified, print plugin meta data and exit.
        
        [--savejson <DIR>] 
        If specified, save json representation file to DIR and exit. 
        
        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.
        
        [--version]
        If specified, print version number and exit. 
        
        [-e|--extension <DICOMextension>]
    	An optional extension to filter the DICOM files of interest from the
    	<inputDir>.

    	[-O|--outputDir <outputDir>]
    	The output root directory that will contain a tree structure identical
    	to the input directory, and each "leaf" node will contain the analysis
    	results.

    	[-F|--tagFile <JSONtagFile>]
    	Parse the tags and their "subs" from a JSON formatted <JSONtagFile>.

    	[-T|--tagStruct <JSONtagStructure>]
        Parse the tags and their "subs" from a JSON formatted <JSONtagStucture>
        string passed directly in the command line. Note that sometimes protecting
        a JSON string can be tricky, especially when used in scripts or as variable
        expansions. If the JSON string is problematic, use the [--tagInfo <string>]
        instead.
        
        [-n|--tagInfo <delimited_parameters>]
    	A token delimited string that is reconstructed into a JSON structure by the
        script. This is often useful if the [--tagStruict] JSON string is hard to
        parse in scripts and variable passing within scripts. The format of this
        string is:
                "<tag1><splitKeyValue><value1><split_token><tag2><splitKeyValue><value2>"
        for example:
                --splitToken ","
                --splitKeyValue ':'
                --tagInfo "PatientName:anon,PatientID:%_md5|7_PatientID"
        or more complexly (esp if the ':' is part of the key):
                --splitToken "++"
                --splitKeyValue "="
                --tagInfo "PatientBirthDate = %_strmsk|******01_PatientBirthDate ++
                           re:.*hysician"   = %_md5|4_#tag"
                           
        [-s|--splitToken <split_token>]
        The token on which to split the <delimited_parameters> string.
        Default is '++'.
        
        [-k|--splitKeyValue <keyValueSplit>]
        The token on which to split the <key> <value> pair. Default is ':'
        but this can be problematic if the <key> itself has a ':' (for example
        in the regular expression expansion).                             

    	[-o|--outputFileStem <outputFileStem>]
    	The output file stem to store data. This should *not* have a file
    	extension, or rather, any "." in the name are considered part of
    	the stem and are *not* considered extensions.

    	[--outputLeafDir <outputLeafDirFormat>]
    	If specified, will apply the <outputLeafDirFormat> to the output
    	directories containing data. This is useful to blanket describe
    	final output directories with some descriptive text, such as
    	'anon' or 'preview'.

    	This is a formatting spec, so

        	--outputLeafDir 'preview-%s'

    	where %s is the original leaf directory node, will prefix each
   	final directory containing output with the text 'preview-' which
    	can be useful in describing some features of the output set.

   	[--threads <numThreads>]
    	If specified, break the innermost analysis loop into <numThreads>
    	threads.
"""


class Dcm_tagSub(ChrisApp):
    """
    This plugin wraps around pfdicom_tagSub and is used to edit the contents of user-specified DICOM tags.
    """
    PACKAGE                 = __package__
    TITLE                   = 'Edits various specified DICOM tags'
    CATEGORY                = 'DICOM'
    TYPE                    = 'ds'
    ICON                    = ''   # url of an icon image
    MIN_NUMBER_OF_WORKERS   = 1    # Override with the minimum number of workers as int
    MAX_NUMBER_OF_WORKERS   = 1    # Override with the maximum number of workers as int
    MIN_CPU_LIMIT           = 2000 # Override with millicore value as int (1000 millicores == 1 CPU core)
    MIN_MEMORY_LIMIT        = 2000  # Override with memory MegaByte (MB) limit as int
    MIN_GPU_LIMIT           = 0    # Override with the minimum number of GPUs as int
    MAX_GPU_LIMIT           = 0    # Override with the maximum number of GPUs as int

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """
        self.add_argument("-i", "--inputFile",
                            help        = "input file",
                            dest        = 'inputFile',
                            type        = str,
                            optional    = True,
                            default     = '')
        self.add_argument("-e", "--fileFilter",
                            help        = "DICOM file extension",
                            type        = str,
                            dest        = 'fileFilter',
                            optional    = True,
                            default     = '')
        self.add_argument("--fileFilterLogic",
                            help        = "the logic to apply across the file filter",
                            optional    = True,
                            type        = str,
                            dest        = 'fileFilterLogic',
                            default     = 'OR')
        self.add_argument("-d", "--dirFilter",
                            help        = "a list of comma separated string filters to apply across the input dir space",
                            type        = str,
                            dest        = 'dirFilter',
                            optional    = True,
                            default     = '')
        self.add_argument("--dirFilterLogic",
                            help        = "the logic to apply across the dir filter",
                            dest        = 'dirFilterLogic',
                            optional    = True,
                            type        = str,
                            default     = 'OR')
        self.add_argument("--syslog",
                            help        = "show outputs in syslog style",
                            dest        = 'syslog',
                            action      = 'store_true',
                            optional    = True,
                            type        = bool,
                            default     = False)

        self.add_argument("-F", "--tagFile",
                            help        = "JSON formatted file containing tags to sub",
                            dest        = 'tagFile',
                            type        = str,
                            optional    = True,
                            default     = '')
        self.add_argument("-T", "--tagStruct",
                            help        = "JSON formatted tag sub struct",
                            dest        = 'tagStruct',
                            type        = str,
                            optional    = True,
                            default     = '')
        self.add_argument("-n", "--tagInfo",
                            help        = "A custom delimited tag sub struct",
                            dest        = 'tagInfo',
                            type        = str,
                            optional    = True,
                            default     = '')
        self.add_argument("-k","--splitKeyValue",
                            help        = "Expression on which to split the <key><value> pairs",
                            type        = str,
                            dest        = 'splitKeyValue',
                            optional    = True,
                            default     = ",")
        self.add_argument("-s","--splitToken",
                            help        = "Expression on which to split the <delimited_tag_info>",
                            type        = str,
                            dest        = 'splitToken',
                            optional    = True,
                            default     = "++")
        self.add_argument("-o", "--outputFileStem",
                            help        = "output file",
                            default     = "",
                            type        = str,
                            optional    = True,
                            dest        = 'outputFileStem')
        self.add_argument("--printElapsedTime",
                            help        = "print program run time",
                            dest        = 'printElapsedTime',
                            action      = 'store_true',
                            type        = bool,
                            optional    = True,
                            default     = False)
        self.add_argument("--threads",
                            help        = "number of threads for innermost loop processing",
                            dest        = 'threads',
                            type        = str,
                            optional    = True,
                            default     = "0")
        self.add_argument("--outputLeafDir",
                            help        = "formatting spec for output leaf directory",
                            dest        = 'outputLeafDir',
                            type        = str,
                            optional    = True,
                            default     = "")
        self.add_argument("-y", "--synopsis",
                            help        = "short synopsis",
                            dest        = 'synopsis',
                            action      = 'store_true',
                            type        = bool,
                            optional    = True,
                            default     = False)
        self.add_argument("--jsonReturn",
                            help        = "output final return in json",
                            dest        = 'jsonReturn',
                            action      = 'store_true',
                            type        = bool,
                            optional    = True,
                            default     = False)
        self.add_argument("--followLinks",
                            help        = "follow symbolic links",
                            dest        = 'followLinks',
                            action      = 'store_true',
                            type        = bool,
                            optional    = True,
                            default     = False)


    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        
        print(Gstr_title)
        print('Version: %s' % self.get_version())
        options.str_desc = ""

        # Output the space of CLI
        d_options = vars(options)
        for k, v in d_options.items():
            print("%20s: %-40s" % (k, v))
        print("")

        pf_dicom_tagSub = pfdicom_tagSub.pfdicom_tagSub(d_options)
        if options.version:
            print('Plugin Version: %s' % Dcm_tagSub.VERSION)
            print('Internal pfdicom_tagSub Version: %s' % pf_dicom_tagSub.str_version)
            sys.exit(0)

        d_pfdicom_tagSub = pf_dicom_tagSub.run(timerStart = True)

        if options.printElapsedTime: 
            pf_dicom_tagSub.dp.qprint(
                                "Elapsed time = %f seconds" % 
                                d_pfdicom_tagSub['runTime']
                            )


    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)
