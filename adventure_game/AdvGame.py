# File: AdvGame.py

"""
This module defines the AdvGame class, which records the information
necessary to play a game.
"""
import math

from pgl import *
from AdvRoom import AdvRoom
from tokenscanner import TokenScanner
from AdvObject import AdvObject


###########################################################################
# Your job in this assignment is to fill in the definitions of the        #
# methods listed in this file, along with any helper methods you need.    #
# Unless you are implementing extensions, you won't need to add new       #
# public methods (i.e., methods called from other modules), but the       #
# amount of code you need to add is large enough that decomposing it      #
# into helper methods will be essential.                                  #
###########################################################################

# Constants
HELP_TEXT = [
    "Welcome to Adventure!",
    "Somewhere nearby is Colossal Cave, where others have found fortunes in",
    "treasure and gold, though it is rumored that some who enter are never",
    "seen again.  Magic is said to work in the cave.  I will be your eyes",
    "and hands.  Direct me with natural English commands; I don't understand",
    "all of the English language, but I do a pretty good job.",
    "",
    "It's important to remember that cave passages turn a lot, and that",
    "leaving a room to the north does not guarantee entering the next from",
    "the south, although it often works out that way.  You'd best make",
    "yourself a map as you go along.",
    "",
    "Much of my vocabulary describes places and is used to move you there.",
    "To move, try words like IN, OUT, EAST, WEST, NORTH, SOUTH, UP, or DOWN.",
    "I also know about a number of objects hidden within the cave which you",
    "can TAKE or DROP.  To see what objects you're carrying, say INVENTORY.",
    "To reprint the detailed description of where you are, say LOOK.  If you",
    "want to end your adventure, say QUIT."
]


