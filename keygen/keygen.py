from tkinter import *
from tkinter.font import Font
from PIL import Image,ImageTk
from tkinter import messagebox
import random
import bcrypt
import pickle
import platform
from os import path
import subprocess
# import datetime
import os

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return path.join(sys._MEIPASS, relative_path)
    return path.join(path.abspath("."), relative_path)

def load_object(object_name):
    with open(object_name, "rb") as file:
        my_depickler = pickle.Unpickler(file)
        data = my_depickler.load()
    return data

def hashStr(stringToHash, key):
    return bcrypt.hashpw(stringToHash.encode("utf-8"),key).decode("utf-8")[29:]

def generate():
    global psw
    salt = load_object(resource_path("salt"))
    input_id = _id.get()
    # # mounthAndYear = datetime.datetime.now().strftime('%b%G')
    generatedSerial = hashStr(input_id, salt)
    psw.set(generatedSerial)
    # messagebox.showinfo("DATE", )
    print(generatedSerial)

def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

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


command = (resource_path('dmidecode.exe')+' -s system-uuid').split()
uniqueID = subprocess.check_output(command , **subprocess_args(False)).decode('utf-8')

print(uniqueID)
root = Tk()
root.title('KEYGEN')
root.minsize(500, 250)
root.maxsize(500, 250)
center(root)
root.iconbitmap(resource_path('keygen.ico'))
logo = Canvas(root,width=720,height=180,bg='#000000    ')
logo.place(relx=0,rely=0, anchor='w')
font = Font(family='Liberation Serif', size=16)
logo.create_text(330,160,text='KEYGEN',fill='white',justify=CENTER,font=font,anchor='center')
image1 = Image.open(resource_path("key.png"))
photo1 = ImageTk.PhotoImage(image1)
# image2 = Image.open(resource_path("innovadrone.png"))
# photo2 = ImageTk.PhotoImage(image2)
logo.create_image(10, 93, image=photo1, anchor='nw')


_id_cv = Canvas(root,width=75,height=30,bg='#000000   ')
_id_cv.place(relx=0.07,rely=.50, anchor='w')
_id_cv.create_text(40,15,text='CPUID',fill='white',justify=CENTER,font=Font(family='Liberation Serif', size=10),anchor='center')
_id = Entry(root,bd=0,insertwidth=2,width=37,font=Font(family='Liberation Serif', size=12),textvariable=StringVar(root,value=uniqueID),takefocus=0)
_id.place(relx=0.237,rely=.50, anchor='w')


cv1 = Canvas(root,width=336,height=2,bg='#000000   ')
cv1.place(relx=0.229,rely=0.555, anchor='w')

serial_cv = Canvas(root,width=75,height=30,bg='#000000  ')
serial_cv.place(relx=0.07,rely=0.68, anchor='w')
serial_cv.create_text(40,15,text='Decrypt Key',fill='white',justify=CENTER,font=Font(family='Liberation Serif', size=10),anchor='center')
psw = StringVar(root,value='Copy this Decrypt Key')
serial =  Entry(root,bd=0,insertwidth=2,width=37,fg='#000000 ',state='readonly',font=Font(family='Liberation Serif', size=12),takefocus=0)
serial.config(textvariable = psw, relief='flat')
serial.place(relx=0.237,rely=.68, anchor='w')

cv2 = Canvas(root,width=336,height=2,bg='#000000   ')
cv2.place(relx=0.229,rely=0.73, anchor='w')


generate = Button(root,text='Generate', bg='#000000', fg='#fff',activebackground="#000000 ",activeforeground ="#fff",command=generate,anchor='center',font=Font(family='Liberation Serif', size=14),justify='center')
generate.place(relx=0.37,rely=0.87, anchor='w')

cv3 = Canvas(root,width=170,height=40)
cv3.place(relx=0.565,rely=0.85, anchor='w')
# cv3.create_image(90, 30, image=photo2, anchor='c')


root.mainloop()
