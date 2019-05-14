#!/usr/bin/env python3

import sys
import getopt

def usage():
    print("\nUsage: ", sys.argv[0], " \n")

class traindatagen:
    
    def main():
        options = {}        # Command line options dict
        
        # Read in the command-line arguments into the opts
        try:
            opts, args = getopt.getopt(sys.argv[1:], "i:")
        
        except getopt.GetoptError as err:
            sys.stdout = sys.stderr

            # Print help information
            print(str(err))

            usage()

            # Exit the program
            sys.exit(2)
            
        for (opt, arg) in opts:
            options[opt] = arg
            
        if "-i" in options.keys():
            in_fp = options["-i"]
        else:
            msg = sys.stdin.read()

    if __name__ == '__main__':
        main()