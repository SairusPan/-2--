#阶段1
import random

DEF_DIFFIC = 10
MAX_TRIALS = 20
MAX_VALUE = 99
OPERATORS = "+-*%"
EQUALITY = "="
DIGITS = "0123456789"
NOT_POSSIBLE = "No FoCdle found of that difficulty"

def create_secret(difficulty=DEF_DIFFIC):
    '''
    Use a random number function to create a FoCdle instance of length 
    `difficulty`. The generated equation will be built around three values 
    each from 1 to 99, two operators, and an equality.
    '''
    count = 0
    expression = ""
    while count <= MAX_TRIALS:
        # Randomly selecting the three values and operators
        expression = str(random.randint(1, MAX_VALUE))
        expression += random.choice(OPERATORS)
        expression += str(random.randint(1, MAX_VALUE))
        expression += random.choice(OPERATORS)
        expression += str(random.randint(1, MAX_VALUE))
        # Evaluating the string using eval
        evaluated = eval(expression)
        expression += EQUALITY
        # Adding the evaluated string result at the end
        expression += str(evaluated)
        # Conditionals for the length of string and values
        if len(expression) == difficulty and evaluated > 0 and evaluated != 0:
            return(expression)
        else:
            # Looping through again if the Focdle does not meet requirements
            count += 1
        if count > MAX_TRIALS:
            return(NOT_POSSIBLE)
#阶段2
GREEN = "green"
YELLO = "yellow"
GREYY = "grey"
def set_colors(secret, guess):
    '''
    Compares the latest `guess` equation against the unknown `secret` one. 
    Returns a list of three-item tuples, one tuple for each character position 
    in the two equations:
        -- a position number within the `guess`, counting from zero;
        -- the character at that position of `guess`;
        -- one of "green", "yellow", or "grey", to indicate the status of
           the `guess` at that position, relative to `secret`.
    The return list is sorted by position.
    '''
    from itertools import groupby
    color_list = []
    repeated_list = []
    green_list = []
    secret_list = []
    content_list = []
    repeated_chars = []
    # Assigning greens
    for i in range(len(secret)):
        for h in range(len(guess)):
            if secret[i] == guess[h] and i == h:
                color_list.append((h, guess[h], GREEN))
                # Adding characters assigned green to a list
                green_list.append(guess[h])
    # Removing characters assigned green for reference
    for components in secret:
        secret_list.append(components)
    for expressions in green_list:
        secret_list.remove(expressions)
    remain = "".join(secret_list)
    for a in range(len(secret)):
        for b in range(len(guess)):
            # Assigning repeated characters to repeated_list
            # Assigning yellows and greys
            if (secret[a] != guess[b] and a == b and guess[b] in secret 
                and guess.count(guess[b]) == 1):
                color_list.append((b, guess[b], YELLO))
            # Repeated character and one of them was assigned green
            # while no green or yellow matches in remaining secret string
            if (secret[a] != guess[b] and a == b and guess[b] not in remain 
                and guess[b] in green_list and guess.count(guess[b]) > 1):
                color_list.append((b, guess[b], GREYY))
            # Repeated character and there is yellow match in secret string
            if (secret[a] != guess[b] and a == b and guess[b] in remain 
                and guess[b] in green_list and guess.count(guess[b]) > 1):
                repeated_list.append((b, guess[b]))
            # If repeated and none of them is green match
            if (secret[a] != guess[b] and a == b and guess[b] in secret
                and guess[b] not in green_list and guess.count(guess[b]) > 1):
                repeated_list.append((b, guess[b]))
                repeated_list = sorted(repeated_list)
    # Grouping repeated characters in repeated_list
    grouped = groupby(repeated_list, lambda repeated_list: repeated_list[1])
    for category, contents in grouped:
        content_list.append(tuple(contents))
    for y in range(len(content_list)):
        repeat = content_list[y]
        # Case for only 1 repeated character
        if len(repeat) == 1:
            for sets in repeat:
                color_list.append(tuple(sets) + (YELLO,))
        # Case for multiple repeated characters
        if len(repeat) > 1:
            for digit in repeat:
                repeated_chars.append(digit)
            # Assigning the leftmost character yellow
            color_list.append(tuple(repeated_chars[0]) + (YELLO,))
            # Assigning the rest grey
            for rest in repeated_chars[1:]:
                color_list.append(tuple(rest) + (GREYY,))
    # Assigning greys
    for c in range(len(secret)):
        for d in range(len(guess)):
            # General case for grey
            if secret[c] != guess[d] and c == d and guess[d] not in secret:
                color_list.append((d, guess[d], GREYY))
    return(sorted(color_list))

