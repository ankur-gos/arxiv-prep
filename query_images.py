import requests
import os
import click
from requests_toolbelt.multipart import decoder
import re
import json

host = os.environ['HOST']
db = os.environ['DB']

def query_images(target_dir, limit=3000):
    endpoint = '_design/queries/_view/type'
    url = os.path.join(host, db, endpoint)
    params = {'key': '"image"', 'limit': limit}
    r = requests.get(url, params=params)
    result = r.json()
    rows = result['rows']
    for row in rows:
        row_id = row['id']
        params = {'attachments': 'true'}
        r2 = requests.get(os.path.join(host, db, row_id), params=params)
        data = decoder.MultipartDecoder.from_response(r2)
        current_uuid = None
        for part in data.parts:
            cd = 'Content-Disposition'.encode()
            ct = 'Content-Type'.encode()
            js = 'application/json'.encode()
            if ct in part.headers:
                if part.headers[ct] == js:
                    j_str = part.text
                    file_obj = json.loads(j_str)
                    current_uuid = file_obj['_id']
                
            if cd in part.headers:
                attachment = part.headers[cd].decode()
                fre = re.match('.*filename="(.*)"', attachment)
                if fre is not None:
                    filename = fre.group(1)
                    fname, _, ext = filename.rpartition('.')
                    write_name = f'{current_uuid}_{fname}.{ext}'
                    with open(os.path.join(target_dir, write_name), 'wb') as wf:
                        wf.write(part.content)



if __name__ == '__main__':
    query_images('figure_dataset')

