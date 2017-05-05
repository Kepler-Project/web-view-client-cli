
"""
Kepler WebView client.

"""

import json
import requests
from requests.auth import HTTPBasicAuth

class WebView:

    def __init__(self):
        
        self._params = {}
        self._url = 'https://localhost:9443/kepler'

        self._urls = {
            'run' : "{}/runwf".format(self._url)
        }

        self._username = 'none'
        self._password = 'none'

    def load_parameter_file(self, name):
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
                        
                    self.set_parameter(name.strip(), value.strip())

    def set_parameter(self, name, value):
        self._params[name] = value

    def set_url(self, url):
        self._url = url
    
    def set_workflow(self, name):
        self._wfname = name

    def start_run(self):
        print("start run")

        data = {
            'wf_name': self._wfname
        }

        if self._params:
            data['wf_params'] = self._params

        response = requests.post(self._urls['run'], data = json.dumps(data),
            auth=HTTPBasicAuth(self._username, self._password),
            #FIXME verify
            verify=False)

        #print(response.text)

        response_json = response.json()

        if response.status_code != requests.codes.ok:
            if 'error' in response_json:
                print("ERROR: {}".format(response_json['error']))
            response.raise_for_status()
        else:
            print(response.json())

    def url(self):
        return self._url

