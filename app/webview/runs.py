
"""
Kepler Web-View Runs

"""

class Runs:

    def __init__(self, runs):

        self._runs = runs

    # get the latest run (based on start time) for a workflow
    # NOTE: this does not query the server for latest runs.
    def latest(self, workflow_name):

        if workflow_name is None:
            raise Exception('Must specify workflow name.')

        latest_run = None
        latest_time = '0'

        for run in self._runs:
            if run.workflow_name() == workflow_name and run.start_time() > latest_time:
                latest_run = run
                latest_time = run.start_time()

        return latest_run

    # get the set of workflow names
    def names(self):
        names = set()
        for run in self._runs:
            names.add(run.workflow_name())
        return names

    def parameters(self):
        p = []
        for run in self._runs:
            p.append({'name':run.workflow_name() , 'parameters':run.parameters()})
        return p
