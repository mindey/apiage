import requests
from progress.bar import Bar
import logging
import time

def get(endpoint,
        silent=False,
        next_key='next',
        count_key='count',
        results_key='results',
        sleep=60,   # seconds [sleep when exception, e.g., 60]
        pause=None, # seconds [pause between requests: e.g., 1]
        proxies=None,
        debug=False):
    '''
    e.g., get('')
    '''

    results = []

    while True:

        if endpoint:
            if debug:
                print(endpoint)
            try:
                if proxies:
                    data = requests.get(endpoint, proxies=proxies).json()
                else:
                    data = requests.get(endpoint).json()
            except:

                data = None

                # Sleep
                if callable(sleep):
                    s = sleep()
                else:
                    s = sleep

                logging.log(20, 'Sleeping for {} seconds'.format(s))

                if debug:
                    print('Sleeping for {} seconds'.format(s))

                time.sleep(s)
        else:
            break

        if data:
            # count_key
            if callable(count_key):
                if not count_key(data):
                    return results
            elif not data.get(count_key):
                return results

            if not silent:

                if 'bar' not in locals():

                    if callable(count_key):
                        if callable(results_key):
                            chunk = len(results_key(data))
                        else:
                            chunk = len(data.get(results_key))
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

            # Pause
            if callable(pause):
                t = pause()
            else:
                t = pause

            if t:
                time.sleep(t)

    if not silent:
        bar.finish()

    return results
