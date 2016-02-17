# Script that traverses a file tree and standardizes the .vcl files to common metrics values and
# identical share keys to the recommendations by Fastly
#
# @param    vcl_root_directory   directory where all the .vcl files are to traverse and update
# @param    directives_file      space-separated file that has the metric to be updated (e.g. .first_byte_timeout) and
#                                the new value for that metric (e.g. 3s)

import os
import sys
from update_vcl_backends import update_backends_metrics

__author__ = 'Chien Huey'

vcl_root_directory = sys.argv[1]
directives_file = sys.argv[2]


def process_vcl_folder_recursively(vcl_root_directory):
    for dirName, subdirlist, fileList in os.walk(vcl_root_directory):
        if subdirlist:
            for subfolder in subdirlist:
                process_vcl_folder_recursively(subfolder)
    for vcl_file in fileList:
        update_backends_metrics(vcl_file, directives_file)


