import re
''' 
Challenge for those more comfortable: If you’re feeling more comfortable, 
try implementing the Markdown to HTML conversion without using any external 
libraries, supporting headings, boldface text, unordered lists, links, and 
paragraphs. You may find using regular expressions in Python helpful.
'''

def main():
    test_content = '''# This is a header
## This is a smaller header
### This is an even smaller header 

This is a paragraph with **bold** text and text.

- This is a list item
- This is another list item
- This is a third list item
'''
    print('\n')
    print(test_content)
    print('\n')

    content = convert_headers(test_content)
    print(content)
    print('\n')

    content = convert_bold(content)
    print(content)
    print('\n')

    content = convert_ul(content)
    print(content)
    print('\n')

    # content = convert_paragraphs(content)
    # print(content)


# Function that uses regex to convert markdown to html
def md_converter(content):
    html_content = convert_headers(convert_bold(convert_ul(content)))

    return html_content


def convert_headers(content):
    content = re.sub(r'(?m)^(#{1,6})\s*(.+?)$', r'<\1>\2</\1>', content)
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
    lines = content.splitlines()
    inside_para = False
    for line in lines:
        if re.match(r'^\s*$', line):
            if not re.match(r'^(<h.>)|(<ul>)', lines[lines.index(line)+1] ):
                if not inside_para:
                    lines[lines.index(line)] = '<p>'
                    inside_para = True
            else:
                lines.insert(lines.index(line), '</p>')
                inside_para = False
    if inside_para:
        lines.append('</p>')
    
    content = '\n'.join(lines)
    return content

                
if __name__ == "__main__":
    main()
