import os, shutil
import urllib.request

url = "http://www.uorenaissance.com/map/house.txt"
dataDir = os.path.join("C:\\", "UORenaissance", "ClassicUO", "Data", "Client")
housesFile = os.path.join(dataDir, "UORHouses.csv")

if not os.path.exists(dataDir):
    print("error: " + dataDir + " does not exist!")
    exit(1)

houseOffsets = {
	"castle": 		[0, -5],
	"fortress": 		[0, -5],
	"keep"    : 		[0, -5],
	"large house": 		[0, -5],
	"log cabin": 		[0, -5],
	"marble patio": 	[0, -5],
	"marble shop": 		[0, -5],
	"patio house": 		[0, -5],
	"sandstone patio":	[0, -6],
	"small house": 		[0, -5],
	"small tower": 		[0, -5],
	"stone shop": 		[0, -5],
	"tower": 		[0, -5],
	"two story house": 	[0, -5],
	"villa": 		[0, -5],
}

housesText = None
print("Downloading houses.txt...", end="")
with urllib.request.urlopen(url) as f:
    housesText = f.read().decode('utf-8')
print(" ok")

file = open(housesFile, 'w')

houseEntries = housesText.replace('\r', '').split('\n')

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
    mapID = 0 #houseData[2]
    
    # update house position with offset
    housePosition[0] = str(int(housePosition[0]) + houseOffsets[houseName][0]) # x coord
    housePosition[1] = str(int(housePosition[1]) + houseOffsets[houseName][1]) # y coord

    icon = houseName # both have same name
    color = 'yellow'
    zoomIndex = 7
    
    # x, y, map id, name, icon, color, zoom index
    file.write("{},{},{},{},{}\n".format(','.join(housePosition), mapID, houseName, icon, color, zoomIndex))
print(" ok")

file.close()
print("Generated " + str(count) + " house entries.\noutput file: '" + housesFile + "'")

print("Checking map icons...", end="")
mapIconsDir = os.path.join(os.getcwd(), "MapIcons")
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
