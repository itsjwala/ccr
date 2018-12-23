#!/usr/bin/env python3

"""
Code Compile Run (CCR)

Usage:
    ccr (<SOURCE>) [-i <INPUT>] [-l <LANG>]
    ccr (-h | --help)
    ccr --version
Example:
    ccr ./test.py -i ./input.txt -l python3
Arguments:
    <SOURCE>        - Source file
Options:
    -v --version    - Show version
    -h --help       - Show this screen
    -i <INPUT>      - optional input file
    -l <LANG>       - optional supported language
Note:
supported languages :
- c             - c++14	        - java
- python	- python3	- pypy
- c#	        - pascal	- ruby
- php	        - go	        - javascript
- haskell	- rust	        - scala
- swift	        - d	        - perl
- fortran	- whitespace	- ada_95
- ocaml	        - intercal	- brainf**k
- assembler	- clips	        - prolog
- icon	        - scheme	- pike
- smalltalk	- jar	        - nice
- lua	        - bash	        - nemerle
- common_lisp	- erlang	- tcl
- kotlin	- perl6	        - text
- pypy_3	- clojure	- cobol
- f#
"""

import os
# import time

from docopt import docopt
from .__init__ import __version__
from .CodeCompileRun import CCR
# import logging

# logger = logging.getLogger("ccr")
# logger.setLevel("INFO")

def start():

	arguments = docopt(__doc__, version='ccr version '+'.'.join(str(i) for i in __version__))
	try:
		source_file_path = os.path.join(os.getcwd(), arguments.get('<SOURCE>'))
		if not os.path.exists(source_file_path):
			raise IOError("Path {} doesn't exist".format(source_file_path))
		input_file_path = arguments.get('-i',None)
		if input_file_path:
			input_file_path =  os.path.join(os.getcwd(),input_file_path[0])
			if not os.path.exists(input_file_path):
				raise IOError("Path {} doesn't exist".format(input_file_path))

		language = arguments.get("-l",None)
		if language:
			language = language[0]

		CCR(source_file_path=source_file_path,input_file_path=input_file_path,lang=language).execute()
	except IOError as e:
		print(e)
	except KeyboardInterrupt:
		print("\nClosing ccr unexpectedly..")
	except Exception as e:
		print("Something Bad happened ;( ; {}".format(e))

