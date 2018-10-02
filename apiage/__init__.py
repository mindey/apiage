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

        if endpoint:
            try:
                data = requests.get(endpoint).json()
            except:
                logging.log('Sleeping for {} seconds'.format(sleep_seconds))
                time.sleep(sleep_seconds)
        else:
            break


        # count_key
        if callable(count_key):
            if not count_key(data):
                return results
        elif not data.get(count_key):
            return results

        if not silent:

            if 'bar' not in locals():

                if callable(count_key):
                    chunk = len(results_key(data))
                    bar = Bar('API Pages:', max=round(count_key(data)/chunk))
                elif count_key in data.keys():
                    chunk = len(data.get(results_key))
                    bar = Bar('API Pages:', max=round(data.get(count_key)/chunk))

            bar.next()

        if callable(results_key):
            if results_key(data):
                results.extend(results_key(data))
        elif results_key in data.keys():
            results.extend(data[results_key])

        if callable(next_key):
            endpoint = next_key(data)
        elif next_key not in data.keys():
            break
        elif not data.get(next_key):
            break
        else:
            endpoint = data[next_key]

    if not silent:
        bar.finish()

    return results
