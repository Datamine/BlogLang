"""
An object to represent the bloglang -> HTML transition
"""

import IOHelper
import ValidationHelper
import Utils
import sys

class Blog(object):
    """
    Object-Oriented way of handling the bloglang -> HTML transition
    """

    CONFIGURATION_OPTIONS = ["TITLE:", "MATHJAX:", "INLINE_CODE:"]

    def __init__(self):
        self.option_title = ''
        self.option_mathjax = False
        self.option_inline_code = False

        self.template = IOHelper.open_template()
        self.blog_lines = IOHelper.open_bloglang_file()
        self.set_options()
        return

    def set_options(self):
        """
        Set the options to their configuration arguments.
        """
        option_set = []
        for line in self.blog_lines:
            for option in self.CONFIGURATION_OPTIONS:
                if option in line:
                    # I don't need to.strip() the line because that's done in open_bloglang_file
                    argument = line[len(option):]
                    option_set.append((option, argument))
                break
            else:
                # if a line contains no config options, then stop processing.
                break

        ValidationHelper.validate_options(option_set)

        # set the options
        for (option_name, argument) in option_set:
            sys.stdout.write("Setting option " + option_name[:-1] + " to '" + argument + "'\n")
            if option_name == "TITLE:":
                self.title = argument
            elif option_name == "MATHJAX:":
                self.mathjax = argument.upper()
            elif option_name == "INLINE_CODE:":
                self.inline_code = argument.lower()

        # omit the option lines -- they're irrelevant from here on
        self.blogfile = self.blogfile[len(option_set):]

    def tokenize(self):

