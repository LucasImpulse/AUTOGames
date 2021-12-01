import psutil; import os; import time; import cv2; import pygetwindow as gw; import win32gui; import win32.lib.win32con as win32con                 #All required modules.
import pyautogui; import numpy as np; from matplotlib import pyplot as plt; import pytesseract; from PIL import Image; from PIL import ImageGrab;   #All required modules.
import winsound; from PIL import ImageFilter

steamOpen = False                      # This is a global variable that helps the program know whether Steam is open.
steamMaybeInstalled = False            # This is when the program thinks that Steam is installed or not. The user may try again if it fails to find Steam the first time.
steamDownloadsOpen = False             # The download page open or not open, as a boolean.


def checkForSteam():
    global steamOpen                                                                    # We need this global variable.
    steamCheckSuccess = int(0)                                                          # The Steam checking success boolean.
    for proc in psutil.process_iter():                                                  # For each process:
        try:
            if str("steam.exe") in proc.name().lower():                                 # Check if process has the name of the one we want,
                steamCheckSuccess += 1                                                  # if it occurs twice, Steam is open.
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):       # If we get these errors:
            pass                                                                        # Ignore them.
    steamOpen = bool(steamCheckSuccess)                                                 # Finally, if Steam was closed, we should've got one handle
    if steamOpen == True:                                                               # of it and this would be False. If it was open,
        print("Yes, Steam's open.")                                                     # we should've gotten two and this'd be True.
        return True
    else:
        print('''Steam not located! Going to try to run it myself.
Please give it time. Valve has programmed their browser protocol horribly.''')  #Self-explanatory.
        time.sleep(15)
        return False
'''This checks every process until it finds Steam. When it does, it marks steamOpen as True, so the program knows what to do.'''

def goToDownloadsWhenOpen():                                        # ((The below is in a function. Append comments where ran.))
        global steamDownloadsOpen                                   # We need this global variable.
        print("Waiting for Steam Downloads to Open...")             # Self-explanatory.
        os.system('explorer "steam://open/downloads"')              # Run this command, it will send us to Downloads in Steam.
        print("Time's up!")                                         # Self-explanatory.
        steamDownloadsOpen = checkForSteam()                        # The download page is open!
        hwnd = win32gui.GetForegroundWindow()                       # Get the download page, which'll be foreground.
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)             # And maximise it.
        pass
        
'''This opens Steam Downloads page if Steam is open, then maximise it.'''

def openSteamIfNotOpen():
        os.system('explorer "steam://open/downloads"')              # This is still gonna run Steam if installed.
        goToDownloadsWhenOpen()                                     # Then it will go to Downloads page after 16 seconds (good job, Valve).
'''Open Steam if it's not open.'''

def steamOpenerUp():
    global steamOpen
    global steamDownloadsOpen

    while True:
        checkForSteam()
        if steamOpen == True:                               # If Steam is open,
            goToDownloadsWhenOpen()                         # Go to function.
        if steamOpen == False:                              # If Steam is not open,
            openSteamIfNotOpen()                            # Go to function.
        if steamDownloadsOpen == True:
            break
'''Steam should now be open and focused.'''

'''
There is an issue. I don't want it to wait when Steam is actually open, to foreground the app.
However, upon research, I found that really this is just a Valve issue.
'''

gamesAndSize = []
counter = int(0)
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
#print(pytesseract.get_tesseract_version())

def replace6BA(text):                                                            
    text = text.replace('6B', ' GB').replace('\'', '’')                         # Replace any 6B with GB, 68 with GB and any ' with ’.
    if text[-2:] == '68':
        text = text.replace('68', 'GB')
    text = text.replace('’‘', '’')
    text = text.replace('.GB','GB').replace('.MB','MB')
    return text                                                                 # Then give it back.

