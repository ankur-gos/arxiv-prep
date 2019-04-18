import click
import os
import glob
import gzip
import tarfile
from  move_tex_to_own_folder import move_to_folder

@click.command()
@click.argument('gzdir')
def gz(gzdir):
    for f in glob.glob(os.path.join(gzdir, '*.gz')):
        basepath, basename = os.path.split(f)
        if tarfile.is_tarfile(f):
            tar = tarfile.open(f)
            try:
                new_dir = basename[:-3]
                fulldir = os.path.join(basepath, new_dir)
                os.makedirs(fulldir)
                tar.extractall(path=fulldir)
            except OSError:
                tar.close()
                continue
            tar.close()
        else:
            with gzip.open(f, 'rb') as gf:
                g_bytes = gf.read()
                try:
                    utf8str = g_bytes.decode('utf-8')
                except UnicodeDecodeError:
                    continue
                with open(os.path.join(basepath, f'{basename[:-2]}tex'), 'w') as wf:
                    wf.write(utf8str)
        os.remove(f)
    move_to_folder(gzdir)
    for f in glob.glob(os.path.join(gzdir, '*.gz')):
        os.remove(f)
    for f in glob.glob(os.path.join(gzdir, '*.pdf')):
        os.remove(f)

if __name__ == '__main__':
    gz()



