
from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='v_videocompile',
    version='0.1',
    description='Script to compile video tools for VEDA',
    url='http://github.com/yro/v_videocompile',
    author='@yro',
    author_email='greg@willowgrain.io',
    license='',
    packages=['v_videocompile'],
    include_package_data=True,
    install_requires=[
        'pyyaml',
        'nose',
        ],
    data_files=['build_repos.yaml'],
    scripts=['bin/v_videocompile'],
    test_suite='nose.collector',
    tests_require=['nose'],
    zip_safe=False
    )