def gigabytesToMegabytes(text):                                                 
    if 'GB' in text and 'MB' in text:
        text = text.replace(' GB', '').replace('GB', '')
        text = text.replace(' MB', '').replace('MB', '') 
        text = solveWeirdRemainings(text)
        return text
    elif 'GB' in text and 'MB' not in text:                                     # If there's GBs read,
        text = text.replace(' GB', '').replace('GB', '')                        # remove GBs,
        text = solveRemainings(text)                                            # solve progressed downloads.
        text = (float(text) * 1000)                                             # convert to float, and times it by 1000 to standardise it to megabytes.
        return text                                                             # Then give it back.
    else:
        text = text.replace(' MB', '').replace('MB', '')                        # otherwise it's MBs, and remove it.
        text = solveRemainings(text)                                            # solve progressed downloads.
        text = float(text)                                                      # convert to float.
        return text                                                             # Then give it back.

def solveRemainings(text):                                                      # This converts any download size that says X/Y where X is downloaded and Y is total download.
    if '/' in text:                                                             # If there is a '/':
        text = text.split('/')                                                      # Split the two numbers.
        text = float(text[1]) - float(text[0])                                      # Take away total downloaded from total to download, to get remaining download.
        return text                                                                 # Then give it back.
    else:
        return text

def solveWeirdRemainings(text):
    text = text.split('/')
    text = float(float(text[1])*1000) - float(text[0])
    return text

def dSB(text):                                                                  # Which stands for downloadSizeBonanza, does all the above 3 functions.
    if not text:                                                                # Safeguard for null list.
        return text
    else:
        text = gigabytesToMegabytes(text)                                       # Standardise to megabytes in float values,
        return text                                                             # then give it back.

def splitLines(text, line=0):                                                   # Splits line strings into list of strings.
    text = text.split('\n')
    try:
        return text[line]
    except:
        print(text)
        return text[0]

cachedCoordsOfDButtons = []

def steamDownloadReader():
    global cachedCoordsOfDButtons
    cachedCoordsOfDButtons = []
    width, height = pyautogui.size()                                            # Get screen resolution.
    screenshot = pyautogui.screenshot(region=(0,0,width,height))                # Take a screenshot of the bit we want.
    screenshot.save("screen.png")                                               # Save it (for debugging purposes, can be removed).
    img = cv2.imread("screen.png")                                              # OpenCV reads the screenshot into a variable.
    img_gray = img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                 # OpenCV greys the screenshot.
    template = cv2.imread('steamDownloadButton.png',0)                          # Make the Steam Download button a template to look for.
    #cv2.imshow("Screen",img_gray)                                              # Show me the screenshot (for debugging).
    #cv2.waitKey(0)                                                             # And wait before proceeding until I click anything.
    #time.sleep(1)                                                              # Wait for window to disappear.
    
    w, h = template.shape[::-1]                                                 # Gets the width and height of the button.
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)             # New image 'res', looking for occurences of the template in the screen.
    threshold = 0.8                                                             # Threshold, helps determine the level of similarity it must be.
    loc = np.where( res >= threshold)                                           # All places in res, where it exceeds the threshold.

    global counter
    coords = []                                                                 # NEW EMPTY LIST CALLED coords.
    counter = 0                                                                 # NEW PROGRAM COUNTER CALLED counter.
    for pt in zip(*loc[::-1]):                                                  # For each match found:
        cv2.rectangle(img_gray, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1)       # Draw a rectangle into img_gray at the button.
        coords.append((int(pt[0] + w/2), int(pt[1] + h/2)))                     # Add that to the coords list.
        #print('Button centre: {}'.format(coords[counter]))                     # Print the coordianates of each button's centre for debugging.
        counter += 1                                                            # Increment the list index upwards by 1.
    
    #cv2.imshow("Test",img_gray)                                                # Show me the image now (for debugging).
    #cv2.waitKey(0)                                                             # And wait for me to look at it.
    #time.sleep(1)                                                              # Wait for window to disappear.

    cv2.imwrite('res.png',img_gray)                                             # Write it to the folder for debugging and reference.
    #print(coords)                                                              # Debug for coords.
    cachedCoordsOfDButtons = coords
    return coords

