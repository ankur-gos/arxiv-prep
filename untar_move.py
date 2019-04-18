import click
import os
import glob
import tarfile

@click.command()
@click.argument('inputdir')
@click.argument('outputdir')
def untar_move(inputdir, outputdir):
    print(inputdir)
    for f in glob.glob(os.path.join(inputdir, '*.tar')):
        print(f)
        with tarfile.open(f) as tf:
            tf.extractall(path=outputdir)

if __name__ == '__main__':
    untar_move()



