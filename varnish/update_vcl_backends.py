# Module with functions to update backend .vcl files

import fileinput
import re

__author__ = 'Chien Huey'


# function that updates the specified backends based on the directives file provided
def update_backends(backends_file, directives_file):
    # load directives_file into dictionary
    directives = {}
    with open(directives_file, "r") as text:
        for line in text:
            metric, value = line.split()
            directives[metric] = str(value)

    # loop through the backends_file and
    for vcl_line in fileinput.input(backends_file):
        # loop through the directives dictionary
        for metric in directives:
            re_pattern = "(\." + metric + ")\s*=\s*(\d+)s"
            match = re.match(re_pattern, vcl_line)
            #re.sub()


update_backends("./sample_backend.vcl", "directives.txt")

regex = "(\t*|\s*)(\.first_byte_timeout)(\t*|\s*)=\s*\w+;"