class AdvGame:

    def __init__(self, prefix):
        """Reads the game data from files with the specified prefix."""
        self._rooms = AdvGame.readRooms(prefix + "Rooms.txt")
        self._objects = AdvGame.readObjects(prefix + "Objects.txt")
        self._inventoryNames = []
        self._synonyms = AdvGame.readSynonyms(prefix + "Synonyms.txt")
        self._gw = GWindow(1000, 600)

        self._keys = self.createKeys(1.5)
        self._lamp = self.createLamp(1.5)
        self._rod = self.createRod(1)
        self._bottle = self.createBottle(1)
        self._bird = self.createBird()
        self._nugget = self.createNugget()
        self._diamond = self.createDiamond()
        self._coins = self.createCoinBag()
        self._emerald = self.createEmerald()
        self._nest = self.createNest()
        self._plant = self.createPlant()
        self._chest = self.createChest()
        self._removableObjects = [self._keys, self._lamp, self._rod, self._bottle, self._bird, self._nugget, self._diamond, self._coins, self._emerald, self._nest, self._plant, self._chest]
        self._currentRoom = self.getRoom("OutsideBuilding")
        self._inventoryButton = self.createInventoryButton()
        self._inventoryPanel = self.createInventoryPanel()
        self._inventoryOpen = False
        self._objectInHand = ""
        self._waterButton = self.createWaterButton()
        self._jumpButton = self.createJumpButton()
        self._xyzzyButton = self.createXYZZYButton()
        self._plughButton = self.createPLUGHButton()
        self._waveButton = self.createWaveButton()
        self._starButton = self.createStarButton()
        self._swimButton = self.createSwimButton()
        self._actionButtons = [self._waveButton, self._swimButton, self._starButton, self._plughButton, self._xyzzyButton, self._jumpButton, self._waterButton]
        self._condensedPassages = []
        self._currentAction = ""
        self._upButton = self.createArrowButton("UP", 0)
        self._downButton = self.createArrowButton("DOWN", 180)
        self._northButton = self.createArrowButton("NORTH", 0)
        self._southButton = self.createArrowButton("SOUTH", 180)
        self._eastButton = self.createArrowButton("EAST", 270)
        self._westButton = self.createArrowButton("WEST", 90)
        self._inButton = self.createArrowButton("IN", 0)
        self._outButton = self.createArrowButton("OUT", 180)
        self._directionButtons = [self._upButton, self._downButton, self._northButton, self._southButton, self._eastButton, self._westButton, self._inButton, self._outButton]

    """
    Function: getRoom
    Returns a room object given the name of the room
    """
    def getRoom(self, name):
        return self._rooms[name]

    """
    Function: getNextRoom
    Given a current room and a user-specified direction, returns the next room that the user is moving to
    Checks passages from the current room that match the user's specified direction and the user's object inventory (if an object is needed for the passage)
    Calls self.checkForced() on the name of the passage destination to check if that room forces the user to another room
    """
    def getNextRoom(self, currentRoom, direction):
        passages = currentRoom.getPassages()
        for passage in passages:
            if passage[0] == direction:
                if passage[2] in self._inventoryNames or passage[2] is None:
                    return self.checkForced(passage[1])
        return None

    """
    Function: checkForced
    Takes in the name of a room and checks if that room forces the user to a different room without waiting for user input
    While the next room has passages with the direction "FORCED", determines which "FORCED" passage to push the user down (depending on if objects are needed and possessed)
    Updates the next room and checks if that next room has "FORCED" passages (continues looping until user reaches a room with no "FORCED" options)
    """
    def checkForced(self, roomName):
        next = self.getRoom(roomName)
        nextPassages = next.getPassages()

        while nextPassages[0][0] == "FORCED":
            for passage in nextPassages:
                if passage[2] in self._inventoryNames or passage[2] is None:
                    """Always prints the long description of the room with the forced passage"""
                    self.printLines(next.getLongDescription())
                    roomName = passage[1]
                    break
            if roomName == "EXIT": break
            next = self.getRoom(roomName)
            nextPassages = next.getPassages()
        return roomName

    """
    Function: placeInitialObjects
    Iterates through the objects dictionary read in from the objects.txt file and adds each object name to the room that was specified as the object's initial location
    If the object's initial location was "PLAYER", the object name is added to the inventory array instead of a room
    """
    def placeInitialObjects(self):
        for objectName in self._objects:
            object = self._objects[objectName]
            placementRoomName = object.getInitialLocation()
            if placementRoomName != "PLAYER":
                placementRoom = self.getRoom(placementRoomName)
                placementRoom.addObject(object.getName())
            else:
                self._inventoryNames.append(objectName)

    """
    Function: printRoomObjects
    Iterates through the array of object names for a specified room and prints their description so the user can see the objects in each room
    """
    def printRoomObjects(self, room):
        for objectName in room.getContents():
            description = self._objects[objectName].getDescription()
            print("There is " + description + " here.")

    """
    Function: printLines
    Iterates through a multi-line body of text and prints each line
    """
    def printLines(self, text):
        for line in text:
            print(line)

    """
    Function: subSynonym
    Takes in a word, checks if it is a synonym for a traditional game command, and if so, returns the traditional game command
    If no synonyms are found or it is already a traditional game command, returns the original word passed in
    """
    def subSynonym(self, word):
        if word in self._synonyms:
            return self._synonyms[word]
        return word

    """
    Function: takeObject
    Allows user to take an object by removing the object name from the current room and adding the object name to the player's inventory
    """
    def takeObject(self, scanner, room):
        space = scanner.nextToken()
        objectName = scanner.nextToken()
        objectName = self.subSynonym(objectName)
        if room.containsObject(objectName):
            room.removeObject(objectName)
            self._inventoryNames.append(objectName)
            print("Taken.")
        else:
            print("I don't understand that response.")

    """
    Function: dropObject
    Allows user to drop an object by removing the object name from the player's inventory and adding it to the object names array of the current room
    """
    def dropObject(self, scanner, room):
        space = scanner.nextToken()
        objectName = scanner.nextToken()
        objectName = self.subSynonym(objectName)
        if objectName in self._inventoryNames:
            self._inventoryNames.remove(objectName)
            room.addObject(objectName)
            print("Dropped.")
        else:
            print("I don't understand that response.")

    """
    Function: printInventory
    Allows the user to see their inventory by printing the description of all the objects they are carrying
    If there are no objects in their inventory, tell them they are empty-handed
    """
    def printInventory(self):
        if len(self._inventoryNames) == 0:
            print("You are empty-handed.")
        else:
            print("You are carrying:")
            for playerObjectName in self._inventoryNames:
                playerObject = self._objects[playerObjectName]
                print("\t" + playerObject.getDescription())

    def createKeys(self, scale):
        circle = GOval(0, 0, 30 * scale, 30 * scale)
        circle.set_color("Orange")
        circle.set_filled(True)

        rect = GRect(9 * scale, 15 * scale, 12 * scale, 50 * scale)
        rect.set_color("Orange")
        rect.set_filled(True)

        horiz1 = GRect(22 * scale, 55 * scale, 6.5 * scale, 5 * scale)
        horiz1.set_color("Orange")
        horiz1.set_filled(True)

        horiz2 = GRect(22 * scale, 47.5 * scale, 6.5 * scale, 5 * scale)
        horiz2.set_color("Orange")
        horiz2.set_filled(True)

        hole = GOval(10 * scale, 3 * scale, 10 * scale, 10 * scale)
        hole.set_color("White")
        hole.set_filled(True)

        keys = GCompound()
        keys.add(rect)
        keys.add(circle)
        keys.add(horiz1)
        keys.add(horiz2)
        keys.add(hole)

        return keys

    def createLamp(self, scale):
        frame = GRect(10 * scale, 30 * scale, 40 * scale, 60 * scale)
        frame.set_color("Brown")
        frame.set_filled(True)

        inside = GRect(15 * scale, 35 * scale, 30 * scale, 50 * scale)
        inside.set_color("White")
        inside.set_filled(True)

        bulbBody = GRect(27.5 * scale, 78 * scale, 5 * scale, 7 * scale)
        bulbBody.set_color("Orange")
        bulbBody.set_filled(True)

        bulb = GOval(20 * scale, 58 * scale, 20 * scale, 20 * scale)
        bulb.set_color("Orange")
        bulb.set_filled(True)

        lampTop = GRect(20 * scale, 20 * scale, 20 * scale, 10 * scale)
        lampTop.set_color("Brown")
        lampTop.set_filled(True)

        lampCircle = GOval(25 * scale, 13 * scale, 10 * scale, 10 * scale)
        lampCircle.set_color("Brown")
        lampCircle.set_filled(True)

        lampRing = GOval(20 * scale, 0 * scale, 20 * scale, 20 * scale)
        lampRing.set_color("Brown")
        lampRing.set_filled(False)

        light1 = GLine(0 * scale, 90 * scale, 20 * scale, 75 * scale)
        light1.set_color("Orange")

        light2 = GLine(0 * scale, 30 * scale, 20 * scale, 55 * scale)
        light2.set_color("Orange")

        light3 = GLine(60 * scale, 30 * scale, 40 * scale, 55 * scale)
        light3.set_color("Orange")

        light4 = GLine(60 * scale, 90 * scale, 40 * scale, 75 * scale)
        light4.set_color("Orange")

        lamp = GCompound()
        lamp.add(frame)
        lamp.add(inside)
        lamp.add(light1)
        lamp.add(light2)
        lamp.add(light3)
        lamp.add(light4)
        lamp.add(bulbBody)
        lamp.add(bulb)
        lamp.add(lampTop)
        lamp.add(lampCircle)
        lamp.add(lampRing)


        return lamp

    def createRod(self, scale):
        body = GRect(10 * scale, 0 * scale, 110 * scale, 20 * scale)
        body.set_color("Black")
        body.set_filled(True)

        top = GOval(110 * scale, 0 * scale, 20 * scale, 20 * scale)
        top.set_color("Black")
        top.set_filled(True)

        bottom = GOval(0 * scale, 0 * scale, 20 * scale, 20 * scale)
        bottom.set_color("Black")
        bottom.set_filled(True)

        star = GLabel("★", 20 * scale, 17 * scale)
        #star.set_font("13")
        #print(star.get_font())
        star.set_color("White")

        rod = GCompound()
        rod.add(body)
        rod.add(top)
        rod.add(bottom)
        rod.add(star)

        return rod

    def createBottle(self, scale):
        body = GRect(0 * scale, 30 * scale, 40 * scale, 100 * scale)
        body.set_color("Blue")
        body.set_filled(True)

        top = GOval(0 * scale, 15 * scale, 40 * scale, 40 * scale)
        top.set_color("Blue")
        top.set_filled(True)

        cap = GRect(10 * scale, 10 * scale, 20 * scale, 10 * scale)
        cap.set_color("Blue")
        cap.set_fill_color("White")
        cap.set_filled(True)

        label = GRect(0 * scale, 50 * scale, 40 * scale, 20 * scale)
        label.set_color("Blue")
        label.set_fill_color("White")
        label.set_filled(True)

        word = GLabel("🌊", 13 * scale, 63 * scale)

        bottle = GCompound()
        bottle.add(body)
        bottle.add(top)
        bottle.add(cap)
        bottle.add(label)
        bottle.add(word)

        return bottle

    def createBird(self):
        head = GOval(30, 50, 30, 30)
        head.set_color("Cyan")
        head.set_filled(True)

        beak = GOval(20, 60, 15, 7.5)
        beak.set_color("Orange")
        beak.set_filled(True)

        eye = GOval(37, 57, 7, 7)
        eye.set_color("Black")
        eye.set_filled(True)

        body = GOval(45, 60, 60, 40)
        body.set_color("Cyan")
        body.set_filled(True)

        wing1 = GOval(70, 30, 20, 50)
        wing1.set_color("Cyan")
        wing1.set_fill_color("Blue")
        wing1.set_filled(True)

        wing2 = GOval(65, 35, 20, 50)
        wing2.set_color("Cyan")
        wing2.set_fill_color("Blue")
        wing2.set_filled(True)

        bird = GCompound()
        bird.add(wing2)
        bird.add(beak)
        bird.add(head)
        bird.add(eye)
        bird.add(body)
        bird.add(wing1)

        return bird

    def createNugget(self):
        nugget = GOval(10, 10, 32, 40)
        nugget.set_color("Orange")
        nugget.set_fill_color("Yellow")
        nugget.set_filled(True)

        goldNugget = GCompound()
        goldNugget.add(nugget)

        return goldNugget

    def createDiamond(self):
        diamond = GOval(10, 10, 20, 30)
        diamond.set_color("Cyan")
        diamond.set_fill_color("White")
        diamond.set_filled(True)

        shine1 = GLine(0, 0, 10, 10)
        shine1.set_color("Cyan")

        shine2 = GLine(40, 0, 30, 10)
        shine2.set_color("Cyan")

        shine3 = GLine(0, 50, 10, 40)
        shine3.set_color("Cyan")

        shine4 = GLine(40, 50, 30, 40)
        shine4.set_color("Cyan")

        shinyDiamond = GCompound()
        shinyDiamond.add(diamond)
        shinyDiamond.add(shine1)
        shinyDiamond.add(shine2)
        shinyDiamond.add(shine3)
        shinyDiamond.add(shine4)

        return shinyDiamond

    def createCoinBag(self):
        bagBottom = GOval(0, 50, 70, 50)
        bagBottom.set_color("Brown")
        bagBottom.set_filled(True)

        bagTop = GOval(10, 25, 50, 50)
        bagTop.set_color("Brown")
        bagTop.set_filled(True)

        bagTie = GRect(20, 20, 30, 10)
        bagTie.set_color("Brown")
        bagTie.set_filled(True)

        coin1 = GOval(22, 15, 7.5, 7.5)
        coin1.set_color("Orange")
        coin1.set_filled(True)

        coin2 = GOval(30, 15, 7.5, 7.5)
        coin2.set_color("Orange")
        coin2.set_filled(True)

        coin3 = GOval(38, 15, 7.5, 7.5)
        coin3.set_color("Orange")
        coin3.set_filled(True)

        label = GLabel("COINS", 10, 80)
        label.set_color("White")

        bag = GCompound()
        bag.add(coin1)
        bag.add(coin2)
        bag.add(coin3)
        bag.add(bagBottom)
        bag.add(bagTop)
        bag.add(bagTie)
        bag.add(label)

        return bag

    def createEmerald(self):
        emerald = GOval(10, 10, 20, 30)
        emerald.set_color("Green")
        #diamond.set_fill_color("White")
        emerald.set_filled(True)

        shine1 = GLine(0, 0, 10, 10)
        shine1.set_color("Green")

        shine2 = GLine(40, 0, 30, 10)
        shine2.set_color("Green")

        shine3 = GLine(0, 50, 10, 40)
        shine3.set_color("Green")

        shine4 = GLine(40, 50, 30, 40)
        shine4.set_color("Green")

        shinyEmerald = GCompound()
        shinyEmerald.add(emerald)
        shinyEmerald.add(shine1)
        shinyEmerald.add(shine2)
        shinyEmerald.add(shine3)
        shinyEmerald.add(shine4)

        return shinyEmerald

    def createNest(self):
        nest = GRect(0, 50, 100, 50)
        nest.set_color("Brown")
        nest.set_filled(True)

        egg1 = GOval(5, 30, 22, 30)
        egg1.set_color("Orange")
        egg1.set_fill_color("White")
        egg1.set_filled(True)

        egg2 = GOval(30, 30, 22, 30)
        egg2.set_color("Orange")
        egg2.set_fill_color("White")
        egg2.set_filled(True)

        egg3 = GOval(55, 30, 22, 30)
        egg3.set_color("Orange")
        egg3.set_fill_color("White")
        egg3.set_filled(True)

        egg4 = GOval(80, 30, 19, 30)
        egg4.set_color("Orange")
        egg4.set_fill_color("White")
        egg4.set_filled(True)

        eggNest = GCompound()
        eggNest.add(egg1)
        eggNest.add(egg2)
        eggNest.add(egg3)
        eggNest.add(egg4)
        eggNest.add(nest)

        return eggNest

    def createPlant(self):
        stem = GRect(30, 10, 10, 90)
        stem.set_color("Green")
        stem.set_filled(True)

        stem1 = GRect(7.5, 29, 25, 10)
        stem1.set_color("Green")
        stem1.set_filled(True)

        stem2 = GRect(40, 50, 25, 10)
        stem2.set_color("Green")
        stem2.set_filled(True)

        leaf1 = GOval(0, 10, 15, 30)
        leaf1.set_color("Green")
        leaf1.set_filled(True)

        leaf2 = GOval(54, 35, 15, 30)
        leaf2.set_color("Green")
        leaf2.set_filled(True)

        label = GLabel("WATER!!", 0, 0)
        label.set_color("Black")

        plant = GCompound()
        plant.add(stem)
        plant.add(leaf1)
        plant.add(stem1)
        plant.add(stem2)
        plant.add(leaf2)
        plant.add(label)

        return plant

    def createChest(self):
        bottom = GRect(0, 30, 120, 80)
        bottom.set_color("Black")
        bottom.set_fill_color("Brown")
        bottom.set_filled(True)

        top = GOval(0, 0, 120, 60)
        top.set_color("Black")
        top.set_fill_color("Brown")
        top.set_filled(True)

        lock = GRect(45, 22.5, 30, 15)
        lock.set_color("Yellow")
        lock.set_filled(True)

        chest = GCompound()
        chest.add(top)
        chest.add(bottom)
        chest.add(lock)

        return chest

    def takeScreenObject(self, objectToRemove):

        if objectToRemove == self._keys:
            objectName = "KEYS"
        elif objectToRemove == self._lamp:
            objectName = "LAMP"
        elif objectToRemove == self._rod:
            objectName = "ROD"
        elif objectToRemove == self._bottle:
            objectName = "WATER"
        elif objectToRemove == self._bird:
            objectName = "BIRD"
        elif objectToRemove == self._nugget:
            objectName = "NUGGET"
        elif objectToRemove == self._diamond:
            objectName = "DIAMOND"
        elif objectToRemove == self._coins:
            objectName = "COINS"
        elif objectToRemove == self._emerald:
            objectName = "EMERALD"
        elif objectToRemove == self._nest:
            objectName = "EGGS"
        elif objectToRemove == self._plant:
            objectName = "PLANT"
        elif objectToRemove == self._chest:
            objectName = "CHEST"

        if self._currentRoom.containsObject(objectName):
            self._gw.remove(objectToRemove)
            self._currentRoom.removeObject(objectName)
            self._inventoryNames.append(objectName)
            print("Taken.")
        elif objectName in self._inventoryNames:
            self._gw.remove(objectToRemove)
            print("Ready to drop.")
            self._inventoryNames.remove(objectName)
            self._objectInHand = objectName
        else:
            print("I don't understand that response.")

    def dropScreenObject(self, posX, posY):
        if self._objectInHand == "KEYS":
            self._gw.add(self._keys, posX, posY)
        elif self._objectInHand == "LAMP":
            self._gw.add(self._lamp, posX, posY)
        elif self._objectInHand == "ROD":
            self._gw.add(self._rod, posX, posY)
        elif self._objectInHand == "WATER":
            self._gw.add(self._bottle, posX, posY)
        elif self._objectInHand == "BIRD":
            self._gw.add(self._bird, posX, posY)
        elif self._objectInHand == "NUGGET":
            self._gw.add(self._nugget, posX, posY)
        elif self._objectInHand == "DIAMOND":
            self._gw.add(self._diamond, posX, posY)
        elif self._objectInHand == "COINS":
            self._gw.add(self._coins, posX, posY)
        elif self._objectInHand == "EMERALD":
            self._gw.add(self._emerald, posX, posY)
        elif self._objectInHand == "EGGS":
            self._gw.add(self._nest, posX, posY)
        elif self._objectInHand == "PLANT":
            self._gw.add(self._plant, posX, posY)
        elif self._objectInHand == "CHEST":
            self._gw.add(self._chest, posX, posY)

        self._currentRoom.addObject(self._objectInHand)
        self._objectInHand = ""
        print("Dropped.")


    def createInventoryButton(self):
        button = GRect(0, 0, 150, 30)
        button.set_color("Black")
        button.set_fill_color("Red")
        button.set_filled(True)

        label = GLabel("INVENTORY", 30, 21.5)
        label.set_color("Black")

        inventoryButton = GCompound()
        inventoryButton.add(button)
        inventoryButton.add(label)
        inventoryButton.label = label

        return inventoryButton

    def createInventoryPanel(self):
        panel = GRect(0, 0, 200, 580)
        panel.set_color("Red")
        panel.set_fill_color("White")
        panel.set_filled(True)

        return panel

    def displayInventory(self):

        if not self._inventoryOpen:
            self._gw.remove(self._inventoryButton)
            self._inventoryButton.label.set_label("CLOSE")
            self._gw.add(self._inventoryPanel, 10, 10)
            self._gw.add(self._inventoryButton)

            for objectName in self._inventoryNames:
                if objectName == "KEYS":
                    self._gw.add(self._keys, 20, 20)
                elif objectName == "LAMP":
                    self._gw.add(self._lamp, 100, 20)
                elif objectName == "ROD":
                    self._gw.add(self._rod, 20, 100)
                elif objectName == "WATER":
                    self._gw.add(self._bottle, 100, 100)
                elif objectName == "BIRD":
                    self._gw.add(self._bird, 20, 180)
                elif objectName == "NUGGET":
                    self._gw.add(self._nugget, 100, 180)
                elif objectName == "DIAMOND":
                    self._gw.add(self._diamond, 20, 260)
                elif objectName == "COINS":
                    self._gw.add(self._coins, 100, 260)
                elif objectName == "EMERALD":
                    self._gw.add(self._emerald, 20, 340)
                elif objectName == "EGGS":
                    self._gw.add(self._nest, 100, 340)
                elif objectName == "PLANT":
                    self._gw.add(self._plant, 20, 420)
                elif objectName == "CHEST":
                    self._gw.add(self._chest, 100, 420)

            self._inventoryOpen = True
        else:
            self._inventoryButton.label.set_label("INVENTORY")
            self._gw.remove(self._inventoryPanel)

            for objectName in self._inventoryNames:
                if objectName == "KEYS":
                    self._gw.remove(self._keys)
                elif objectName == "LAMP":
                    self._gw.remove(self._lamp)
                elif objectName == "ROD":
                    self._gw.remove(self._rod)
                elif objectName == "WATER":
                    self._gw.remove(self._bottle)
                elif objectName == "BIRD":
                    self._gw.remove(self._bird)
                elif objectName == "NUGGET":
                    self._gw.remove(self._nugget)
                elif objectName == "DIAMOND":
                    self._gw.remove(self._diamond)
                elif objectName == "COINS":
                    self._gw.remove(self._coins)
                elif objectName == "EMERALD":
                    self._gw.remove(self._emerald)
                elif objectName == "EGGS":
                    self._gw.remove(self._nest)
                elif objectName == "PLANT":
                    self._gw.remove(self._plant)
                elif objectName == "CHEST":
                    self._gw.remove(self._chest)

            self._inventoryOpen = False

    def storeAction(self, clickedObject):
        if clickedObject.label.get_label() in self._condensedPassages:
            self._currentAction = clickedObject.label.get_label()
        else:
            self._currentAction = ""


    def clickAction(self, e):
        posX = e.get_x()
        posY = e.get_y()
        clickedObject = self._gw.get_element_at(posX, posY)

        if clickedObject in self._removableObjects:
            self.takeScreenObject(clickedObject)
        elif clickedObject == self._inventoryButton:
            self.displayInventory()
        elif clickedObject in self._actionButtons or clickedObject in self._directionButtons:
            self.storeAction(clickedObject)
        elif self._objectInHand != "":
            self.dropScreenObject(posX, posY)

    def displayRoomObjects(self, room):
        for objectName in room.getContents():

            if objectName == "KEYS":
                self._gw.add(self._keys, 200, 100)
            elif objectName == "LAMP":
                self._gw.add(self._lamp, 200, 300)
            elif objectName == "ROD":
                self._gw.add(self._rod, 300, 200)
            elif objectName == "WATER":
                self._gw.add(self._bottle, 300, 400)
            elif objectName == "BIRD":
                self._gw.add(self._bird, 400, 100)
            elif objectName == "NUGGET":
                self._gw.add(self._nugget, 400, 300)
            elif objectName == "DIAMOND":
                self._gw.add(self._diamond, 500, 200)
            elif objectName == "COINS":
                self._gw.add(self._coins, 500, 400)
            elif objectName == "EMERALD":
                self._gw.add(self._emerald, 600, 100)
            elif objectName == "EGGS":
                self._gw.add(self._nest, 600, 300)
            elif objectName == "PLANT":
                self._gw.add(self._plant, 700, 200)
            elif objectName == "CHEST":
                self._gw.add(self._chest, 700, 400)

    def createWaterButton(self):
        button = GRect(0, 0, 150, 30)
        button.setColor("Black")
        button.set_fill_color("Blue")
        button.set_filled(True)

        label = GLabel("WATER", 0, 0)
        label.set_color("White")

        labelX = (button.getWidth() - label.getWidth()) / 2
        labelY = (button.getHeight() + label.getAscent()) / 2

        label.setLocation(labelX, labelY)

        waterButton = GCompound()
        waterButton.add(button)
        waterButton.add(label)
        waterButton.background = button
        waterButton.label = label

        return waterButton

    def createJumpButton(self):
        button = GRect(0, 0, 150, 30)
        button.setColor("Black")
        button.set_fill_color("Orange")
        button.set_filled(True)

        label = GLabel("JUMP", 0, 0)
        label.set_color("White")

        labelX = (button.getWidth() - label.getWidth()) / 2
        labelY = (button.getHeight() + label.getAscent()) / 2

        label.setLocation(labelX, labelY)

        jumpButton = GCompound()
        jumpButton.add(button)
        jumpButton.add(label)
        jumpButton.background = button
        jumpButton.label = label

        return jumpButton

    def createXYZZYButton(self):
        button = GRect(0, 0, 150, 30)
        button.setColor("Black")
        button.set_fill_color("Yellow")
        button.set_filled(True)

        label = GLabel("XYZZY", 0, 0)
        label.set_color("Black")

        labelX = (button.getWidth() - label.getWidth()) / 2
        labelY = (button.getHeight() + label.getAscent()) / 2

        label.setLocation(labelX, labelY)

        XYZZYButton = GCompound()
        XYZZYButton.add(button)
        XYZZYButton.add(label)
        XYZZYButton.background = button
        XYZZYButton.label = label

        return XYZZYButton

    def createPLUGHButton(self):
        button = GRect(0, 0, 150, 30)
        button.setColor("Black")
        button.set_fill_color("Purple")
        button.set_filled(True)

        label = GLabel("PLUGH", 0, 0)
        label.set_color("White")

        labelX = (button.getWidth() - label.getWidth()) / 2
        labelY = (button.getHeight() + label.getAscent()) / 2

        label.setLocation(labelX, labelY)

        PLUGHButton = GCompound()
        PLUGHButton.add(button)
        PLUGHButton.add(label)
        PLUGHButton.background = button
        PLUGHButton.label = label

        return PLUGHButton

    def createWaveButton(self):
        button = GRect(0, 0, 150, 30)
        button.setColor("Black")
        button.set_fill_color("Pink")
        button.set_filled(True)

        label = GLabel("WAVE", 0, 0)
        label.set_color("White")

        labelX = (button.getWidth() - label.getWidth()) / 2
        labelY = (button.getHeight() + label.getAscent()) / 2

        label.setLocation(labelX, labelY)

        waveButton = GCompound()
        waveButton.add(button)
        waveButton.add(label)
        waveButton.background = button
        waveButton.label = label

        return waveButton

    def createStarButton(self):
        button = GRect(0, 0, 30, 30)
        button.setColor("Black")
        button.set_fill_color("Brown")
        button.set_filled(True)

        label = GLabel("*", 0, 0)
        label.set_color("White")

        labelX = (button.getWidth() - label.getWidth()) / 2
        labelY = (button.getHeight() + label.getAscent()) / 2

        label.setLocation(labelX, labelY)

        starButton = GCompound()
        starButton.add(button)
        starButton.add(label)
        starButton.background = button
        starButton.label = label

        return starButton


    def createSwimButton(self):
        button = GRect(0, 0, 100, 30)
        button.setColor("Black")
        button.set_fill_color("Cyan")
        button.set_filled(True)

        label = GLabel("SWIM", 0, 0)
        label.set_color("White")

        labelX = (button.getWidth() - label.getWidth()) / 2
        labelY = (button.getHeight() + label.getAscent()) / 2

        label.setLocation(labelX, labelY)

        swimButton = GCompound()
        swimButton.add(button)
        swimButton.add(label)
        swimButton.background = button
        swimButton.label = label

        return swimButton

    def createArrowButton(self, label, theta):
        arrow_body = GRect(-10, 80, 50, 20)
        arrow_body.setColor("Gray")
        arrow_body.set_fill_color("Gray")
        arrow_body.set_filled(True)
        arrow_body.rotate(90)

        label = GLabel(label, 0, 0)
        label.set_color("Black")

        labelX = (arrow_body.getWidth() - label.getWidth()) / 2 - 8
        labelY = (arrow_body.getHeight() + label.getAscent()) / 2

        label.setLocation(labelX, labelY)

        arrowBody = GCompound()
        arrowBody.add(arrow_body)

        arrowhead = GPolygon()
        arrowhead.add_vertex(0, 0)
        arrowhead.add_vertex(15, -30)
        arrowhead.add_vertex(-15, -30)
        arrowhead.setColor("Gray")
        arrowhead.set_fill_color("Gray")
        arrowhead.set_filled(True)
        arrowhead.rotate(180)
        arrowButton = GCompound()
        arrowButton.rotate(theta)
        arrowBody.add(label)
        arrowButton.add(arrowhead)
        arrowButton.add(arrowBody)
        arrowButton.label = label
        arrowButton.body = arrow_body
        arrowButton.head = arrowhead
        return arrowButton

    def displayButtons(self, room):
        passages = room.getPassages()
        self._condensedPassages = []

        for passage in passages:
            if passage[0] not in self._condensedPassages:
                self._condensedPassages.append(passage[0])

        if "WATER" in self._condensedPassages:
            self._waterButton.background.set_fill_color("Blue")
        else:
            self._waterButton.background.set_fill_color("Gray")

        if "JUMP" in self._condensedPassages:
            self._jumpButton.background.set_fill_color("Orange")
        else:
            self._jumpButton.background.set_fill_color("Gray")

        if "XYZZY" in self._condensedPassages:
            self._xyzzyButton.background.set_fill_color("Yellow")
        else:
            self._xyzzyButton.background.set_fill_color("Gray")

        if "PLUGH" in self._condensedPassages:
            self._plughButton.background.set_fill_color("Purple")
        else:
            self._plughButton.background.set_fill_color("Gray")

        if "WAVE" in self._condensedPassages:
            self._waveButton.background.set_fill_color("Pink")
        else:
            self._waveButton.background.set_fill_color("Gray")

        if "SWIM" in self._condensedPassages:
            self._swimButton.background.set_fill_color("Cyan")
        else:
            self._swimButton.background.set_fill_color("Gray")

        if "*" in self._condensedPassages:
            self._starButton.background.set_fill_color("Brown")
        else:
            self._starButton.background.set_fill_color("Gray")

        if "UP" in self._condensedPassages:
            self._upButton.body.set_fill_color("Pink")
            self._upButton.head.set_fill_color("Pink")
        else:
            self._upButton.body.set_fill_color("Gray")
            self._upButton.head.set_fill_color("Gray")

        if "DOWN" in self._condensedPassages:
            self._downButton.body.set_fill_color("Pink")
            self._downButton.head.set_fill_color("Pink")
        else:
            self._downButton.body.set_fill_color("Gray")
            self._downButton.head.set_fill_color("Gray")

        if "NORTH" in self._condensedPassages:
            self._northButton.body.set_fill_color("Pink")
            self._northButton.head.set_fill_color("Pink")
        else:
            self._northButton.body.set_fill_color("Gray")
            self._northButton.head.set_fill_color("Gray")

        if "SOUTH" in self._condensedPassages:
            self._southButton.body.set_fill_color("Pink")
            self._southButton.head.set_fill_color("Pink")
        else:
            self._southButton.body.set_fill_color("Gray")
            self._southButton.head.set_fill_color("Gray")

        if "WEST" in self._condensedPassages:
            self._westButton.body.set_fill_color("Pink")
            self._westButton.head.set_fill_color("Pink")
        else:
            self._westButton.body.set_fill_color("Gray")
            self._westButton.head.set_fill_color("Gray")

        if "EAST" in self._condensedPassages:
            self._eastButton.body.set_fill_color("Pink")
            self._eastButton.head.set_fill_color("Pink")
        else:
            self._eastButton.body.set_fill_color("Gray")
            self._eastButton.head.set_fill_color("Gray")

        if "OUT" in self._condensedPassages:
            self._outButton.body.set_fill_color("Pink")
            self._outButton.head.set_fill_color("Pink")
        else:
            self._outButton.body.set_fill_color("Gray")
            self._outButton.head.set_fill_color("Gray")

        if "IN" in self._condensedPassages:
            self._inButton.body.set_fill_color("Pink")
            self._inButton.head.set_fill_color("Pink")
        else:
            self._inButton.body.set_fill_color("Gray")
            self._inButton.head.set_fill_color("Gray")

        self._gw.add(self._waterButton, 225, 550)
        self._gw.add(self._jumpButton, 500, 550)
        self._gw.add(self._xyzzyButton, 665, 550)
        self._gw.add(self._plughButton, 830, 550)
        self._gw.add(self._waveButton, 500, 500)
        self._gw.add(self._swimButton, 665, 500)
        self._gw.add(self._starButton, 830, 500)
        self._gw.add(self._upButton, 500, 10)
        self._gw.add(self._downButton, 470, 590)
        self._gw.add(self._northButton, 450, 10)
        self._gw.add(self._southButton, 415, 590)
        self._gw.add(self._eastButton, 970, 300)
        self._gw.add(self._westButton, 20, 300)
        self._gw.add(self._inButton, 450, 270)
        self._gw.add(self._outButton, 510, 350)


    def run(self):
        """Plays the adventure game stored in this object."""

        # MAKE STARTING GLABEL INSTRUCTIONS AND SUCH!!
        print("Welcome to Adventure!")
        current = "OutsideBuilding"
        room = self.getRoom(current)
        self.printLines(room.getLongDescription())
        room.setVisited(True)

        """Places all the objects in their initial locations and prints the objects for the starting room"""
        self.placeInitialObjects()
        self.printRoomObjects(room)

        self._currentRoom = room
        print(self._currentRoom.getContents())
        self._gw.add_event_listener("click", self.clickAction)
        image = GImage(current + ".png", 0, 0)
        self._gw.add(image)
        self.displayRoomObjects(room)
        self._gw.add(self._inventoryButton, 50, 550)
        self.displayButtons(room)

        while current != "EXIT":
            """Stores user input, uses TokenScanner to break user input into tokens, checks for token synonyms"""
            #self._gw.add_event_listener("click", self.clickAction)
            #print(self._currentAction)

            if self._currentAction != "":
                token = self._currentAction
                self._currentAction = ""
            else:
                verb = input("> ").strip().upper()
                scanner = TokenScanner(verb)
                token = scanner.nextToken()
                token = self.subSynonym(token)

            """Checks if user input is any of the built-in action verbs and carries out corresponding functions"""
            if token == "QUIT": quit()
            elif token == "HELP":
                self.printLines(HELP_TEXT)
            elif token == "LOOK":
                self.printLines(room.getLongDescription())
                self.printRoomObjects(room)
            elif token == "TAKE":
                self.takeObject(scanner, room)
            elif token == "DROP":
                self.dropObject(scanner, room)
            elif token == "INVENTORY":
                self.printInventory()
            else:
                """If user input isn't one of the built-in action verbs, then it is likely a motion verb and they are trying to move rooms"""
                """Use their motion verb to get the next room, and print the short vs. long description based on if the room has been visited and print the objects in the room"""

                next = self.getNextRoom(room, token)
                if next is None:
                    print("I don't understand that response.")
                else:
                    self._gw.remove(image)
                    current = next
                    if current == "EXIT": break
                    room = self.getRoom(current)
                    self._currentRoom = room
                    if room.hasBeenVisited():
                        print(room.getShortDescription())
                    else:
                        self.printLines(room.getLongDescription())
                        room.setVisited(True)

                    image = GImage(current + ".png", 0, 0)
                    self._gw.add(image)
                    self.printRoomObjects(room)
                    self.displayRoomObjects(room)
                    self._gw.add(self._inventoryButton)
                    self.displayButtons(room)
                    #print(self._currentRoom.getContents())

    """
    Function: readRooms
    Opens the given file and continues reading through the room descriptions and creating AdvRoom objects (by calling readRoom) until the end of the file
    Adds each room to the rooms dictionary with the room name as the key and the AdvRoom object as the value
    """
    @staticmethod
    def readRooms(f):
        rooms = {}
        with open(f) as file:
            while True:
                room = AdvRoom.readRoom(file)
                if room is None: break
                name = room.getName()
                rooms[name] = room
        return rooms

    """
    Function: readObjects
    Opens the given file and continues reading through the object descriptions and creating AdvObject objects (by calling readObject) until the end of the file
    Adds each object to the objects dictionary with the object name as the key and the AdvObject object as the value
    Since some game versions don't have objects, if there is no objects.txt file to open, an empty objects dictionary is returned
    """
    @staticmethod
    def readObjects(f):
        objects = {}
        try:
            with open(f) as file:
                while True:
                    object = AdvObject.readObject(file)
                    if object is None: break
                    name = object.getName()
                    objects[name] = object
        except IOError:
            objects = {}
        return objects

    """
    Function: readSynonyms
    Opens the given file and continues reading through the synonym pairs until the end of the file
    Adds each pair to a synonyms dictionary with the abbreviation/alternate word as the key and the traditional game command as the value
    Since some game versions don't support synonyms, if there is no synonyms.txt file to open, an empty synonyms dictionary is returned
    """
    @staticmethod
    def readSynonyms(f):
        synonyms = {}
        try:
            with open(f) as file:
                while True:
                    pair = file.readline().rstrip()
                    if pair == "": break
                    synonym = pair[:pair.find("=")]
                    fullCommand = pair[pair.find("=") + 1:]
                    synonyms[synonym] = fullCommand
        except IOError:
            synonyms = {}
        return synonyms
