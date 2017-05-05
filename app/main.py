#!/usr/bin/env python

"""

Kepler WebView client CLI

"""

import argparse
from webview import WebView



if __name__ == '__main__':

    client = WebView()

    parser = argparse.ArgumentParser(description='Kepler WebView Client.')
    parser.add_argument('-url', dest='url', default=client.url(),
        help="Kepler WebView server hostname (default: {})".format(client.url()))
    parser.add_argument('-paramFile', dest='param_file',
        help='Parameter file')
    parser.add_argument('-run', dest='run', action='store_true',
        help='Start a workflow execution.')

    args = parser.parse_known_args()

    if args[0].url:
        client.set_url(args[0].url)

    if not args[0].run:
        raise Exception("Must specify at least one command: -run")

    if args[0].run:
        if args[0].param_file:
            client.load_parameter_file(args[0].param_file)
        
        if len(args[1]) % 2 != 1:
            raise Exception("Must specify name and value for each parameter and workflow name.")
       
        i = 0
        while i < len(args[1]):

            # last argument is workflow name
            if i == len(args[1]) - 1:
                client.set_workflow(args[1][i])
            else:
                # make sure name starts with '-' and is longer than 1 character
                if len(args[1][i]) < 2 or args[1][i][0] != '-':
                    raise Exception("Parameter name must be formatted like -name, not: {}".format(args[1][i]))

                client.set_parameter(args[1][i][1:], args[1][i+1])

                i += 1

            i += 1

        client.start_run()
