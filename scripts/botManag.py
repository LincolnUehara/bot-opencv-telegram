import subprocess
import glob
import os
import cv2

def getDirectoryPath():
    '''
    Return the path of working directory. 
    '''

    PIPE = subprocess.PIPE
    WORK_DIR = subprocess.Popen(['pwd'], stdout = PIPE, stderr = PIPE).communicate()
    WORK_DIR = WORK_DIR[0].decode("utf-8")
    WORK_DIR = WORK_DIR.split('\n')
    return (WORK_DIR[0] + "/")

def getScriptPath():
    '''
    Return the path of 'scripts' folder.
    This folder should already exist.
    '''
    return (getDirectoryPath() + "scripts/")

def getImagePath():
    '''
    Return the path of 'images' folder.
    This folder should already exist.
    '''
    return (getScriptPath() + "images/")

def getFolderPath(folder_name = None):
    '''
    Return the path of attributed folder name in working directory.
    If it does not exist yet, create it.
    '''
    subprocess.Popen(["test -d {} || mkdir -p {}".format(folder_name, folder_name)], shell=True)
    return (getDirectoryPath() + "{}/".format(folder_name))

def moveFile(from_path = None, to_path = None):
    '''
    Move the file from one location to another.
    '''
    subprocess.Popen(["mv {} {}".format(from_path, to_path)], shell=True)

def lastFileOnFolder(folder_name = None):
    '''
    Return the name of most recent file of given folder.
    '''
    archive_path = getFolderPath(folder_name)
    list_of_files = glob.glob(archive_path + '*jpg')
    return (max(list_of_files, key = os.path.getctime))[-18:]

def makeFileName(fileDate = None):
    '''
    Return a name based on the date of the file.
    '''

    year = str(fileDate.year)

    month = fileDate.month
    if (month < 10):
        month = "0" + str(month)
    else:
        month = str(month)
    
    day = fileDate.day
    if (day < 10):
        day = "0" + str(day)
    else:
        day = str(day)
    
    hour = fileDate.hour
    if (hour < 10):
        hour = "0" + str(hour)
    else:
        hour = str(hour)

    minute = fileDate.minute
    if (minute < 10):
        minute = "0" + str(minute)
    else:
        minute = str(minute)
    
    second = fileDate.second
    if (second < 10):
        second = "0" + str(second)
    else:
        second = str(second)
    
    return year + month + day + hour + minute + second

def resizeFile():
    '''
    This code intended to resize the image to accelerate identification
    or pickles generating process. However it is not used actually.
    '''

    # Load the received image to be resized.
    #image = cv2.imread(file_path)

    # Perform the resizing of the image.
    #img_rows = image.shape[0]
    #img_columns = image.shape[1]
    #final_rows = int(img_rows * proportion)
    #dim = (final_rows, int(img_rows * (final_rows / img_columns)))
    #resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    
    # Save the resized image.
    #cv2.imwrite(resized_archive, resized)

    pass

# If this file was run directly, exit leaving a message.
if __name__ == "__main__":
    print("This script is not the main script to run.\n")
    print("Please check the documents.\n")
    exit()