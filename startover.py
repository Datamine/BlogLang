"""
This is a parser for BlogLang files. Read the docs at github.com/datamine/bloglang.
John Loeber | Python 2.7.10 | contact@johnloeber.com | October 31, 2016 (spooky.)
"""

import sys

footnotes = False
current_footnote_body = 0
current_footnote_end = 0

# configuration options are all falsy by default.
title = ''
mathjax = False
inline_code = False

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
    line_offset = set_config_options(blog_lines)
    return blog_lines[line_offset:]

def set_global_arg_for_config_option(global_option, option_name, argument):
    """
    Set the global argument for the configuration option. Check first that it isn't
    already set. Note that the default args for all the config opts are falsy.
    """
    sys.stdout.write("Setting option " + option_name[:-1] + " to " + argument + "\n")
    global global_option
    if global_option:
        throw_error('multiple_options')
    else:
        global_option = argument

def set_config_option(option, argument):
    """
    Set an individual configuration option. Check that it isn't already set.
    We call this from set_config_options, where we've ensured that _option_ is
    valid. NB: this code technically lets the user set an argument to '' as many
    times as they like, because it's recognized as falsy, but this is not a
    concerning bug. -- actually no this sucks. need to change.
    """
    sys.stdout.write("Setting option " + option[:-1] + " to " + argument + "\n")
    if option == "TITLE:":
        global title
        if title:
            throw_error('multiple_options')
        else:
            title = argument
    elif option == "MATHJAX:":
         global mathjax
         if mathjax:
            throw_error('multiple_options')
         else:
            mathjax = argument.lower()
    elif option == "INLINE_CODE:":
        global inline_code
        if inline_code:
            throw_error('multiple_options')
        else:
            inline_code = argument.lower()

def set_config_options(blog_lines):
    """
    Set various configuration options for the output.
    The configuration options are set by the first lines in the blog file,
    so we return the number of those lines, so we can omit them as we proceed.
    """
    configuration_options = ["TITLE:", "MATHJAX:", "INLINE_CODE:"]
    options_set = 0
    for line in blog_lines:
        for option in configuration_options:
            if option in line:
                argument = line[len(option):].strip()
                set_config_option(option, argument)
                break
        else:
            # if this line contains no config options, then stop processing.
            abreak

    global title
    if title == '':
        throw_error('no_title')
    # return the number of lines that we processed/can omit going forward.
    return options_set

def main():
    template = open_template()
    blog_lines = open_bloglang_file()
    print [title, mathjax, inline_code]
if __name__ == '__main__':
    main()
