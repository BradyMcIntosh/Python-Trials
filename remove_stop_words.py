import re

file = open('data/stop_words.txt', 'r')
stop_words = file.readlines()
file.close()

# Open a user-specified file
while True:
    value = input("Enter a file name (q to quit):\n")
    if value == "q":
        break
    try:
        file = open(value, 'r')

        print("Original text: ")
        print(file.read())
        file.seek(0)

        print("\nRemoving stop-words... ")
        for line in file:
            count = 0
            for entry in line.split():
                w_print = True
                for stop_word in stop_words:
                    # Strip non-alphanumeric characters and convert to lower-case
                    # ... before comparing to stop-word list
                    # print("\"%s\" == \"%s\" ?" % (entry.lower(), stop_word.strip()))
                    if entry.lower() == stop_word.strip():
                        w_print = False
                        break
                if w_print:
                    print("%s " % entry, end='')
                    count += 1
            if count > 0:
                print()
        file.close()
    except FileNotFoundError:
        print("Invalid directory!")
    print()

