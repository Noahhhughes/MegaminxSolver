import Side
import Mega
import time
import queue
from random import randint

# Takes in the information for a side object and sets the values of any neighboring sides to the ten small nodes on the
# megaminx side in question
def setNodeNeighbors(sideColor, currentNeighborList):

    tempList = sideColor.nodeVal
    for i in range(len(sideColor.nodeVal)):
        if i % 2 == 0:
            tempList[i][1] = currentNeighborList[int(i / 2)]
            if i == 0:
                tempList[i][2] = currentNeighborList[4]
            else:
                tempList[i][2] = currentNeighborList[int((i / 2) - 1)]
        else:
            tempList[i][1] = currentNeighborList[int((i - 1) / 2)]
    sideColor.set_nodeVal(tempList)

    return

# Prints out a megaminx object
def displayMega(megaminx):

    for i in range(len(megaminx.sides)):
        print("      ", megaminx.sides[i].nodeVal[2][0][:2], end='')
        print("           ", end='')
    print()
    for i in range(len(megaminx.sides)):
        print("  ", megaminx.sides[i].nodeVal[1][0][:2], "    ", megaminx.sides[i].nodeVal[3][0][:2], end='')
        print("       ", end='')
    print()
    for i in range(len(megaminx.sides)):
        print(megaminx.sides[i].nodeVal[0][0][:2], "          ", megaminx.sides[i].nodeVal[4][0][:2], end='')
        print("    ", end='')
    print()
    for i in range(len(megaminx.sides)):
        print(" ", megaminx.sides[i].nodeVal[9][0][:2], "      ", megaminx.sides[i].nodeVal[5][0][:2], end='')
        print("      ", end='')
    print()
    for i in range(len(megaminx.sides)):
        print("   ", megaminx.sides[i].nodeVal[8][0][:2], megaminx.sides[i].nodeVal[7][0][:2], megaminx.sides[i].nodeVal[6][0][:2], end='')
        print("        ", end='')
    print()
    print()
    for i in range(len(megaminx.sides)):
        print(" ", megaminx.sides[i].bigColor, "side", i, end='')
        print("      ", end='')
    print()
    print()

    return

# Resets the megaminx object to its default, correct values were all nodes are in the correct location
def resetMega(megaminx):

    for i in range(len(megaminx.sides)):
        for j in range(len(megaminx.sides[i].nodeVal)):
            megaminx.sides[i].nodeVal[j][0] = megaminx.sides[i].bigColor

    return

# Rotates a specified side of a megaminx object in the specified direction
def rotateSide(megaminx, num, clockwise):

    rotatingList = []
    for u in range(len(megaminx.sides[num].neighborColor)):
        for i in range(len(megaminx.sides)):
            if megaminx.sides[i].bigColor == megaminx.sides[num].neighborColor[u]:
                for j in range(10):
                    if megaminx.sides[i].nodeVal[j][1] == megaminx.sides[num].bigColor or megaminx.sides[i].nodeVal[j][2] == megaminx.sides[num].bigColor:
                        rotatingList.append([j, megaminx.sides[i].bigColor, megaminx.sides[i].nodeVal[j][1], megaminx.sides[i].nodeVal[j][2], megaminx.sides[i].nodeVal[j][0]])

    tempRotatingColorList = []

    for n in range(len(rotatingList)):
        tempRotatingColorList.append(rotatingList[n][4])
    if clockwise:
        for i in range(3):
            tempRotatingColorList = [tempRotatingColorList[-1]] + tempRotatingColorList[:-1]
    else:
        for i in range(3):
            tempRotatingColorList = tempRotatingColorList[1:] + [tempRotatingColorList[0]]

    for u in range(len(rotatingList)):
        for i in range(len(megaminx.sides)):
            if megaminx.sides[i].bigColor == rotatingList[u][1]:
                megaminx.sides[i].nodeVal[rotatingList[u][0]][0] = tempRotatingColorList[u]

    tempColorList = []
    for m in range(len(megaminx.sides[num].nodeVal)):
        tempColorList.append(megaminx.sides[num].nodeVal[m][0])

    if clockwise:
        for i in range(2):
            tempColorList = [tempColorList[-1]] + tempColorList[:-1]
    else:
        for i in range(2):
            tempColorList = tempColorList[1:] + [tempColorList[0]]

    for i in range(len(megaminx.sides[num].nodeVal)):
        megaminx.sides[num].nodeVal[i][0] = tempColorList[i]

    return

