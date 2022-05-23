

from tkinter import messagebox
from tkinter import*
from PIL import Image, ImageTk
import cv2
from tkinter import filedialog
import mediapipe as mp
import pyttsx3
import time


win = Tk()
width=win.winfo_screenwidth()
height=win.winfo_screenheight()
global img, finalImage,finger_tips,thumb_tip,cap,mylabel1, image, rgb, hand, results, _, w, h,status,mpDraw,mpHands,hands,label1,frame_1,btn,btn2
win.geometry("%dx%d" % (width, height))
frame_1 = Frame(win, width=width, height=height, bg="#232224").place(x=0, y=0)
win.iconbitmap('icon.ico')
win.title('Sign Language Converter')
mylabel1= Label(win,text='Sign Language Converter',font=('Helvetica',24,'bold'),bd=5,bg='gray',fg='#232224',relief=GROOVE,width=5000 ).pack(pady=15,padx=300)


##########################################DROP DOWN##########################################################
def about():
    messagebox.showinfo('The Developers', 'Project Developed by:\nMuhammad Zain Syed (2020-MC-23)\nNimra Areeb (2020-MC-33)')

menubar = Menu(win, background='#ff8000', foreground='black', activebackground='white', activeforeground='black')  
win.config(menu=menubar)
file = Menu(menubar, tearoff=1, background='#ffcc99', foreground='black')  
file.add_command(label="New")      
file.add_separator()  
file.add_command(label="Exit", command=win.quit)  
menubar.add_cascade(label="File", menu=file)  
edit = Menu(menubar, tearoff=0)  
edit.add_command(label="Undo")  
edit.add_separator()     
menubar.add_cascade(label="Edit", menu=edit)  
help = Menu(menubar, tearoff=0)  
help.add_command(label="About", command=about)  
menubar.add_cascade(label="Help", menu=help)     

###############################CLOCK##########################################################

tlabel=Label(win,font=('Helvetica',24,'bold'),pady=15,bd=10,relief=GROOVE,fg='#232224',bg='gray')
tlabel.place(x=1285,y=100)
def clock():
    hour=time.strftime("%H")
    minute = time.strftime('%M')
    second = time.strftime("%S")
    am_pm = time.strftime("%p")
    tlabel.config(text=hour + ":" + minute + ":" + second + " " + am_pm)
    tlabel.after(1000,clock)
def update():
    tlabel.config(text="New Text")

###############################################################################################


#####################################Initiate###################################################
def wine():
    global finger_tips,thumb_tip,mpDraw,mpHands,cap,w,h,hands,label1,label1,frame_1,check,img
   

    finger_tips = [8, 12, 16, 20]
    thumb_tip = 4
    w = 500
    h = 400
    label1 = Label(win, width=w, height=h,bg="#232224") #video on 
    label1.place(x=40, y=200)
#LIne drawn on hands
    mpHands = mp.solutions.mediapipe.python.solutions.hands  # From different
    hands = mpHands.Hands()  # The hands object from Hands Solution
    mpDraw = mp.solutions.mediapipe.python.solutions.drawing_utils
    cap = cv2.VideoCapture(0)
    
   


