"""
This is a parser for BlogLang files. Read the docs at github.com/datamine/bloglang.
John Loeber | Python 2.7.10 | contact@johnloeber.com | October 31, 2016 (spooky.)
"""

import sys
import Helpers.BlogObject as BlogObject

def plaintext_substitution(line):
    """
    Replace particular text (punctuation) with its proper HTML representation.
    """
    # turn primes into apostrophes
    # turn double-primes into quotation marks
    # less than, greater than -- but not in latex

    # also handle: ampersands, em dashes, en dashes
    return line

def main():
    """
    Main function... fill this in
    """
    blog = BlogObject.Blog()

if __name__ == '__main__':
    main()
