#!/usr/bin/python

#######################################################
#                                                     #
#  Copyright Masterchain Grazcoin Grimentz 2013-2014  #
#  https://github.com/grazcoin/mastercoin-tools       #
#  https://masterchain.info                           #
#  masterchain@@bitmessage.ch                         #
#  License AGPLv3                                     #
#                                                     #
#######################################################

import git
from optparse import OptionParser
from msc_utils_general import *

d=False # debug_mode

def main():
    parser = OptionParser("usage: %prog [options]")
    parser.add_option("-d", "--debug", action="store_true",dest='debug_mode', default=False,
                        help="turn debug mode on")
    parser.add_option( "-r", "--repository-path", dest='repository_path', default="~/mastercoin-tools", 
    	help="Specify the location of the mastercoin-tools repository (defaults to ~/mastercoin-tools" )

    (options, args) = parser.parse_args()
    d=options.debug_mode

    # zip all parsed data and put in downloads
    archive_parsed_data( options.repository_path )

if __name__ == "__main__":
    main()
