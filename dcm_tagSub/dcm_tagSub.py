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
import  pfdicom_tagSub
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

(Edit this in-line help for app specifics. At a minimum, the 
flags below are supported -- in the case of DS apps, both
positional arguments <inputDir> and <outputDir>; for FS and TS apps
only <outputDir> -- and similarly for <in> <out> directories
where necessary.)

    NAME

       pfdicom_tagsub.py 

    SYNOPSIS

        python pfdicom_tagsub.py                                         \\
            [-h] [--help]                                               \\
            [--json]                                                    \\
            [--man]                                                     \\
            [--meta]                                                    \\
            [--savejson <DIR>]                                          \\
            [-v <level>] [--verbosity <level>]                          \\
            [--version]                                                 \\
            <inputDir>                                                  \\
            <outputDir> 

    BRIEF EXAMPLE

        * Bare bones execution

            docker run --rm -u $(id -u)                             \
                -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
                fnndsc/pl-pfdicom_tagSub dcm_tagSub                 \
                /incoming /outgoing

    DESCRIPTION

        `pfdicom_tagsub.py` ...

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
    MIN_CPU_LIMIT           = 1000 # Override with millicore value as int (1000 millicores == 1 CPU core)
    MIN_MEMORY_LIMIT        = 200  # Override with memory MegaByte (MB) limit as int
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
        self.add_argument("-e", "--extension",
                            help        = "DICOM file extension",
                            dest        = 'extension',
                            type        = str,
                            optional    = True,
                            default     = '')
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
        self.add_argument("-I", "--tagInfo",
                            help        = "Semicolon-delimited tag sub struct",
                            dest        = 'tagInfo',
                            type        = str,
                            optional    = True,
                            default     = '')
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

    @staticmethod
    def tag_info_to_struct(tagInfo):
        fields = re.findall(r'(?:^|;\s*)"(.*?)"\s*:\s*"(.*?)"', tagInfo.strip())
        return json.dumps(dict(fields))

    def get_tag_struct(self, options):
        if options.tagStruct and options.tagInfo:
            msg = " Must give either tagStruct or tagInfo, not both."
            raise ValueError(msg)
        if options.tagInfo:
            return self.tag_info_to_struct(options.tagInfo)
        return options.tagStruct

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        
        print(Gstr_title)
        print('Version: %s' % self.get_version())
        pf_dicom_tagSub = pfdicom_tagSub.pfdicom_tagSub(
                        inputDir            = options.inputdir,
                        inputFile           = options.inputFile,
                        extension           = options.extension,
                        outputDir           = options.outputdir,
                        outputFileStem      = options.outputFileStem,
                        outputLeafDir       = options.outputLeafDir,
                        tagFile             = options.tagFile,
                        tagStruct           = self.get_tag_struct(options),
                        threads             = options.threads,
                        verbosity           = options.verbosity,
                        followLinks         = options.followLinks,
                        json                = options.jsonReturn
                    )

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
