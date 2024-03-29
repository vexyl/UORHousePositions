# For ClassicUO world map house markers on UO Renaissance
# based on Chadarius's fork of Quick's uorhousepositions
# https://github.com/Chadarius/uorhousepositions/tree/worldmap
# icons in BikrMapIcons made by Bikr
import os, shutil
import urllib.request

uoDir = r"C:\UORenaissance" # change this to your UO:R directory
alternativeIcons = False # change to True to use 3D icons

localMapIcons = "BikrMapIcons"
if alternativeIcons:
    localMapIcons = "MapIconsOld"

url = "http://www.uorenaissance.com/map/house.txt"
dataDir = os.path.join(uoDir, "ClassicUO", "Data", "Client")
housesFile = os.path.join(dataDir, "UORHouses.csv")

if not os.path.exists(dataDir):
    print("error: " + dataDir + " does not exist!")
    exit(1)

housesText = None
print("Downloading house.txt...", end="")
with urllib.request.urlopen(url) as f:
    housesText = f.read().decode('utf-8')
print(" ok")

file = open(housesFile, 'w')
houseEntries = housesText.replace('\r', '').split('\n')

# House coords seem to be center-x, center-y + 5
# So we want to draw the icon at x, y - 5
yOffset = -5

print("Processing house entries...", end="")
count = 0
for entry in houseEntries:
    if entry == "" or entry == "+EOF":
        continue
    
    count = count + 1
    
    entry = entry.split(':')
    houseName = entry[0][1:] # [1:] to remove initial +
    houseData = entry[1][1:].split(' ') # [1:] to remove initial space

    housePosition = houseData[0:2] # position is x,y only, leave out mapID
    
    # mapID should be 0, reading the id from house.txt makes the icon/name not show up at all
    mapID = 0 #houseData[2]
    
    # update house position with offset
    housePosition[0] = str(int(housePosition[0])) # x coord
    housePosition[1] = str(int(housePosition[1]) + yOffset) # y coord

    icon = houseName # both have same name
    color = 'yellow'
    zoomIndex = 7
    
    # x, y, map id, name, icon, color, zoom index (optional)
    # zoomIndex is the level of zoom you need to show a map marker icon (default=3)
    # so 0 would show the house markers even if you zoomed all the way out on the map
    file.write("{},{},{},{},{},{}\n".format(','.join(housePosition), mapID, houseName, icon, color, zoomIndex))
print(" ok")

file.close()
print("Generated " + str(count) + " house entries.\noutput file: '" + housesFile + "'")

print("Checking map icons...", end="")
mapIconsDir = os.path.join(os.getcwd(), localMapIcons)
if os.path.exists(mapIconsDir):
    mapIcons = os.listdir(mapIconsDir)
    dest = os.path.join(dataDir, "MapIcons")
    flag = False
    for icon in mapIcons:
        if not os.path.exists(os.path.join(dest, icon)):
            if not flag:
                flag = True
                print(" missing")
            shutil.copy2(os.path.join(mapIconsDir, icon), dest)
            print("\tcopied file '" + icon + "'")
    if not flag:
        print(" ok")
else:
    print(" failed")
    print("warning: '" + mapIconsDir + "' does not exist!")

input("\nPress ENTER to quit.")
