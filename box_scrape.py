from base64 import decodestring
from webbot import Browser
from boxsdk import OAuth2
from boxsdk import Client
from PIL import Image
import os

CLIENT_ID = None
CLIENT_SECRET = None
EMAIL = None
PASSWORD = None

def create_local_folder(name):
    # Get path to foldername
    cwd = os.getcwd()
    path = os.path.join(cwd, name)
    
    # Create folder if it does not exist
    if not os.path.exists(path):
        os.mkdir(path)
        print("Created folder: ", path)

    return path
    
def web_auth(auth_url, csrf_token):
    # Constants
    state_param = 'state='
    code_param = 'code='
    url_separator = '&'

    # Instantiate browser
    web = Browser()

    # Web authentication process
    web.go_to(auth_url)
    web.type(EMAIL, 'login')
    web.type(PASSWORD,'password')
    web.click('Authorize')
    web.click('Grant access to Box')
    
    # Get url for access code
    access_url = web.get_current_url()
    
    # Close browser
    web.close_current_tag()

    print("URL: " + access_url)
    # Get access codes
    access_csrf = access_url[access_url.index(state_param) + len(state_param):access_url.index(url_separator)]
    access_code = access_url[access_url.index(code_param) + len(code_param):]
    
    # Return access codes
    return access_csrf, access_code

def box_login():
    # Create OAuth Object
    oauth = OAuth2(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
    )

    # Get auth url and csrf token
    auth_url, csrf_token = oauth.get_authorization_url('https://127.0.0.1:8082/Auth')

    # Get csrf reference and access code
    access_csrf, access_code = web_auth(auth_url,csrf_token)

    # Check csrf validity and authenticate OAuth
    assert access_csrf == csrf_token
    refresh_token, access_token = oauth.authenticate(access_code)

    return oauth

def main():
    # Get oauth object
    oauth = box_login()

    # Create Box client
    client = Client(oauth)

    # Get Box root folder
    root = client.folder(folder_id='0')
    root_folder_items = root.get_items(limit=100, offset=0)

    # Get latest folder
    latest_folder = root_folder_items[len(root_folder_items)-1]
    latest_folder_items = latest_folder.get_items(limit=100, offset=0)

    # Create a folder in the local root directory with the name of the latest folder in Box
    local_folder = create_local_folder(str(latest_folder))

    # Write all images to the local folder
    for i in range(len(latest_folder_items)):
        # Add bytestream from Box into a byte array
        byte_array = latest_folder_items[i].content()

        # Set the path of the image
        image_path = os.path.join(local_folder, str(latest_folder_items[i])+".jpg")

        # Write the image as bytes to the image path
        f = open(image_path,"wb")
        f.write(byte_array)
        f.close()

        print(image_path, "completed.")


if __name__ == "__main__":
    main()
