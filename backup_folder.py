import zipfile
import os
import argparse

# commandline args
parser = argparse.ArgumentParser(description="backup folder tree to zip")

parser.add_argument('-f', 'folder', default='.', help="folder to zip, default is current folder")
parser.add_argument('-o', 'output', help="output zip file")

# get args
args = parser.parse_args()

FOLDER = args.folder
OUTPUT = args.output

# Backup the entire contents of "folder" into a ZIP file.
def backup_to_zip(folder):
    folder = os.path.abspath(folder) # make sure folder is absolute

    if OUTPUT:
        zip_filename = OUTPUT
    else:
        # Figure out the filename this code should use based on how many times the backup run.
        number = 1
        while True:
            zip_filename = os.path.basename(folder) + '_' + str(number) + '.zip'
            if not os.path.exists(zip_filename):
                break
            number += 1

    print('Creating {zip_filename}'.format(zip_filename=zip_filename))
    backup_zip = zipfile.ZipFile(zip_filename, 'w')

    # Walk the entire folder tree and compress the files in each folder.
    for foldername, subfolders, filenames in os.walk(folder):
        print('Adding files in {foldername}'.format(foldername=foldername))
        # Add the current folder to the ZIP file.
        backup_zip.write(foldername)
        # Add all the files in this folder to the ZIP file.
        for filename in filenames:
            folder_name = os.path.basename(folder) + '_'
            if filename.startswith(folder_name) and filename.endswith('.zip'):
                continue   # don't backup the backup ZIP files
            backup_zip.write(os.path.join(foldername, filename))
    backup_zip.close()
    print('Done.')

if __name__ == '__main__':
    backup_to_zip(FOLDER)