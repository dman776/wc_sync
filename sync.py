import os
import sys
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
import datetime, time
from pprint import pprint
from configparser import ConfigParser

config = ConfigParser({'directory': '', 'dropbox_folder': '', 'db_token': ''})
config_data = config.read("sync.ini")
if not config.has_section("src"):
    config.add_section("src")
if not config.has_section("dst"):
    config.add_section("dst")

directory = config.get("src", "directory")
dropbox_folder = config.get("dst", "dropbox_folder")
db_token = config.get("dst", "db_token")

def backup(dbx, target_filename, folder):
    with open(target_filename, 'rb') as f:
        # We use WriteMode=overwrite to make sure that the settings in the file
        # are changed on upload
        path = os.path.split(target_filename)
        name = path[len(path) - 1]

        print("Uploading " + target_filename + " to Dropbox as " + folder + "/" + name + "...")
        try:
            res = dbx.files_upload(f.read(), folder + "/" + name, mode=WriteMode('overwrite'))
        except ApiError as err:
            # This checks for the specific error where a user doesn't have
            # enough Dropbox space quota to upload this file
            if (err.error.is_path() and
                    err.error.get_path().reason.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient space.")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()
        return res

# MAIN ##########

dbx = dropbox.Dropbox(db_token)

folders = []
for d in os.listdir(directory):
    if ".DS_Store" not in d:
        folders.append(os.path.join(directory, d))

latest_folder = max(folders, key=os.path.getmtime)
for f in os.listdir(latest_folder):
    if ".DS_Store" not in f:
        backup(dbx, latest_folder + "/" + f, dropbox_folder)

