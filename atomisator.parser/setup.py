import codecs
import os
# import sys
 
try:
    from setuptools import setup, find_packages
except:
    from distutils.core import setup

 
# def read(fname):
#     return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()
 
setup(
    name = 'atomisator.parser',
    version = '0.1.0',
    description = 'This is parser.',
    long_description = 'LONG_DESCRIPTION',
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords = 'atomisator.parser',
    author = 'maidi',
    author_email = '',
    url = '',
    license = 'MIT',
    packages = find_packages(exclude=['ez_setup']),
    namespace_packages = ['atomisator'],
    include_package_data=True,
    # zip_safe=True,
    install_requires=[
        'setuptools', 
        'feedparser'],
    test_suite = 'nose.collector',
    test_requires = ['Nose'],
    entry_points = """
    """,
)