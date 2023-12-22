import generaluselib as glib #Required, a custom made library.
from math import ceil


         #### UNIVERSAL ASSEMBLER ####
        
      # ! # N O T  A N  E M U L A T O R # ! #
      # ! # N O T  A N  E M U L A T O R # ! #
      # ! # N O T  A N  E M U L A T O R # ! #
      # ! # N O T  A N  E M U L A T O R # ! #
   
   # DO NOT CHANGE ANYTHING NOT MARKED FOR USER #

#User variables#

mode = "bin" #'bin', 'hex'
outmethod = "combined" #'split', 'combined'
askuser = True #Ask the user for the file paths
askuser2 = True #Ask the user for the mode and outmethod variables
filepath = "test.ird"
filepath2 = "out.irdb"

debug = False

#Code variables#
cpuname = "Iridium"
linecount = 512
sizeKiB = linecount/1024 #do not even think about touching this value
filext = ".ird" #the dots are required!
filextb = ".irdb"

splitt = ""
combined = ""

if isinstance(mode, str) and isinstance(outmethod, str) and isinstance(filepath, str) and isinstance(filepath2, str) and isinstance(askuser, bool) and isinstance(askuser2, bool) and isinstance(debug, bool):
    if mode not in ["bin", "hex"]:
        raise ValueError("Mode variable was given an invalid value.")
    if outmethod not in ["split", "combined"]:
        raise ValueError("Outmethod variable was given an invalid value.")
else:
    raise TypeError("The user defined variables weren't even the right type. (They need to be str.)")

# User ISA #

isa = {
    "MULTI": ("00000", ["bin1", "bin1", "bin1"]), #Binary Opcode | Operand[Number of bits]
    "ADD":  ("00001", ["dec4"]),
    "SUB":  ("00010", ["dec4"]),
    "LDI":  ("00011", ["dec4", "dec8"]),
    "LIA":  ("00100", ["dec8"]),
    "ADR":  ("00101", ["dec4"]),
    "SBR":  ("00110", ["dec4"]),
    "AND":  ("00111", ["dec4"]),
    "OR":   ("01000", ["dec4"]),
    "XOR":  ("01001", ["dec4"]),
    "LOAD": ("01010", ["dec4"]),
    "STORE":("01011", ["dec4"]),
    "IN":   ("01100", ["dec4"]),
    "OUT":  ("01101", ["dec4"]),
    "CMP":  ("01110", ["dec4"]),
    "JMP":  ("01111", ["dec9"]),
    "BRCH": ("10000", ["dec3", "dec9"]),
    "ADC":  ("10001", ["dec4"]),
    "SBB":  ("10010", ["dec4"]),
    "NAND": ("10011", ["dec4"]),
    "NOR":  ("10100", ["dec4"]),
    "XNOR": ("10101", ["dec4"]),
    "INC":  ("10110", []),
    "DEC":  ("10111", []),
    "SHIFT":("11000", ["bin1"]),
    "BSB":  ("11001", ["dec4"]),
    "RLD":  ("11010", ["dec4"]),
    "RST":  ("11011", ["dec4"])
}

if askuser == True:
    print(f"What is the file path to the input .ird file? (From root.)")
    filepath = input("Enter here: ")
    print("What should the output file be named? (Accepts paths, by default relative to root.)")
    filepath2 = input("Enter here: ")
if askuser2 == True:
    print("What is the preferred output mode? (bin, hex)")
    mode = input("Enter here: ")
    print("How should the assembler output? One big number or split lines? (combined, split)")
    outmethod = input("Enter here: ")

if glib.letter(filepath, ".") == 0:
    filepath += filext
else:
    if filepath[filepath.index("."):] != filext:
        raise NameError(f"The provided file was not a supported format. ({filepath[:filepath.index('.')+1]})")
if glib.letter(filepath2, ".") == 0:
    filepath2 += filextb
else:
    if filepath2[filepath2.index("."):] != filextb:
        raise NameError(f"The provided output file was not a supported format. ({filepath2[:filepath2.index('.')+1]})")

