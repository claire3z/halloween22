import cv2
import time
import numpy as np
import matplotlib.pyplot as plt
import os

from playsound import playsound
import pyttsx3 #convert text to speech

def SpeakText(command,v=0):
    engine = pyttsx3.init()
    # set voices: 0= EN-US_DAVID; 1= EN-GB_HAZEL; 2= EN-US_ZIRA; 3= ZH-CN_HUIHUI
    voices = engine.getProperty('voices')
    engine.setProperty('voice',voices[v].id)
    engine.say(command)
    engine.runAndWait()

#SpeakText("Hello Children!",2)
greetings = ["Hello Children! You are being watched!",
             "Freeeeeze! Don't Move!",
             "Hi, Pumkin Pie!",
             "Trick or Treat?" ]

greetFiles = os.listdir('./greetings/')
soundFiles = os.listdir('./sound/')
#soundFiles = ['Dracula.mp3','Scream.mp3','Scream1.mp3','Werewolf.mp3','Whisper.mp3']
# n = len(soundFiles)
# file = './sound/'+soundFiles[np.random.choice(n)]
# playsound(file)

def enconter():
    count = 0

    SpeakText("Video surveillance is in opearation. This area is being watched!")
    greet = True

    while cam.isOpened():
        ret, frame1 = cam.read()
        ret, frame2 = cam.read()

        # record video
        #out.write(frame2)

        diff_ = cv2.absdiff(frame1, frame2) # (480, 640, 3)
        diff = cv2.cvtColor(diff_, cv2.COLOR_RGB2GRAY) # (480, 640, 1)
        diff = cv2.resize(diff, (x,y))

        # frame = cv2.rotate(frame2, cv2.ROTATE_90_CLOCKWISE)
        frame = cv2.rotate(diff_, cv2.ROTATE_90_CLOCKWISE)
        cv2.imshow('Droidcam', frame)

        if (diff>gray_threshold).sum() > pct_threshold*x*y:
            count+=1

            # record/output plots
            # fig, ax = plt.subplots(1, 2)
            # ax[0].imshow(diff_)
            # ax[0].set_title("original diff")
            # ax[1].imshow(diff, cmap='gray')
            # ax[1].set_title("resized diff")

            # play sound
            if greet: # greet message only once
                # SpeakText(greetings[np.random.choice(len(greetings))], np.random.choice(len(greetings)))
                playsound('./greetings/' + greetFiles[np.random.choice(len(greetFiles))])
                greet = False
                start = time.time() # start timer
            else:
                playsound('./sound/' + soundFiles[np.random.choice(len(soundFiles))])
#            print('time=',round(time.time()-start,2))

        if not greet: # this ensure start timer is set
            if time.time() - start > time_threshold:
                # This should only happen after encounter is triggered
                # SpeakText("Now say your password. Pumpkin Wishes and Candy Corn Kisses!",1)
                #SpeakText("Happy Halloween! Boo!",1)
                playsound('./enter/To enter the gate you must say your password_.mp3')
                time.sleep(1)
                # SpeakText("Hmmm, louder, louder, please! Pumpkin Wishes and Candy Corn Kisses!",1)
                playsound('./enter/Hmm_Louder louder please_Pumpkin wishes and candy corn kisses.mp3')
                time.sleep(1)
                # SpeakText("OK! Now you may enter the gate!",1)
                playsound('./enter/Heh heh heh_Now you may enter the gate.mp3')
                playsound('./sound/happy-halloween-cute-voices-97839.mp3')
                break

        if cv2.waitKey(10) == ord('a'):
            break

    cv2.destroyAllWindows()
    print('\t ... triggered {} times'.format(count))


def run():
    t = 1
    try:
        while True:
            print('round', t)
            try:
                #TODO - Change this to ip cam video
                cam = cv2.VideoCapture('https://xxx.xxx.xx.xxx:xxxx/video')  # Droid cam Note 5
                cam.setExceptionMode(True)
                ret, frame = cam.read()
                print('camera connected:', ret)

            except Exception:
                print('try again')
                continue

            enconter()
            cam.release()
            time.sleep(200)
            t+=1
            if t > 10:
                # cam.release()
                # out.release()
                return
    except KeyboardInterrupt:
        # cam.release()
        print('program stopped')
        return

x,y = 120,160 # resize from (480, 640, 3)
gray_threshold = 75
pct_threshold = 0.0010
time_threshold = 30 #second

#cam.release()
#cam = cv2.VideoCapture('output_daylight.mp4')
#cam = cv2.VideoCapture('https://xxx.xxx.xx.xxx:xxxx/video')  # Droid cam Note 5
#ret, frame = cam.read()
#plt.imshow(frame)
#plt.show()

# record video
# frame_width = int(cam.get(3))
# frame_height = int(cam.get(4))
# fps = int(cam.get(cv2.CAP_PROP_FPS))
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('output_night.mp4', fourcc, fps, (frame_width, frame_height))
# out.release()

#time.sleep(20)
run()


### Manual sequence - Robotic voice
# 1. Greetings
SpeakText(greetings[np.random.choice(len(greetings))], np.random.choice(len(greetings)))

# 2. Spooky sounds
playsound('./sound/' + soundFiles[np.random.choice(len(soundFiles))])

# 3. Enter sequence
SpeakText("Now say your password. Pumpkin Wishes and Candy Corn Kisses!", 1)

SpeakText("Hmmm, louder, louder, please! Pumpkin Wishes and Candy Corn Kisses!", 1)

SpeakText("OK! Now you may enter the gate!", 1)

playsound('./sound/happy-halloween-cute-voices-97839.mp3')


### Manual sequence - Human voice

# 1. Greetings
playsound('./greetings/' + greetFiles[np.random.choice(len(greetFiles))])

# 2. Spooky sounds
playsound('./sound/' + soundFiles[np.random.choice(len(soundFiles))])

# 3. Enter sequence
playsound('./enter/To enter the gate you must say your password_.mp3')

playsound('./enter/Hmm_Louder louder please_Pumpkin wishes and candy corn kisses.mp3')

playsound('./enter/Heh heh heh_Now you may enter the gate.mp3')

playsound('./sound/happy-halloween-cute-voices-97839.mp3')


# TODO:
# gather data to determine optimal threshold level [DONE]
# download more voice clips [DONE]
# say greeting only once. Have a flag and turn off for subsequent movements. [DONE]
# might need to fine-tune the threshold parameters on the day depending on weather / lighting. [DONE]