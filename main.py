import argparse
import requests
import os
import shutil
from zipfile import ZipFile

def zip_directory(directory_path):
    # Create a temporary zip file
    zip_file_name = os.path.basename(directory_path) + '.zip'
    zip_file_path = os.path.join(os.path.dirname(directory_path), zip_file_name)

    # Create a ZipFile object
    with ZipFile(zip_file_path, 'w') as zipf:
        # Iterate over all files and directories in the specified directory
        for root, _, files in os.walk(directory_path):
            for file in files:
                # Get the file path
                file_path = os.path.join(root, file)
                # Get the relative path within the zip file
                relative_path = os.path.relpath(file_path, directory_path)
                # Add the file to the zip file
                zipf.write(file_path, relative_path)

    return zip_file_path

def upload_to_dropbox(access_token, local_path, dropbox_path):
    # Determine if the local path is a file or a directory
    is_directory = os.path.isdir(local_path)
    file_to_upload = local_path

    # If the local path is a directory, zip it
    if is_directory:
        file_to_upload = zip_directory(local_path)

    # Define the API endpoint URL
    url = 'https://content.dropboxapi.com/2/files/upload'

    # Set the headers for the API request
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/octet-stream',
        'Dropbox-API-Arg': '{"path":"' + dropbox_path + '","mode":"add","autorename":true,"mute":false,"strict_conflict":false}'
    }

    # Read the file in binary mode
    with open(file_to_upload, 'rb') as f:
        file_data = f.read()

    # Send the POST request to the Dropbox API
    response = requests.post(url, headers=headers, data=file_data)

    # Print the response
    print(response.text)

    # If a zip file was created, remove it after the upload
    if is_directory:
        os.remove(file_to_upload)

def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description='Upload a file or directory to Dropbox.')

    # Define the command-line arguments
    parser.add_argument('-t', '--token', required=True, help='Dropbox API access token.')
    parser.add_argument('-l', '--local', required=True, help='Local file path or directory to be uploaded.')
    parser.add_argument('-d', '--dropbox', required=True, help='Path in Dropbox where the file or directory will be uploaded.')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the upload_to_dropbox function with the parsed arguments
    upload_to_dropbox(args.token, args.local, args.dropbox)

if __name__ == '__main__':
    main()
