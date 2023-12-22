#The file where the funcstacker came from.. Yes, I am aware Python has a few obscure functions that mirror mine..#
from time import sleep as wait #DON'T QUESTION IT!!
import keyboard
#import mouse
#This is a compilation of useful library functions.

def letter(string: str, char: str):
    '''Return the occurances of a singular character in a string.
    
    -   string: String to operate upon
    -   char: Singular character to find'''
    if len(char) != 1:
        raise(ValueError, "More than one character to search for was provided. As of now, the function can only handle searching for singular characters.")
    num = 0
    length = len(string)
    for i in range(length):
        if string[i].lower() == char.lower():
            num += 1
    return num

def send(input: str, sendkey: str = 'enter', waittime: float = 0.05):
    '''Input a message and then send it. (In theory, at least.)
    -   input: str      | The message to input.
    -   sendkey: str    | The key to press after the message is written.
    -   waittime: float | The time to wait between pressing and releasing sendkey.'''
    keyboard.write(input)
    keyboard.press(sendkey)
    wait(waittime)
    keyboard.release(sendkey)

def sendmsg(input: str, firstkey: str = 'enter', sendkey: str = 'enter', waittime: float = 0.05):
    '''Press a key, input a message, then send it (In theory, at least.)
    -   input: str      | The message to input.
    -   firstkey: str   | The key to press before the message is writtne.
    -   sendkey: str    | The key to press after the message is written.
    -   waittime: float | The time to wait between pressing and releasing sendkey at the start then end.'''
    keyboard.press(firstkey)
    wait(waittime)
    keyboard.release(firstkey)
    keyboard.write(input)
    keyboard.press(sendkey)
    wait(waittime)
    keyboard.release(sendkey)


def findinstance(path: str, instance: str, mode: int = 0):
   '''Find an instance within a file. Depending on the mode it will do something different.
   -  path: str     | The file path to look for. No try/catch for this one.
   -  instance: str | The instance within the file to look for.
   -  mode: int = 0 | The mode. 0 will count how many times the instance occurs, 1 will return the lines it occurs in, 2 will return the lines it occurs in with the indices of the instance.'''
   count: int = 0
   instances: list = []
   modes = [0, 1, 2]
   if mode not in modes:
       raise ValueError(f"The mode provided for function 'findinstance' ({mode}) is invalid. Mode can be: {modes}")
   with open(path, "r") as file:
       for line in file:
           if mode == 0:
               if instance in line.strip():
                  count += 1
           elif mode == 1:
               if instance in line.strip():
                  instances.append(line.strip())
           elif mode == 2:
               if instance in line.strip():
                  start_index = line.strip().index(instance)
                  end_index = start_index + len(instance)
                  instances.append(f'{start_index}: {line.strip()} :{end_index}')
   if mode == 0:
       return count
   elif mode == 1:
       return instances
   elif mode == 2:
       return instances
   
def dbin(num: int, target: int = 4, debug: bool = False):
    '''Custom D2B. Uses inbuilt bin() but strips it away and fixes it to your target.'''
    b2 = bin(num)[2:]
    n = len(b2)
    filled = target - n
    if debug:
        print(b2, n, filled)
    if filled > 0:
        b2 = '0' * filled + b2
    return b2

def dhex(num: int, target: int = 2, debug: bool = False):
    '''Custom H2D. uses inbuilt hex() but strips it away and fixes it to your target.'''
    h2 = hex(num)[2:]
    n = len(h2)
    filled = target - n
    if debug:
        print(h2, n, filled)
    if filled > 0:
        h2 = '0' * filled + h2
    return h2

def bitsize(num: int, target: int = 4):
    '''Check the size of something converted to binary in bits.'''
    return len(dbin(num, target)) #that is really simple

def bitcomp(num: int, compare: int = 4):
    '''Return True if the binary equivelent of the number is in the specified range, else return false.'''
    return True if len(dbin(num, compare)) == compare else False #one liner!!

def funcstacker(*functions):
    '''The boss fight of functions. Takes the output of anything it is given (including non functions) and puts them into one (string) output seperated by spaces.'''
    combined = ""
    for func in functions:
        if callable(func):
            combined += str(func()) + " "
        else:
            combined += str(func) + " "
    return combined.strip()
