#Script for translating HGVS to genomic notation
# using transvar: transvar.readthedocs.io

import os
import sys
import subprocess

DEBUG = False;
VALID_OUT_MODIFIERS = ['g', 'c', 'p', 'pp']
MSG_INVALID_ARG2 = "\033[91m Invalid output modifier (second argument). Valid values are: %s" % str(VALID_OUT_MODIFIERS)[1:-1]
MSG_MISSING_ARG = "\033[91m Missing required argument #%d - %s"
MSG_TRANSVAR_NO = "\033[91m Transvar was not detected, please install transvar first."
MSG_TRANSVAR_CALL_ERR = "Transvar call failed."
MSG_TRANSVAR_EX = "\033[91m TRANSVAR EXCEPTION"
MSG_ARGUMENT_EX = "\033[91m ARGUMENT EXCEPTION"
MSG_VALUE_ERR = "\033[91m ERROR DURING Popen CALL"
MSG_INPUT_PARSE_ERR = "\033[91m INPUT PROCESSING ERROR - %s"
MSG_VALS_MISSINGARG1 = (1, "String with the notation you'd like to translate.")
MSG_USAGE = """
    GNOTT USAGE:
    This script takes a string argument in HGVS format, and
    translates it to genomic notation using transvar
    (transvar.readthedocs.io)
    NOTE - this scipt can theoretically take any input that
           Transvar accepts. The only requirement is that
           the string has a ":x" sequence in it, where the
           'x' is one of g/c/p characters, denoting the
           type of encoding.
    -------------------------------------------------------
    Protein level annotation example:
        input  : $python gnott.py 'NM_000492.3:p.Gly480Cys'
        output : chr7:g.117199563G>T
    -------------------------------------------------------
    OUTPUT MODIFIER: use second argument to modify the output format.
        Possible values: 'g', 'c', 'p', 'pp'
            g  - genomic reference sequence
               - ignored if input sequence is in g.
            c  - coding DNA reference sequence
            p  - protein reference sequence, 1-letter coding
            pp - protein reference sequence, 3-letter coding
            DEFAULTS TO: 'g' or 'p' if input sequence is in g.

    Protein level annotation example, output modifier 'c'
        input  : $python gnott.py 'NM_000492.3:p.Gly480Cys' c
        output : chr7:c.1438G>T

    cDNA level annotation example, output modifier 'p'
        input  : $python gnott.py 'NM_000492.3:c.1438G>T' p
        output : chr7:p.G480C
    -------------------------------------------------------
    INPUT TYPE (g/c/p) is detected automatically. See above
    for c/p type input examples.
    If the input is genomic level annotation (g),
    then the output is HGVS coded protein and mutation.
        In this case, OUTPUT MODIFIER can only be c or p,
        and defaults to p. If modifier g is passesd it will
        be ignored.
    Genomic level annotation example:
        input  : $python gnott.py 'chr7:g.117199563G>T' c
        output : NM_000492:c.1438G>T
            """

class ArgException(Exception):
    """
        Exception extension thrown when there is a problem with arguments.
    """
    def __init__(self, value):
        self.value = "%s: %s" % (MSG_ARGUMENT_EX, value)
    def __str__(self):
        return self.value


#variable setup
inputSequence = ""
inMode = ""
outMode = "g"
tvar = ""


#Arguments checks and read
try:
    if(len(sys.argv) < 2 ):
        raise ArgException(MSG_MISSING_ARG % MSG_VALS_MISSINGARG1)
    elif(len(sys.argv) > 2):
        arg2 = sys.argv[2]
        if(arg2 not in VALID_OUT_MODIFIERS):
            raise ArgException(MSG_INVALID_ARG2)
        elif(DEBUG):
            print "Second argument primary validation success (%s)." % arg2
        outMode = arg2

    inputSequence = sys.argv[1]

except ArgException as e:
    print e.value
    print MSG_USAGE
    sys.exit()


#Preprocessing the input sequence
inputSequence.replace(" ", "")
delimFound = False;
for c in inputSequence:
    if(delimFound):
        inMode = c
        break
    if(c == ":"):
        delimFound = True;

if(inMode == ""):
    print MSG_INPUT_PARSE_ERR % "':' not found"
    sys.exit()
elif(DEBUG):
    print "input mode detected: %s" % c


#Preparing arguments for transvar
protMode = ""
tvarMode = ""

if(outMode == "pp"):
    protMode = "--aa3"
    outMode = "p"

tvarMode = "%sanno" % inMode
targs = ["transvar", tvarMode, "-i", inputSequence, "--ucsc" ]

if(protMode != ""):
    targs.append(protMode)

#Calling transvar. Its output is stored in the 'tvar' variable
try:
    p = subprocess.Popen(targs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    tvar, error = p.communicate()
    if(p.returncode != 0):
        print MSG_TRANSVAR_EX, ":", tvar, error
        sys.exit()    
except OSError as e:
    if(e.errno == os.errno.ENOENT):
        print MSG_TRANSVAR_NO
    else:
        print MSG_TRANSVAR_CALL_ERR
    traceback.print_exc()
    sys.exit()
except ValueError as e:
    print MSG_VALUE_ERR
    traceback.print_exc()
    sys.exit()

# 3-letter --aa3
#Processing the transvar output
print tvar
