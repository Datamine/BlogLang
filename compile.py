# John Loeber | Python 2.7.10 | contact@johnloeber.com | December 28, 2015

import sys
import itertools

footnotes = False

def handle_links(line):
    """ turn BlogLang links into HTML links"""
    while "[" in line and "]" in line:
        start_text = line.index("[")
        end_text = line.index("]")
        # allow for some spaces. note: this does not allow for links across lines
        try:
            if line[end_text+1]=="(" or line[end_text+2]=="(" or line[end_text+3]=="(":
                start_url = line.index("(",end_text)
                end_url =   line.index(")",end_text)
                text = line[start_text+1:end_text]
                url = line[start_url+1:end_url]
                replace = '<a href="' + url + '">' + text + "</a>"
                line = line[:start_text] + replace + line[end_url+1:]
            else:
                break
        except:
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
        line = "<li>" + line[1:] + "</li>"
    else:
        try:
            dot = line.index(".")
            if line[:dot].isdigit():
                # have to differentiate bullets from numbers
                line = "x<li>" + line[dot+1:] + "</li>"
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
     if line[:2]=="##":
        line = "<sh>\n" + line[2:] + "\n</sh>\n"
     elif line[0]=="#":
        line = "<atitle>\n"+line[1:]+"\n</atitle>\n"
     return line

def footnote(line):
    global footnotes
    # footnote reference
    if "^[" in line:
        loc_start = line.find("^[")
        loc_end = line.find("]",loc_start+2)
        content = line[loc_start+2:loc_end]
        text = '<small><sup><a href="footnote' + content + '" name="note' + content + '">[' + content + ']</a></sup></small>'
        line = line[:loc_start] + text + line[loc_end+1:]
        footnotes = True

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

def isplit(iterable,splitters):
    return [list(g) for k,g in itertools.groupby(iterable,lambda x:x in splitters) if not k]

def main():
    infile = sys.argv[1]
    with open(infile,'r') as f:
        lines = f.readlines()
    lines = map(lambda x: x.lstrip(" "), lines)
    lines = map(lambda x: x.rstrip("\n"),lines)
    lines = map(lambda x: x.rstrip(" "),lines)
    # totally leave out comments. do not turn them into <!-- -->
    # this is a conscious design decision to prevent accidental inclusion of unwanted text.
    lines = filter(lambda x: not x.startswith("%"),lines)
    #wrap in paragraphs
    sections = isplit(lines,('',))
    for s in range(len(sections)):
        # omit titles and the first footnote
        if (not sections[s][0].startswith("#")) and (not sections[s][0].startswith('[0]')):
            sections[s] = ["<p>"] + sections[s] + ["</p>"]
    lines = [item for sublist in sections for item in sublist]
    lines = filter(lambda x: x != '', lines)
    lines = map(process, lines)
    lines_copy = []
    for i in range(len(lines)):
        if lines[i].startswith("<atitle"):
            lines_copy.append("<br><br>")
            lines_copy.append(lines[i])
        elif lines[i].startswith("<sh>"):
            if lines[i-1].startswith("<atitle"):
                lines_copy.append("<br><br>")
                lines_copy.append(lines[i])
            else:
                lines_copy.append("<p>")
                lines_copy.append(lines[i])
                lines_copy.append("</p>")
        elif lines[i].startswith("<li>"):
            if not lines[i-1].startswith("<li>"):
                lines_copy.append("<ul>")
            lines_copy.append(lines[i])
            if not lines[i+1].startswith("<li>"):
                lines_copy.append("</ul>")
        elif lines[i].startswith("x<li>"):
            if not lines[i-1].startswith("x<li>"):
                lines_copy.append("<ol>")
            lines_copy.append(lines[i][1:])
            if not lines[i+1].startswith("x<li>"):
                lines_copy.append("</ol>")
        else:
            lines_copy.append(lines[i])
    lines_copy = map(lambda x: x + "\n", lines_copy)
    # now put it in the template
    global footnotes
    with open("template.html",'r') as f:
        template = f.readlines()
    if footnotes:
        start = None
        for x in range(len(lines_copy)):
            if lines_copy[x].startswith('<a href="#note0"'):
                # because the paragraph tag before the footnote
                start = x
                break
        all_lines = template[:39] + lines_copy[:start] + template[39:42] + lines_copy[start:] + template[43:]
    if not footnotes:
        all_lines = template[:39] + lines_copy + template[39:]
    # at this point we're done formatting and can place the completed lines in the template
    with open("output.html","w") as f:
        f.writelines(all_lines)
    
if __name__=='__main__':
    main()
