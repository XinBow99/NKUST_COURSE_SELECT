import SelectInfo
import os


def main():
    path = "課程"
    full_path = []
    for d in os.listdir(path):
        for f in os.listdir(path + '/' + d):
            print(f)

if __name__ == "__main__":
    main()
