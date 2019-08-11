from flask import *
import os, sys
import webbrowser
from decrypt_functions import *
from flask import request, jsonify
import subprocess


if getattr(sys,'frozen', False):
    template_folder = os.path.join(sys._MEIPASS,'templates')
    static_folder = os.path.join(sys._MEIPASS,'static')
    app = Flask(__name__, template_folder = template_folder, static_folder = static_folder)
else:
    app = Flask(__name__)
app.config['SECRET_KEY'] = 'gafy'

# Get unique System UUID 
command = (resource_path('dmidecode.exe') + ' -s system-uuid').split()
cpuID = subprocess.check_output(command , **subprocess_args(False)).decode('utf-8')


@app.route('/')
def home():
    # Get current drive
    current_drive = os.getcwd().split('\\')[0]

    # List all drives
    dl = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    drives=['%s:' % d for d in dl if os.path.exists('%s:' % d)]

    crypted_files = isCryptedFileGetData(current_drive)
    
    print("here")
    return render_template('index.html',
                    cpuID=cpuID,
                    drives=drives,
                    current_drive=current_drive,
                    crypted_files_length = len(crypted_files)
                    )



@app.route('/changeSelectedDrive', methods=['POST'])
def handleChangeSelectedDrive():
    data = request.get_json()
    selected_drive = data['drive']

    crypted_files = isCryptedFileGetData(selected_drive)

    return jsonify({
        "crypted_files_length" : len(crypted_files)
    })




@app.route('/decrypt', methods=['POST'])
def handle_decrypt():

    # Reception des données postées
    data = request.get_json()
    drive = data['drive']
    key = data['key']

    print(data)
	# Load salt and hash the unique UUID
    salt = load_object(resource_path("salt"))
    keyToCrypt = hashStr(cpuID, salt)
    # print(keyToCrypt)
    # Check if key is equals to keyToCrypt

    # Get stored cpuID in "isCrypted"
    storedCpuID = getStoredCpuID(drive)
    if storedCpuID and storedCpuID !=cpuID:
        return jsonify({
            "error": True,
            "type" : "HOST_INVALID"
        })

    elif key == keyToCrypt:
        files = isCryptedFileGetData(drive)
        if not files:
            files = getListOfFiles(drive + "\\")
        
        # Decrypt files in isCrypted file or in all files in drive
        for file in files:
            print(file)
            decryptedOutput = toDecrypt(file, key)

            # Remove crypted file is decrytion is success
            if  decryptedOutput[1]:
                os.remove(file)
                os.rename(decryptedOutput[0], file)

            # Don't change anything if decryption is failed
            else:
                os.remove(decryptedOutput[0])
            
            # Delete decrypted file in isCrypted file
            if getIsCryptedFile(drive):
                deleteFileInIsCrypted(getIsCryptedFile(drive), file)
            
        # Delete "isCrypted" file
        os.remove(getIsCryptedFile(drive))
        return jsonify({
            "error": False
        })
            
    else:
        return jsonify({
            "error": True,
            "type" : "KEY_INVALID"
        })


if __name__ == '__main__':
    port = 42687
    webbrowser.open('http://127.0.0.1:'+str(port), new=1)
    if not is_port_in_use(port):
        app.run(debug=False, threaded=True, port=port)
    