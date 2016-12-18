"""
This module contains functions for validating various parts of the input
to the bloglang compiler.
"""

import sys
import BlogObject
import IOHelper

def validate_options(option_set):
    """
    Checks the configuration options for validity.
    """
    options = [option for (option, _) in option_set]
    if not "TITLE:" in options:
        IOHelper.throw_error('no title')
    if len(set(options)) < len(options):
        IOHelper.throw_error('multiple_options')
    # should check the validity of MATHJAX and INLINE_CODE args here
