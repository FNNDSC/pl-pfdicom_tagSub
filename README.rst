################################
pl-pfdicom_tagSub
################################

Abstract
********

This app performs a recursive walk down an input tree, and for each DICOM file (as filtered with a ``-e .dcm``), will 
perform an edit or substitution on a pattern of user specified DICOM tags. Resultant edited files are saved in the  corresponding location in the output tree. This page is not the canonical reference for ``pfdicom_tagSub`` on which this plugin is based. Please see https://github.com/FNNDSC/pfdicom_tagSub for detail about the actual tag substitution process and the pattern of command line flags. 

Note that the only different between this plugin and the reference ``pfdicom_tagSub`` is that the reference has explicit flags for ``inputDir`` and ``outputDir`` while this plugin uses positional arguments for the same.

Run
***

Using ``docker run``
====================

.. code-block:: bash

    docker run -it --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing  \
            fnndsc/pl-pfdicom_tagsub dcm_tagSub.py                      \
            --tagStruct '
            {
                "PatientName":       "anonymized",
                "PatientID":         "%_md5|7_PatientID",
                "AccessionNumber":   "%_md5|10_AccessionNumber",
                "PatientBirthDate":  "%_strmsk|******01_PatientBirthDate"
            }
            ' --threads 0 -v 2 -e .dcm                                  \
            /incoming /outgoing

Assuming that ``$(pwd)/in`` contains a tree of DICOM files, then the above will generate, for each leaf directory node in ``$(pwd)/in`` that contains files satisfying the search constraint of ending in ``.dcm``, new DICOM files with the above tag subsitutions: The ``PatientName`` is set to ``anonymized``, the ``PatientID`` is replaced with the first seven chars of an ``md5`` hash of the original ``PatientID`` -- similarly for the ``AssessionNumber``. Finally the ``PatientBirthDate`` is masked so that the birthday is set to the first of the month.

Debug
*****

Invariably, some debugging will be required. In order to debug efficiently, map the following into their respective locations in the container:

.. code-block:: bash

    docker run -it --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
            -v $(pwd)/dcm_tagSub/dcm_tagSub.py:/usr/src/dcm_tagSub/dcm_tagSub.py  \
            -v $(pwd)/dcm_tagSub/pfdicom_tagSub.py:/usr/local/lib/python3.5/dist-packages/pfdicom_tagSub/pfdicom_tagSub.py \
            fnndsc/pl-pfdicom_tagsub dcm_tagSub.py                          \
            --tagStruct '
            {
                "PatientName":       "anonymized",
                "PatientID":         "%_md5|7_PatientID",
                "AccessionNumber":   "%_md5|10_AccessionNumber",
                "PatientBirthDate":  "%_strmsk|******01_PatientBirthDate"
            }
            ' --threads 0 -v 2 -e .dcm                                      \
            /incoming /outgoing

This assumes that the source code the underlying ``pfdicom_tagExtract.py`` module is accessible as shown.

Make sure that the host ``$(pwd)/out`` directory is world writable!

