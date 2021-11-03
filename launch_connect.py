#Launcher connection and compatibility module for AUTOGames, which acts the same whether first time call or normal call, except for a few text changes, this just gives me more options to differentiate them in future, if I wanted to make the first time an insanely more welcoming experience.

#import all requirements on the line below


def initLaunchConnect(a):
	if a == 0:
		#firstTimeLaunchConnect()
		None
	else:
		#LaunchConnect()
	#Return value from either to whatever called.
		None
		
def firstTimeLaunchConnect():
	#Similar to LaunchConnect() but first time.
	None
	
def LaunchConnect():
	#It connects launchers.
	
	#START WINDOW 1
		#Text near top-middle that explains this is the first time launcher connector. They can connect a launcher like Steam, Origin, UPlay or Epic Games.
		#Layout the supported launchers in the middle of the window.
		#Put a Skip button at the bottom, which changes to Finish if the user adds at least one launcher.
	
		#STEAM BUTTON CLICKED
			#Find out if Steam exists.
			#If can't find, ask user to point to exe or quit to previous screen.
			#Add Steam as an entry to the launcher-list.txt
		
		#LAUNCHER BUTTON CLICKED
			#Just like above.
		
		#SkipFinish CLICKED
			#Return LaunchConnect() to initLaunchConnect()
	None