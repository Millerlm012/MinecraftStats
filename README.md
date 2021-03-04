# MinecraftStats

About: MinecraftStats was created because I have a Minecraft server running and my friends were wanting to see some of their stats. So... I wrote a python program to handle making the jsons into some nice csvs to be uploaded to Google Sheets. I think some point in the future I'd like to make a dedicated website to display the stats... Kind of like a leaderboad. <br />
***

To begin I first dug around in the servers directories to determine where the stats were and how they were offered. After learning that they're all stored in some nice jsons, I exported them from the server to my laptop. (The server is completely command-line based and I appreciate my text editor over using Nano or VIM) <br />

Once I had all of the jsons, I wrote a Python function that would open the usercache.json and pair up the each player's UUID with their username. Once I had that I was able to begin opening each players 'UUID'.json and begin extracting their stats. The 'UUID'.json's were stored as jsons with more jsons inside them. This made it a little more difficult to transfer them to jsons, but I was able to make it work. <br />

After transferring the jsons to csvs, I wrote a upload function that took the csvs and uploaded them to Google Sheets. I had to be careful working with the logic as I wanted it to be as efficient as possible and avoid using up the API request quota. After I finished writing the program and testing it, I exported the program back over to the server. I wrote a bash script that allowed me to write a cronjob to initialize the program at midnight everyday. This enables the stats to stay up to date. <br />

I plan to write a Google Apps Script that compiles the data into a nice Master spreadsheet.
