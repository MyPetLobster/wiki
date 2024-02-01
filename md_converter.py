import re
''' 
Challenge for those more comfortable: If you’re feeling more comfortable, 
try implementing the Markdown to HTML conversion without using any external 
libraries, supporting headings, boldface text, unordered lists, links, and 
paragraphs. You may find using regular expressions in Python helpful.
'''
# Function that uses regex to convert markdown to html
def md_converter(content):
    html_content = convert_headers(convert_bold(convert_ul(content)))

    return html_content


def convert_headers(content):
    # Do i need that \s at the end of this?
    content = re.sub(r'(?m)^(#{1,6})\s*(.+?)\s*$', r'<\1>\2</\1>', content)
    content = content.replace('<#>', '<h1>').replace('</#>', '</h1>')
    content = content.replace('<##>', '<h2>').replace('</##>', '</h2>')
    content = content.replace('<###>', '<h3>').replace('</###>', '</h3>')
    content = content.replace('<####>', '<h4>').replace('</####>', '</h4>')
    content = content.replace('<#####>', '<h5>').replace('</#####>', '</h5>')
    content = content.replace('<######>', '<h6>').replace('</######>', '</h6>')
    return content

def convert_bold(content):
    return re.sub(r'(?m)\*\*(.+?)\*\*', r'<strong>\1</strong>', content)

def convert_ul(content):
    content = re.sub(r'(?m)^(\s*)?[-|*|+]\s*(.+?)\s*$', r'\1    <li>\2</li>', content)
    lines = content.splitlines()
    inside_ul = False

    for line in lines:
        # Check if the line contains an <li> tag
        if '<li>' in line:
            # If not already inside a list, insert <ul> tag before the first <li> tag
            if not inside_ul:
                lines.insert(lines.index(line), '<ul>')
                inside_ul = True
        else:
            # If inside a list, insert </ul> tag before this line
            if inside_ul:
                lines.insert(lines.index(line), '</ul>')
                inside_ul = False

    if inside_ul:
        lines.append('</ul>')

    content = '\n'.join(lines)

    return content

def convert_paragraphs(content):
    content = re.sub(r'', r'', content)

content = '''
- test item one
- test item two
-test item three
    - indent one
    - indent two
- test item 4

<p>Not a list a paragraph</p>

- LIST two item one
- List two item two
'''