def getInfo():
    input = open("input3.txt", "r")
    side = 0
    officer = 0
    scooter = 0
    map = {}
    for num, line in enumerate(input):
        if num == 0:
            side = int(line.strip())
        elif num == 1:
            officer = int(line.strip())
        elif num == 2:
            scooter = int(line.strip())
        else:
            coordinate = line.strip()
            map[coordinate] = map.get(coordinate, 0) + 1
    return side, officer, scooter, map


def nQueens(side, officer):
    candidates = []
    visited = {'col': set(), 'row-col':set(), 'row+col': set()}
    backtrack(candidates, [], visited, side, officer, 0)
    return candidates


def backtrack(candidates, can, visited, side, officer, row):
    if len(can) == officer:
        candidates.append(list(can))
    else:
        for i in range(row, row+side-officer+1):
            for j in range(side):
                if j in visited['col']:
                    continue
                if (i - j) in visited['row-col']:
                    continue
                if (i + j) in visited['row+col']:
                    continue

                visited['col'].add(j)
                visited['row-col'].add(i - j)
                visited['row+col'].add(i + j)
                s = str(i)+ ',' + str(j)
                can.append(s)
                backtrack(candidates, can, visited, side, officer, i + 1)
                visited['col'].remove(j)
                visited['row-col'].remove(i - j)
                visited['row+col'].remove(i + j)
                can.pop()


def count(item, map):
    sum = 0
    for point in item:
        sum = map.get(point, 0) + sum
    return sum

if __name__ == "__main__":
    res = 0
    side, officer, scooter, map = getInfo()
    candidates = nQueens(side, officer)
    for item in candidates:
        res = max(res, count(item, map))
    print(res)
    output = open("output.txt", "w")
    output.write(str(res))
