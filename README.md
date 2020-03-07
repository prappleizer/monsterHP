# monsterHP
A GUI-based MPL program for dynamically tracking creature/monster HP during D&amp;D sessions.

## What it is 
The purpose of monsterHP is to make it fast and easy to track the health of your monsters
and other baddies during DnD sessions. Setup is designed to be quick, with both GUI and 
API-style implementations for launching encounters. 

This is a barebones piece of software -- not intended for the careful entry of many monster properties, etc.
Instead, it allows you to see health bars for each creature, and subtract off damage (or add back in HP)
by simply typing in the damage and hitting enter. I've found that in the middle of battle, that's all
I really need, and this allows me to keep combat moving quickly. 

## Usage 

There are three ways to set up and run an encounter using monsterHP. 

The first is through the GUI, which allows for the manual entry of monsters or the loading of a `.csv` file containing a list of monsters with their HP and AC. To launch this GUI, begin by starting a python/ipython session and importing the following from monsterHP:

```
from monsterHP.monsterHP import Launcher
```
Next, we can launch the GUI by typing 
```
launcher = Launcher()
launcher.launch()
```
This should spawn a MPL window that is the GUI interface for monsterHP. There are 3 text entry fields at the top, which allow you to enter a monster name, HP, an AC. This can be added to your encounter with the plus-symbol box next to the text entry fields, and the monster just entered should appear below. 

At the bottom of the window, there is also a text entry field to load a csv file containing your monsters, of the form 
```
monster_name,HP,AC
monster_name,HP,AC
monster_name,HP,AC
```

If you type a file name that is in the **same directory** as you ran monsterHP, it should be able to load this file and text should appear saying the file was loaded correctly. There is some rudimentary error handling in this load function (namely, IOError if file not present, and parsing error if, e.g., the file does not contain only comma-separated values of 3 in each row). Other issues with your data files might not (yet) be caught. 

Once you have set up your monster list (either through manual entry or loading a file), hit the GO button. The entry window will close, and another window will open which contains the encounter. You should see horizontal health bars for each of your monsters, with the monster name and AC listed within each for reference. At the bottom, you'll see a text entry box for each monster. You can now begin adjusting the HP of your monsters by entering a number and hitting enter. Entering something that cannot be evaluated as a number will have no effect. Negative numbers correspond to adding health. When a monster gets down to 10% of its initial health, its bar turns red. 


The other way to run an encounter is to skip the launcher and set up your monsters interactively in the following way: 
```
from monsterHP.monsterHP import Monster,Encounter

m1 = Monster('name',15,12)
m2 = Monster('name2',35,15)
m3 = Monster('name3',41,13)

monster_list = [m1,m2,m3]

encounter = Encounter(monster_list)
encounter.run_encounter()
```

The above can be done interactively in the terminal, but can of course also be entered into a python `.py` file, which you would simply run from ipython to spawn a session. This allows you to set up several encounters in different python files and quickly run them during your sessions via 

```
run some_encounter.py
```








