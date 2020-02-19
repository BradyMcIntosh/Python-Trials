import os


while True:
    value = input("Enter a directory path (q to quit):\n")
    if value == "q":
        break
    try:
        ldir = os.listdir(value)
        print("Printing contents:")
        for item in ldir:
            print(item)
    except FileNotFoundError:
        print("Invalid directory!")
    print()
