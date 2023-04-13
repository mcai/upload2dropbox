import argparse
import requests
import zipfile
import os

def zip_file(file_path):
    # Create a temporary zip file in the same directory as the original file
    zip_file_path = os.path.join(os.path.dirname(file_path), 'temp_zip_file.zip')
    
    # Create a new zip file
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add the file to the zip archive
        zipf.write(file_path, os.path.basename(file_path))
    
    return zip_file_path

def upload_to_dropbox(access_token, local_file_path, dropbox_path):
    # Determine if the local file path is a file
    if os.path.isfile(local_file_path):
        # Zip the file before uploading
        local_file_path = zip_file(local_file_path)
    
    # Define the API endpoint URL
    url = 'https://content.dropboxapi.com/2/files/upload'

    # Set the headers for the API request
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/octet-stream',
        'Dropbox-API-Arg': '{"path":"' + dropbox_path + '","mode":"add","autorename":true,"mute":false,"strict_conflict":false}'
    }

    # Read the file in binary mode
    with open(local_file_path, 'rb') as f:
        file_data = f.read()

    # Send the POST request to the Dropbox API
    response = requests.post(url, headers=headers, data=file_data)

    # Print the response
    print(response.text)
    
    # Delete the temporary zip file if it was created
    if local_file_path.endswith('.zip'):
        os.remove(local_file_path)

def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description='Upload a file to Dropbox.')

    # Define the command-line arguments
    parser.add_argument('-t', '--token', required=True, help='Dropbox API access token.')
    parser.add_argument('-l', '--local', required=True, help='Local file path of the file to be uploaded. If a file, it will be zipped before uploading.')
    parser.add_argument('-d', '--dropbox', required=True, help='Path in Dropbox where the file will be uploaded.')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the upload_to_dropbox function with the parsed arguments
    upload_to_dropbox(args.token, args.local, args.dropbox)

if __name__ == '__main__':
    main()
