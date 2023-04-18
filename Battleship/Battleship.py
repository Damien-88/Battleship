import pandas as pd
import os
from time import sleep

# Class that handles user interaction with each other and the board.;
class Player:

    def __init__(self, new_name):
        
        self.name = new_name
        
        # Stores the attack coordinates;
        self.target = "00"
        
        # Stores the locations the user places each piece;
        self.location_dict = {"Carrier": [], "Battleship": [], "Cruiser": [], "Submarine": [], "Destroyer": []}
        
        # Stores a list of spaces that contain a piece;
        self.locations = []

        # Piece names and sizes;
        self.pieces = ("Carrier", "Battleship", "Cruiser", "Submarine", "Destroyer")
        self.sizes = (5, 4, 3, 3, 2)
        
        # List of available targets with sub lists of each row;
        self.available_targets = [
            ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10"],
            ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10"],
            ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10"],
            ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10"],
            ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", "E10"],
            ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10"],
            ["G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10"],
            ["H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H10"],
            ["I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8", "I9", "I10"],
            ["J1", "J2", "J3", "J4", "J5", "J6", "J7", "J8", "J9", "J10"]
            ]

    def __repr__(self):
        stats = """
            "Location Dictionary: {} \n
            "Locations: {} \n
            "Target: {} \n
            "Available Targets: \n
            """.format(
                self.location_dict, 
                self.locations, 
                self.target
            )
        for entry in self.available_targets:
            stats += str(entry) + "\n"

        return stats

    # Method for selecting an available target to attack
    def attack(self):

        index = 0
        row = ""
        available = False

        while not available:
            # Take in coordinates for attack.
            coordinates = input("\n\n\tEnter the coordinates for your attack: ")
            self.target = coordinates.capitalize()
            
            # Loop through available targets to check if available
            for sublist in self.available_targets:
                if self.target in sublist: 
                    # Remove from available targets
                    index = self.available_targets.index(sublist)
                    self.available_targets[index].remove(self.target)
                    available = True

                    return self.target
                    
            if not available: # Show available. Continue loop
                print("\n\tInvalid target. Please enter an available target\n")
                print("\tAvailable targets: ")
                for i in self.available_targets:
                    row += "\n\t"
                    for h in i:
                        row += h + "  "
                print(row)

    # Method for selecting locations for each piece
    def choose(self):

        # Loop through each piece
        for x in range(0, len(self.pieces)):

            check = True

            # Loop to allow user to select a new position if selection is invalid
            while check:
                # Lists to store the Row Letter and Column #, toggle availability
                char = []
                num = []
                handy = True

                # Lists to store sorted num & char. Dict to give char a value
                char_ref = {
                    "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9, "J": 10
                    }

                # Asks for number of spaces oppropriate for indicated piece
                piece = input(
                    "\n\t" + self.name + " enter " + 
                    str(self.sizes[x]) + " spaces for your " + 
                    self.pieces[x] + ": "
                    )
                piece = piece.upper()
                piece = piece.split(",")
                for item in range(0, len(piece)):
                    piece[item] = piece[item].strip()
                
                # Verify the correct number of spaces was chosen
                if len(piece) == self.sizes[x]:
                    # Loop to separate & append Row & Col lists with each selection
                    for p in piece:
                        char.append(p[0])
                        num.append(p[1:])
                        # Loop through locations to check if space has been taken.
                        for t in self.locations:
                            if p in t:
                                print("\n\tPieces Overlap!\n\n")
                                handy = False
                else:
                    if len(piece) < self.sizes[x]:
                        print("\n\tNot Enough Spaces Selected! Ensure entries are separated by commas.\n\n")
                    else:
                        print("\n\tToo Many Spaces Selected!\n\n")
                    handy = False
                
                # Change num types to int
                num_int = []
                for s in num:
                    num_int.append(int(s))

                # Sort coordinate Letters & Numbers in Descending order
                sorted_num = sorted(num_int, reverse = True)
                sorted_char = sorted(char, reverse = True)

                # Variables to hold the previous element in the loop
                temp_num = sorted_num[0]
                temp_let = char_ref[sorted_char[0]]

                # Loop through sorted num list to check for skipped spaces
                for n in range(1, len(sorted_num)):
                    if temp_num - sorted_num[n] != 1:
                        for l in range(1, len(sorted_char)):
                            if temp_let - char_ref[sorted_char[l]] != 1:
                                print("\n\tInvalid entry! Cannot skip spaces.\n\n")
                                handy = False
                                break
                            else:
                                temp_let = char_ref[sorted_char[l]]
                        break
                    else:
                        temp_num = sorted_num[n]
                
                # Actions if all chosen spaces are available.
                if handy:
                    # Check if selection is Vertical. 
                    inquire = pd.unique(char)
                    if len(inquire) == len(char):
                        inquire = pd.unique(num)
                        # Verify selection is Linear. Place piece. Exit loop
                        if len(inquire) == 1:
                            self.placement(self.pieces[x], piece)
                            self.locations.append(piece)
                            check = False
                        # If Not Linear, ouput message and continue Loop
                        else:
                            print("\n\tInvalid entry! Ensure selection is a linear path.\n\n")
                    # Check if selection is Horizontal
                    elif len(inquire) == 1:
                        inquire = pd.unique(num)
                        # Verify selection is Linear. Place piece. Exit loop
                        if len(inquire) == len(num):
                            self.placement(self.pieces[x], piece)
                            self.locations.append(piece)
                            check = False
                        # If Not Linear, ouput message and continue Loop
                        else:
                            print("\n\tInvalid entry! Ensure selection is a linear path.\n\n")
                    # If Neither, ouput message and continue Loop
                    else:
                        print("\n\tInvalid entry! Ensure selection is a linear path.\n\n")
    
    # Method for placing pieces in the dictionary
    def placement(self, new_piece, new_location):
        for p in self.pieces:
            if p == new_piece:
                self.location_dict[new_piece] = new_location
                break

    # Method for removing location selections.
    def reset_choices(self):
        self.location_dict = {"Carrier": [], "Battleship": [], "Cruiser": [], "Submarine": [], "Destroyer": []}
        self.locations = []
        
