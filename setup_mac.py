from setuptools import setup

APP = ['Cooltrollers_v16_2.py']
OPTIONS = {'argv_emulation': True, 'includes': ['EXTERNAL LIBRARY'],}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)