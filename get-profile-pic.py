#!/usr/bin/python

import requests
import re
import json
import sys
from io import BytesIO
from PIL import Image

def main():
    BASE_URL = 'https://www.instagram.com/{profile}/?hl=es'
    arg = ''
    if len(sys.argv) > 1:
        arg = sys.argv[1]
    profile = arg or 'bighelmet7'
    url = BASE_URL.format(profile=profile)
    resp = requests.get(url)
    pattern = re.compile('window._sharedData = ({.*})')
    if resp:
        match = pattern.search(resp.text)
        if match:
            json_script = match.group(0)
            text = json_script.split(' = ')[1] 	# window._sharedData = {} we need the json obj only.
            text = text.replace(';', '')	# espace the ; of the json.
            info = json.loads(text)
            entry_data = info.get('entry_data', {})
            profile_page = entry_data.get('ProfilePage', [])
            graphql = profile_page[0].get('graphql', {})	# ProfilePage its an array of one element.
            user = graphql.get('user', {})
            profile_pic_url = user.get('profile_pic_url_hd', '')
            if profile_pic_url:
                resp = requests.get(profile_pic_url)
                if resp:
                    img = Image.open(BytesIO(resp.content))
                    img.show()

if __name__ == '__main__':
    main()
