import os
import subprocess
import argparse

ING = OUG = "g"
INC = OUC = "c"
INP = OUP = "p"
OUPP = "pp"
INA = "a"

VALID_IN_MODIFIERS = [ING, INC, INP, INA]
VALID_OUT_MODIFIERS = [OUG, OUC, OUP, OUPP]

MSG_ARG1_DESC = "File with HGVS protein code on line 1, and variants on following lines."
MSG_ARG2_DESC = "Denotes what format are the variants in."
MSG_ARG3_DESC = "Denotes what format should the output string be in."
MSG_ARG4_DESC = "Runs debug mode, shows more details about progress and errrors."

#Read arguments
parser = argparse.ArgumentParser()
parser.add_argument("filename", help=MSG_ARG1_DESC)
parser.add_argument("-i", help=MSG_ARG2_DESC, choices=VALID_IN_MODIFIERS, default=INA)
parser.add_argument("-o", help=MSG_ARG3_DESC, choices=VALID_OUT_MODIFIERS, default=OUG)
parser.add_argument("-debug", help=MSG_ARG4_DESC, action='store_true', default=False)

args = parser.parse_args()
fname = args.filename
mode = args.i
outMode = args.o
debug = args.debug

#Check input mode
if(mode == INA):
    mode = ""
else:
    mode+="."

#Load file
with open(fname) as f:
    content = f.readlines()
content = [x.strip() for x in content]

prot = content[0]

#Call gnott
for variant in content[1:]:
    code = "%s:%s%s" % (prot, mode, variant)
    gargs = ["python", "gnott.py", code, "-o%s" % outMode]
    if(debug):
        gargs.append("-debug")
    subprocess.call(gargs)
