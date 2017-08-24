
"""
Kepler WebView client.

"""

import json
import os
import requests
from requests.auth import HTTPBasicAuth
from webview.run import Run
from webview.runs import Runs

class WebView:
    url = "https://localhost:9443/kepler"

    def _load_parameter_file(self, name):
        params = {}
        with open(name) as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                # skip empties and comments
                if len(line) > 0 and line[0] != '#':
                    try:
                        (name, value) = line.split('=', 1)
                    except(Exception):
                        raise Exception("Parameter file lines must be name = value, not: {}".format(line))
                        
                    params[name.strip()] = value.strip()
        return params

    # get the runs. returns a list of Run objects.
    def runs(self, url=url, username=None, password=None):
        if url == None:
            raise Exception("Must specify url to Kepler WebView.")

        runs_url = "{}/runs".format(url)
        
        response = requests.get(runs_url, auth=HTTPBasicAuth(username, password),
            #FIXME verify
            verify=False)

        if response.text == 'Unauthorized':
            raise Exception("Wrong username or password.")
        else:
            response_json = response.json()
    
            if 'error' in response_json:
                raise Exception(response_json['error'])

            if 'runs' not in response_json:
                raise Exception("Unexpeted response: {}".format(json.dumps(response_json)))

            runs = []
            for fields in response_json['runs']:
                runs.append(Run(url=url,username=username,password=password,fields=fields))

        return Runs(runs)

        #return Run(url=url, username=username, password=password, response=response)

    # start a workflow execution run.
    def start_run(self, url=url, workflow_name=None, workflow_file=None,
        username=None, password=None, parameters=None, parameter_file=None,
        provenance=True, synchronous=False):

        if url == None:
            raise Exception("Must specify url to Kepler WebView.")

        run_url = "{}/runwf".format(url)
        
        if workflow_name == None and workflow_file == None:
            raise Exception("Must specify either workflow name or workflow file name.")
        elif workflow_name != None and workflow_file != None:
            raise Exception("Cannot specify both workflow name and workflow file name.")

        wf_data = {}
        data = None
        files = None

        if workflow_name != None:
            wf_data['wf_name'] = workflow_name
        else:
            files = {'file': (os.path.basename(workflow_file), 
                open(workflow_file, 'rb'), 'application/octet-stream')}

        if parameter_file:
            params = _load_parameter_file(parameter_file)
        else:
            params = {}

        if parameters:
            params.update(parameters)

        if len(params) > 0:
            wf_data['wf_param'] = params

        wf_data['prov'] = provenance
        wf_data['sync'] = synchronous

        if files:
            files['json'] = (None, json.dumps(wf_data), 'application/json')
        else:
            data = json.dumps(wf_data)

        response = requests.post(run_url, data=data, files=files,
            auth=HTTPBasicAuth(username, password),
            #FIXME verify
            verify=False)

        return Run(url=url, username=username, password=password, response=response)
