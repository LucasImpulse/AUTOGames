#This module gets the time from the system, then it acquires the zone and language of the system, and stores it in a config file or something.

#Import all needed modules below this line.
import datetime; import os; import locale;

localFolder = os.path.dirname(os.path.abspath(__file__))

#autoConfig(0) is an initial configuration and autoConfig(1) is a reconfiguration.
def autoConfig(inst):
    if inst == None:
      inst = 1
    if inst != 0 and inst != 1:
        print("\n\nERROR! Invalid autoConfig instruction passed! Will not (re)configure anything!")
        return None

#Get system datetime. If system says no, use The End of Time.
    try:
      now = datetime.datetime.now()
    except:
      now = "The End of Time"
    print("Current time: "+str(now))

#Get system time zone. If system says no, use STC (Space-Time Coordinate).
    try:  
      local_timezone = datetime.datetime.utcnow().astimezone().tzinfo
    except:
      local_timezone = "UTC"
    print("Timezone: "+str(local_timezone))

#Get system main language. If system says no, use Intergalactic-Standard Mandarin, UTF-2048.
    try:
      locale.getdefaultlocale()
      langencode = locale.getdefaultlocale()
    except:
      langencode = ("Intergalactic-Standard Mandarin", "UTF-2048")
    print("Language code + encoding: "+str(langencode))

#Split langencode into lang and encode
    lang = langencode[0]
    print("Language: "+lang)
    encode = langencode[1]
    print("Encoding: "+encode)

#IF this is an inital config:
#Set all values in to the initial config log, and make a config log if it doesn't already exist.
#THIS WILL WIPE THE CONFIGLOG FILE.
    if inst == 0:
      concan = str("INITIAL FILE SETUP: "+str(now)+" "+str(local_timezone)+". Language: "+str(lang)+". Encoding: "+encode+".\n")
      print("\n\nConcatenation: \n"+concan)
      file = open("LocaleCFG.log","w")
      file.write(concan)
      file.close()

#IF this is a reconfig:
#Set all values in to the config log. Append after previous line.
    if inst == 1:
      concan = str("\nRECONFIG: "+str(now)+" "+str(local_timezone)+". Language: "+str(lang)+". Encoding: "+encode+".")
      print("\n\nConcatenation: \n"+concan)
      file = open("LocaleCFG.log","a")
      file.write(concan)
      file.close()

#Create a config file, add empty config options, and close for next function.
    file = open("Locale.cfg","w")
    file.write("Last time application ran: ["+str(now)+"] \nTimezone: ["+str(local_timezone)+"]\nLanguage: ["+str(lang)+"]")
    file.close()

#Put information into the config file.
    file = open("Locale.cfg","w")
    file.write("Timezone: "+str(local_timezone)+"\n")
    file.write("Language: "+lang+"\n")
    file.write("Encoding: "+encode+"\n")
    file.close()
    return concan

def reConfig():
  autoConfig(1)

def firstConfig():
  autoConfig(0)

if __name__ == "__main__":
    pass