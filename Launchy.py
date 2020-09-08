#7/29 added namelist and dirlst
#can launch stuff based on the name and dir text files
#8/5 non case sensitive, single file instead of name and dir text files
#8/10 can launch web pages and directory
#opening directories still doesnt work
#8/22 sorted listnames and multiple shortcuts with the same name now works

import subprocess
import webbrowser
import os
import sys

runProg = 1
print ("************************")
print ("Launchy")
print ()
print ("Enter shortcut name, or comlist for list of commands")
print ("************************")

usemode = 0;


# program loop

while runProg == 1:
    if usemode == 1:
        print ("Enter shortcut name, or comlist for list of commands")
    usemode = 0;
    print (">>")
    
    launchyInput = input ()
    
    if launchyInput == "quit":
        runProg = 0
        break

# listing available shortcut names

    elif launchyInput == "listnames":
        nmdrList = open('LaunchyDir.txt', 'r')
        scnameList = []
        for line in nmdrList:
            curLine = line.split (';;')
            curLineName = curLine[0]
            scnameList.append (curLineName)
            continue
        scnameList.sort()
        for scnameElem in scnameList:
            print (scnameElem)
        
# open launchy dir doesnt work
    elif launchyInput == "launchydir":
        openingDir = "explorer ."
        webbrowser.open(openingDir)
        print ("Openinig Launchy Directory")

# list OS type
    elif launchyInput == "whatOS":
        thisOS = sys.platform
        print (thisOS)

# command list
    elif launchyInput == "comlist":
        print ("comlist")
        print ("-Lists this list of commands")

        print ()
        print ("addsc")
        print ("-Add a new shortcut")

        print ("listnames")
        print ("-Lists all available shortcut names")

        print ("usemode")
        print ("-Returns usemode")

# adding shortcuts
    elif launchyInput == "addsc":
        usemode = 1;
        while usemode == 1:
            print ("Enter new shortcut name, or quit to cancel: ")
            newscName = input ()
            if newscName == "quit":
                break
            
            nmdrList = open('LaunchyDir.txt', 'r')
            for line in nmdrList:
                curLine = line.split (';;')
                curLineName = curLine [0]
                curLineLow = curLineName.lower()
                newscNameLow = newscName.lower()
                
                if (curLineLow == newscNameLow):
                        print ("Shortcut with same name exits")
                        break

            if not(curLineLow == newscNameLow):            
                print ("Enter shortcut type [1, 2, 3]:")
                scTypeDesc = ["--","File Shortcut","Web Shortcut","Directory Shortcut"]
                print ("1 - File shortcut (.exe, .png, etc)")
                print ("2 - Web shortcut (URL)")
                print ("3 - Directory shortcut (Opens file manager)")
                newscType = int (input ())
                
                if not((newscType > 3) or (newscType == 0)):
                    if newscType == 1:
                        print ("Enter file directory")
                        newscDir = input()                            
                    if newscType == 2:
                        print ("Enter URL")
                        newscDir = input()                            
                    if newscType == 3:
                        print ("Enter folder directory")
                        newscDir = input()

                nmdrList.close()
                print ()
                print ("Add this shortcut [y, n]?")
                print (newscName)
                print (newscDir)
                print (scTypeDesc[newscType])                        
                yesno = input()
                    
                if yesno == "y":
                    with open('LaunchyDir.txt','a') as nmdrList:
                        nmdrList.write("\n")
                        scTypeTag = ["--","sc","web","dir"]
                    
                        newscEntry = (newscName + ";;" + newscDir + ";;" + scTypeTag[newscType] + ";;")
                        nmdrList.write (newscEntry)
                    
                        print ("Added shortcut")
                        break
                if yesno == "n":
                    print ("Cancelled")
                    break
                    
                

# loading stuff

    elif (launchyInput != ""):
        with open('LaunchyDir.txt', 'r') as nmdrList:
            inputResult = []
            for line in nmdrList:
                # reading each lines, loop
                curLine = line.split (';;')
                curLineName = curLine[0]
                curLineDir = curLine[1]
                whatsCurLine = curLine[2] # sc for shortcut, web for webpages, dir for directories

                inputLow = launchyInput.lower()
                curLineLow = curLineName.lower()                
                if (curLineLow.startswith(inputLow) == True):                  
                    inputResult.append (curLineName)
                    continue
                
            ## input and search done, display results or open shortcut
            inputResult.sort()

            ## open shortcut when theres only 1 matching result
            if (len(inputResult) == 1):
                with open('LaunchyDir.txt', 'r') as nmdrList:
                    for line in nmdrList:
                        curLine = line.split (';;')
                        curLineName = curLine[0]
                        curLineDir = curLine[1]
                        whatsCurLine = curLine[2]
                        if (inputResult[0] == curLineName):
                            if (whatsCurLine == "sc"):
                                print ("Launching "+curLineName)
                                print (curLineDir)
                                
                                #check if linux or windows
                                if (sys.platform == 'win32'):
                                    subprocess.Popen ([curLineDir], shell = True)
                                    break
                                if (sys.platform == 'linux'):
                                    openscLine = "xdg-open "+ (curLineDir)
                                    print (openscLine)
                                    os.system (openscLine)
                                    break
                                break
                            if (whatsCurLine == "web"):
                                print ("Accessing "+curLineName)
                                print (curLineDir)
                                webbrowser.open(curLineDir)
                                break
                            if (whatsCurLine == "dir"):
                                print ("Opening " + curLineName)
                                print (curLineDir)
                                if (sys.platform == 'win32'):
                                    openingDir = "explorer "+curLineDir
                                    os.startfile(curLineDir)
                                    break
                                if (sys.platform == 'linux'):
                                    opendirLine = "xdg-open "+(curLineDir)
                                    print (opendirLine)
                                    os.system (opendirLine)
                                    break
                                break

            ## open shortcut when theres multiple result
            elif (len(inputResult) > 1):
                print ("Found multiple shortcuts, launch which one?")
                resultCounter = 1
                ## show results of search
                for inputElem in inputResult:
                    multipleResultStr = str(resultCounter) + " - " + str(inputElem)
                    print (multipleResultStr)
                    resultCounter = resultCounter + 1
                    
                ## take input to launch shortcut
                multiResInput = int (input())
                multiResInput = multiResInput - 1
                with open('LaunchyDir.txt', 'r') as nmdrList:
                    for line in nmdrList:
                        curLine = line.split (';;')
                        curLineName = curLine[0]
                        curLineDir = curLine[1]
                        whatsCurLine = curLine[2]
                        if (inputResult[multiResInput] == curLineName):
                            if (whatsCurLine == "sc"):
                                print ("Launching "+curLineName)
                                print (curLineDir)
                                subprocess.Popen ([curLineDir], shell = True)
                                break
                            if (whatsCurLine == "web"):
                                print ("Accessing "+curLineName)
                                print (curLineDir)
                                webbrowser.open(curLineDir)
                                break
                            if (whatsCurLine == "dir"):
                                print ("Opening " + curLineName)
                                print (curLineDir)
                                openingDir = "explorer "+curLineDir
                                os.startfile(curLineDir)
                                break
            else:
                print ("Invalid input 2")                
                    
    else:
        print ("Invalid Input 1")
