
"""
Kepler Web-View Run

"""

import requests

class Run:

    def __init__(self, url, response):
    
        self._error = None
        self._response_json = None
        self._success = False

        if response.text == 'Unauthorized':
            self._error = response.text
        else:
            self._response_json = response.json()

            if response.status_code != requests.codes.ok:
                if 'error' in self._response_json:
                    self._error = self._response_json['error']
            else:
                self._success = True

    # wait until run finished
    # returns True if success, False otherwise
    def finish(self):
        return self._success

    # get error message if failure, otherwise None
    def error(self):
        return self._error

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
