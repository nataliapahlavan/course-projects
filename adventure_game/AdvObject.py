# File: AdvObject.js

"""
This module defines a class that models an object in Adventure.
"""

###########################################################################
# Your job in this assignment is to fill in the definitions of the        #
# methods listed in this file, along with any helper methods you need.    #
# You won't need to work with this file until Milestone #4.  In my        #
# solution, none of the milestones required any public methods beyond     #
# the ones defined in this starter file.                                  #
###########################################################################

class AdvObject:

    def __init__(self, name, description, location):
        """Creates an AdvObject from the specified properties."""
        self._name = name
        self._description = description
        self._location = location

    def getName(self):
        """Returns the name of this object."""
        return self._name

    def getDescription(self):
        """Returns the description of this object."""
        return self._description

    def getInitialLocation(self):
        """Returns the initial location of this object."""
        return self._location

    """
    Function: readObject
    Reads through the given text of a file, reads in the unique attributes for each object, and uses them to create and return an AdvObject object
    Reads in the first line as the object name, second line as the object description, and third line as the object's location (scans fourth blank line to move onto next object)
    """
    @staticmethod
    def readObject(f):
        name = f.readline().rstrip()
        if name == "":
            return None
        description = f.readline().rstrip()
        location = f.readline().rstrip()
        blank = f.readline().rstrip()
        return AdvObject(name, description, location)
