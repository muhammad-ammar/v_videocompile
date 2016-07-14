
from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='ff_compiler',
    version='0.1',
    description='Script to compile ffmpeg',
    url='http://github.com/yro/ff_compiler',
    author='@yro',
    author_email='greg@willowgrain.io',
    license='',
    packages=['ff_compiler'],
    include_package_data=True,
    install_requires=[
        'pyyaml',
        'nose',
        ],
    test_suite='nose.collector',
    tests_require=['nose'],
    zip_safe=False
    )


FF = FFCompiler()
if FF.check() is False:
    FF.run()

