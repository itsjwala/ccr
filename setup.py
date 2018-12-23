from ccr import __version__

import os
import sys

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup


dependencies = ['requests','docopt']


def publish():
	os.system("python3 setup.py sdist upload")



if sys.argv[-1] == "publish":
	publish()
	sys.exit()


setup(
	name='ccr',
	version='.'.join(str(i) for i in __version__),
	description='command line tool for executing programs with input test file with 40+ languages support',
	url='https://github.com/jigarWala/ccr',
	author='Jigar Wala',
	author_email='jigar.wala@somaiya.edu',
	install_requires=dependencies,
	packages=['ccr'],
	package_dir={'ccr': 'ccr'},
    package_data={'ccr': ['pickle/*.pickle']},
	entry_points={
		'console_scripts': [
			'ccr=ccr.cli:start'
		]
	},
	classifiers=[
		'Intended Audience :: Developers',
		'Natural Language :: English',
		'Programming Language :: Python',
		"Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
	]
	)
