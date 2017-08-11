

class Utils:

    # expand text template from keys-values in a run
    def template(run, text):
        kv = run.keys_values()
        
        for k,v in kv.items():
            text = text.replace('${}'.format(k), v)

        return text
