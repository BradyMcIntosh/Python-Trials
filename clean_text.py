# This program is intended to clean html files extracted from the Gutenberg online library.
# Some manual processing, particularly at the beginning and end of the file, will be necessary.
# Otherwise, this program will remove page numbers, images, redundant line breaks, and other markup elements.

# TODO: Read all files in a "text-source" folder, clean and add to a "text-clean" folder
# TODO: Remove chapter headers.
# TODO: (in a new file) Combine various clean texts into larger files organized by author, genre, etc.

import csv, re
import string, time
from pathlib import Path

html_list_csv = open('data/html symbol list short.csv', mode='r')
csv_reader = csv.DictReader(html_list_csv)

time_html = 0
time_regex = 0

print_count = 0

# replace html codes with respective ascii symbols
def csv_edit(line):
    global csv_reader
    # TODO: find a more efficient method that recognizes patterns and records how many escape codes were replaced

    # To match letter codes:
    r"&[a-zA-Z0-9]+;"

    # To match number codes:
    r"&#[0-9]+;"

    # To match all codes:
    r"&#?[a-zA-Z0-9]+;"

    row_count = 0;
    char_i = 0;

    # print("Line: ", line)
    for row in csv_reader:
        if row_count != 0:
            line = line.replace(row["Name Code"], row["Character"])
            line = line.replace(row["Number Code"], row["Character"])
            # if line.find(row["Name Code"]) > -1:
            #     new_line = line.replace(row["Name Code"], row["Character"])
            #     print(f"Replaced {row['Description']}")
            #     line = new_line
            # if line.find(row["Number Code"]) > -1:
            #     new_line = line.replace(row["Number Code"], row["Character"])
            #     print(f"Replaced {row['Description']}")
            #     line = new_line
        row_count += 1
    html_list_csv.seek(0)

    return line


# delete/replace markup syntax using regex
def regex_edit(line):
    global print_count

    if print_count < 10:
        print(repr(line))
        print_count += 1

    # List of content expressions to delete matches for - in order of precedence
    list_delete_content = [r"<p><span class=\"pagenum\">.*?</span></p>",
                           r"<ins class=\"(mycorr|authcorr)\".*?>.*?</ins>",
                           r"<p class=\"illustration( chapter)?\">.*?</p>",
                           r"<p class=\"ph3\">.*?</p>"
                           ]

    # List of tag expressions to delete matches for - in order of precedence
    list_delete_tags = [r"</?[ahpib].*?>",
                        r"</?(small|strong|span|div|br|em|blockquote).*?>"
                        ]

    # Remove complex tags with inner content
    for exp in list_delete_content:
        line = re.sub(exp, "", line)

    # (?<=x) lookbehind for x
    # (?<!x) negative lookbehind for x
    # Replace mid-sentence line breaks with spaces
    line = re.sub(r"(?<=.)(?<!>)[\r\n]", " ", line)

    # Remove all other line breaks
    line = re.sub(r"[\r\n]", "", line)

    # Add line breaks between paragraph/header blocks
    line = re.sub(r"</(p|h.)>", r"</\1>\r\n", line)

    # Remove all remaining tags
    for exp in list_delete_tags:
        line = re.sub(exp, "", line)

    #
    line = re.sub("æ", "ae", line)

    return line

# Open a user-specified file
while True:
    usr = input("Enter a file name (q to quit):\n")
    if usr == "q":
        break
    try:
        text_read = open(usr, 'r', encoding='utf-8', errors='replace')
        text = text_read.readlines()
        text_read.close()

        p = Path(usr)
        print(f"path = \"{p.parent}\", filename = \"{p.stem}\"")

        text_write = open(f"{p.parent}/{p.stem}.txt", "w+", encoding='utf-8', errors='replace')

        line_count = 0
        for line in text:
            line_count += 1

            # time_init = time.perf_counter()
            # line = csv_edit(line)
            # time_html += time.perf_counter()-time_init

            time_init = time.perf_counter()
            line = regex_edit(line)
            time_regex += time.perf_counter() - time_init

            text_write.write(line)
        text_write.close()
        print(f"Processed {line_count} lines.")
        print(f"Replacing html escape codes took {time_html:.2f} seconds.")
        print(f"Regex editing took {time_regex:.2f} seconds.")
        print(f"Created file: {p.parent}/{p.stem}.txt")

    except FileNotFoundError:
        print("Invalid file")
    print()

html_list_csv.close()