# Class that handles activity on the board
class Board:

    # Method taking in Player Objects and setting Attributes
    def __init__(self, new_player, other_player):

        # Sets which player is Attacking & which is Defending
        self.attacker = new_player.name
        self.defender = other_player.name

        # List containing Current Layout
        self.panel_list = [[], [], [], [], [], [], [], [], [], []]

        # Visualization of Current Layout of indicated Player Side
        self.header = "\t" + self.attacker 
        self.layout = ""
        
        # Import Defender Piece Locations
        self.hit_dict = other_player.location_dict
        self.hit_list = other_player.locations

        # Import Attacker Target
        self.aim = ""

        # Lists holding Remaining Spaces for each Piece
        self.carrier = self.hit_dict["Carrier"]
        self.battleship = self.hit_dict["Battleship"]
        self.cruiser = self.hit_dict["Cruiser"]
        self.submarine = self.hit_dict["Submarine"]
        self.destroyer = self.hit_dict["Destroyer"]
        
        # List of Sunk Pieces
        self.downed = []

    def __repr__(self):
        stats = """
            "Hit Dictionary: {} \n
            "Hit List: {} \n
            "Coordinate: {} \n
            "Carrier: {} \n
            "Battleship: {} \n
            "Cruiser: {} \n
            "Submarine: {} \n
            "Destroyer: {} \n
            """.format(
            self.hit_dict,
            self.hit_list,
            self.aim,
            self.carrier,
            self.battleship,
            self.cruiser,
            self.submarine,
            self.destroyer
            )
        return stats

    # Method for Default Board layout
    def panel(self):

        list_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        list_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        for letter in range(0, len(list_letters)):
            for number in list_numbers:
                self.panel_list[letter].append(list_letters[letter] + str(number))

        self.mark_panel()
    
    # Method for Updating Board Display
    def mark_panel(self):

        self.layout = ""

        for l in self.panel_list:
            self.layout += "\n\n\t"
            for i in l:
                self.layout += i + "    "
    
    # Method verifying Hit or Miss
    def hit_miss(self, new_target):

        self.aim = new_target
        area = 0
        there = False

        # Loop trough list of piece locations.
        for loc in self.hit_list:
            # Check if Piece is in Target location
            for l in loc:
                if self.aim == l:
                    # If it is, Remove Space from hit_list.
                    area = loc
                    there = True
                    loc.remove(l)
                    break
        if there:
            # Update Board. Call Hit functions
            print("\n\tHit")
            self.blowed_up()
            self.good_hit(area)

        elif not there:
             print("\n\tMiss")
    
    # Method for Updating Board with Affirmative Hits
    def blowed_up(self):

        # Variable for Hit indication
        hit = "X "

        # Find Board Locationand Update Layout
        if self.aim[0] == "A":
            self.panel_list[0][int(self.aim[1:])-1] = hit
        elif self.aim[0] == "B":
            self.panel_list[1][int(self.aim[1:])-1] = hit
        elif self.aim[0] == "C":
            self.panel_list[2][int(self.aim[1:])-1] = hit
        elif self.aim[0] == "D":
            self.panel_list[3][int(self.aim[1:])-1] = hit
        elif self.aim[0] == "E":
            self.panel_list[4][int(self.aim[1:])-1] = hit
        elif self.aim[0] == "F":
            self.panel_list[5][int(self.aim[1:])-1] = hit
        elif self.aim[0] == "G":
            self.panel_list[6][int(self.aim[1:])-1] = hit
        elif self.aim[0] == "H":
            self.panel_list[7][int(self.aim[1:])-1] = hit
        elif self.aim[0] == "I":
            self.panel_list[8][int(self.aim[1:])-1] = hit
        elif self.aim[0] == "J":
            self.panel_list[9][int(self.aim[1:])-1] = hit
        
        # Update Display
        self.mark_panel()

    # Method for handling Hits 
    def good_hit (self, location):
        # Find coinsiding Piece Remove Space from it's list.
        if location == 0:
            self.carrier.remove(self.aim)
            self.hit_dict["Carrier"].remove(self.aim)
        elif location == 1:
            self.battleship.remove(self.aim)
            self.hit_dict["Battleship"].remove(self.aim)
        elif location == 2:
            self.cruiser.remove(self.aim)
            self.hit_dict["Cruiser"].remove(self.aim)
        elif location == 3:
            self.submarine.remove(self.aim)
            self.hit_dict["Submarine"].remove(self.aim)
        elif location == 4:
            self.destroyer.remove(self.aim)
            self.hit_dict["Destroyer"].remove(self.aim)
        
        # Check piece status 
        self.check_status()
    
    # Method for checking Status of each piece
    def check_status(self):

        # If no spaces left Call Sank for that piece
        if not any(self.carrier) and "Carrier" not in self.downed:
            self.sank(1)
        elif not any(self.battleship) and "Battleship" not in self.downed:
            self.sank(2)
        elif not any(self.cruiser) and "Cruiser" not in self.downed:
            self.sank(3)
        elif not any(self.submarine) and "Submarine" not in self.downed:
            self.sank(4)
        elif not any(self.destroyer) and "Destroyer" not in self.downed:
            self.sank(5)

 
    # Method for handling Sunken Piece
    def sank(self, new_piece):

        if new_piece == 1:
            self.downed.append("Carrier")
            print("\n\t" + self.attacker + " sank " + self.defender + "'s Carrier!\n")
        elif new_piece == 2:
            self.downed.append("Battleship")
            print("\n\t" + self.attacker + " sank " + self.defender + "'s Battleship!\n")
        elif new_piece == 3:
            self.downed.append("Cruiser")
            print("\n\t" + self.attacker + " sank " + self.defender + "'s Cruiser!\n")
        elif new_piece == 4:
            self.downed.append("Submarine")
            print("\n\t" + self.attacker + " sank " + self.defender + "'s Submarine!\n")
        elif new_piece == 5:
            self.downed.append("Destroyer")
            print("\n\t" + self.attacker + " sank " + self.defender + "'s Destroyer!\n")

        sleep(2)
    
    # Method for handling Game Over
    def game_over(self):

        if len(self.downed) == 5:
            print("\n\tGAME OVER\n\n")
            sleep(2)
            return False
        else:
            return True

