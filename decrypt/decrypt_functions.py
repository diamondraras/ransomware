import pyAesCrypt
from os import stat
import os, sys, subprocess
import pickle
import bcrypt


def toDecrypt(file, password, bufferSize=64 * 1024):
    encFileSize = stat(file).st_size
    with open(file, 'rb') as fIn:
        decryptedOutput = file+".decrypted"
        with open(decryptedOutput, 'wb') as fOut:
            try:
                pyAesCrypt.decryptStream(
                    fIn, fOut, password, bufferSize, encFileSize)
                return (decryptedOutput,True)
            except ValueError:
                return (decryptedOutput, False)

def load_object(object_name):
    with open(object_name, "rb") as file:
        my_depickler = pickle.Unpickler(file)
        data = my_depickler.load()
    return data

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

    
def hashStr(stringToHash, key):
    return bcrypt.hashpw(stringToHash.encode("utf-8"),key).decode("utf-8")[29:]


def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles

def isCryptedFileGetData(drive):

    # Check if "isCrypted" exists
    isCryptedFile = getIsCryptedFile(drive)
    isCryptedFileExists = os.path.isfile(isCryptedFile)
    crypted_files = list()
    if isCryptedFileExists:
        with open(isCryptedFile, 'r', encoding="utf-8") as file:
            crypted_files = file.read().split('\n')[1:-1]
            crypted_files.remove('')
        print(crypted_files)
    return crypted_files

def getIsCryptedFile(drive):
    return drive + "\\" + "isCrypted"
        

def deleteFileInIsCrypted(isCryptedFile, file):
    files = list()
    with open(isCryptedFile, 'r', encoding="utf-8") as _:
        files = _.read().split('\n')
        files.remove(file)
    removeAttribcmd = "attrib " + isCryptedFile + " -s -h"
    addAttribcmd = "attrib " + isCryptedFile + " +s +h"
    subprocess.call(removeAttribcmd)
    with open(isCryptedFile, 'w', encoding="utf-8") as __:
        __.write("\n".join(files))
    subprocess.call(addAttribcmd)

def getStoredCpuID(drive):
    isCryptedFile = getIsCryptedFile(drive)
    print(isCryptedFile)
    isCryptedFileExists = os.path.isfile(isCryptedFile)

    if isCryptedFileExists:
        with open(isCryptedFile, 'r', encoding="utf-8") as file:
            return file.read().split('\n')[0]+'\r\n'
    return None

def subprocess_args(include_stdout=True):
    # The following is true only on Windows.
    if hasattr(subprocess, 'STARTUPINFO'):
        # On Windows, subprocess calls will pop up a command window by default
        # when run from Pyinstaller with the ``--noconsole`` option. Avoid this
        # distraction.
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        # Windows doesn't search the path by default. Pass it an environment so
        # it will.
        env = os.environ
    else:
        si = None
        env = None

    # ``subprocess.check_output`` doesn't allow specifying ``stdout``::
    #
    #   Traceback (most recent call last):
    #     File "test_subprocess.py", line 58, in <module>
    #       **subprocess_args(stdout=None))
    #     File "C:\Python27\lib\subprocess.py", line 567, in check_output
    #       raise ValueError('stdout argument not allowed, it will be overridden.')
    #   ValueError: stdout argument not allowed, it will be overridden.
    #
    # So, add it only if it's needed.
    if include_stdout:
        ret = {'stdout': subprocess.PIPE}
    else:
        ret = {}

    # On Windows, running this from the binary produced by Pyinstaller
    # with the ``--noconsole`` option requires redirecting everything
    # (stdin, stdout, stderr) to avoid an OSError exception
    # "[Error 6] the handle is invalid."
    ret.update({'stdin': subprocess.PIPE,
                'stderr': subprocess.PIPE,
                'startupinfo': si,
                'env': env })
    return ret
def is_port_in_use(port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0