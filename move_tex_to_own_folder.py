import glob
import click
import os

def move_to_folder(inpdir):
    for f in glob.glob(os.path.join(inpdir, '*.tex')):
        basepath, basename = os.path.split(f)
        folder_name = basename[:-4]
        os.makedirs(os.path.join(basepath, folder_name))
        os.rename(f, os.path.join(basepath, folder_name, basename))

@click.command()
@click.argument('inpdir')
def move_wrapper(inpdir):
    move_to_folder(inpdir)


if __name__ == '__main__':
    move_wrapper()

