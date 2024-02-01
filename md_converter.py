import re
''' 
Challenge for those more comfortable: If you’re feeling more comfortable, 
try implementing the Markdown to HTML conversion without using any external 
libraries, supporting headings, boldface text, unordered lists, links, and 
paragraphs. You may find using regular expressions in Python helpful.
'''
# Function that uses regex to convert markdown to html
def md_converter(content):
    # Convert headers 

    # Do i need that \s at the end of this?
    content = re.sub(r'(?m)^(#{1,6})\s*(.+?)\s*$', r'<\1>\2</\1>', content)
    content = content.replace('<#>', '<h1>').replace('</#>', '</h1>')
    content = content.replace('<##>', '<h2>').replace('</##>', '</h2>')
    content = content.replace('<###>', '<h3>').replace('</###>', '</h3>')
    content = content.replace('<####>', '<h4>').replace('</####>', '</h4>')
    content = content.replace('<#####>', '<h5>').replace('</#####>', '</h5>')
    content = content.replace('<######>', '<h6>').replace('</######>', '</h6>')

    # Convert boldface text
    content = re.sub(r'(?m)\*\*(.+?)\*\*', r'<strong>\1</strong>', content)

    # Convert unordered lists
    content = re.sub(r'(?m)^(\s*)?[-|*|+]\s*(.+?)\s*$', r'\1    <li>\2</li>', content)

    lines = content.splitlines()
    inside_ul = False

    for i, line in lines:
        if '<li>' in line:
            if not inside_ul:
                lines.insert(i, '<ul>')
                inside_ul = True
        else:
            if inside_ul:
                lines.insert(i, "</ul>")
                inside_list = False
        




    return content



content = '''
- test item one
- test item two
-test item three
    - indent one
    - indent two
- test item 4
'''