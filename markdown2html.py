#!/usr/bin/env python3

import sys
import os
import re
import hashlib


def convert_markdown_to_html(markdown_text):
    html_lines = []
    lines = markdown_text.split('\n')
    in_unordered_list = False
    in_ordered_list = False
    in_paragraph = False
    paragraph_lines = []

    for line in lines:
        # Convert **text** to <b>text</b>
        line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
        # Convert __text__ to <em>text</em>
        line = re.sub(r'__(.*?)__', r'<em>\1</em>', line)
        # Convert [[text]] to MD5 hash
        line = re.sub(
            r'\[\[(.*?)\]\]',
            lambda m: hashlib.md5(m.group(1).encode()).hexdigest(),
            line
        )
        # Convert ((text)) by removing all 'c' and 'C'
        line = re.sub(
            r'\(\((.*?)\)\)',
            lambda m: m.group(1).replace('c', '').replace('C', ''),
            line
        )

        if line.startswith('#'):
            if in_unordered_list:
                html_lines.append('</ul>')
                in_unordered_list = False
            if in_ordered_list:
                html_lines.append('</ol>')
                in_ordered_list = False
            if in_paragraph:
                html_lines.append(
                    '<br />\n    '.join(paragraph_lines) + '\n</p>'
                )
                in_paragraph = False
                paragraph_lines = []
            heading_level = len(line.split(' ')[0])
            heading_text = line[heading_level:].strip()
            if 1 <= heading_level <= 6:
                html_lines.append(
                    f'<h{heading_level}>{heading_text}</h{heading_level}>'
                )
            else:
                html_lines.append(line)
        elif line.startswith('- '):
            if in_ordered_list:
                html_lines.append('</ol>')
                in_ordered_list = False
            if in_paragraph:
                html_lines.append(
                    '<br />\n    '.join(paragraph_lines) + '\n</p>'
                )
                in_paragraph = False
                paragraph_lines = []
            if not in_unordered_list:
                html_lines.append('<ul>')
                in_unordered_list = True
            list_item = line[2:].strip()
            html_lines.append(f'    <li>{list_item}</li>')
        elif line.startswith('* '):
            if in_unordered_list:
                html_lines.append('</ul>')
                in_unordered_list = False
            if in_paragraph:
                html_lines.append(
                    '<br />\n    '.join(paragraph_lines) + '\n</p>'
                )
                in_paragraph = False
                paragraph_lines = []
            if not in_ordered_list:
                html_lines.append('<ol>')
                in_ordered_list = True
            list_item = line[2:].strip()
            html_lines.append(f'    <li>{list_item}</li>')
        elif line.strip() == '':
            if in_paragraph:
                html_lines.append(
                    '<br />\n    '.join(paragraph_lines) + '\n</p>'
                )
                in_paragraph = False
                paragraph_lines = []
            if in_unordered_list:
                html_lines.append('</ul>')
                in_unordered_list = False
            if in_ordered_list:
                html_lines.append('</ol>')
                in_ordered_list = False
        else:
            if in_unordered_list:
                html_lines.append('</ul>')
                in_unordered_list = False
            if in_ordered_list:
                html_lines.append('</ol>')
                in_ordered_list = False
            if not in_paragraph:
                paragraph_lines.append('<p>')
                paragraph_lines.append('    ' + line.strip())
                in_paragraph = True
            else:
                paragraph_lines.append('    ' + line.strip())

    if in_paragraph:
        html_lines.append('<br />\n    '.join(paragraph_lines) + '\n</p>')
    if in_unordered_list:
        html_lines.append('</ul>')
    if in_ordered_list:
        html_lines.append('</ol>')

    return '\n'.join(html_lines)


def main():
    if len(sys.argv) < 3:
        print(
            "Usage: ./markdown2html.py README.md README.html",
            file=sys.stderr
        )
        sys.exit(1)

    markdown_file = sys.argv[1]
    html_file = sys.argv[2]

    if not os.path.exists(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
    except IOError as e:
        print(f"Error reading {markdown_file}: {e}", file=sys.stderr)
        sys.exit(1)

    html_content = convert_markdown_to_html(md_content)

    try:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
    except IOError as e:
        print(f"Error writing {html_file}: {e}", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
