from tkinter import *
from tkinter.font import Font
from PIL import Image,ImageTk
import random
import platform
import os

def login():
    os.system('python keygen.py')
    quit()


ordi_name = platform.uname().node

root = Tk()
root.title('KEYGEN')
root.geometry('720x360+320+200')
logo = Canvas(root,width=720,height=180,bg='#00695c')
logo.place(relx=0,rely=0, anchor='w')
font = Font(family='Liberation Serif', size=16)
logo.create_text(340,160,text='LOGiN',fill='white',justify=CENTER,font=font,anchor='center')
image1 = Image.open("key.png")
photo1 = ImageTk.PhotoImage(image1)
#logo.create_image(0, 93, image=photo1, anchor='nw')


psw_cv = Canvas(root,width=100,height=30,bg='#00695c')
psw_cv.place(relx=0.180,rely=.45, anchor='w')
psw_cv.create_text(45,15,text='Password *',fill='white',justify=CENTER,font=Font(family='Liberation Serif', size=10),anchor='center')
psw = Entry(root,bd=0,insertwidth=2,width=38,font=Font(family='Liberation Serif', size=12),textvariable=StringVar(root,value=''),takefocus=0)
psw.place(relx=0.33,rely=.45, anchor='w')
cv1 = Canvas(root,width=340,height=2,bg='#00695c')
cv1.place(relx=0.327,rely=0.49, anchor='w')

"""pass_cv = Canvas(root,width=100,height=30,bg='#00695c')
pass_cv.place(relx=0.180,rely=0.58, anchor='w')
pass_cv.create_text(45,15,text='Password',fill='white',justify=CENTER,font=Font(family='Liberation Serif', size=10),anchor='center')
psw = StringVar(root,value='Exemple')
password = Label(root,textvariable = psw, fg='#00695c',font=Font(family='Liberation Serif', size=10),anchor='center')
password.place(relx=0.36,rely=.58, anchor='w')
cv2 = Canvas(root,width=340,height=2,bg='#00695c')
cv2.place(relx=0.33,rely=0.62, anchor='w')"""


loged = Button(root,text='Login', bg='#00695c', fg='#fff',activebackground="#00695c",activeforeground ="#fff",command=login,anchor='center',font=Font(family='Liberation Serif', size=14),justify='center')
loged.place(relx=0.42,rely=0.75, anchor='w')

root.mainloop()
