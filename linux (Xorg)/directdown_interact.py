# All modules imported below this line.
from download import download

# Peculiarly enough there's a module on PyPI called download and it downloads.

def addDownload():
    urlTarget = input("Paste here the target URL you wish to download.")
    dirTarget = input("Where would you like to put this file?")
    replaceOrNot = input("If there is already a file, should it be replaced?")
    # THIS LAST INPUT PROMPT IS BEYOND STUPID, I KNOW, AND I WILL REPLACE IT WITH A TKINTER YES/NO BOX. 
    path = download(urlTarget, dirTarget, replace=replaceOrNot, progressbar=True)
    print("Download successful.")
    
