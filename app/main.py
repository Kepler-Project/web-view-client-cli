#!/usr/bin/env python

"""

Kepler WebView client CLI

"""

import argparse
from webview import WebView


if __name__ == '__main__':

    client = WebView()

    parser = argparse.ArgumentParser(description='Kepler WebView Client.')
    parser.add_argument('-url', dest='url', default=client.url,
        help="Kepler WebView server hostname")
    parser.add_argument('-paramFile', dest='param_file',
        help='Parameter file')
    parser.add_argument('-run', dest='run', action='store_true',
        help='Start a workflow execution.')
    parser.add_argument('-wfname', dest='workflow_name', help="Name of workflow (on server).")
    parser.add_argument('-wf', dest='workflow_file', help="Workflow file.")

    args = parser.parse_known_args()

    if not args[0].run:
        raise Exception("Must specify at least one command: -run")

    if args[0].run:

        if len(args[1]) % 2 != 0:
            raise Exception("Must specify name and value for each parameter.")
      
        params = {}

        i = 0
        while i < len(args[1]):

            # make sure name starts with '-' and is longer than 1 character
            if len(args[1][i]) < 2 or args[1][i][0] != '-':
                 raise Exception("Parameter name must be formatted like -name, not: {}".format(args[1][i]))

            params[args[1][i][1:]] = args[1][i+1]

            i += 2

        run = client.start_run(url=args[0].url, workflow_name=args[0].workflow_name, 
            workflow_file=args[0].workflow_file, parameters=params, 
            parameter_file=args[0].param_file)

        print(run.error())
        print(run.outputs())

