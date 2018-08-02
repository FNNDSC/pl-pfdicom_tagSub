################################
pl-pfdicom_tagSub
################################


Abstract
********

This plugin wraps around pfdicom_tagSub and is used to edit the contents of user-specified DICOM tags.

Run
***

Using ``docker run``
====================

Assign an "input" directory to ``/incoming`` and an output directory to ``/outgoing``

.. code-block:: bash

    docker run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing   \
            fnndsc/pl-pfdicom_tagSub dcm_tagSub.py            \
            /incoming /outgoing

This will ...

Make sure that the host ``$(pwd)/out`` directory is world writable!







