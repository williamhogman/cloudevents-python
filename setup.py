#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='cloudevents-python',
      version='0.1.0',
      description='Python implmenetation of cloudevents',
      author='William Rudenmalm',
      author_email='me@whn.se',
      url='https://github.com/williamhogman/cloudevents-python',
      license='MIT',
      packages=find_packages(exclude=['tests*']),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
      ],
)
