# This program is intended to clean html files extracted from the Gutenberg online library.
# Some manual processing, particularly at the beginning and end of the file, will be necessary.
# Otherwise, this program will remove page numbers, images, redundant line breaks, and other markup elements.

# TODO: Read all files in a "text-source" folder, clean and add to a "text-clean" folder
# TODO: (in a new file) Combine various clean texts into larger files organized by author, genre, etc.

import re, html, unidecode
import string, time
from pathlib import Path
from cchardet import UniversalDetector

__time__ = True
__count__ = True

time_html = 0
time_regex = 0
count_html = 0
count_regex = 0


# Replace html codes and unicode symbols with respective ascii symbols
def html_edit(line):
    global count_html

    # To match letter codes:
    r"&[a-zA-Z0-9]+;"

    # To match number codes:
    r"&#[0-9]+;"

    # To match all codes:
    r"&#?[a-zA-Z0-9]+?;"

    # To match non-ascii characters
    r"[^\x00-\x7F]"

    # Remove leading spaces
    line = line.lstrip(' \t')

    # Replace html escape codes with respective symbols
    if __count__:
        count_html += len(re.findall(r"&#?[a-zA-Z0-9]+?;", line))
    line = html.unescape(line)

    # Replace non-ascii characters with ascii equivalent strings
    if __count__:
        count_html += len(re.findall(r"[^\x00-\x7F]", line))
    line = unidecode.unidecode(line)

    return line


# delete/replace markup syntax using regex
def regex_edit(line):
    global count_regex

    # List of complex expressions to delete matches for - in order of precedence
    list_delete_content = [r"<p><span class=(\"|\')pagenum\1>.*?</span></p>",
                           r"<span class=(\"|\')pagenum\1>.*?</span>",
                           r"<p class=(\"|\')(ph2|center pfirst)\1.*?>.*?</p>",
                           r"<(h[0-9]+?).*?>.*?</\1>",
                           r"<ins class=(\"|\')(mycorr|authcorr)\1.*?>.*?</ins>",
                           r"<p class=(\"|\')illustration( chapter)?\1>.*?</p>",
                           r"<p class=(\"|\')(ph3|center pfirst)\1>.*?</p>",
                           r"(?<=>)CHAPTER.*?(?=<)",
                           r"<p class=\"title\">.*?\."
                           ]

    # List of complex expressions to delete surroundings for - in order of precedence
    # list_delete_surround = [r"<span class=\"smcap\">(.*?)</span>"
    #                        ]

    # List of tag expressions to delete matches for - in order of precedence
    list_delete_tags = [r"</?[ahpibu].*?>",
                        r"</?(small|strong|span|div|br|em|ins|cite|blockquote).*?>"
                        ]

    # (?<=x) lookbehind for x
    # (?<!x) negative lookbehind for x
    # Replace mid-sentence line breaks with spaces
    if __count__:
        count_regex += len(re.findall(r"(?<=.)(?<!>)[\r\n]", line))
    line = re.sub(r"(?<=.)(?<!>)[\r\n]", " ", line)

    # Remove all other line breaks
    if __count__:
        count_regex += len(re.findall(r"[\r\n]", line))
    line = re.sub(r"[\r\n]", "", line)

    # Remove complex tags with inner content
    for exp in list_delete_content:
        if __count__:
            count_regex += len(re.findall(exp, line))
        line = re.sub(exp, "", line)

    # Remove complex surrounding tags
    # for exp in list_delete_surround:
    #     if __count__:
    #         count_regex += len(re.findall(exp, line))
    #     line = re.sub(exp, r"\1", line)

    # Class for alphanumeric or punctuation symbol
    c1 = "[A-Za-z0-9_.,:;!? \"\'$]"
    c2 = "[A-Za-z0-9_.,:;!?\"\'$]"

    # Add line breaks between content blocks
    if __count__:
        count_regex += len(re.findall(rf"(?<={c2})</(p|u|h.|div|span)>(?!{c1}{c2})", line))
    line = re.sub(rf"(?<={c2})</(p|u|h.|div|span)>(?!{c1}{c2})", r"</\1>\r\n", line)
    # Explanation for this pattern:
    # This pattern matches terminating tags surrounded by alphanumeric/punctual characters.
    # Matches must be preceded by at least one character, and NOT followed by two.
    # The first character after the match must, also, not be a space.

    # Remove all remaining tags
    for exp in list_delete_tags:
        if __count__:
            count_regex += len(re.findall(exp, line))
        line = re.sub(exp, "", line)

    return line


# Open a user-specified file
while True:
    usr = input("Enter a file name (q to quit):\n")
    if usr == "q":
        break
    try:
        # Detect file encoding
        file = open(usr, 'rb')
        det = UniversalDetector()
        for line in file.readlines():
            det.feed(line)
            if det.done:
                break
        det.close()
        usr_enc = det.result.get("encoding")

        print(f"File encoding: {usr_enc}")

        text_read = open(usr, 'r', encoding=usr_enc, errors='ignore')
        text = text_read.readlines()
        text_read.close()

        p = Path(usr)
        # print(f"path = \"{p.parent}\", filename = \"{p.stem}\"")

        text_write = open(f"{p.parent}/{p.stem}.txt", "w+", encoding='utf-8', errors='replace')

        time_html = 0
        count_html = 0
        time_regex = 0
        count_regex = 0
        time_init = 0

        line_count = 0
        for line in text:
            line_count += 1

            # HTML edit section
            if __time__:
                time_init = time.perf_counter()
            line = html_edit(line)
            if __time__:
                time_regex += time.perf_counter() - time_init

            # Regex edit section
            if __time__:
                time_init = time.perf_counter()
            line = regex_edit(line)
            if __time__:
                time_regex += time.perf_counter() - time_init

            text_write.write(line)
        text_write.close()
        print(f"Processed {line_count} lines.")
        # Debug printout section
        if __time__ or __count__:

            # HTML info section
            print("HTML:  ", end="")
            if __count__:
                print(f"{count_html:-8d} codes   ", end="")
            if __count__ and __time__:
                print("--", end="")
            if __time__:
                print(f"{time_html:-6.2f} seconds ", end="")
            print()

            # Regex info section
            print("Regex: ", end="")
            if __count__:
                print(f"{count_regex:-8d} matches ", end="")
            if __count__ and __time__:
                print("--", end="")
            if __time__:
                print(f"{time_regex:-6.2f} seconds ", end="")
            print()

        print(f"Created file: {p.parent}/{p.stem}.txt")

    except FileNotFoundError:
        print("Invalid file")
    print()

# ...