# Game Play
jump = "\n" * 4        
new_game = True
def clear():
   os.system('cls')

# Title Layout
title = """
\tBBBBBB    AAA   TTTTTTTTTTTTTTT L       EEEEEEE   SSSSS  H     H IIIIIII PPPPPP
\tB     B  A   A     T       T    L       E        S     S H     H    I    P     P
\tB     B A     A    T       T    L       E        S       H     H    I    P     P
\tBBBBBB  AAAAAAA    T       T    L       EEEEE     SSSSS  HHHHHHH    I    PPPPPP
\tB     B A     A    T       T    L       E              S H     H    I    P    
\tB     B A     A    T       T    L       E        S     S H     H    I    P
\tBBBBBB  A     A    T       T    LLLLLLL EEEEEEE   SSSSS  H     H IIIIIII P
"""

while new_game:

    clear()

    game_on = True
    wrong = True
    coordinates = ""
    lines = ""

    # Output Title
    print(jump + title)

    name_1 = input(jump + "\tFirst Player. Enter a Name: ")
    name_2 = input("\n\n\tSecond Player. Enter a Name: ")

    if len(name_1) == 0:
        name_1 = "Player One"

    if len(name_2) == 0:
        name_2 = "Player Two"

    clear()

    # Setup First Player Object
    first = Player(name_1)

    # Setup Second Player Object
    second = Player(name_2)

    # Output Selection Reference
    for l in first.available_targets:
        lines += "\n\n\t"
        for c in l:
            lines += c + "    "

    print(jump + lines + "\n")

    # Set First Player's Piece Locations
    first.choose()

    clear()

    # Output Selection Reference
    print(jump + lines + "\n")

    # Set Second Player's Piece Locations
    second.choose()

    clear()

    # Setup First Player Board
    board_1 = Board(first, second)
    board_1.panel()

    # Setup Second Player Board
    board_2 = Board(second, first)
    board_2.panel()

    # Turn Loop for Gamplay
    while game_on:

        # Display Defending Board
        print(jump + board_1.header)
        print(board_1.layout)

        # First Player Attack
        open_fire = first.attack()

        # Check Contact
        board_1.hit_miss(open_fire)

        # Verification
        #print("\n", board_1, "\n")
        #print("\n", second, "\n")

        # Check for Game Over
        game_on = board_1.game_over()
        if not game_on:
            clear()
            print(jump + board_1.header + " WINS!")
            print(board_2.layout)
            break

        sleep(1)
        clear()

        # Display Defending Board
        print(jump + board_2.header)
        print(board_2.layout)

        # Second Player Attack
        open_fire = second.attack()

        # Check Contact
        board_2.hit_miss(open_fire)

        # Verification
        #print("\n", board_2, "\n")
        #print("\n", second, "\n")

        # Check for Game Over
        game_on = board_2.game_over()
        if not game_on:
            clear()
            print(jump + board_2.header + " WINS!")
            print(board_2.layout)
            break

        sleep(1)
        clear()
    
    while wrong:
        new = input(jump + "\tStart a New Game? Y/N: ")
        new = new.lower()

        if new == "y":
            wrong = False
            new_game = True
        elif new == "n":
            wrong = False
            new_game = False
            break
        else:
            print("\n\n\tEnter Y for yes N for No")

# Quick Setup
# a1, a2, a3, a4, a5
# b7, c7, d7, e7
# j9, j7, j6
# h8, h7, h6
# f2, g2

# b1, c1, d1, e1, f1
# a10, b10, c10, d10
# g4, g5, g6
# f5, f6, f7
# e5, e6