def getNamesOfGames(buttonCoords):                                                                                  # Gets names of games using Tesseract.
    global gamesAndSize                                                                                             # The gamesAndSize list to upload to.
    global counter                                                                                                  # A program/list counter.
    counter = 0                                                                                                     # Reset the program counter.
    width, height = pyautogui.size()                                                                                # Grab resolution.
    for coordinates in buttonCoords:                                                                                # For each button found:

        upperBound = buttonCoords[counter][1] + 40                                                                  # 40 pixels above the button, upperbound,
        lowerBound = upperBound - 80                                                                                # And 40 pixels below, lowerbound.
        leftBound = 190                                                                                             # 190 pixel off the left-hand side of the screen, the leftbound,
        rightBound = width - 450                                                                                    # And 400 pixels off the right-hand side of the screen, the rightbound.
        
        infoGame = ImageGrab.grab(bbox=(leftBound,lowerBound,rightBound,upperBound))                                # Screenshot the bounds, which will capture ONLY the game name, and download size/remaining.
        tesseractText = pytesseract.image_to_string(infoGame, lang='eng', config='--oem 1 --psm 6')  # Tesseract will translate text in the screenshot to strings.
        infoGame.save("image{}.png".format(counter))                                                                # Save it as an image for debugging.
        tesseractText = tesseractText[:-2]                                                                          # Tesseract uses this symbol why???
        tesseractText = replace6BA(tesseractText)                                                                   # Tesseract makes mistakes when reading GB, as 6B.
        #print(tesseractText)                                                                                       # Print it for debugging.
        tupleGame = (splitLines(tesseractText, 0), dSB(splitLines(tesseractText, 1)))                               # tupleGame = gameName and size.
        if tupleGame not in gamesAndSize:                                                                           # If we haven't added this game already,
            gamesAndSize.append(tupleGame)                                                                          # Add the game name, and the standardised download size remaining in megabytes.
        else:                                                                                                       # Otherwise,
            pass                                                                                                    # next!

        #print(tesseractText)                                                                                       # Print it for debugging.
        counter += 1                                                                                                # Add one to the program counter.
        pass                                                                                                        # Next!
    #print(gamesAndSize)                                                                                        # When the list has been looped through, print the list for debugging.
    pass                                                                                                        # Next!

def checkForNewGames():
    getNamesOfGames(steamDownloadReader())

def checkDownloadList():                                                                                        # Check the download list for pending downloads.

    os.system('explorer "steam://open/downloads"')                                                              # Run this command, it will send us to Downloads in Steam.
    time.sleep(0.5)
    hwnd = win32gui.GetForegroundWindow()                                                                       # Get the download page, which'll be foreground.
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)                                                             # And maximise it.

    for i in range(3): winsound.Beep(900,250);time.sleep(0.5)
    winsound.Beep(1300,250)

    width, height = pyautogui.size()                                                                            # Get screen resolution.
    pyautogui.click(5, (height/2))                                                                              # Click the mouse on X = 5 and Y = half the screen height to focus the Steam downloads list.
    pyautogui.press("home")                                                                                     # Home to go to the top of the list.
    screenshot1 = None                                                                                          # Initialise the previous-screenshot buffer.
    while True:                                                                                                 # While True loop.
        winsound.Beep(1000,100)                                                                                 # Short beep once, to indicate that the screen is about to be read.
        time.sleep(0.3)                                                                                         # 0.3 second delay to allow scrolling to settle.
        checkForNewGames()                                                                                      # Check for games previously non-indexed.
        screenshot0 = pyautogui.screenshot(region=(0,0,width,height-45))                                        # Take a screenshot, and exclude the Windows taskbar.
        if screenshot0 != screenshot1:                                                                          # If this screenshot is not the same as the last screenshot,
            screenshot1 = screenshot0                                                                           # the last screenshot buffer now is this screenshot.
            pyautogui.press("pgdn")                                                                             # Scroll down.
        else:                                                                                                   # Otherwise if this screenshot is the same as the last screenshot,
            break                                                                                               # We're done scrolling.
    for i in range(2):                                                                                          
        winsound.Beep(1000,500)                                                                                     # Long beeps twice to indicate finished.

