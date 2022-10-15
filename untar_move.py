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
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tf, path=outputdir)

if __name__ == '__main__':
    untar_move()



