#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    "pyvcf",
    "sqlalchemy"
]

test_requirements = []

setup(
    name='vcf-annotate-polyphen',
    version='0.1.2',
    description="a tool to annotate human VCF files with PolyPhen2 effect measures",
    long_description=readme,
    author="B. Arman Aksoy",
    author_email='arman@aksoy.org',
    url='https://github.com/hammerlab/vcf-annotate-polyphen',
    packages=['vap'],
    package_dir={'vap': 'vap'},
    include_package_data=True,
    install_requires=requirements,
    license="http://www.apache.org/licenses/LICENSE-2.0.html",
    zip_safe=False,
    keywords='vcf-annotate-polyphen',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    entry_points = {'console_scripts': ['vcf-annotate-polyphen=vap.cli:main']},
    test_suite='tests',
    tests_require=test_requirements
)