with open(filepath, "r") as file:
    lines = file.readlines()
    if len(lines) != 0:
        if len(lines) < 512:
            for lnum, line in enumerate(lines, start=1):
                line = line.strip()
                if debug:
                    print(f"Processing line {lnum} (containing '{line}')")
                split = line.split()
                instr = split[0]
                if instr.upper() in isa:
                    if debug:
                        print("Line was in ISA instructions.")
                    bop, opfrm = isa[instr.upper()]
                    if len(split)-1 != len(opfrm):
                        raise SyntaxError(f"MismatchedOperandsError at line {lnum}: Expecting {len(opfrm)}, got {len(split)-1}")
                    if mode == "bin":
                        combined += bop
                        splitt += bop + " "
                    if mode == "hex":
                        combined += glib.dhex(int(bop,2),2)
                        splitt += glib.dhex(int(bop,2),2) + " "
                    if debug:
                        print("Going into match statement..")
                    match len(opfrm):
                        case 0:
                            splitt = splitt[:-1] + "\n"
                        case 1:
                            if mode.lower() == "bin":
                                if glib.funcstacker(glib.bitcomp(int(split[1]),int(opfrm[0][-1:]))) == "True":
                                    combined += glib.dbin(int(split[1]),int(opfrm[0][-1:]))
                                    splitt += glib.dbin(int(split[1]),int(opfrm[0][-1:])) + "\n"
                                else:
                                    raise SyntaxError(f"InvalidOperandError at line {lnum}: Input for operand 1 greater than integer limit of operand in decimal ({glib.intlimit(opfrm[0][-1:])}).")
                            elif mode.lower() == "hex":
                                if glib.funcstacker(glib.bitcomp(int(split[1]),int(opfrm[0][-1:]))) == "True":
                                    combined += glib.dhex(int(split[1]),ceil(int(opfrm[0][-1:])/4))
                                    splitt += glib.dhex(int(split[1]),ceil(int(opfrm[0][-1:])/4)) + "\n"
                                else:
                                    raise SyntaxError(f"InvalidOperandError at line {lnum}: Input for operand 1 greater than integer limit of operand in decimal ({glib.intlimit(opfrm[0][-1:])}).")
                        case 2:
                            if mode.lower() == "bin":
                                if glib.funcstacker(glib.bitcomp(int(split[1]),int(opfrm[0][-1:])),glib.bitcomp(int(split[2]),int(opfrm[1][-1:]))) == "True True":
                                    combined += glib.dbin(int(split[1]),int(opfrm[0][-1:]))+glib.dbin(int(split[2]),int(opfrm[1][-1:]))
                                    splitt += glib.dbin(int(split[1]),int(opfrm[0][-1:]))+" "+glib.dbin(int(split[2]),int(opfrm[1][-1:])) + "\n"
                                else:
                                    raise SyntaxError(f"InvalidOperandError at line {lnum}: Input for operand 2 greater than integer limit of operand in decimal ({glib.intlimit(opfrm[1][-1:])}).")
                            elif mode.lower() == "hex":
                                if glib.funcstacker(glib.bitcomp(int(split[1]),int(opfrm[0][-1:])),glib.bitcomp(int(split[2]),int(opfrm[1][-1:]))) == "True True":
                                    combined += glib.dhex(int(split[1]),ceil(int(opfrm[0][-1:])/4))+glib.dhex(int(split[2]),ceil(int(opfrm[1][-1:])/4))
                                    splitt += glib.dhex(int(split[1]),ceil(int(opfrm[0][-1:])/4))+" "+glib.dhex(int(split[2]),ceil(int(opfrm[1][-1:])/4)) + "\n"
                                else:
                                    raise SyntaxError(f"InvalidOperandError at line {lnum}: Input for operand 2 greater than integer limit of operand in decimal ({glib.intlimit(opfrm[1][-1:])}).")
                        case 3:
                            if mode.lower() == "bin":
                                if glib.funcstacker(glib.bitcomp(int(split[1]),int(opfrm[0][-1:])),glib.bitcomp(int(split[2]),int(opfrm[1][-1:])),glib.bitcomp(int(split[3]),int(opfrm[2][-1:]))) == "True True True":
                                    combined += glib.dbin(int(split[1]),int(opfrm[0][-1:]))+glib.dbin(int(split[2]),int(opfrm[1][-1:]))+glib.dbin(int(split[2]),int(opfrm[2][-1:]))
                                    splitt += glib.dbin(int(split[1]),int(opfrm[0][-1:]))+" "+glib.dbin(int(split[2]),int(opfrm[1][-1:]))+" "+glib.dbin(int(split[2]),int(opfrm[2][-1:])) + "\n"
                                else:
                                    raise SyntaxError(f"InvalidOperandError at line {lnum}: Input for operand 3 greater than integer limit of operand in decimal ({glib.intlimit(opfrm[2][-1:])}).")
                            elif mode.lower() == "hex":
                                if glib.funcstacker(glib.bitcomp(int(split[1]),int(opfrm[0][-1:])),glib.bitcomp(int(split[2]),int(opfrm[1][-1:])),glib.bitcomp(int(split[3]),int(opfrm[2][-1:]))) == "True True True":
                                    combined += glib.dhex(int(split[1]),ceil(int(opfrm[0][-1:])/4))+glib.dhex(int(split[2]),ceil(int(opfrm[1][-1:])/4))+glib.dhex(int(split[3]),ceil(int(opfrm[2][-1:])/4))
                                    splitt += glib.dhex(int(split[1]),ceil(int(opfrm[0][-1:])/4))+" "+glib.dhex(int(split[2]),ceil(int(opfrm[1][-1:])/4))+" "+glib.dhex(int(split[3]),ceil(int(opfrm[2][-1:])/4)) + "\n"
                                else:
                                    raise SyntaxError(f"InvalidOperandError at line {lnum}: Input for operand 3 greater than integer limit of operand in decimal ({glib.intlimit(opfrm[2][-1:])}).")
                    if debug:
                        print("Exiting match statement.")
                else:
                    raise SyntaxError(f"InvalidOperandError at line {lnum}: No matching opcode in ISA.")
        else:
            raise ValueError(f"File was above the maximum {sizeKiB} ({linecount} line) limit of {cpuname}.")
    else:
        print("File was empty..")
    if debug:
        print("Should be complete!")

if debug:
    print("Continuing to writing process.")

if combined != "" and splitt != "":
    if debug:
        print("Combined and split were not empty.")
    if outmethod.lower() == "combined":
        if debug:
            print("Writing to file with combined output.")
        with open(filepath2, "w") as file:
            file.write(combined)
        if debug:
            print("Done.")
    elif outmethod.lower() == "split":
        if debug:
            print("Writing to file with split output.")
        with open(filepath2, "w") as file:
            file.write(splitt[:-1])
        if debug:
            print("Done.")
else:
    print("No output to write to a file..")
