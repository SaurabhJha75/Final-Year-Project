#importing modules for python Image Steganography project
from tkinter import *
from tkinter.filedialog import *
from PIL import ImageTk,Image
from stegano import exifHeader as stg
from tkinter import messagebox
import cv2
import numpy as np
from PIL import Image

#it convert data in binary formate


def data2binary(data):
    if type(data) == str:
        p = ''.join([format(ord(i), '08b')for i in data])
    elif type(data) == bytes or type(data) == np.ndarray:
        p = [format(i, '08b')for i in data]
    return p


# hide data in given img

def hidedata(img, data):
    data += "$$"                                   #'$$'--> secrete key
    d_index = 0
    b_data = data2binary(data)
    len_data = len(b_data)

 #iterate pixels from image and update pixel values

    for value in img:
        for pix in value:
            r, g, b = data2binary(pix)
            if d_index < len_data:
                pix[0] = int(r[:-1] + b_data[d_index])
                d_index += 1
            if d_index < len_data:
                pix[1] = int(g[:-1] + b_data[d_index])
                d_index += 1
            if d_index < len_data:
                pix[2] = int(b[:-1] + b_data[d_index])
                d_index += 1
            if d_index >= len_data:
                break
    return img

# decoding

def find_data(img):
    bin_data = ""
    for value in img:
        for pix in value:
            r, g, b = data2binary(pix)
            bin_data += r[-1]
            bin_data += g[-1]
            bin_data += b[-1]

    all_bytes = [bin_data[i: i + 8] for i in range(0, len(bin_data), 8)]

    readable_data = ""
    for x in all_bytes:
        readable_data += chr(int(x, 2))
        if readable_data[-2:] == "$$":
            break
    return readable_data[:-2]


def decode():
    img_name = input("\nEnter Image name : ")
    image = cv2.imread(img_name)
    img=Image.open(img_name,'r')
    msg = find_data(image)
    return msg




# decoding the file for python Image Steganography project
def Decode():
    Screen.destroy()
    DecScreen = Tk()
    DecScreen.title("Decoding Screen")
    DecScreen.geometry("500x500+300+300")
    DecScreen.config(bg="pink")
    def OpenFile():
        global FileOpen
        FileOpen=StringVar()
        FileOpen = askopenfilename(initialdir="/Desktop",title="Select the File",filetypes=(("only png files","*png"),("all type of files","*.*")))
        
    def Decoder():
        image = cv2.imread(FileOpen)
        img=Image.open(FileOpen,'r')
        msg = find_data(image)

        label3 = Label(text=msg)
        label3.place(relx=0.3,rely=0.3)
        
    SelectButton = Button(text="Select the file",command=OpenFile)
    SelectButton.place(relx=0.1,rely=0.4)
    EncodeButton=Button(text="Decode",command=Decoder)
    EncodeButton.place(relx=0.4,rely=0.5)

def Encode():
    Screen.destroy()
    EncScreen = Tk()
    EncScreen.title("Encoding Screeen")
    EncScreen.geometry("500x500+300+300")
    EncScreen.config(bg="yellow")
    label = Label(text="Confidential Message")
    label.place(relx=0.1,rely=0.2)
    entry=Entry()
    entry.place(relx=0.5,rely=0.2)
    label1 = Label(text="Name of the File")
    label1.place(relx=0.1,rely=0.3)
    SaveEntry = Entry()
    SaveEntry.place(relx=0.5,rely=0.3)
 
    def OpenFile():
        global FileOpen
        FileOpen=StringVar()
        FileOpen = askopenfilename(initialdir = "/Desktop" , title = "SelectFile",filetypes=(("jpeg files","*jpg"),("all files","*.*")))
 
        label2 = Label(text=FileOpen)
        label2.place(relx=0.3,rely=0.3)
 
    def Encoder():
        Response= messagebox.askyesno("PopUp","Do you want to encode the image")
        if Response == 1:
            image = cv2.imread(FileOpen)
            img = Image.open(FileOpen, 'r')
            w, h = img.size
            data = entry.get()
            if len(data) == 0:
                raise ValueError("Empty data")
            enc_img = SaveEntry.get()+".png"
            enc_data = hidedata(image, data)
            cv2.imwrite(enc_img, enc_data)
            img1 = Image.open(enc_img, 'r')
            img1 = img1.resize((w, h),Image.ANTIALIAS)
            # optimize with 65% quality
            if w != h:
                img1.save(enc_img, optimize=True, quality=65)
            else:
                img1.save(enc_img)

            messagebox.showinfo("Pop Up","Successfully Encoded the image")
        else:
            messagebox.showwarning("Pop Up","Unsuccessful,please try again")
 
    SelectButton = Button(text="Select the file",command=OpenFile)
    SelectButton.place(relx=0.1,rely=0.4)
    EncodeButton=Button(text="Encode",command=Encoder)
    EncodeButton.place(relx=0.4,rely=0.5)

#Initializing the screen for python Image Steganography project
Screen = Tk()
Screen.title("Image Steganography Project 2022")
Screen.geometry("500x500+300+300")
Screen.config(bg= "blue")
#creating buttons
EncodeButton = Button(text="Encode",command=Encode)
EncodeButton.place(relx=0.3,rely=0.4)
 
DecodeButton = Button(text="Decode",command=Decode)
DecodeButton.place(relx=0.6,rely=0.4)



mainloop()