def queueNew():
    pass

def huntDownTheGame(gameSelected):
    global gamesAndSize
    coordinateTuple = (int(), int())
    
    os.system('explorer "steam://open/downloads"')                                                              # Run this command, it will send us to Downloads in Steam.
    time.sleep(0.5)
    hwnd = win32gui.GetForegroundWindow()                                                                       # Get the download page, which'll be foreground.
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)                                                             # And maximise it.
    
    for i in range(3): winsound.Beep(1200,150);time.sleep(0.1)                                                  # The beeps for this specific function.
    winsound.Beep(1300,250)

    width, height = pyautogui.size()                                                                            # Get screen resolution.
    pyautogui.click(5, (height/2))                                                                              # Click the mouse on X = 5 and Y = half the screen height to focus the Steam downloads list.
    pyautogui.press("home")                                                                                     # Home to go to the top of the list.

    screenshot1 = None                                                                                          # Initialise the previous-screenshot buffer.
    while True:                                                                                                 # While True loop.
        winsound.Beep(1000,100)                                                                                 # Short beep once, to indicate that the screen is about to be read.
        time.sleep(0.6)                                                                                         # 0.6 second delay to allow scrolling to settle.
        cachedGamesAvailable = []                                                                               # Empty this list.
        gamesAndSize = []                                                                                       # Empty this list.
        checkForNewGames()                                                                                      # Check for games previously non-indexed.

        for i in range(len(cachedCoordsOfDButtons)):                                                            # Each time we see a download button:
            cachedGamesAvailable.append((gamesAndSize[i],cachedCoordsOfDButtons[i]))                            # Mash the two lists together.
            #print("cachedGamesAvailable "+str(cachedGamesAvailable))                                           # For debugging purposes, so I can see what the list looks like.
        for i in range(len(cachedGamesAvailable)):                                                              # For each item in cachedGamesAvailable:
            if str(gameSelected) == str(cachedGamesAvailable[i][0][0]):                                         # If the game we were told to find is visible:
                coordinateTuple = (int(cachedGamesAvailable[i][1][0]), int(cachedGamesAvailable[i][1][1]))      # coordinateTuple is defined as the coordinates on the screen to click.
                #print(coordinateTuple)                                                                         # For debugging, variable checking.
                pyautogui.click(coordinateTuple[0], coordinateTuple[1])                                         # Click that download button, 
                return                                                                                          # then return and end.

        screenshot0 = pyautogui.screenshot(region=(0,0,width,height-45))                                        # Take a screenshot, and exclude the Windows taskbar.
        if screenshot0 != screenshot1:                                                                          # If this screenshot is not the same as the last screenshot,
            screenshot1 = screenshot0                                                                           # the last screenshot buffer now is this screenshot.
            pyautogui.press("pgdn")                                                                             # Scroll down.
        else:                                                                                                   # Otherwise if this screenshot is the same as the last screenshot,
            break                                                                                               # We're done scrolling.
    for i in range(2):                                                                                          
        winsound.Beep(1000,500)                                                                                 # Long beeps twice to indicate finished.