# Randomizes the megaminx object randomNum times by randomly selecting a side to rotate, rotates sides clockwise
def randomize(megaminx, randomNum):

    for i in range(randomNum):
        #directionNum = randint(0, 1)
        directionNum = 1
        sideNum = randint(0, 11)

        if directionNum == 0:
            clockwise = False
            direction = "counter clockwise"
        else:
            clockwise = True
            direction = "clockwise"

        rotateSide(megaminx, sideNum, clockwise)

    return

# Makes sure that the user's input is valid, warns the user if not
def validator(inputVal):
    valid = False
    if inputVal != "r" and inputVal != "q" and inputVal != "t" and inputVal != "s":
        try:
            int(inputVal)
            if int(inputVal) >= 0 and int(inputVal) <= 11:
                valid = True
            else:
                print("That is not a valid input.")
        except:
            print("That is not a valid input.")
    elif inputVal == "r" or inputVal == "q" or inputVal == "t" or inputVal == "s":
        valid = True
    else:
        print("That is not a valid input.")

    return valid

# This is the A* algorithm, that takes in a megaminx object and, using a priority queue, compares the heuristic values
# to solve for the correct path. This returns the number of nodes expanded during the search.
def megaSolver(megaminx):

    megaQueue = queue.PriorityQueue()
    megaminx.set_heuristicVal(heuristicEstimate(megaminx))
    megaminx.set_depth(0)
    megaminx.set_priority(megaminx.depth + megaminx.heuristicVal)
    megaQueue.put(megaminx)
    expanded = 0

    while not megaQueue.empty():

        mainMega = megaQueue.get()

        if mainMega.heuristicVal == 0:
            break

        for i in range(12):
            newMega = copyMega(mainMega)
            rotateSide(newMega, i, False)
            newMega.set_heuristicVal(heuristicEstimate(newMega))
            newMega.set_depth(mainMega.depth + 1)
            newMega.set_priority(newMega.depth + newMega.heuristicVal)
            megaQueue.put(newMega)
            expanded += 1

    return [mainMega, expanded]

# Copies the contents of one megaminx object into another
def copyMega(megaminx):

    newMega = megaMaker()
    for i in range(len(newMega.sides)):
        for j in range(len(newMega.sides[i].nodeVal)):
            newMega.sides[i].nodeVal[j][0] = megaminx.sides[i].nodeVal[j][0]
    newMega.set_depth(megaminx.depth)
    newMega.set_heuristicVal(megaminx.heuristicVal)

    return newMega

# This calculates and returns a heuristic value. This was done using the distance each node was from its correct location.
# Distance was calculated by looking at how many faces away the correct location for the node was. Manhattan distance.
# These distances were summed and divided by 10, the amount of nodes on a face that are rotated.
def heuristicEstimate(megaminx):

    incorrectSum = 0
    for i in range(len(megaminx.sides)):
        for j in range(len(megaminx.sides[i].nodeVal)):
            if megaminx.sides[i].nodeVal[j][0] == megaminx.sides[i].bigColor:
                incorrectSum += 0
            elif megaminx.sides[i].nodeVal[j][0] in megaminx.sides[i].neighborColor:
                incorrectSum += 1
            elif megaminx.sides[i].nodeVal[j][0] == megaminx.sides[i].oppColor:
                incorrectSum += 3
            else:
                incorrectSum += 2
    incorrectSum = incorrectSum / 10

    return incorrectSum

# This function tests the solver for k values of randomizations, 5 iterations each
def testK():

    for k in range(3, 12):
        total = 0
        start_time = time.time()
        megaList = [megaMaker() for i in range(5)]
        for h in range(5):
            randomize(megaList[h], k)
        for i in range(5):
            expanded = megaSolver(megaList[i])[1]
            total = total + expanded
            print("Megaminx number", i+1, "with", k, "random iterations expanded", expanded, "nodes")
        print("The average number of expanded nodes was", total/5)
        print("The operation took", time.time() - start_time, "seconds")
        print()

    return

