import sys
import requests
from workflow import Workflow3

API_URL = 'https://maps.googleapis.com/maps/api/geocode/json?address=paris'


def add_suggests(items):
    for address in items:
        if not address['geometry']['location']:
            return

        coordinates_string = '%s,%s' % (address['geometry']['location']['lng'], address['geometry']['location']['lat'])
        item = wf.add_item(
            address['formatted_address'],
            subtitle='Copy lng,lat : %s' % coordinates_string,
            arg=coordinates_string,
            valid=True,
        )
        coordinates_string = '%s,%s' % (address['geometry']['location']['lat'], address['geometry']['location']['lng'])
        item.add_modifier('alt', subtitle='Copy lat,lng : %s' % coordinates_string, arg=coordinates_string)


def main(wf):
    args = wf.args
    query = args[0]

    try:
        response = requests.get(API_URL, params={
            'address': query
        })
        response.raise_for_status()
        add_suggests(response.json()['results'])
    except requests.RequestException:
        wf.add_item('Unable to decode address')

    # Send output to Alfred. You can only call this once.
    # Well, you *can* call it multiple times, but Alfred won't be listening
    # any more...
    wf.send_feedback()


if __name__ == '__main__':
    # Create a global `Workflow` object
    wf = Workflow3()
    # Call your entry function via `Workflow.run()` to enable its helper
    # functions, like exception catching, ARGV normalization, magic
    # arguments etc.
    sys.exit(wf.run(main))
