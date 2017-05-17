
"""
Kepler Web-View Run

"""

import requests
from requests.auth import HTTPBasicAuth

class Run:

    def __init__(self, url='https://localhost:9443/kepler', username=None, 
        password=None, response=None, id=None):

        self._error = None
        self._is_running = None
        self._password = password
        self._response_json = None
        self._run_id = id
        self._success = False
        self._url = url
        self._username = username

        #print(response.text)

        if response is not None:
            if response.text == 'Unauthorized':
                self._error = response.text
            else:
                self._response_json = response.json()
    
                if response.status_code != requests.codes.ok:
                    if 'error' in self._response_json:
                        self._error = self._response_json['error']
                else:
                    self._success = True
    
                    if 'runid' in self._response_json:
                        self._run_id = self._response_json['runid']
    
                    if 'responses' in self._response_json:
                        self._is_running = False
                    else:
                        self._is_running = True

    # get error message if failure, otherwise None
    def error(self):
        return self._error

    # wait until run finished
    # returns True if success, False otherwise
    def finish(self):
        return self._success

    # get the run id. returns None if provenance not enabled.
    def id(self):
        return self._run_id
    
    # get if the run is still running.
    def is_running(self):
        if self._is_running is False:
            return False
        else:
            response = requests.get("{}/runs/{}".format(self._url, self._run_id),
                auth=HTTPBasicAuth(self._username, self._password),
                #FIXME verify
                verify=False)
        
            if response.text == 'Unauthorized':
                raise Exception(response.text)

            json = response.json()
            #print(json)

            if response.status_code != requests.codes.ok:
                self._error = json['error']
                raise Exception(self._error)

            self._is_running = json['status'] == 'running'
            return self._is_running

    # get the output
    def outputs(self):
        if self._response_json and 'responses' in self._response_json:
            return self._response_json['responses']
        return None

    # TODO
    def output(self, name):
        pass

    # TODO
    # get the provenance trace of the run
    def provenance(self, format='json'):
        pass
