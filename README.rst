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

This plugin wraps around pfdicom_tagSub and is used to edit the contents of user-specified DICOM tags.


Description
-----------

``pfdicom_tagsub`` is a ChRIS-based application that...


Usage
-----

.. code::

    python pfdicom_tagsub.py
        [-h|--help]
        [--json] [--man] [--meta]
        [--savejson <DIR>]
        [-v|--verbosity <level>]
        [--version]
        [-e|--extension <DICOMextension>]
        [-O|--outputDir <outputDir>]
        [-F|--tagFile <JSONtagFile>]
        [-T|--tagStruct <JSONtagStructure>]
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
    passed directly in the command line.

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

    docker run --rm fnndsc/pl-pfdicom_tagSub pfdicom_tagsub --man

Run
~~~

You need to specify input and output directories using the `-v` flag to `docker run`.


.. code:: bash

    docker run --rm -u $(id -u)                             \
        -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
        fnndsc/pl-pfdicom_tagSub pfdicom_tagsub                        \
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

Put some examples here!


.. image:: https://raw.githubusercontent.com/FNNDSC/cookiecutter-chrisapp/master/doc/assets/badge/light.png
    :target: https://chrisstore.co
