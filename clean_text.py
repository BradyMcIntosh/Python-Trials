# This program is intended to clean html files extracted from the Gutenberg online library.
# Some manual processing, particularly at the beginning and end of the file, will be necessary.
# Otherwise, this program will remove page numbers, images, and other markup elements.

import csv, re
import string
from pathlib import Path

html_list_csv = open('data/html symbol list short.csv', mode='r')
csv_reader = csv.DictReader(html_list_csv)


# replace html codes with respective ascii symbols
def csv_edit(line):
    row_count = 0;
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
    return line


# Open a user-specified file
while True:
    usr = input("Enter a file name (q to quit):\n")
    if usr == "q":
        break
    try:
        text_read = open(usr, 'r')
        text = text_read.readlines()
        text_read.close()

        p = Path(usr)
        print(f"path = \"{p.parent}\", filename = \"{p.stem}\"")

        text_write = open(f"{p.parent}/{p.stem}.txt", "w+")

        line_count = 0
        for line in text:
            line_count += 1

            line = regex_edit(csv_edit(line))
            text_write.write(line)
        text_write.close()
        print(f"Processed {line_count} lines.")
        print(f"created file: {p.parent}/{p.stem}.txt")

    except FileNotFoundError:
        print("Invalid file")
    print()

html_list_csv.close()
