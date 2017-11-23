import sys

filename = sys.argv[1]
ascii_range = range(32, 127)
# figure out how to catch escape chars that aren't part of an html tag
escape_chars = [] #['<', '>', '&']

with open(filename, 'r') as f:
    for index, line in enumerate(f):
        line = line.rstrip('\n')
        if any((ord(char) not in ascii_range) or (char in escape_chars) for char in line):
            print("{} | {}".format(str(index).zfill(3), line))
