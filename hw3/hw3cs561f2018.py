import numpy as np
import random
global gridSize, obstacles

def getInfo():
	global gridSize, obstacles
	input = open("HW3_Test_Cases/input.txt", "r")
	output = open("output.txt", "w")
	obstacles = set()
	startLoc = []
	endLoc = []
	for num, line in enumerate(input):
		if num == 0:
			gridSize = int(line.strip())
		elif num == 1:
			carNumber = int(line.strip())
		elif num == 2:
			obstacleNumber = int(line.strip())
		elif num <= 2 + obstacleNumber:
			obs = line.strip().split(",")
			obstacles.add((int(obs[1]),int(obs[0])))
		elif num <= 2 + obstacleNumber + carNumber:
			loc = line.strip().split(",")
			startLoc.append((int(loc[1]),int(loc[0])))
		elif num <= 2 + obstacleNumber + carNumber * 2:
			loc = line.strip().split(",")
			endLoc.append((int(loc[1]),int(loc[0])))

	for i in range(carNumber):
		policy, environment = getPolicy(startLoc[i], endLoc[i])
		total = 0
		for j in range(10):
			reward = 0
			pos = startLoc[i]
			np.random.seed(j)
			swerve = np.random.random_sample(1000000)
			k = 0
			while pos != endLoc[i]:
				action = policy[pos]
				if swerve[k] > 0.7:
					if swerve[k] > 0.8:
						if swerve[k] > 0.9:
							action = turn_right(turn_right(action))
						else:
							action = turn_right(action)
					else:
						action = turn_left(action)
				k += 1

				x = pos[0]
				y = pos[1]
				if action == 0:
					y -= 1
				elif action == 1:
					y += 1
				elif action == 2:
					x += 1
				elif action == 3:
					x -= 1

				if x >= 0 and x < gridSize and y >= 0 and y < gridSize:
					pos = (x, y)					

				reward += environment[pos[0]][pos[1]]
			total += reward
		output.write(str(int(total//10)) + "\n")
	
def turn_left(move):
	if move == 0:
		return 2
	elif move == 1:
		return 3
	elif move == 2:
		return 1
	else:
		return 0

def turn_right(move):
	if move == 0:
		return 3
	elif move == 1:
		return 2
	elif move == 2:
		return 0
	else:
		return 1

# def update(grid, environment, policy, end):
# 	# copy = np.zeros((gridSize, gridSize))
# 	# for  i in range(gridSize):
# 	# 	for j in range(gridSize):
# 	# 		copy[i][j] = grid[i][j]

# 	diff = 0.0
# 	for i in range(gridSize):
# 		for j in range(gridSize):
# 			if (i,j) == end:
# 				continue 
# 			maxValue = float('-inf')

# 			for tryAction in range(4):
# 				newValue = 0
# 				for action in range(4):
# 					if action == 0:
# 						x = i
# 						y = j - 1
# 					if action == 1:
# 						x = i
# 						y = j + 1
# 					if action == 2:
# 						x = i + 1
# 						y = j
# 					if action == 3:
# 						x = i - 1
# 						y = j
# 					if action == tryAction:
# 						if x >= 0 and x < gridSize and y >= 0 and y < gridSize:
# 							newValue += grid[x][y] * 0.7
# 						else:
# 							newValue += grid[i][j] * 0.7
# 					else:
# 						if x >= 0 and x < gridSize and y >= 0 and y < gridSize:
# 							newValue += grid[x][y] * 0.1
# 						else:
# 							newValue += grid[i][j] * 0.1
# 				if newValue > maxValue:
# 					maxValue = newValue
# 					policy[i][j] = tryAction
# 			last = grid[i][j]
# 			grid[i][j] = environment[i][j] + 0.9*maxValue
# 			diff += abs(grid[i][j] - last)

# 	if diff < 0.1:
# 		return 1

# 	return 0

def getPolicy(start, end):
	grid = np.zeros((gridSize, gridSize))
	environment = np.zeros((gridSize, gridSize))
	policy = np.zeros((gridSize, gridSize))

	environment.fill(-1)
	grid.fill(-1)
	for o in obstacles:
		environment[o[0]][o[1]] = -101
		grid[o[0]][o[1]] = -101
	environment[end[0]][end[1]] = 99
	grid[end[0]][end[1]] = 99

	while True:
		diff = 0.0
		for i in range(gridSize):
			for j in range(gridSize):
				if (i,j) == end:
					continue 

				valList = []

				xLoc0 = i
				yLoc0 = j - 1
				valLoc0 = grid[i][j]
				if yLoc0 >= 0:
					valLoc0 = grid[xLoc0][yLoc0]
				valList.append(valLoc0)

				xLoc1 = i
				yLoc1 = j + 1
				valLoc1 = grid[i][j]
				if yLoc1 < gridSize:
					valLoc1 = grid[xLoc1][yLoc1]
				valList.append(valLoc1)
				
				xLoc2 = i + 1
				yLoc2 = j
				valLoc2 = grid[i][j]
				if xLoc2 < gridSize:
					valLoc2 = grid[xLoc2][yLoc2]
				valList.append(valLoc2)
				
				xLoc3 = i - 1
				yLoc3 = j 
				valLoc3 = grid[i][j]
				if xLoc3 >= 0:
					valLoc3 = grid[xLoc3][yLoc3]
				valList.append(valLoc3)

				newValue = 0
				maxValue = valLoc0
				tryAction = 0
				for num in range(len(valList)):
					newValue += valList[num] * 0.1
					if valList[num] > maxValue:
						maxValue = valList[num]
						tryAction = num
				policy[i][j] = tryAction
				newValue += valList[tryAction] * 0.6

				last = grid[i][j]
				grid[i][j] = environment[i][j] + 0.9*newValue
				diff += abs(grid[i][j] - last)

		if diff < 0.01:
			break
	return policy, environment

getInfo()