# This creates a new megaminx object, with all values set to their defaults
def megaMaker():

    megaminx = Mega.Mega()

    bigGreen = Side.Side("green")
    bigWhite = Side.Side("white")
    bigPurple = Side.Side("purple")
    bigBlue = Side.Side("blue")
    bigGold = Side.Side("gold")
    bigRed = Side.Side("red")
    bigLime = Side.Side("lime")
    bigSilver = Side.Side("silver")
    bigOrange = Side.Side("orange")
    bigYellow = Side.Side("yellow")
    bigNavy = Side.Side("navy")
    bigPink = Side.Side("pink")

    bigGreen.set_oppColor("lime")
    bigWhite.set_oppColor("silver")
    bigPurple.set_oppColor("pink")
    bigBlue.set_oppColor("navy")
    bigGold.set_oppColor("yellow")
    bigRed.set_oppColor("orange")
    bigLime.set_oppColor("green")
    bigSilver.set_oppColor("white")
    bigOrange.set_oppColor("red")
    bigYellow.set_oppColor("gold")
    bigNavy.set_oppColor("blue")
    bigPink.set_oppColor("purple")

    neighborList = [["white", "red", "gold", "blue", "purple"], ["yellow", "navy", "red", "green", "purple"],
                    ["yellow", "white", "green", "blue", "orange"], ["purple", "green", "gold", "silver", "orange"],
                    ["green", "red", "pink", "silver", "blue"], ["white", "navy", "pink", "gold", "green"],
                    ["navy", "yellow", "orange", "silver", "pink"], ["lime", "orange", "blue", "gold", "pink"],
                    ["yellow", "purple", "blue", "silver", "lime"], ["white", "purple", "orange", "lime", "navy"],
                    ["white", "yellow", "lime", "pink", "red"], ["navy", "lime", "silver", "gold", "red"]]
    sideList = [bigGreen, bigWhite, bigPurple, bigBlue, bigGold, bigRed, bigLime, bigSilver, bigOrange, bigYellow,
                   bigNavy, bigPink]

    megaminx.set_sides(sideList)
    resetMega(megaminx)

    for i in range(len(sideList)):
        for j in range(5):
            sideList[i].set_neighborColor(neighborList[i])

    for t in range(len(sideList)):
        setNodeNeighbors(sideList[t], neighborList[t])

    return megaminx


if __name__ == "__main__":

    megaminx = megaMaker()
    displayMega(megaminx)

    valid = False
    while valid != True:
        inputVal = input("Please enter a side number to rotate (0 through 11), enter r to randomize, enter t to test the puzzle solver, s to solve the current puzzle, or q to quit: ")
        valid = validator(inputVal)
    valid = False



    while inputVal != "q":
        if inputVal == "r":
            randomNum = input("Please enter the number of times to randomize: ")
            try:
                int(randomNum)
                randomize(megaminx, int(randomNum))
                displayMega(megaminx)
            except:
                print("That is not a valid input.")
                inputVal = input(
                    "Please enter a side number to rotate (0 through 11), enter r to randomize, enter t to test the puzzle solver, s to solve the current puzzle, or q to quit: ")
        elif inputVal == "t":
            testK()
        elif inputVal == "s":
            megaminx = copyMega(megaSolver(megaminx)[0])
            displayMega(megaminx)

        else:
            clockVal = input("Please enter c for clockwise, or cc for counter clockwise rotation (defaults to clockwise for other inputs): ")
            if clockVal == "cc":
                clockwise = False
            else:
                clockwise = True
            rotateSide(megaminx, int(inputVal), clockwise)
            displayMega(megaminx)
        while valid != True:
            inputVal = input(
                "Please enter a side number to rotate (0 through 11), enter r to randomize, enter t to test the puzzle solver, s to solve the current puzzle, or q to quit: ")
            valid = validator(inputVal)
        valid = False
