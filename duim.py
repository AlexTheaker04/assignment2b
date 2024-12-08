#!/usr/bin/env python3

import subprocess
import sys
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
    """
    
    Used to parse command line arguments
    
    """

    # add 3 command line args
    parser = argparse.ArgumentParser(description="DU Improved -- See Disk Usage Report with bar charts",epilog="Copyright 2024")
    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    parser.add_argument("-H", "--human-readable", action="store_true", help="Makes the output size in human readable format")

    # add argument for "target". set number of args to 1.
    parser.add_argument("target",nargs="?",default=".", help="The directory to scan.")
    arguments = parser.parse_args()
    return arguments


def percent_to_graph(percent: int, total_chars: int) -> str:
    """
    
    returns a string representation of a % based on total chars..

    returns a string: eg. '##  ' for 50 if total_chars == 4
       
    """

    equals = int(round((percent / 100) * total_chars)) # find the number of equal signs
    spaces = total_chars - equals # and then find the empty space needed
    return '=' * equals + ' ' * spaces

def call_du_sub(location: str) -> list:
    """
    
    uses subprocess to call the du command, and will return a list of the output.   
    
    
    """

    command = ["du", "-d", "1", location]

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        return stdout.strip().split('\n')

    except:
        print("Error running du command")
        return []

def create_dir_dict(raw_dat: list) -> dict:
    """
    
    takes raw list from du command and will return a dictionary with the
    directories and the size associated
       
    
    """
    dictionary = {}

    for item in raw_dat: # iterate through the items, splits based on tab char and add them to a dictionary
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

        # add code for coloured output
        green_start = "\033[92m"
        light_blue_start = "\033[94m"
        color_end = "\033[0m"
        colored_graph_bar = f"{green_start}{graph_bar}{color_end}"
        colored_filepath = f"{light_blue_start}{filepath}{color_end}"

        if args.human_readable:
            filesize_str = bytes_to_human_r(filesize)
            total_filesize_str = bytes_to_human_r(total_filesize)
        else:
            filesize_str = f"{filesize} B"
            total_filesize_str = f"{total_filesize} B"
        print(f"{percentage:>3.0f}% [{colored_graph_bar}] {filesize_str}\t{colored_filepath}")

    print(f"Total: {total_filesize_str}   {args.target}")
