#! /usr/bin/python

__author__ = 'MQ'

import sys
import copy
import subprocess
import re
import os

ERROR_ARGS_MESSAGE = '\nERROR: Please provide "class path" as first argument and "path\jar name" as second argument\n'
STEP_1_MESSAGE = '\n*** STEP 1 - ANALYZING CLASS PATH: '
STEP_2_MESSAGE = '\n*** STEP 2 - ANALYZING JARS INSIDE JAR: '
STEP_3_MESSAGE = '\n*** STEP 3 - ANALYZING CLASSES INSIDE JAR: '


def analyze(files):
    duplicates = []
    files.sort()
    for to_find_file in files:
        search_list = copy.deepcopy(files)
        search_list.remove(to_find_file)
        for file_name in search_list:
            original_file = to_find_file
            if to_find_file.find('/') > 0:
                original_file = to_find_file[to_find_file.rindex('/') + 1:]

            if original_file.find('-') > 0:
                original_file = original_file[:original_file.rindex('-')]

            compare_with_file = file_name
            if file_name.find('/') > 0:
                compare_with_file = file_name[file_name.rindex('/') + 1:]

            if compare_with_file.find('-') > 0:
                compare_with_file = compare_with_file[:compare_with_file.rindex('-')]

            if original_file == compare_with_file:
                duplicates.append(to_find_file)
                break

    print 'Found: ' + str(len(files))
    print 'Duplicated: ' + str(len(duplicates))
    duplicates.sort()
    print duplicates


def find_duplicates(class_path, jar_name):
    print STEP_1_MESSAGE + class_path + '\n'
    files = []
    path = class_path
    for (directory, dir_names, file_names) in os.walk(path):
        files.extend(file_names)
        break

    analyze(files)

    print STEP_2_MESSAGE + jar_name + '\n'

    jars = subprocess.check_output(['jar', 'tf', jar_name])
    jar_jars = re.findall(r'.*?\.jar', jars)
    jar_classes = re.findall(r'.*?\.class', jars)

    analyze(jar_jars)

    print STEP_3_MESSAGE + jar_name + '\n'

    analyze(jar_classes)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(ERROR_ARGS_MESSAGE)
        exit(1)

    find_duplicates(sys.argv[1], sys.argv[2])
