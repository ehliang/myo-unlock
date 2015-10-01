#This program takes simple input from the Mio to unlock a complex password string and log in to email
#Further developement would allow it to log into social media accounts/computerss
#A program by Ethan Liang

from __future__ import print_function

import myo as libmyo; libmyo.init()
import time
import sys
import smtplib
import getpass
import email.header
import re
import datetime
import json
import email
import requests



gesturesGiven = []
userInput = []
userPassword = []
originalUsernameString = ""
originalPasswordString = ""
activated = False
useringesture = ""
userpasscheck = ""
counter = 1 



class Listener(libmyo.DeviceListener):
    """
    Listener implementation. Return False from any function to
    stop the Hub.
    """

    interval = 0.05  # Output only 0.05 seconds
    pose_run = False




    def on_connect(self, myo, timestamp):
            print("Hello, Myo!")

    def on_disconnect(self, myo, timestamp):
            print("Goodbye, Myo!")

#    def on_orientation_data(self, myo, timestamp, quat):
#           print("Orientation:", quat.x, quat.y, quat.z, quat.w)

    def passcheck(self):
        print("Enter the password. Please make a gesture. When finished with your combination, press 0, otherwise enter any character after each gesture.")

        userPassword.append(userpasscheck)
        print("Detected: " + str(userpasscheck))
        confirm3 = raw_input()
        if confirm3 == "3":
            activated = True
            if userpasscheck == userInput:
                print(userInput)
                fromaddr = originalUsernameString
                toaddrs = "ethanliang@live.com"
                msg = "Test"

                username = originalUsernameString   
                password = originalPasswordString

                server = smtplib.SMTP('smtp.gmail.com:587')
                server.starttls()
                server.login(username,password)
                server.sendmail(fromaddr, toaddrs, msg)
                server.quit() 
                activated=True

            else:
                print("Error")
                activated=True
        else:
            activated = False

    def record(self):
        global count, activated 
        count = 1
        print("Please make a gesture, this is the "+ str(count) + " character of the password. When finished with your combination, press 0, otherwise enter any character")
        activated = True
        userInput.append(useringesture)
        print("Detected: " + str(useringesture))

        confirm = raw_input()
        if confirm == "0":
           # activated = True
            print("Was your password string " + str(userInput) + "? If yes, enter 3. Otherwise, enter 4. ")
            confirm2 = int(raw_input())
            if confirm2 == 3:
                print("abc")
                activated = False
                self.passcheck()
                confirm = "p"

            elif confirm2 == 4:
                del userInput[:]
                activated = False  

        else:   
            activated = False

        
        # print("Was your gesture" + str(useringesture) + "? Please enter yes or no")
        # print("Was your gesture" + str(useringesture) + "? Please enter yes or no")
        # confirm = raw_input()
        # while confirm != "yes" and confirm != "no":
        #     print("Was your gesture" + str(useringesture) + "? Please enter yes or no")
        #     confirm = raw_input()    
        #     if confirm == "yes":
            
        #def keyPressHandler(event):
        #   if event.keysym == "0":
        #      activated = True


    def on_pose(self, myo, timestamp, pose):
        global useringesture, userpasscheck, confirm2
        if activated == False:
            if pose!= libmyo.Pose.rest and confirm2==3:
                userpasscheck = pose
                self.passcheck() 
            elif pose!= libmyo.Pose.rest:
                useringesture = pose
                self.record()   
            #count+=1

    


       #     if pose == libmyo.Pose.fist:
       #         print("Don't show me 'ya fist!")
       #         gesturesGiven.append(pose)
       #         print(gesturesGiven[0])
       #  #Stops the Hub
       #     if pose == libmyo.Pose.wave_out:
       #         print("abcd")
       #         gesturesGiven.append(pose)
       #         print(gesturesGiven)
       #         return False
       # if self.pose_run:
       #     return
       #     self.pose_run = True

            if userPassword == userInput:
                originalUsernameString = ""
                originalPasswordString = ""

                fromaddr = originalUsernameString
                toaddrs = ""
                msg = "Test"

                username = originalUsernameString
                password = originalPasswordString

                server = smtplib.SMTP('smtp.gmail.com:587')
                server.starttls()
                server.login(username,password)
                server.sendmail(fromaddr, toaddrs, msg)
                server.quit()
    

def main():
    print("Connecting to Myo ... Use CTRL^C to exit.")
    print("If nothing happens, make sure the Bluetooth adapter is plugged in,")
    print("Myo Connect is running and your Myo is put on.")
    hub = libmyo.Hub()
    hub.set_locking_policy(libmyo.LockingPolicy.none)
    hub.run(1, Listener())

    # Listen to keyboard interrupts and stop the hub in that case.
    try:
        while hub.running:
            time.sleep(0.25)
    except KeyboardInterrupt:
        print("\nQuitting ...")
    finally:
        print("Shutting down hub...")
        hub.shutdown()


if __name__ == '__main__':
    main()


