#!/usr/bin/env python3

import subprocess, sys
import argparse

'''
OPS445 Assignment 2
Program: duim.py 
Author: "Alex Theaker"
The python code in this file (duim.py) is original work written by
"Student Name". No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or on-line resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: This program runs the du command, which is used to inspect directories.
What this program does is it improves the output by including a graphical
representation of the output, as well as it can format the output to be human
readable.

Date: December 8, 2024
'''

def parse_command_args():
    "Set up argparse here. Call this function inside main."
    parser = argparse.ArgumentParser(description="DU Improved -- See Disk Usage Report with bar charts",epilog="Copyright 2024")
    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    # add argument for "human-readable". USE -H, don't use -h! -h is reserved for --help which is created automatically.
    parser.add_argument("-H", "--human-readable", action="store_true", help="Makes the output size in human readable format")
    # check the docs for an argparse option to store this as a boolean.
    # add argument for "target". set number of args to 1.
    parser.add_argument("target",nargs="?",default=".")
    args = parser.parse_args()
    return args


def percent_to_graph(percent: int, total_chars: int) -> str:
    "returns a string: eg. '##  ' for 50 if total_chars == 4"

    equals = int(round((percent / 100) * total_chars))
    spaces = total_chars - equals
    return '=' * equals + ' ' * spaces

def call_du_sub(location: str) -> list:
    "use subprocess to call `du -d 1 + location`, rtrn raw list"

    command = ["du", "-d", "1", location]

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        return stdout.strip().split('\n')

    except:
        print("Error running du command")
        return []


    pass

def create_dir_dict(raw_dat: list) -> dict:
    "get list from du_sub, return dict {'directory': 0} where 0 is size"
    dictionary = {}

    for item in raw_dat:
        size, path = item.split('\t',1)
        dictionary[path] = int(size)

    return dictionary

def bytes_to_human_r(kibibytes: int, decimal_places: int=2) -> str:
    "turn 1,024 into 1 MiB, for example"
    suffixes = ['KiB', 'MiB', 'GiB', 'TiB', 'PiB']  # iB indicates 1024
    suf_count = 0
    result = kibibytes 
    while result > 1024 and suf_count < len(suffixes):
        result /= 1024
        suf_count += 1
    str_result = f'{result:.{decimal_places}f} '
    str_result += suffixes[suf_count]
    return str_result

if __name__ == "__main__":
    args = parse_command_args()

    # will need to error check in future
    target_dir = args.target

    raw_data = call_du_sub(target_dir)

    data = create_dir_dict(raw_data)
   
    total_filesize = sum(data.values())

    for filepath, filesize in data.items():
        percentage = (filesize / total_filesize) * 100 if total_filesize > 0 else 0
        graph_bar = percent_to_graph(percentage, args.length)

        if args.human_readable:
            filesize_str = bytes_to_human_r(filesize)
            total_filesize_str = bytes_to_human_r(total_filesize)
        else:
            filesize_str = f"{filesize} B"
            total_filesize_str = f"{total_filesize} B"

        print(f"{percentage:>3.0f}% [{graph_bar}] {filesize_str}\t{filepath}")

    print(f"Total: {total_filesize_str}   {args.target}")
