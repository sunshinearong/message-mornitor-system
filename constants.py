# COMP1040: The Craft of Computing
#
# This file defines enumerated types and constants that are used throughout the simulation. You
# may add additional constants to this file.
#

from enum import IntEnum

class PersonalityType(IntEnum):
    CHATTY = 0
    QUIET = 1

class MessageType(IntEnum):
    RED = 0
    GREEN = 1
    BLUE = 2

