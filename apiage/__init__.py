import requests
from progress.bar import Bar
import time

def get(endpoint,
        silent=False,
        next_key='next',
        count_key='count',
        results_key='results',
        sleep_seconds=60):
    '''
    e.g., get('')
    '''

    results = []

    while True:

        try:
            data = requests.get(endpoint).json()
        except:
            logging.log('Sleeping for {} seconds'.format(sleep_seconds))
            time.sleep(sleep_seconds)


        if not data.get(count_key):
            return results

        if not silent:
            if count_key in data.keys() and 'bar' not in locals():
                chunk = len(data.get(results_key))
                bar = Bar('API Pages:', max=round(data.get(count_key)/chunk))

            bar.next()

        if results_key in data.keys():
            results.extend(data[results_key])
        if next_key not in data.keys():
            break
        elif not data.get(next_key):
            break
        else:
            endpoint = data[next_key]

    if not silent:
        bar.finish()

    return results