#阶段3
GREEN = "green"
YELLO = "yellow"
GREYY = "grey"
def passes_restrictions(guess, all_info):
    '''
    Tests a `guess` equation against `all_info`, a list of known restrictions, 
    one entry in that list from each previous call to set_colors(). Returns 
    True if that `guess` complies with the collective evidence imposed by 
    `all_info`; returns False if any violation is detected. Does not check the 
    mathematical accuracy of the proposed candidate equation.
    '''
    from itertools import groupby
    info = []
    info_list = []
    remain = []
    remove_green = []
    remove_yellow = []
    remain_yellow = []
    green_list = []
    yellow_list = []
    dictionary  ={}
    # Remain is the list used to delete characters assigned green
    for characters in guess:
        remain.append(characters)
    # Remain_yellow is the list used to delete characters 
    # assigned green and yellow
    for characters in guess:
        remain_yellow.append(characters)
    if len(all_info) == 0:
        return True
    for groups in all_info:
        info.append(groups)
        # Nested loop to find each tuples in all_info
        for information in info:
            for tuples in information:
                # Appending all tuples in all_info to a list
                info_list.append(tuples)
                # Sorting the list for grouping
                info_list=sorted(info_list, key=lambda info_list: info_list[2])
            # Grouping information by colors
            grouped = groupby(info_list, lambda info_list: info_list[2])
    for category, contents in grouped:
        dictionary[category] = list(contents)
    # Adding characters assigned green to a list
    for greens in dictionary[GREEN]:
        if guess[greens[0]] == greens[1]:
            green_list.append(greens)
    # Using set to remove repeated green characters
    green_set = set(green_list)
    for green_index in green_set:
        # Adding indexes to be removed into list
        remove_green.append(green_index[0])
    for indexes in sorted(remove_green, reverse=True):
        # Deleting characters assigned green
        del remain[indexes]
        # Case for returning false for green
        if guess[greens[0]] != greens[1]:
            return False
        # Case for all green matches
        if guess[greens[0]] == greens[1] and len(remain) == 0:
            return True
    # Adding characters assigned yellow to a list
    for yellows in dictionary[YELLO]:
        if guess[yellows[0]] != yellows[1] and yellows[1] in remain:
            yellow_list.append(yellows)
    # Using set to remove repeated yellow characters
    yellow_set = set(yellow_list)
    for yellow_index in yellow_set:
        # Adding indexes to be removed into remove_yellow
        remove_yellow.append(yellow_index[0])
    # Adding yellow and green characters index to be removed
    remove_yellow = set(remove_green + remove_yellow)
    remove_yellow = list(remove_yellow)
    for indexes in sorted(remove_yellow, reverse=True):
        # Deleting characters assigned yellow and green
        del remain_yellow[indexes]
        # Case for returning false for yellow
        if guess[yellows[0]] == yellows[1] and yellows[1] in remain:
            return False
        if guess[yellows[0]] == yellows[1] and yellows[1] not in remain:
            return False
        if guess[yellows[0]] != yellows[1] and yellows[1] not in remain:
            return False
    for greys in dictionary[GREYY]:
        # Case for returning false for grey
        if guess[greys[0]] == greys[1] and greys[1] not in remain_yellow:
            return False
        if guess[greys[0]] != greys[1] and greys[1] in remain_yellow:
            return False
        if guess[greys[0]] == greys[1] and greys[1] in remain_yellow:
            return False
        else:
            return True