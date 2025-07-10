import os

def main():
    files = os.listdir("outputs")
    if files:
        for file in files:
            print(file)
    else:
        print("No files detected")