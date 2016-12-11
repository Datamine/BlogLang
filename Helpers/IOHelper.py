"""
IO Helpers for Bloglang
Also handles error throwing
"""

import sys

def throw_error(complaint):
    """
    Throw various errors with helpful descriptions.
    """
    error_messages = {'bad_file': "You did not supply a valid bloglang file as a command-line argument.",
                      'multiple_options': "You supplied multiple arguments for the same configuration option.",
                      'no_title': "You must supply an argument to title configuration."}
    raise Exception("Error!" + error_messages[complaint] + "\n")

def open_template():
    """
    Open and return the template.
    """
    TEMPLATE_FILENAME = 'template.html'
    with open(TEMPLATE_FILENAME, 'r') as f:
        return f.readlines()

def open_bloglang_file():
    """
    Open and return the blog file. Handle the case when no valid file is supplied.
    """
    if len(sys.argv) == 1:
        throw_error('bad_file')

    with open(sys.argv[1], 'r') as f:
        # filter out comments, strip extraneous whitespace and newlines
        filtered_comments = filter(lambda x: x[0] != '%', f.readlines())
        # strip extraneous whitespace and newlines
        blog_lines = [x.strip(' ') for x in filtered_comments]
        if len(blog_lines) == 0:
            throw_error('bad_file')

    return blog_lines
