import os
import urllib.request

url = "http://www.uorenaissance.com/map/house.txt"
housesFile = "C:\\UORenaissance\\ClassicUO\Data\\Client\\UORHouses.csv"

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
    houseType = entry[0][1:] # [1:] to remove initial +
    housePosition = entry[1][1:].split(' ') # [1:] to remove initial space

    # update house position with offset
    housePosition[0] = str(int(housePosition[0]) + houseOffsets[houseType][0]) # x coord
    housePosition[1] = str(int(housePosition[1]) + houseOffsets[houseType][1]) # y coord
    housePosition[2] = '0'                                                     # z coord

    # pos, type, type, color, unknown
    file.write("{},{},{},{},{}\n".format(','.join(housePosition), houseType, houseType, 'yellow', 7))
print(" ok")

file.close()
print("Generated " + str(count) + " house entries.\noutput file: " + housesFile)
