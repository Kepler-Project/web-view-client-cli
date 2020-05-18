
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

    def __init__(self, url='https://localhost:9443/kepler', username=None, password=None, debug=False):

        if url is None:
            raise Exception("Must specify url to Kepler WebView.")

        self._url = url
        self._username = username
        self._password = password
        self._debug = debug
        
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
    def runs(self, name=None, parameters=None):
        
        runs_url = "{}/runs".format(self._url)

        data = {}

        if name is not None:
            data['name'] = name

        if parameters is not None:
            data['parameters'] = parameters
        
        response = requests.post(runs_url, data=data, auth=HTTPBasicAuth(self._username, self._password),
            #FIXME verify
            verify=False)

        if self._debug:
            print("DEBUG: response: {}".format(response.text))
    
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
                runs.append(Run(url=self._url,username=self._username,password=self._password,fields=fields,debug=self._debug))

        return Runs(runs)

    # start a workflow execution run.
    def start_run(self, workflow_name=None, workflow_file=None, 
        parameters=None, parameter_file=None, paramset=None,
        provenance=True, synchronous=False, webhook=None, reqId=None):

        run_url = "{}/runwf".format(self._url)
        
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

        if paramset and len(paramset) > 0:
            wf_data['wf_paramset'] = paramset

        wf_data['prov'] = provenance
        wf_data['sync'] = synchronous

        if webhook:
            wf_data['webhook'] = webhook

        if reqId:
            wf_data['reqid'] = reqId

        if files:
            files['json'] = (None, json.dumps(wf_data), 'application/json')
        else:
            data = json.dumps(wf_data)

        response = requests.post(run_url, data=data, files=files,
            auth=HTTPBasicAuth(self._username, self._password),
            #FIXME verify
            verify=False)
        
        return Run(url=self._url, username=self._username, password=self._password, response=response, debug=self._debug)
