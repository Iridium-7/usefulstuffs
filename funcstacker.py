def funcstacker(*functions):
    '''The boss fight of functions. Takes the output of anything it is given (including non functions) and puts them into one (string) output seperated by spaces.'''
    combined = ""
    for func in functions:
        if callable(func):
            combined += str(func()) + " "
        else:
            combined += str(func) + " "
    return combined.strip()

#This is the function I was talking about. It looks like an angel to me. I made it for my variable CPU assembler which has a format that goes spagetti very quickly.#
#Have fun.#
