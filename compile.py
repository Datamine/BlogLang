# John Loeber | Python 2.7.10 | contact@johnloeber.com | December 28, 2015

import sys

def handle_links(line):
    """ turn BlogLang links into HTML links"""
    while "[" in line and "]" in line:
        start_text = line.index("[")
        end_text = line.index("]")
        # allow for some spaces. note: this does not allow for links across lines
        if line[end_text+1]=="(" or line[end_text+2]=="(" or line[end_text+3]=="(":
            start_url = line.index("(",end_text)
            end_url =   line.index(")",end_text)
            text = line[start_text+1:end_text]
            url = line[start_url+1:end_url]
            replace = '<a href="' + url + '">' + text + "</a>"
            line = line[:start_text] + replace + line[end_url+1:]
        else:
            break
    return line

def substitute(line):
    """ carry out special character substitutions """
    line = line.replace("--","&mdash;")
    line = line.replace(" '"," &lsquo;")
    line = line.replace("'"," &rsquo;")
    line = line.replace(' "'," &ldquo;")
    line = line.replace('"'," &rdquo;")
    return line

def bullet(line):
    if line[0]=="*":
        line = "<li>" + line[1:]
    else:
        try:
            dot = line.index(".")
            if line[:dot].isdigit():
                line = "<li>" + line[dot+1:]
        except:
            pass
    return line

def emphasis(line):
    """ parse italic and bold markup """
    while line.count("*")>0:
        # catch bold
        locbold = line.find("**")
        locunbold = line.find("**",locbold+1)   
        if locbold >= 0 and locunbold >=0:
            line = line[:locbold] + "<b>" + line[locbold+2:locunbold] + "</b>" + line[locunbold+2:]
        
        # catch italic
        locital = line.find("*")
        locunital = line.find("*",locital+1)
        if locital >= 0 and locunital >=0:
            line = line[:locital] + "<b>" + line[locital+1:locunital] + "</b>" + line[locunital+1:]
    return line

def code(line):
    while line.count("`")>0:
        loc_code = line.find("`")
        loc_uncode = line.find("`",loc_code+1)
        if loc_code >= 0 and loc_uncode >= 0:
            line = line[:loc_code] + "<code>" + line[loc_code+1:loc_uncode] + "</code>" + line[loc_uncode+1:]
        else:
            break
    return line

def header(line):
    if line[0]=="#":
        line = "<atitle>\n"+line[1:]+"</atitle>/n"
    elif line[0]=="##":
        line = "<sh>\n" + line[1:] + "</sh>/n"
    return line

def footnote(line):
    # footnote reference
    if "^[" in line:
        loc_start = line.find("^[")
        loc_end = line.find("]",loc_start+2)
        content = line[loc_start+2,loc_end]
        text = '<small><sup><a href="footnote' + content + '" name="note' + content + '">[' + content + ']</a></sup></small>'
        line = line[:loc_start] + text + line[loc_end+1:]

    # footnote itself
    if line.startswith("["):
        loc_end = line.find("]")
        content = line[1:loc_end]
        if content.isdigit():
            text = '<a href="#note' + content + '" name="footnote' + content + '">[' + content + ']</a> '
            line = text + line[loc_end+1:]
    return line
            
def process(line):
    """ process a single line: parse from BlogLang to HTML"""
    line = substitute(line)
    line = handle_links(line)
    line = bullet(line)
    line = emphasis(line)
    line = header(line)
    line = code(line)
    line = footnote(line)
    return line

def main():
    infile = sys.argv[1]
    with open(infile,'r') as f:
        lines = f.readlines()
    lines = map(lambda x: x.lstrip(" "),lines)
    # totally leave out comments. do not turn them into <!-- -->
    # this is a conscious design decision to prevent accidental inclusion of unwanted text.
    lines = filter(lambda x: not x.startswith("%"),lines)
    lines = map(process, lines)
    print lines
    
if __name__=='__main__':
    main()
