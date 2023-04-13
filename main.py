import argparse
import requests

def upload_to_dropbox(access_token, local_file_path, dropbox_path):
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

def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description='Upload a file to Dropbox.')

    # Define the command-line arguments
    parser.add_argument('-t', '--token', required=True, help='Dropbox API access token.')
    parser.add_argument('-l', '--local', required=True, help='Local file path of the file to be uploaded.')
    parser.add_argument('-d', '--dropbox', required=True, help='Path in Dropbox where the file will be uploaded.')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the upload_to_dropbox function with the parsed arguments
    upload_to_dropbox(args.token, args.local, args.dropbox)

if __name__ == '__main__':
    main()
