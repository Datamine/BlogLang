"""
This is a parser for BlogLang files. Read the docs at github.com/datamine/bloglang.
John Loeber | Python 2.7.10 | contact@johnloeber.com | October 31, 2016 (spooky.)
"""

import sys

CONFIGURATION_OPTIONS = ["TITLE:", "MATHJAX:", "INLINE_CODE:"]
# global variables: config options
title = ''
mathjax = False
inline_code = False

# global variables: other junk
footnotes = False
current_footnote_body = 0
current_footnote_end = 0

def throw_error(complaint):
    """
    Throw various errors with helpful descriptions.
    """
    error_messages = {'bad_file':  "You did not supply a valid bloglang file as a command-line argument.",
                      'multiple_options': "You supplied multiple arguments for the same configuration option.",
                      'no_title': "You must supply an argument to title configuration."}
    sys.stderr.write("Error!" + error_messages[complaint] + "\n")
    sys.exit(1)

def open_template():
    """
    Open and return the template.
    """
    with open('template.html') as f:
        return f.readlines()

def open_bloglang_file():
    """
    Open and return the blog file. Handle the case when no valid file is supplied.
    """
    if len(sys.argv) == 1:
        throw_error('bad_file')

    with open(sys.argv[1]) as f:
        # filter out comments, strip extraneous whitespace and newlines
        blog_lines = map(lambda x: x.strip(), filter(lambda x: x[0] != '%', f.readlines()))
        if len(blog_lines) == 0:
            throw_error('bad_file')

    # do more AST parsing here?
    line_offset = handle_config_options(blog_lines)
    return blog_lines[line_offset:]

def set_options(option_set):
    """
    Set the options to their configuration arguments. All option names are ensured
    validity by handle_config_options, and arguments are already stripped.
    """
    for (option_name, argument) in option_set:
        sys.stdout.write("Setting option " + option_name[:-1] + " to '" + argument + "'\n")
        if option_name == "TITLE:":
            global title
            title = argument
        elif option_name == "MATHJAX:":
            global mathjax
            mathjax = argument.upper()
        elif option_name == "INLINE_CODE:":
            global inline_code
            inline_code = argument.lower()

def validate_options(option_set):
    """
    Checks the configuration options for validity.
    """
    options = [option for (option, _) in option_set]
    if not "TITLE:" in options:
        throw_error('no title')
    if len(set(options)) < len(options):
        throw_error('multiple_options')
    # should check the validity of MATHJAX and INLINE_CODE args here

def handle_config_options(blog_lines):
    """
    Set various configuration options for the output.
    The configuration options are set by the first lines in the blog file,
    so we return the number of those lines, so we can omit them as we proceed.
    """
    global CONFIGURATION_OPTIONS
    option_set = []
    for line in blog_lines:
        for option in CONFIGURATION_OPTIONS:
            if option in line:
                argument = line[len(option):].strip()
                option_set.append((option, argument))
                break
        else:
            # if a line contains no config options, then stop processing.
            break

    validate_options(option_set)
    set_options(option_set)
    # return the number of lines that we processed/can omit going forward.
    return len(option_set)

def plaintext_substitution(line):
    """
    Replace particular text (punctuation) with its proper HTML representation.
    """
    # turn primes into apostrophes
    # turn double-primes into quotation marks
    # less than, greater than

    # also handle: ampersands, em dashes, en dashes
    return line

def main():
    """
    Main function... fill this in
    """
    template = open_template()
    blog_lines = map(plaintext_substitution, open_bloglang_file())

if __name__ == '__main__':
    main()
