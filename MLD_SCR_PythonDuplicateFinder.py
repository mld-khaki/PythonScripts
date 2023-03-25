from collections import namedtuple
import os
import hashlib
import numpy as np
import datetime

# Function to calculate the hash value of a file
def hash_file(filename):
    hasher = hashlib.md5()
    with open(filename, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

# Set the path of the folder you want to scan
folder_path = """e:\Zeus\Media\Music\\"""
folder_path = folder_path.replace("\\","/")

# Define a Set to store the hash and size of each file that has been checked
checked_files = set()

FileInfo = ('aaa', 11)


# FileInfo = namedtuple('Structure', ['hash', 'size'])

# List of namedtuples representing an array of structures
SpaceReleased = 0
CheckedSize   = 0
AddCount = 0
RemCount = 0

LastPrint = datetime.datetime.now()
# Traverse through all the files in the folder
for root, dirs, files in os.walk(folder_path):
    for file in files:
        # Get the full path of the file
        file_path = os.path.join(root, file)
        file_size = os.path.getsize((file_path))
        # Calculate the hash value of the file
        file_hash = hash_file(file_path)
        
        FileInfo = (file_hash,file_size)
        # Check if the file is a duplicate
        AddCount += 1
        CheckedSize += file_size
        if (file_hash, file_size) in [s for s in checked_files]:
            # If the file is a duplicate, delete it
            # os.remove(file_path)
            SpaceReleased += file_size
            RemCount += 1
            print(f"\nDuplicate file removed: {file}\n, *** Released Data = {SpaceReleased/1.0e9:14.10f}, Checked size = {CheckedSize/1.0e9:7.3f}")
            
        else:
            # Define a namedtuple for a single structure
            checked_files.add(FileInfo)
            
            TimeSinceLastPrint = LastPrint - datetime.datetime.now()
            
            if np.mod(AddCount,100) == 0 or TimeSinceLastPrint.total_seconds() >= 10:
                LastPrint = datetime.datetime.now()
                print(f"\n*** RemCnt = {RemCount}, Released Data = {SpaceReleased/1.0e9:14.10f} GB, Checked size = {CheckedSize/1.0e9:7.3f} GB")
                print(f"File added to set: {file}, total files count = {AddCount}")

