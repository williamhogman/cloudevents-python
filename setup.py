#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='cloudevents-python',
      version='0.2.1',
      description='Python implmenetation of cloudevents',
      author='William Rudenmalm',
      author_email='me@whn.se',
      url='https://github.com/williamhogman/cloudevents-python',
      license='MIT',
      packages=find_packages(exclude=['tests*']),
      test_suite='nose.collector',
      tests_require=['nose', 'requests_mock>=1.4.0', 'requests>=2.18.4'],
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
