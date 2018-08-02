#                                                            _
# dcm_tagSub ds app
#
# (c) 2016 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

import os

# import the Chris app superclass
from chrisapp.base import ChrisApp

# import the pfdicom_tagSub module
import  pfdicom_tagSub
import  pudb
import  sys


class Dcm_tagSub(ChrisApp):
    """
    This plugin wraps around pfdicom_tagSub and is used to edit the contents of user-specified DICOM tags..
    """
    AUTHORS                 = 'FNNDSC (dev@babyMRI.org)'
    SELFPATH                = os.path.dirname(os.path.abspath(__file__))
    SELFEXEC                = os.path.basename(__file__)
    EXECSHELL               = 'python3'
    TITLE                   = 'Edits various specified DICOM tags'
    CATEGORY                = 'DICOM'
    TYPE                    = 'ds'
    DESCRIPTION             = 'This plugin wraps around pfdicom_tagSub and is used to edit the contents of user-specified DICOM tags.'
    DOCUMENTATION           = 'https://github.com/FNNDSC/pl-pfdicom_tagSub'
    VERSION                 = '1.0'
    ICON                    = '' # url of an icon image
    LICENSE                 = 'Opensource (MIT)'
    MAX_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MIN_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MAX_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MIN_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MAX_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_GPU_LIMIT           = 0  # Override with the minimum number of GPUs, as an integer, for your plugin
    MAX_GPU_LIMIT           = 0  # Override with the maximum number of GPUs, as an integer, for your plugin

    # Fill out this with key-value output descriptive info (such as an output file path
    # relative to the output dir) that you want to save to the output meta file when
    # called with the --saveoutputmeta flag
    OUTPUT_META_DICT = {}
 
    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
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
        self.add_argument("-x", "--man",
                            help        = "man",
                            dest        = 'man',
                            action      = 'store_true',
                            type        = bool,
                            optional    = True,
                            default     = False)
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
        self.add_argument("-v", "--verbosity",
                            help        = "verbosity level for app",
                            dest        = 'verbosity',
                            type        = str,
                            optional    = True,
                            default     = "1")
        self.add_argument('--version',
                            help        = 'if specified, print version number',
                            dest        = 'b_version',
                            action      = 'store_true',
                            type        = bool,
                            optional    = True,
                            default     = False)

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        pf_dicom_tagSub = pfdicom_tagSub.pfdicom_tagSub(
                        inputDir            = options.inputdir,
                        inputFile           = options.inputFile,
                        extension           = options.extension,
                        outputDir           = options.outputdir,
                        outputFileStem      = options.outputFileStem,
                        outputLeafDir       = options.outputLeafDir,
                        tagFile             = options.tagFile,
                        tagStruct           = options.tagStruct,
                        threads             = options.threads,
                        verbosity           = options.verbosity,
                        json                = options.jsonReturn
                    )

        if options.b_version:
            print('Plugin Version: %s' % Dcm_tagSub.VERSION)
            print('Internal pfdicom_tagSub Version: %s' % pf_dicom_tagSub.str_version)
            sys.exit(0)

        d_pfdicom_tagSub = pf_dicom_tagSub.run(timerStart = True)

        if options.printElapsedTime: 
            pf_dicom_tagSub.dp.qprint(
                                "Elapsed time = %f seconds" % 
                                d_pfdicom_tagSub['runTime']
                            )


# ENTRYPOINT
if __name__ == "__main__":
    app = Dcm_tagSub()
    app.launch()
