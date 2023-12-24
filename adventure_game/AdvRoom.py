# File: AdvRoom.py

"""
This module is responsible for modeling a single room in Adventure.
"""

###########################################################################
# Your job for Milestone #1 is to fill in the definitions of the         #
# methods listed in this file, along with any helper methods you need.    #
# The public methods shown in this file are the ones you need for         #
# Milestone #1.  You will need to add other public methods for later      #
# milestones, as described in the handout.  For Milestone #7, you will    #
# need to move the getNextRoom method into the AdvGame class and replace  #
# it with a getPassages method that returns the dictionary of passages.   #
###########################################################################

# Constants

MARKER = "-----"

class AdvRoom:

    def __init__(self, name, shortdesc, longdesc, passages):
        """Creates a new room with the specified attributes."""
        self._name = name
        self._shortdesc = shortdesc
        self._longdesc = longdesc
        self._passages = passages
        self._visited = False
        self._objectNames = []

    def getName(self):
        """Returns the name of this room."""
        return self._name

    def getShortDescription(self):
        """Returns a one-line short description of this room."""
        return self._shortdesc

    def getLongDescription(self):
        """Returns the list of lines describing this room."""
        return self._longdesc

    def getNextRoom(self, verb):
        """Returns the name of the destination room after applying verb."""
        next = self._passages.get(verb, None)
        if next is None:
            next = self._passages.get("*", None)
        return next

    def getPassages(self):
        """Returns the array of tuples for each passage that connects to this room"""
        return self._passages

    def setVisited(self, visited):
        """Sets the visited flag for this room to the parameter boolean"""
        self._visited = visited

    def hasBeenVisited(self):
        """Returns the visited flag for this room (True or False)"""
        return self._visited

    def addObject(self, objectName):
        """Adds the given object name to this room's list of contained object names"""
        self._objectNames.append(objectName)

    def removeObject(self, objectName):
        """Removes the given object name from this room's list of contained object names"""
        self._objectNames.remove(objectName)

    def containsObject(self, objectName):
        """Checks if the given object name is in this room's list of contained object names and returns the corresponding boolean (True or False)"""
        return objectName in self._objectNames

    def getContents(self):
        """Returns the array of this room's contained object names"""
        return self._objectNames.copy()

    """
    Function: readRoom
    Reads through the given text of a file, reads in the unique attributes for each room, and uses them to create and return an AdvRoom object
    Reads in the first line as the name, the second line as the short description, and everything from there till the marker as the long description
    Creates a passages array by reading each passage line and creating a tuple of the direction of the passage, the destination the passage leads to, and the key object if there is one
    """
    @staticmethod
    def readRoom(f):
        name = f.readline().rstrip()
        if name == "":
            return None
        shortdesc = f.readline().rstrip()
        longdesc = []
        while True:
            line = f.readline().rstrip()
            if line == MARKER: break
            longdesc.append(line)
        passages = []
        while True:
            line = f.readline().rstrip()
            if line == "": break
            """Find the colon in the line and set direction to everything before the colon"""
            colon = line.find(":")
            if colon == -1:
                raise ValueError("Missing colon in " + line)
            direction = line[:colon].strip().upper()
            """Find the slash in the line; if no slash, destination is everything after the colon and there is no key object
               If there is a slash, destination is everything between the colon and the slash, and the key object is everything after the slash"""
            slash = line.find("/")
            if slash == -1:
                destination = line[colon + 1:].strip()
                key = None
            else:
                destination = line[colon + 1:slash].strip()
                key = line[slash + 1:].strip()
            passages.append((direction, destination, key))
        return AdvRoom(name, shortdesc, longdesc, passages)


