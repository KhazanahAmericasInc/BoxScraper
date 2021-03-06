from configparser import ConfigParser
from webbot import Browser
from boxsdk import OAuth2
from boxsdk import Client
from PIL import Image
import os


# Creates and returns the path a folder in /project/downloads/<name>
def create_local_folder(name):
    # Get path to foldername
    cwd = os.getcwd()
    path_downloads = os.path.join(cwd, 'downloads')

    if not os.path.exists(path_downloads):
        os.mkdir(path_downloads)
        print("Created downloads folder.")

    path = os.path.join(path_downloads, name)
    
    # Create folder if it does not exist
    if not os.path.exists(path):
        os.mkdir(path)
        print("Created folder: ", path)

    return path


# Obtains the access csrf and access codes for Box (OAuth)
def web_auth(auth_url, csrf_token, email, password):
    # Constants
    state_param = 'state='
    code_param = 'code='
    url_separator = '&'

    # Instantiate browser
    web = Browser()

    # Web authentication process
    web.go_to(auth_url)
    web.type(email, 'login')
    web.type(password,'password')
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


# Logs into box via id, secret, email and password
def box_login(id, secret, email, password):
    print(id,secret,email,password)
    # Create OAuth Object
    oauth = OAuth2(
        client_id=id,
        client_secret=secret,
    )

    # Get auth url and csrf token
    auth_url, csrf_token = oauth.get_authorization_url('https://127.0.0.1:8082/Auth')

    # Get csrf reference and access code
    access_csrf, access_code = web_auth(auth_url,csrf_token, email, password)

    # Check csrf validity and authenticate OAuth
    assert access_csrf == csrf_token
    refresh_token, access_token = oauth.authenticate(access_code)

    return oauth


# Loads from config file
def loadBoxInfo():
    config = ConfigParser()
    config.read('config.ini')
    return config['BOX']


# Main loop
def main():
    box_info = loadBoxInfo()

    # Get oauth object
    try:
        oauth = box_login(box_info['CLIENT_ID'], box_info['CLIENT_SECRET'], box_info['EMAIL'], box_info['PASSWORD'])
    except ValueError:
        print("\n********** Value Error! Double check your credentials in the config.ini file. **********\n")
        exit()

    # Create Box client
    client = Client(oauth)

    # Get Box root folder
    root = client.folder(folder_id='0')
    root_folder_items = root.get_items(limit=1000, offset=0)

    # Get latest folder
    latest_folder = root_folder_items[len(root_folder_items)-1]
    latest_folder_items = latest_folder.get_items(limit=100, offset=0)

    # Create a folder in the local root directory with the name of the latest folder in Box
    #local_folder = create_local_folder(str(latest_folder))
    local_folder = create_local_folder('')

    """ DOWNLOADS ALL IMAGES FROM BOX""" 
    for i in range(len(root_folder_items)):
        _latest_folder_items = root_folder_items[i].get_items(limit=100, offset=0)

        for j in range(len(_latest_folder_items)):
            image_path = os.path.join(local_folder, str(_latest_folder_items[j]) + ".jpg")

            if os.path.exists(image_path):
                print("Exists: ", image_path)
                continue

            byte_array = _latest_folder_items[j].content()

            f = open(image_path, "wb")
            f.write(byte_array)
            f.close()

            print(image_path," completed.")

    print("Box scrape complete.")


    """ DOWNLOAD LATEST FOLDER ONLY
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
    """
if __name__ == "__main__":
    main()
