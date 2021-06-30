pl-pfdicom_tagSub
================================

.. image:: https://img.shields.io/docker/v/fnndsc/pl-pfdicom_tagSub?sort=semver
    :target: https://hub.docker.com/r/fnndsc/pl-pfdicom_tagSub

.. image:: https://img.shields.io/github/license/fnndsc/pl-pfdicom_tagSub
    :target: https://github.com/FNNDSC/pl-pfdicom_tagSub/blob/master/LICENSE

.. image:: https://github.com/FNNDSC/pl-pfdicom_tagSub/workflows/ci/badge.svg
    :target: https://github.com/FNNDSC/pl-pfdicom_tagSub/actions


.. contents:: Table of Contents


Abstract
--------

This app performs a recursive walk down an input tree, and for each DICOM file (as filtered with a -e .dcm), will perform an edit or substitution on a pattern of user specified DICOM tags. Resultant edited files are saved in the corresponding location in the output tree. This page is not the canonical reference for pfdicom_tagSub on which this plugin is based. Please see https://github.com/FNNDSC/pfdicom_tagSub for detail about the actual tag substitution process and the pattern of command line flags.

Note that the only different between this plugin and the reference pfdicom_tagSub is that the reference has explicit flags for inputDir and outputDir while this plugin uses positional arguments for the same.


Description
-----------

``pl-pfdicom_tagsub`` is a ChRIS-based application that wraps around pfdicom_tagSub and is used to edit the contents of user-specified DICOM tags..


Usage
-----

.. code::

    python dcm_tagSub.py
        [-h|--help]
        [--json] [--man] [--meta]
        [--savejson <DIR>]
        [-v|--verbosity <level>]
        [--version]
        [-e|--extension <DICOMextension>]
        [-O|--outputDir <outputDir>]
        [-F|--tagFile <JSONtagFile>]
        [-T|--tagStruct <JSONtagStructure>]
        [-n|--tagInfo <delimited_parameters>]
        [-s|--splitToken <split_token>]
        [-k|--splitKeyValue <keySplit>]             
        [-o|--outputFileStem <outputFileStem>]
        [--outputLeafDir <outputLeafDirFormat>]
        [--threads <numThreads>]
        <inputDir> <outputDir>


Arguments
~~~~~~~~~

.. code::

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


Getting inline help is:

.. code:: bash

    docker run --rm fnndsc/pl-pfdicom_tagSub dcm_tagSub --man

Run
~~~

You need to specify input and output directories using the `-v` flag to `docker run`.


.. code:: bash

    docker run --rm -u $(id -u)                             \
        -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
        fnndsc/pl-pfdicom_tagSub dcm_tagSub             \
        /incoming /outgoing


Development
-----------

Build the Docker container:

.. code:: bash

    docker build -t local/pl-pfdicom_tagSub .

Run unit tests:

.. code:: bash

    docker run --rm local/pl-pfdicom_tagSub nosetests

Examples
--------

.. code:: bash

    docker run -it --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing  \
        fnndsc/pl-pfdicom_tagsub dcm_tagSub                             \
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
        ' --threads 0 -v 2 -e .dcm                                  \
        /incoming /outgoing

 -- OR equivalently --
 
 .. code:: bash
 
    docker run -it --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing  \
        fnndsc/pl-pfdicom_tagsub dcm_tagSub                             \
            -e dcm                                                      \
            --splitToken ","                                            \
            --splitKeyValue "="                                         \
            --tagInfo '
                PatientName         =  %_name|patientID_PatientName,
                PatientID           =  %_md5|7_PatientID,
                AccessionNumber     =  %_md5|8_AccessionNumber,
                PatientBirthDate    =  %_strmsk|******01_PatientBirthDate,
                re:.*hysician       =  %_md5|4_#tag,
                re:.*stitution      =  #tag,
                re:.*ddress         =  #tag
            ' --threads 0 --printElapsedTime

.. image:: https://raw.githubusercontent.com/FNNDSC/cookiecutter-chrisapp/master/doc/assets/badge/light.png
    :target: https://chrisstore.co
