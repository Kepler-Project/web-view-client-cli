
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
        self._outputs = None
        self._run_id = id
        self._success = False
        self._url = url
        self._username = username

        if response is not None:
            
            print("DEBUG: {}".format(response.text))

            if response.text == 'Unauthorized':
                self._error = response.text
            else:
                response_json = response.json()
    
                if response.status_code != requests.codes.ok:
                    if 'error' in response_json:
                        self._error = response_json['error']
                else:
                    self._success = True
    
                    if 'runid' in response_json:
                        self._run_id = response_json['runid']
    
                    if 'responses' in response_json:
                        self._is_running = False
                        self._outputs = response_json['responses']

    # get error message if failure, otherwise None
    def error(self):
        # see if error already set or no longer running
        if self._error is not None or self._is_running is False:
            return self._error
        
        self.status();
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
            self.status()
            return self._is_running

    # get the run status
    def status(self, outputs=False):
        response = requests.get("{}/runs/{}?outputs={}".format(self._url, 
            self._run_id, str(outputs).lower()), auth=HTTPBasicAuth(self._username, self._password),
            #FIXME verify
            verify=False)
        
        if response.text == 'Unauthorized':
            raise Exception(response.text)

        self._status = response.json()

        # error handling first
        if 'error' in self._status:
            self._error = self._status['error']

        if response.status_code != requests.codes.ok:
            return
            #raise Exception(self._error)
      
        self._is_running = self._status['status'] == 'running'
                    
        if 'responses' in self._status:
           self._outputs = self._status['responses']

        return self._status


    # get the output
    def outputs(self):
        if self._outputs is not None:
            return self._outputs
        self.status(outputs=True)
        return self._outputs

    # TODO
    def output(self, name):
        pass

    # TODO
    # get the provenance trace of the run
    def provenance(self, format='json'):
        pass
