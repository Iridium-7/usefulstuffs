import generaluselib as glib #Required, a custom made library.
from math import ceil
import sys #Exit

class CustomError:
    def __new__(cls, errorname):
        return type(errorname, (Exception,), {"get_class_name": lambda self: self.__class__.__name__})

moperror = CustomError("MismatchedOperandsError")
ioperror = CustomError("InvalidOperandError")
iopcerror = CustomError("InvalidOpcodeError")


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

cpuname = "LightRISC-1 Capable CPU"
linecount = 256
filext = ".lr1" #the dots are required!
filextb = ".lr1b"

#Code variables#

sizeKiB = linecount/1024 #do not even think about touching this value

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
    "PRINT": ("00000", ["dec3", "bin1", "bin1"]), #Binary Opcode | Operand[Number of bits]
    "ADD":   ("00001", ["dec3"]),
    "SUB":   ("00010", ["dec3"]),
    "LDI":   ("00011", ["dec3", "dec8"]),
    "LIA":   ("00100", ["dec8"]),
    "AND":   ("00101", ["dec3"]),
    "OR":    ("00110", ["dec3"]),
    "XOR":   ("00111", ["dec3"]),
    "ADC":   ("01000", ["dec3"]),
    "SBB":   ("01001", ["dec3"]),
    "ADR":   ("01010", ["dec3"]),
    "SBR":   ("01011", ["dec3"]),
    "CMP":   ("01100", ["dec3"]),
    "BRNCH": ("01101", ["dec3", "dec3"]),
    "NAND":  ("01110", ["dec3"]),
    "NOR":   ("01111", ["dec3"]),
    "XNOR":  ("10000", ["dec3"]),
    "BSB":   ("10001", ["dec3"]),
    "JMP":   ("10010", ["dec3"]),
}

if askuser == True:
    print(f"What is the file path to the input {filext} file? (From root.) Enter 'exit' on any input to quit.")
    filepath = input("Enter here: ")
    if filepath == "exit":
        sys.exit(0)
    print("What should the output file be named? (Accepts paths, by default relative to root.)")
    filepath2 = input("Enter here: ")
    if filepath2 == "exit":
        sys.exit(0)
if askuser2 == True:
    print("What is the preferred output mode? (bin, hex)")
    mode = input("Enter here: ")
    if mode == "exit":
        sys.exit(0)
    print("How should the assembler output? One big number or split lines? (combined, split)")
    outmethod = input("Enter here: ")
    if outmethod == "exit":
        sys.exit(0)

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
if mode not in ["bin", "hex"]:
    raise NameError("Invalid mode. (Must be either bin or hex.)")
if outmethod not in ["split", "combined"]:
    raise NameError("Invalid output method. (Must be either split or combined.)")

