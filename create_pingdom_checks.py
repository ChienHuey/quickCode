# Script to create pingdom alerts from entries in a file
#
# python create_pingdom_checks.py <csv with checks to be created> <username> <password> <api key>
#
# requires csv file to be formatted as follows: <name of check>,<URL to be checked>
#
# @param    path to csv file
# @param    Pingdom username
# @param    Pingdom password
# @param    Pingdom API key

import csv
import pingdomlib
import sys
import urlparse

__author__ = 'chhuey'

if len(sys.argv) < 4:
    print "Please specify the csv file containing the Pingdom checks you wish to create"
    sys.exit(0)
else:
    filename = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    apikey = sys.argv[4]

api = pingdomlib.Pingdom(username, password, apikey)

with open(filename,'r') as pingdomChecksFile:
    for check in pingdomChecksFile:
        url = urlparse.urlparse(check.rstrip())
        checkName = "{0}{1}".format(url[1], url[2])
        checkHost = "{0}".format(url[1])
        checkType = "checktype='{0}'".format(url[0])
        checkURL = "[url={0}]".format(url[2])

        api.newCheck(checkName, checkHost, checkType, checkURL)
        print "{0} check created successfully".format(checkName)