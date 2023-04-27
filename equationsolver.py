import os
import keyboard
import traceback
import sys
import re

debug = False

print("Please wait. initalizing")
# initalize essential definitions

def waitForKeyUnpress(key):
    while True:
        if not keyboard.is_pressed(key):
            return()

def clear():
 
    if os.name == 'nt':
        os.system('cls')

    else:
        os.system('clear')
 
def equationCreate():
    ff = open("equations.txt", "a")
    clear()
    Name = ""
    while True:
        name = input("Please enter a equation name. ")
        if len(name) <= 18 and not name == "":
            break
        else:
            clear()
            if not name == "":
                print("Please enter a name less than 19 characters long.")
    while not len(name) == 19: # makes name 19 characters long
        name = name + " "
    name = name + "| "
    description = input("Please enter a description for your equation. ")
    name = name + description
    equation = input("Please enter your equation seperated by spaces: ").replace("^", "**")
    equation = list(equation.split(" "))
    toadd = []
    toadd.append("\n!m!\n")
    toadd.append(name + "\n")
    toadd.append("!m!\n")
    for i in equation:
        toadd.append(i + "\n")
    toadd.append("!e!" + "\n")
    for i in toadd:
        ff.write(i)
    ff.close

if not os.path.isfile("equations.txt"):
    ans = ""
    while True:
        if ans == "y" or ans == "n":
            break
        clear()
        print("\x1b[3;30;47m" + "It appears you have no equations created. Would you like to make one now? (y/n) " + "\x1b[0;37;40m")
        ans = input("")
    if ans == "n":
        exit()
    else:
        ff = open("equations.txt", "a")
        equationCreate()

# create variables

ff = open("equations.txt", "r")
formsnoclean = []
forms = []
for i in ff:
    formsnoclean.append(i)
ff.close()
forms = [x[:-1] for x in formsnoclean] # removes newline
names = []
equations = []
variableNames = []
variableNamesToAdd = ''
index = 0

#define functions

def error(text):
    print("\x1b[0;30;41m" + text + "\x1b[0;37;40m")

def warn(text):
    print("\x1b[0;30;43m" + text + "\x1b[0;37;40m")

def grabData():
    i = 0
    while i < len(forms):
        if "!m" in forms[i]:
            i += 1
            names.append(forms[i])
            i += 1
            equationToCombine = ''
            variableNamesToAdd = ''
            while not "!e" in forms[i + 1]:
                i += 1
                if forms[i].isalpha() == True:
                    variableNamesToAdd = variableNamesToAdd + forms[i] + ','
                equationToCombine = equationToCombine + forms[i]

            variableNamesToAdd = variableNamesToAdd[:-1] # removes last comma
            variableNames.append(variableNamesToAdd)
            equations.append(equationToCombine)

        i += 1     

try: # tries to grab data from equations.txt
    grabData()
except:
    clear()
    error("Your equations appear to be malformed or corrupted. Please double check your equations file. \nDebug data is written below.")
    print('Forms:')
    print(forms)
    print('equations:')
    print(equations)
    print(i)
    traceback.print_exc()
    os.system("pause")
    exit()

def renderNames():
    clear()
    i = 0
    while i < len(names):
        if index == i:
            print("\x1b[0;30;47m" + names[i] + "\x1b[0;37;40m")
        else:
            print(names[i])
        i = i + 1
    if debug:
        print(index)

names.append("Create new equation| Creates a equation")

if debug:
    print(forms)
    print(names)
    print(equations)
    print(variableNames)
    os.system("pause")

def executeequation():
    while True:
        copiedequation = equations[index]
        vars = list(variableNames[index].split(','))
        global var
        for i in vars:
            var = input(i + ": ")
            if var.lower() == 'exit': break
            if not re.search('[a-zA-Z]', var) == None or var == "":
                while not re.search('[a-zA-Z]', var) == None or var == "":
                    clear()
                    if not var == "": print("Please enter a valid number.")
                    var = input(i + ": ")
                    if var.lower() == 'exit': break
            copiedequation = copiedequation.replace(i, var)
        if var.lower() == 'exit':
            break
        clear()
        print(eval(copiedequation))

# user gui to select equation

renderNames()

while True:
    while True: # key detection
        if keyboard.is_pressed("down"): break
        if keyboard.is_pressed("up"): break
        if keyboard.is_pressed("enter"): break
    #code to execute based on key press
    if keyboard.is_pressed("enter"):
        waitForKeyUnpress("enter")
        if index == len(names) - 1:
            equationCreate()
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            while True:
                try:
                    executeequation()
                except: # fixes weird input executing bug
                    traceback.print_exc()
                    warn("There was a problem executing the equation " + equations[index])
                if var.lower() == "exit":
                    waitForKeyUnpress("enter")
                    renderNames()
                    break

    if keyboard.is_pressed("down"):
        if not index == len(names) - 1:
            index += 1
            renderNames()
        waitForKeyUnpress("down")

    if keyboard.is_pressed("up"):
        if not index == 0:
            index -= 1
            renderNames()
        waitForKeyUnpress("up")