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
            line = line[:locbold] + "<b>" + line[locbold+2:locunbold] + "</b>" + line[locunbold+2]
        
        # catch italic
        locital = line.find("*")
        locunital = line.find("*",locital+1)
        if locital >= 0 and locunital >=0:
            line = line[:locital] + "<b>" + line[locital+1:locunital] + "</b>" + line[locunital+1]
    return line

def header(line):
    if line[0]=="#":
        line = "<atitle>\n"+line[1:]+"</atitle>/n"
    elif line[0]=="##":
        line = "<sh>\n" + line[1:] + "</sh>/n"
    return line

def process(line):
    """ process a single line: parse from BlogLang to HTML"""
    line = line.lstrip(" ")
    line = substitute(line)
    line = handle_links(line)
    line = bullet(line)
    line = emphasis(line)
    line = header(line)
    return line

def main():
    infile = sys.argv[1]
    with open(infile,'r') as f:
        lines = f.readlines()
    lines = map(lambda x: process(x), lines)
    print lines
    
if __name__=='__main__':
    main()
