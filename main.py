import os
import sys
import requests
from collections import deque
from bs4 import BeautifulSoup
from colorama import Fore


class Browser:
    def __init__(self):
        self.dir = None
        self.url = None
        self.file_name = ""
        self.saved_files = set()
        self.stack = deque()
        self.text = ""
        self.write_file_bool = False
        self.back = False
        self.tags = ["p", "a", "ul", "ol", "li", "h1", "h2", "h3", "h4", "h5", "h6"]

    def make_dir(self):
        current_dir = os.getcwd()
        dir_name = sys.argv[1]
        dir_path = os.path.join(current_dir, dir_name)
        self.dir = dir_path
        try:
            os.mkdir(dir_path)
        except FileExistsError:
            pass

    def get_url(self):
        while True:
            user_input = input()
            if user_input == "exit":
                exit()
            elif user_input == "back":
                if len(self.stack) <= 1:
                    continue
                try:
                    self.stack.pop()
                    self.file_name = self.stack[-1] + "_com"
                    self.back = True
                except IndexError:
                    pass
                break
            else:
                if user_input[:8] != "https://":
                    user_input = "https://" + user_input
                self.url = user_input
                for char in self.url.replace("https://", ''):
                    if char != ".":
                        self.file_name += char
                    else:
                        break
                break

    def print_content(self):
        # add so that it knows to print from dir (if user input is back)
        if not self.back:
            try:
                r = requests.get(self.url)
            except:
                try:
                    with open(os.path.join(self.dir, self.file_name), "r") as f:
                        print(f.read())
                        return
                except:
                    print("Invalid URL")
                    return
            soup = BeautifulSoup(r.content, "html.parser")
            self.text = ""
            for tag in self.tags:
                s = soup.find_all(tag)
                for i in s:
                    if tag == "a":
                        self.text += Fore.BLUE + i.text + Fore.RESET + "\n"
                    else:
                        self.text += i.text
            self.write_file_bool = True
            print(self.text)
        else:
            with open(os.path.join(self.dir, self.file_name), "r") as f:
                print(f.read())
            self.back = False

    def write_file(self):
        if self.write_file_bool:
            if self.file_name not in self.saved_files:
                self.saved_files.add(self.file_name)
                with open(os.path.join(self.dir, self.file_name), "w") as f:
                    f.write(self.text)
                self.write_file_bool = False


def main():
    program = Browser()
    program.make_dir()
    while True:
        program.get_url()
        program.print_content()
        program.write_file()
        program.file_name = ""


if __name__ == "__main__":
    main()
