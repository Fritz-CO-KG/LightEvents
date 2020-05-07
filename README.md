# LightEvents
Bingo plugin written in python for minecraft servers

Instructions on how to install:

1. Download the correct Jython version under

search.maven.org/remotecontent?filepath=org/python/jython-standalone/2.7.0/jython-standalone-2.7.0.jar

Then rename the downloaded file to jython.jar and put it into the minecraft servers folder.
Create a new folder called "lib" inside of you minecraft server's folder and put the jython.jar inside of it.

2. Download pploader v.1.2.0
I could only find one source for this file:

https://www.daniel-braun.com/wp-content/uploads/2017/07/pploader1.2.0.zip

extract the contents and put pploader.jar into your server's plugin files.

3. Clone my repository and put the "presets.json" file in sources into your server's plugin directory.

4. Copy the plugin.py and plugin.yml into a folder named "lightevents.py.dir" inside of your servers plugin files.

5. Open the plugin.py file and scroll down to JSON_DIR = "/home/fritz/jsons"
Replace the path with the path to the folder to where presets.json is found
Example:
/home/username/minecraft-server/plugins (assumes that presets.json is found directly in your plugin folder)

Please note thet later on there will not be any need of thes rather annoying file copying...
