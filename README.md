# AutoGAMES
AutoGAMES is a program that aims to control all file/game downloads according to user-defined schedule.
AutoGAMES' endgame is to be able to queue games across Steam, Epic Games, Origin etc. in whatever order needed.
For example: 2 games of 5 download first on Steam, only 1 game downloads on Origin, and then Steam continues.
This allows better downloading as games can download one at a time without relying on the launcher's own schedulers.
The audience intended is people with low bandwidth, which used to be me but no longer is.

Windows compatible so far:
  Queue games on Steam immediately.
  Scan for games on Steam.

Linux catching up, then development continues.

I recognise my program as a new category of program, Automated Download Manager (ADM), all download managers can be automated to help with their downloads, but those are with torrents and direct downloads. My program aims to interact directly with external interfaces automatically to throw all kinds of other downloads in there, and not just direct downloads from HTTPS or torrents.

I want to add Steam first, completely finished, then I can add modules manually for other launchers, like an _origin_interact.py_ or _epic\_interact.py_ or _riot\_interact.py_.
