#!/usr/bin/python
#
# Copyright (C) 2019 Darryl Quinn
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# You must not misrepresent the origin of the material contained within.
#
# Modified versions must be modified to attribute to the original source
# and be marked in reasonable ways as differentiate it from the original
# version.
#
import os
import sys
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
from pprint import pprint
from configparser import ConfigParser


def backup(dbx, target_filename, folder):
    with open(target_filename, 'rb') as f:
        path = os.path.split(target_filename)
        name = path[len(path) - 1]

        try:
            res = dbx.files_upload(f.read(), folder + "/" + name, mode=WriteMode('overwrite'))
        except ApiError as err:
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
#       Init config ###########
config = ConfigParser({'directory': '', 'files': '', 'dropbox_folder': '', 'db_token': ''})
config_data = config.read("sync.ini")
if not config.has_section("src"):
    config.add_section("src")
if not config.has_section("dst"):
    config.add_section("dst")

directory = config.get("src", "directory")
files_string = config.get("src", "files")
dropbox_folder = config.get("dst", "dropbox_folder")
db_token = config.get("dst", "db_token")
files = files_string.split(",")

# Connect to Dropbox
dbx = dropbox.Dropbox(db_token)

# Get src folders
folders = []
for d in os.listdir(directory):
    if ".DS_Store" not in d:
        folders.append(os.path.join(directory, d))

# get latest folder info
latest_folder = max(folders, key=os.path.getmtime)
pfolds = os.path.split(latest_folder)

db_dst_folder = "{}/{}".format(dropbox_folder, pfolds[1])

# process all files in the latest folder
for f in os.listdir(latest_folder):
    tmppath = latest_folder + "/" + f
    if ".DS_Store" not in f:
        # filter files
        if f in files:
            print("Backing up file: {0} to DROPBOX:{1}/{2}".format(tmppath, db_dst_folder, f))
            backup(dbx, tmppath, db_dst_folder)
        else:
            print("Skipping file: {}".format(tmppath))

print("done.")