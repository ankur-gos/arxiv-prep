import click
import requests
import glob
import os
import mimetypes
import json
import uuid
import multiprocessing as mp

host = os.environ['HOST']
db = os.environ['DB']

def add_docs_from_src_dir(srcdir, docname):
    for f in glob.glob(os.path.join(srcdir, '*')):
        if os.path.isdir(f):
            add_docs_from_src_dir(f, docname)
            continue
        basename, fname = os.path.split(f)
        ext = fname.split('.')[-1]
        base_obj = {'docname': docname, 'fname':fname, 'type':'other'}
        if ext == 'pdf' or ext == 'png' or ext == 'jpg' or ext == 'eps':
            base_obj['type'] = 'image'
        elif ext == 'tex':
            base_obj['type'] = 'src'
        uid = uuid.uuid4()
        r = requests.put(os.path.join(host, db, str(uid)), json = base_obj)
        if r.status_code == 201:
            jdata = r.json()
            rev = jdata['rev']
            # add the attachment
            with open(f, 'rb') as rf:
                mimetype, encoding = mimetypes.guess_type(fname)
                if mimetype is None:
                    mimetype = 'application/octet-stream'
                headers = {'Content-type': mimetype}
                content = rf.read()
                rev = {'rev': rev}
                r2 = requests.put(os.path.join(host, db, str(uid), fname), data=content, headers=headers, params=rev)
                print(r2.text)
                



def populate_db_from_srcdir(srcdir):
    for d in glob.glob(os.path.join(srcdir, '*')):
        basepath, docname = os.path.split(d)
        add_docs_from_src_dir(srcdir, docname)



def populate_db_from_pdfdir(pdfdir, bulk=100):
    pass

@click.command()
@click.argument('srcdir')
@click.argument('pdfdir')
def run(srcdir, pdfdir):
    populate_db_from_srcdir(srcdir)
    populate_db_from_pdfdir(pdfdir)

if __name__ == '__main__':
    run()

