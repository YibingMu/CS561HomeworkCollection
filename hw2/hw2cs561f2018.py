global lahsa, spla, candidates, lahsaChoosen, splaChoosen, lahsaQualified, splaQualified
global numberOfBed, numberOfPlace, mapping

def initialize():
	global lahsa, spla, candidates, lahsaChoosen, splaChoosen, lahsaQualified, splaQualified, mapping
	lahsa = [0,0,0,0,0,0,0]
	spla = [0,0,0,0,0,0,0]
	lahsaChoosen = []
	splaChoosen = []
	candidates = []
	lahsaQualified = []
	splaQualified = []
	mapping = {}


def getInfo():
	global numberOfBed, numberOfPlace
	input = open("input14.txt", "r")
	lahsaSoFar = 0
	splaSoFar = 0
	totalNumber = 0
	for num, line in enumerate(input):
		if num == 0:
			numberOfBed = int(line.strip())
		elif num == 1:
			numberOfPlace = int(line.strip())
		elif num == 2:
			lahsaSoFar = int(line.strip())
		elif num <= 2 + lahsaSoFar:
			lahsaChoosen.append(line.strip())
		elif num == 2 + lahsaSoFar + 1:
			splaSoFar = int(line.strip())
		elif num <= 2 + lahsaSoFar + 1 + splaSoFar:
			splaChoosen.append(line.strip())
		elif num == 2 + lahsaSoFar + 1 + splaSoFar + 1:
			totalNumber = int(line.strip())
		else:
			candidates.append(line.strip())
			qualified(line.strip())
	updateList()


def updateList():
	for item in lahsaChoosen:
		number = int(item)
		info = candidates[number-1]
		for num, time in enumerate(candidates[number-1][13:20]):
			if time == '1':
				lahsa[num] += 1
	for item in splaChoosen:
		number = int(item)
		for num, time in enumerate(candidates[number-1][13:20]):
			if time == '1':
				spla[num] += 1

	for item in candidates[:]:
		number = item[:5]
		if number in lahsaChoosen or number in splaChoosen:
			candidates.remove(item)

def qualified(info):
	age = int(info[6:7]) * 100 + int(info[7:8]) * 10 + int(info[8:9])
	if info[5:6] == 'F' and age > 17 and info[9:10] == 'N': 
		lahsaQualified.append(info)
	if info[10:11] == 'N' and info[11:12] == 'Y' and info[11:12] == 'Y':
		splaQualified.append(info)

def q(info, name):
	if name == "lahsa":
		age = int(info[6:7]) * 100 + int(info[7:8]) * 10 + int(info[8:9])
		if info[5:6] == 'F' and age > 17 and info[9:10] == 'N': 
			return True
	elif name == "spla":
		if info[10:11] == 'N' and info[11:12] == 'Y' and info[11:12] == 'Y':
			return True
	return False

def canAdd(info, name):
	if not q(info, name):
		return False
	if name == "lahsa":
		for index, time in enumerate(info[-7:]):
			if time == '1' and lahsa[index] == numberOfBed:
				return False
	elif name == "spla":
		for index, time in enumerate(info[-7:]):
			if time == '1' and spla[index] == numberOfPlace:
				return False
	return True

def addSpaceOrBed(info, name):
	if name == "lahsa":
		for index, time in enumerate(info[-7:]):
			if time == '1':
				lahsa[index] = lahsa[index] + 1
	else:
		for index, time in enumerate(info[-7:]):
			if time == '1':
				spla[index] = spla[index] + 1

def deleteSpaceOrBed(info, name):
	if name == "lahsa":
		for index, time in enumerate(info[-7:]):
			if time == '1':
				lahsa[index] = lahsa[index] - 1
	else:
		for index, time in enumerate(info[-7:]):
			if time == '1':
				spla[index] = spla[index] - 1

def numberCanAdd(info):
	numberOfCanAdd = 0
	for time in info[-7:]:
		if time == '1':
			numberOfCanAdd += 1
	return numberOfCanAdd



def splaChooseStart():
	maxValue = 0
	result = ""
	for index, info in enumerate(candidates):
		if not canAdd(info, "spla"):
			continue
		addSpaceOrBed(info, "spla")
		candidates.remove(info)
		s, l = lahsaChoose()
		print((s, l))
		
		total = s + numberCanAdd(info)
		print(total)
		if total > maxValue:
			maxValue = total
			result = info
		candidates.insert(index, info)
		deleteSpaceOrBed(info, "spla")
	print(maxValue)
	return result

def lahsaChoose():
	string = "".join(candidates)
	pair = string + "l"
	if pair in mapping.keys():
		temp = mapping.get(pair)
		return temp[0], temp[1]
	# print(candidates)
	lMax = 0
	sMax = 0
	numberOfChoose = 0
	n = 0
	for index, info in enumerate(candidates):
		if canAdd(info, "spla"):
			n += 1
		if not canAdd(info, "lahsa"):
			continue
		#print(canAdd(info, "lahsa"))
		numberOfChoose += 1
		candidates.remove(info)
		#print(index)
		addSpaceOrBed(info, "lahsa")
		s, l = splaChoose()
		total = l + numberCanAdd(info)
		if total > lMax:
			lMax = total
			sMax = s
		candidates.insert(index, info)
		deleteSpaceOrBed(info, "lahsa")
	if numberOfChoose == 0 and n == 0:
		mapping[pair] = [0,0]
		return 0, 0
	if numberOfChoose == 0:
		s, l = splaChoose()
		mapping[pair] = [s,0]
		return s, 0
	mapping[pair] = [sMax,lMax]
	return sMax, lMax

def splaChoose():
	string = "".join(candidates)
	pair = string + "s"
	if pair in mapping.keys():
		temp = mapping.get(pair)
		return temp[0], temp[1]

	# print(candidates)
	lMax = 0
	sMax = 0
	numberOfChoose = 0
	n = 0
	for index, info in enumerate(candidates):
		if canAdd(info, "lahsa"):
			n += 1
		if not canAdd(info, "spla"):
			continue
		numberOfChoose += 1
		candidates.remove(info)
		addSpaceOrBed(info, "spla")
		s, l = lahsaChoose()
		total = s + numberCanAdd(info)
		if total > sMax:
			sMax = total
			lMax = l
		candidates.insert(index, info)
		deleteSpaceOrBed(info, "spla")
	if numberOfChoose == 0 and n == 0:
		mapping[pair] = [0,0]
		return 0, 0
	if numberOfChoose == 0:
		s, l = lahsaChoose()
		mapping[pair] = [0,l]
		return 0, l
	mapping[pair] = [sMax, lMax]
	return sMax, lMax


if __name__ == "__main__":
	initialize()
	getInfo()
	a = splaChooseStart()
	# print(a)
	output = open("output.txt", "w")
	output.write(a[0:5])
	# print(lahsa)
	# print(spla)
	# print(candidates)
	# print(lahsaChoosen)
	# print(splaChoosen)
	# print(numberOfBed)
	# print(numberOfPlace)

	# print(lahsaQualified)
	# print(splaQualified)







