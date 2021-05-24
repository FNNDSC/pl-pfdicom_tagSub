from os import path
from setuptools import setup

with open(path.join(path.dirname(path.abspath(__file__)), 'README.rst')) as f:
    readme = f.read()

setup(
    name             = 'dcm_tagSub',
    version          = '3.0.0',
    description      = 'This plugin wraps around pfdicom_tagSub and is used to edit the contents of user-specified DICOM tags.',
    long_description = readme,
    author           = 'Sandip Samal',
    author_email     = 'sandip.samal@childrens.harvard.edu',
    url              = 'https://github.com/FNNDSC/pl-pfdicom_tagSub',
    packages         = ['dcm_tagSub'],
    install_requires = ['chrisapp','pfdicom_tagSub'],
    test_suite       = 'nose.collector',
    tests_require    = ['nose'],
    license          = 'MIT',
    zip_safe         = False,
    python_requires  = '>=3.6',
    entry_points     = {
        'console_scripts': [
            'dcm_tagSub = dcm_tagSub.__main__:main'
            ]
        }
)