with open(filepath, "r") as file:
    lines = file.readlines()
    if len(lines) != 0:
        if len(lines) < linecount:
            for lnum, line in enumerate(lines, start=1):
                line = line.strip()
                if debug:
                    print(f"Processing line {lnum} (containing '{line}')")
                if glib.letter(line, ";") != 0:
                    line = line[:line.index(";")]
                if line != "":
                    split = line.split()
                    instr = split[0]
                    if instr.upper() in isa:
                        if debug:
                            print("Line was in ISA instructions.")
                        bop, opfrm = isa[instr.upper()]
                        if len(split)-1 != len(opfrm):
                            raise moperror(f"at line {lnum}: Expecting {len(opfrm)}, got {len(split)-1}")
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
                                        raise ioperror(f"at line {lnum}: Input for operand 1 greater than integer limit of operand in decimal ({glib.intlimit(opfrm[0][-1:])}).")
                                elif mode.lower() == "hex":
                                    if glib.funcstacker(glib.bitcomp(int(split[1]),int(opfrm[0][-1:]))) == "True":
                                        combined += glib.dhex(int(split[1]),ceil(int(opfrm[0][-1:])/4))
                                        splitt += glib.dhex(int(split[1]),ceil(int(opfrm[0][-1:])/4)) + "\n"
                                    else:
                                        raise ioperror(f"at line {lnum}: Input for operand 1 greater than integer limit of operand in decimal ({glib.intlimit(opfrm[0][-1:])}).")
                            case 2:
                                if mode.lower() == "bin":
                                    if glib.funcstacker(glib.bitcomp(int(split[1]),int(opfrm[0][-1:])),glib.bitcomp(int(split[2]),int(opfrm[1][-1:]))) == "True True":
                                        combined += glib.dbin(int(split[1]),int(opfrm[0][-1:]))+glib.dbin(int(split[2]),int(opfrm[1][-1:]))
                                        splitt += glib.dbin(int(split[1]),int(opfrm[0][-1:]))+" "+glib.dbin(int(split[2]),int(opfrm[1][-1:])) + "\n"
                                    else:
                                        raise ioperror(f"at line {lnum}: Input for operand 2 greater than integer limit of operand in decimal ({glib.intlimit(opfrm[1][-1:])}).")
                                elif mode.lower() == "hex":
                                    if glib.funcstacker(glib.bitcomp(int(split[1]),int(opfrm[0][-1:])),glib.bitcomp(int(split[2]),int(opfrm[1][-1:]))) == "True True":
                                        combined += glib.dhex(int(split[1]),ceil(int(opfrm[0][-1:])/4))+glib.dhex(int(split[2]),ceil(int(opfrm[1][-1:])/4))
                                        splitt += glib.dhex(int(split[1]),ceil(int(opfrm[0][-1:])/4))+" "+glib.dhex(int(split[2]),ceil(int(opfrm[1][-1:])/4)) + "\n"
                                    else:
                                        raise ioperror(f"at line {lnum}: Input for operand 2 greater than integer limit of operand in decimal ({glib.intlimit(opfrm[1][-1:])}).")
                            case 3:
                                if mode.lower() == "bin":
                                    if glib.funcstacker(glib.bitcomp(int(split[1]),int(opfrm[0][-1:])),glib.bitcomp(int(split[2]),int(opfrm[1][-1:])),glib.bitcomp(int(split[3]),int(opfrm[2][-1:]))) == "True True True":
                                        combined += glib.dbin(int(split[1]),int(opfrm[0][-1:]))+glib.dbin(int(split[2]),int(opfrm[1][-1:]))+glib.dbin(int(split[2]),int(opfrm[2][-1:]))
                                        splitt += glib.dbin(int(split[1]),int(opfrm[0][-1:]))+" "+glib.dbin(int(split[2]),int(opfrm[1][-1:]))+" "+glib.dbin(int(split[2]),int(opfrm[2][-1:])) + "\n"
                                    else:
                                        raise ioperror(f"at line {lnum}: Input for operand 3 greater than integer limit of operand in decimal ({glib.intlimit(opfrm[2][-1:])}).")
                                elif mode.lower() == "hex":
                                    if glib.funcstacker(glib.bitcomp(int(split[1]),int(opfrm[0][-1:])),glib.bitcomp(int(split[2]),int(opfrm[1][-1:])),glib.bitcomp(int(split[3]),int(opfrm[2][-1:]))) == "True True True":
                                        combined += glib.dhex(int(split[1]),ceil(int(opfrm[0][-1:])/4))+glib.dhex(int(split[2]),ceil(int(opfrm[1][-1:])/4))+glib.dhex(int(split[3]),ceil(int(opfrm[2][-1:])/4))
                                        splitt += glib.dhex(int(split[1]),ceil(int(opfrm[0][-1:])/4))+" "+glib.dhex(int(split[2]),ceil(int(opfrm[1][-1:])/4))+" "+glib.dhex(int(split[3]),ceil(int(opfrm[2][-1:])/4)) + "\n"
                                    else:
                                        raise ioperror(f"at line {lnum}: Input for operand 3 greater than integer limit of operand in decimal ({glib.intlimit(opfrm[2][-1:])}).")
                        if debug:
                            print("Exiting match statement.")
                    else:
                        raise iopcerror(f"at line {lnum}: No matching opcode in ISA.")
                else:
                    if debug:
                        print("Line was empty.. Continuing.")
                        continue
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
