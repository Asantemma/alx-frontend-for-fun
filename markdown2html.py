#!/usr/bin/python3

"""
Converts markdown text to html.
"""
import sys
import os.path
import re
import hashlib

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: ./markdown2html.py README.md README.html',
              file=sys.stderr)
        exit(1)

    if not os.path.isfile(sys.argv[1]):
        print('Missing {}'.format(sys.argv[1]), file=sys.stderr)
        exit(1)

    with open(sys.argv[1]) as input_file:
        with open(sys.argv[2], 'w') as output_file:
            ul_open, ol_open, in_paragraph = False, False, False
            # bold syntax
            for current_line in input_file:
                current_line = current_line.replace('**', '<b>', 1)
                current_line = current_line.replace('**', '</b>', 1)
                current_line = current_line.replace('__', '<em>', 1)
                current_line = current_line.replace('__', '</em>', 1)

                # md5
                md5_matches = re.findall(r'\[\[.+?\]\]', current_line)
                md5_content = re.findall(r'\[\[(.+?)\]\]', current_line)
                if md5_matches:
                    current_line = current_line.replace(
                        md5_matches[0], hashlib.md5(md5_content[0].encode()).hexdigest())

                # remove the letter C
                c_matches = re.findall(r'\(\(.+?\)\)', current_line)
                c_content = re.findall(r'\(\((.+?)\)\)', current_line)
                if c_matches:
                    no_c_content = ''.join(ch for ch in c_content[0]
                                           if ch not in 'Cc')
                    current_line = current_line.replace(c_matches[0],
                                                        no_c_content)

                line_length = len(current_line)
                heading_content = current_line.lstrip('#')
                heading_level = line_length - len(heading_content)
                ul_content = current_line.lstrip('-')
                ul_level = line_length - len(ul_content)
                ol_content = current_line.lstrip('*')
                ol_level = line_length - len(ol_content)
                # headings, lists
                if 1 <= heading_level <= 6:
                    current_line = '<h{}>'.format(
                        heading_level) + heading_content.strip()
                    + '</h{}>\n'.format(
                        heading_level)

                if ul_level:
                    if not ul_open:
                        output_file.write('<ul>\n')
                        ul_open = True
                    current_line = '<li>' + ul_content.strip() + '</li>\n'
                if ul_open and not ul_level:
                    output_file.write('</ul>\n')
                    ul_open = False

                if ol_level:
                    if not ol_open:
                        output_file.write('<ol>\n')
                        ol_open = True
                    current_line = '<li>' + ol_content.strip() + '</li>\n'
                if ol_open and not ol_level:
                    output_file.write('</ol>\n')
                    ol_open = False

                if not (heading_level or ul_open or ol_open):
                    if not in_paragraph and line_length > 1:
                        output_file.write('<p>\n')
                        in_paragraph = True
                    elif line_length > 1:
                        output_file.write('<br/>\n')
                    elif in_paragraph:
                        output_file.write('</p>\n')
                        in_paragraph = False

                if line_length > 1:
                    output_file.write(current_line)

            if ul_open:
                output_file.write('</ul>\n')
            if ol_open:
                output_file.write('</ol>\n')
            if in_paragraph:
                output_file.write('</p>\n')
    exit(0)
