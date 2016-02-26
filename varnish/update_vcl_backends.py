# Module with functions to update backend .vcl files

import fileinput
import re

__author__ = 'Chien Huey'


# function that updates the specified backend metrics based on the directives file provided
#
# @param    backends_file       .vcl file with backend definitions
# @param    directives_file     space-separated file that has the metric to be updated (e.g. .first_byte_timeout) and
#                                the new value for that metric (e.g. 3s)
#
def update_backend_metrics(backends_file, directives_file):
    # load directives_file into dictionary
    directives = {}
    # empty array with the new file lines
    new_backends_file = []

    with open(directives_file, "r") as text:
        for line in text:
            metric, value = line.split()
            directives[metric] = str(value)

    # loop through the backends_file and
    for vcl_line in fileinput.input(backends_file):
        # loop through the directives dictionary
        for metric in directives:
            re_pattern = "(\\t*|\\s*)(" + metric + ")(\\t*|\\s*)=\\s*(\\w+);"
            match = re.match(re_pattern, vcl_line)
            if match:
                old_value = match.group(match.lastindex)
                new_value = directives[metric]
                vcl_line = vcl_line.replace(old_value, new_value)
                match = None
        # write line to new backends file array
        new_backends_file.append(vcl_line)

    # after all lines processed, close input file
    fileinput.close()

    # overwrite the file with the updated lines from the array buffer
    with open(backends_file, "w") as text:
        for line in new_backends_file:
            text.write(line)

# function that updates the specified backend shareids based on the directives file provided
#
# @param    backends_file       .vcl file with backend definitions
#
def  update_backend_shareids(backends_file):
    # empty array with the new file lines
    new_backends_file = []
    # last backend name - this variable needs to survive each iteration
    last_backend_name = ""
    # loop through the backends_file and
    for vcl_line in fileinput.input(backends_file):
        # check for a match for the backend
        re_pattern_backend = "(backend)\\s*([\\w_]*)"
        match_backend = re.match(re_pattern_backend, vcl_line)
        if match_backend:
            last_backend_name = match_backend.group(match_backend.lastindex)
            last_backend_name = last_backend_name.replace('_','')
            match_backend = None

        # check for a match for the shareid
        re_pattern_shareid = "(\\t*|\\s*)(.share_key)(\\t*|\\s*)=(\\t*|\\s*)\"([\\w\\d]*)\";"
        match_shareid = re.match(re_pattern_shareid, vcl_line)
        if match_shareid:
            old_value = match_shareid.group(match_shareid.lastindex)
            new_value = last_backend_name
            vcl_line = vcl_line.replace(old_value, new_value)
            match_shareid = None
        # write line to new backends file array
        new_backends_file.append(vcl_line)

    # after all lines processed, close input file
    fileinput.close()

    # overwrite the file with the updated lines from the array buffer
    with open(backends_file, "w") as text:
        for line in new_backends_file:
            text.write(line)