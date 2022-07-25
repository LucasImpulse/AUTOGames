# AutoGAMES
AutoGAMES is a program that aims to control all file/game downloads according to user-defined schedule.
AutoGAMES' endgame is to be able to queue games across Steam, Epic Games, Origin etc. in whatever order needed.
For example: 2 games of 5 download first on Steam, only 1 game downloads on Origin, and then Steam continues.
This allows better downloading as games can download one at a time without relying on the launcher's own schedulers.
The audience intended is people with low bandwidth, which used to be me but no longer is. So also it will unify game launchers.

I would call my program an Automated Download Manager (ADM), all download managers can be automated to help with their downloads, but those are with torrents and direct downloads. My program aims to interact directly with launchers automatically to throw all kinds of other downloads in there, and not just direct downloads from HTTPS or torrents.

I want to add Steam first then work on other launchers.

Originally was Python, but C++ works faster and so.
