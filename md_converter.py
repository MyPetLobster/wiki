import re


def md_converter(markdown_content):
    # Check if the input is a non-empty string
    if not markdown_content or not isinstance(markdown_content, str):
        print('Invalid input to md_converter. Please provide a non-empty string.')
        return None
    
    # List of all conversion functions
    conversion_functions = [
        convert_headers,
        convert_bold_italic,
        convert_ul,
        convert_ol,
        convert_paragraphs,
        convert_links
    ]
    
    # Apply each conversion function
    html_content = markdown_content
    for func in conversion_functions:
        html_content = func(html_content)
    
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


def convert_bold_italic(content):
    content = re.sub(r'(?m)\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
    return re.sub(r'(?m)\*(.+?)\*', r'<em>\1</em>', content)


def convert_paragraphs(content):
    
    lines = content.splitlines()
    converted_lines = []
    inside_para = False

    for line in lines:
        # If the line is not empty and we're not inside a paragraph, start a new paragraph
        if line.strip() and not re.match(r'^(<.*?>)|(    <.*?>)', line) and not inside_para:
            converted_lines.append('<p>')
            inside_para = True

        # If the line is empty and we're inside paragraph, end the paragraph
        elif not line.strip() and inside_para:
            converted_lines.append('</p>')
            inside_para = False

        # If the line is not empty, add it to the current paragraph
        if line.strip():
            converted_lines.append(line)
    
    # If we're still inside a paragraph at the end, end the paragraph
    if inside_para:
        converted_lines.append('</p>')

    return '\n'.join(converted_lines)


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


def convert_ol(content):
    content = re.sub(r'(?m)^(\s*)?\d+\.\s*(.+?)\s*$', r'\1    <liOL>\2</liOL>', content)
    lines = content.splitlines()
    inside_ol = False

    for line in lines:
        # Check if the line contains an <li> tag
        if '<liOL>' in line:
            # If not already inside a list, insert <ol> tag before the first <li> tag
            if not inside_ol:
                lines.insert(lines.index(line), '<ol>')
                inside_ol = True
        else:
            # If inside a list, insert </ol> tag before this line
            if inside_ol:
                lines.insert(lines.index(line), '</ol>')
                inside_ol = False

    if inside_ol:
        lines.append('</ol>')
        
    content = '\n'.join(lines)

    return content.replace('<liOL>', '<li>').replace('</liOL>', '</li>')

def convert_links(content):
    return re.sub(r'\[(.+)\]\((.+)\)', r'<a href="\2">\1</a>', content)