def commandLineInterface():                                                                                     # This command line greets the user and offers options.

    def menuOptions(menu, listGiven=None):                                                                      # Menu options function, can accept an integer for which function it should do, and a list can be passed if needed.
        if menu == 0:                                                                                            # This is the main menu.
            print('''Welcome to AUTOGames' CLI for Steam! Here are your options:
            1: Check what can be downloaded.
            2: (Create a schedule to) update games. NOTE: we must check the list first.
            3: Manage current schedules. (TBA - doesn't yet work)
            4: Manage priorities. (TBA - doesn't yet work)
            ''')
            while True:
                choice = input("Choose an option: ")                                                            # User input.
                menuChoiceList = [str(1), str(2), str(3), str(4)]
                if choice in menuChoiceList:                                                                    # Input validation.
                    return choice                                                                               # The option they chose.

                else:
                    print("The program did not understand that response.\n")                                    # Asking user to try again.
        
        if menu == 1:                                                                                            # "Updating a game" menu.
            print("Okay. Pick the first game you'd like to download.")                                          
            timeIsUp = False                                                                                    # Defining variables needed later. This one stops the program looping if the user doesn't want to add more games.
            listToProcess = listGiven                                                                           # Take the list given to work with.
            listProcessed = []                                                                                  # New empty list which will be our result.
            gameNumbersAvailable = []                                                                           # What game numbers you can choose each loop.
            counterMenu = 0                                                                                     # The menu counter.
            while True:                                                                                         # Loop, nest 1.
                gameNumbersAvailable.clear()                                                                        # Clear gameNumbersAvailable from a recent loop.
                if counterMenu != 0 and listToProcess != []:                                                        # If this is not the first time this loop has ran, but the list is not yet empty:
                    print("\nNow choose the next game that will update.")
                elif listToProcess == []:                                                                           # Otherwise if the list is empty:
                    print("There are no more games to update. Queue complete by default.")
                    break                                                                                           # Stop the loop by default.
                def printTheListToProcess():                                                                        # Prints the listToProcess in a user friendly format.
                    counter = 0                                                                                         # Temporary ticking counter:
                    for i in listToProcess:                                                                             # For each item in listToProcess:
                        if listToProcess[counter] != None:                                                                  # If we haven't already popped this game:
                            printedThing = str(str(listToProcess[counter][0])+": "+str(listToProcess[counter][1])+"\n")         # printedThing becomes "X: Y" where X is the number of the game, and Y is the name of the game.
                            print(printedThing)                                                                                 # print printedThing
                            gameNumbersAvailable.append(listToProcess[counter][0])                                              # Add the game's number to the list which lets us refer to it as being available to queue.
                        counter += 1                                                                                        # Tick the counter.
                printTheListToProcess()                                                                             # Do the function above.
                while True:                                                                                         # Loop, nest 2.
                    inputNumber = int(input("Game number: "))                                                           # User inputs number of which game they'd like to update.
                    if inputNumber in gameNumbersAvailable:                                                             # If the number matches with the number available (input validation):
                        break                                                                                           # End loop, nest 2.
                    else:                                                                                               # Otherwise, print below and do the function above.
                        print("That's not a number in the list above. Here is the list again.")
                        printTheListToProcess()

                listProcessed.append(listToProcess[inputNumber-1])                                                  # Add the game selected from the old listToProcess to the new listProcessed.
                listToProcess[inputNumber-1] = None                                                                 # And nullify it from the old list.
                gameNumbersAvailable[inputNumber-1] = None                                                          # Remove the game number chosen as an available number.
                counterMenu += 1                                                                                    # Tick the menu counter.
                
                while True:                                                                                         # Loop, nest 2.
                    continueChoice = input("Would you like to add another game? Y/N: ")                                 # User input whether they would like to continue.

                    if continueChoice.lower() == "y":                                                                   # If user says they want to add another game,
                        break                                                                                               # exit loop, nest 2.
                    elif continueChoice.lower() == "n":                                                                 # But if user says no, they would not like to add another game,
                        timeIsUp = True                                                                                     # set this to true so the loop doesn't continue.
                        break                                                                                               # exit loop, nest 2.
                    else:                                                                                               # If user is not intelligent enough we will validate their input.
                        print("Unrecognised input.")
                if timeIsUp == True:                                                                                # exit loop, nest 1, if timeIsUp was set to True.
                    break

            listProcessed.reverse()                                                                             # Invert the list, so that they will be queued properly in Steam.
            print("Games will be queued in 5 seconds.")
            time.sleep(5)                                                                                       # Ten second delay, lets user know.
            queueCounter = 0                                                                                    # A counter to track queuing.
            for i in listProcessed:                                                                             # For each game we want to update,
                huntDownTheGame(listProcessed[queueCounter][1])                                                 # update in order given.
                queueCounter += 1                                                                               # tick the queue counter.

    def reCacheList():                                                                                          # Function for later.
            a1 = int(-1)                                                                                        # A counter integer.
            listOfGamesToPrint.clear(); listOfGamesChoosable.clear()                                            # We need fresh lists.
            for i in cachedGamesAndSize:                                                                        # For each item in the cached gamesAndSize list:
                a1 += 1                                                                                         # Counter integer that starts at 0.
                b1 = a1 + 1                                                                                     # Counter integer that starts at 1.
                aStr = str(a1)                                                                                  # String of counter integer a1.
                bStr = str(b1)                                                                                  # String of counter integer b1.
                c = str(cachedGamesAndSize[a1][1])                                                              # Helps with concatenation in the next line by avoiding an "object 'type' is not subscriptable" error.
                listOfGamesToPrint.append(aStr+": "+cachedGamesAndSize[a1][0]+" - "+c+" est. megabytes.")       # Add to the list what presenting all games would look like.
                listOfGamesChoosable.append((b1, cachedGamesAndSize[a1][0]))                                    # Add to this list what we want to use as we process.
            #print(listOfGamesToPrint)                                                                          # Print both for debugging purposes.
            #print(listOfGamesChoosable)

    global gamesAndSize                                                                                         # Global games list,
    cachedGamesAndSize = gamesAndSize                                                                           # which is subject to change so cache it.
    listOfGamesToPrint = []                                                                                     # Set up two new lists.
    listOfGamesChoosable = []
    listChecked = 1                                                                                             # New variable that will check whether games have been checked or not.
    if gamesAndSize != []:                                                                                      # If there are items in gamesAndSize, indicating the list has been checked,
        reCacheList()                                                                                           # Cache the list.
    else:
        listChecked = 0                                                                                         # Otherwise we didn't check the list.

    menuPrompt = menuOptions(0)

    if menuPrompt == "1":                                                                                       # Present menu, and if user picks 1:
        checkDownloadList()                                                                                     # Check download list.
        a = 0                                                                                                   # A counter variable.
        cachedGamesAndSize = gamesAndSize; reCacheList()                                                        # Recache gamesAndSize and reCache all our lists.
        print("\n------------------------------------------------\nUpdates/downloads that are pending:\n")      # Start the list in CLI.
        for i in listOfGamesToPrint:                                                                            # For each item in listOfGamesToPrint:
            print(listOfGamesToPrint[a]+"\n")                                                                   # Print the game name in order.
            a += 1                                                                                              # Tick the counter.
        print("------------------------------------------------")

    if menuPrompt == "2":                                                                                       # Present menu, and if user picks 2:
        if listChecked == 0:                                                                                    # If the list is empty, tell this to the user and check download list:
            print("Either the download list hasn't been checked or the last time it was checked, it was empty. We will check now.")
            checkDownloadList() 
            cachedGamesAndSize = gamesAndSize; reCacheList()                                                    # Recache lists.
        menuOptions(1, listOfGamesChoosable)                                                                    # Use this function and forward the list.

    if menuPrompt == "3" or menuPrompt == "4":                                                                  # If the user chooses an option not yet functional, let them know so.
        print("Currently unavailable, will be added in future updates.")

while True:
    commandLineInterface()