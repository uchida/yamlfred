'''
yamlfred:

Note that "python setup.py test" invokes pytest on the package. With appropriately
configured setup.cfg, this will check both xxx_test modules and docstrings.

Copyright 2014, Akihiro Uchida.
Licensed under CC0.
'''
from setuptools import setup, find_packages

version = "0.1"

setup(name="yamlfred",
      version=version,
      description="manage Alfred workflow via yaml templates",
      long_description=open("README.rst").read(),
      classifiers=[ # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 1 - Planning',
        'Programming Language :: Python'
      ],
      keywords="", # Separate with spaces
      author="Akihiro Uchida",
      author_email="",
      url="",
      license="CC0",
      packages=find_packages(exclude=['examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=['PyYAML'],
      entry_points={
        'console_scripts':
            ['yamlfred=yamlfred:main']
      }
)