###########################################Detection##########################################
def live():
    global v
    global upCount
    global cshow,img
    cshow=0
    upCount = StringVar()#tkinter defined variable , efficiently 
    # global img, finalImage,engine, image, rgb, hand, results, _, w, h,upCount,status,mpDraw,mpHands,hands,label1
    _, img = cap.read()
    
    img = cv2.resize(img, (w, h))
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks: 
            lm_list = []
            for id, lm in enumerate(hand.landmark):
                lm_list.append(lm)
            finger_fold_status = []

            for tip in finger_tips:
                x, y = int(lm_list[tip].x * w), int(lm_list[tip].y * h)  
                if lm_list[tip].x < lm_list[tip - 2].x:   
                    finger_fold_status.append(True)
                else:
                    finger_fold_status.append(False)
            
            print(finger_fold_status)
            x, y = int(lm_list[8].x * w), int(lm_list[8].y * h)
            print(x, y)
            # stop
            if lm_list[4].y < lm_list[2].y and lm_list[8].y < lm_list[6].y and lm_list[12].y < lm_list[10].y and \
                    lm_list[16].y < lm_list[14].y and lm_list[20].y < lm_list[18].y and lm_list[17].x < lm_list[0].x < \
                    lm_list[5].x:
                cshow = 'STOP ! Dont move.'
                upCount.set('STOP ! Dont move.')
                print('STOP ! Dont move.')
            # okay
            elif lm_list[4].y < lm_list[2].y and lm_list[8].y > lm_list[6].y and lm_list[12].y < lm_list[10].y and \
                    lm_list[16].y < lm_list[14].y and lm_list[20].y < lm_list[18].y and lm_list[17].x < lm_list[0].x < \
                    lm_list[5].x:
                cshow = 'Perfect , You did  a great job.'
                print('Perfect , You did  a great job.')
                upCount.set('Perfect , You did  a great job.')
               
            # spidey
            elif lm_list[4].y < lm_list[2].y and lm_list[8].y < lm_list[6].y and lm_list[12].y > lm_list[10].y and \
                    lm_list[16].y > lm_list[14].y and lm_list[20].y < lm_list[18].y and lm_list[17].x < lm_list[0].x < \
                    lm_list[5].x:
                cshow = 'Good to see you.'
                print(' Good to see you. ')
                upCount.set('Good to see you.')
                
            # Point
            elif lm_list[8].y < lm_list[6].y and lm_list[12].y > lm_list[10].y and \
                    lm_list[16].y > lm_list[14].y and lm_list[20].y > lm_list[18].y:
                upCount.set('You Come here.')
                print("You Come here.")
                cshow = 'You Come here.'
            # Victory
            elif lm_list[8].y < lm_list[6].y and lm_list[12].y < lm_list[10].y and \
                    lm_list[16].y > lm_list[14].y and lm_list[20].y > lm_list[18].y:
                upCount.set('Yes , we won.')
                print("Yes , we won.")
                cshow = 'Yes , we won.'
            # Left
            elif lm_list[4].y < lm_list[2].y and lm_list[8].x < lm_list[6].x and lm_list[12].x > lm_list[10].x and \
                    lm_list[16].x > lm_list[14].x and lm_list[20].x > lm_list[18].x and lm_list[5].x < lm_list[0].x:
                upCount.set('Move Left')
                print(" MOVE LEFT")
                cshow = 'Move Left'
            # Right
            elif lm_list[4].y < lm_list[2].y and lm_list[8].x > lm_list[6].x and lm_list[12].x < lm_list[10].x and \
                    lm_list[16].x < lm_list[14].x and lm_list[20].x < lm_list[18].x:
                upCount.set('Move Right')
                print("Move RIGHT")
                cshow = 'Move Right'
            if all(finger_fold_status):
                # like
                if lm_list[thumb_tip].y < lm_list[thumb_tip - 1].y < lm_list[thumb_tip - 2].y and lm_list[0].x < lm_list[3].y:
                    print("I like it")
                    upCount.set('I Like it')
                    cshow = 'I Like it'
                # Dislike
                elif lm_list[thumb_tip].y > lm_list[thumb_tip - 1].y > lm_list[thumb_tip - 2].y and lm_list[0].x < lm_list[3].y:
                    upCount.set('I dont like it.')
                    print(" I dont like it.")
                    cshow = 'I dont like it.'

            mpDraw.draw_landmarks(rgb, hand, mpHands.HAND_CONNECTIONS)
        cv2.putText(rgb, f'{cshow}', (10, 50),
                cv2.FONT_HERSHEY_COMPLEX, .75, (0, 255, 255), 2)

    image = Image.fromarray(rgb)
    finalImage = ImageTk.PhotoImage(image)
    label1.configure(image=finalImage)
    label1.image = finalImage
    win.after(1, live)
    crr=Label(win,text='Current Status :',font=('Helvetica',18,'bold'),bd=5,bg='gray',width=15,fg='#232224',relief=GROOVE )
    status = Label(win,textvariable=upCount,font=('Helvetica',18,'bold'),bd=5,bg='gray',width=50,fg='#232224',relief=GROOVE )
  
    status.place(x=400,y=700)
    crr.place(x=120,y=700)
#################################################################################################

#####################################VOICE###############################################################################
def voice():
    
    engine = pyttsx3.init()
    engine.say((upCount.get()))
    engine.runAndWait()

##########################################################################################################################
def video():
    global cap,ex,label1
   
    filename =filedialog.askopenfilename(initialdir="/", title="Select file ",
                                               filetypes=(("mp4 files", ".mp4"), ("all files", ".")))
    cap = cv2.VideoCapture(filename)
    w = 500
    h = 400
    label1 = Label(win, width=w, height=h,relief=GROOVE)
    label1.place(x=40, y=200)
    live()
###############################################################################################

#############################################Destroy Functions ################################
def lbl():
    global label1
    label1.destroy()

def lbl2():
    global label1
    cv2.destroyAllWindows()
    label1.destroy()
    wine()
##################################################################################################
clock()
wine()

#################################################BUTTONS############################################################################################
btn2 = Button(win, text='Live',padx=95,bg='gray',fg='#232224',relief=GROOVE ,width=7,bd=5,font=('Helvetica',14,'bold'),command=live).place(x=1200,y=400)
btn = Button(win, text='Video',padx=95,bg='gray',fg='#232224',relief=GROOVE,width=7,bd=5,font=('Helvetica',14,'bold') ,command= video).place(x=1200,y=450)
ex=Button(win,text='Exit',padx=95,bg='gray',fg='#232224',relief=GROOVE,width=7,bd=5,font=('Helvetica',14,'bold') ,command=win.destroy).place(x=1200,y=600)
vc=Button(win,text='Sound',padx=95,bg='gray',fg='#232224',relief=GROOVE,width=7,bd=5,font=('Helvetica',14,'bold') ,command=voice).place(x=1200,y=500)
des=Button(win,text='Change Vid',padx=95,bg='gray',fg='#232224',relief=GROOVE ,width=7,bd=5,font=('Helvetica',14,'bold'),command=lbl).place(x=1200,y=550)
des=Button(win,text='Change Cam',width=7,bd=5,fg='#232224',font=('Helvetica',14,'bold'),padx=95,bg='gray',relief=GROOVE ,command=lbl2).place(x=1200,y=650)
win.mainloop()

