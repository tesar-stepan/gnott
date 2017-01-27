# Gnott
**Genomic Notation Translator**

This script takes a string argument in HGVS format, and translates it to genomic notation using transvar (transvar.readthedocs.io).
Useful for cerain use-case specific batch procesing.

## Instalation
Gnott itself is a simple python script - just download and run in python, but it requires that transvar is present in your system.

#### Transvar setup:

See: http://transvar.readthedocs.io/en/latest/download_and_install.html

And: http://transvar.readthedocs.io/en/latest/quick_start.html

Or you can just run these:

```bash
sudo pip install transvar
#or locally: pip install --user transvar

# set up databases
transvar config --download_anno --refversion hg19

# download have a reference
transvar config --download_ref --refversion hg19
```

## Usage
This scipt can theoretically take any input that Transvar accepts. The only requirement is that the string has a ":x" sequence in it, where the 'x' is one of g/c/p characters, denoting the type of encoding. However, I wrote gnott for a very specific use-case, so only the formats you see below were tested.

### Limitation
this script will skip mutations ending with 'X' or 'Fs', since the output of Transvar for this type of input is not useful for the use-case this script was originally created for.

gnott.py \[-h] [-o g,c,p,pp] string

-o {g,c,p,pp}  Denotes what format should the output string be in.
-debug         Runs debug mode, shows more details about progress and errrors.

#### Basic example:

```bash
python gnott.py 'NM_000492.3:p.Gly480Cys'
chr7:g.117199563G>T
```

### OUTPUT MODIFIER: -o 

use to modify the output format.

Possible values: 'g', 'c', 'p', 'pp'

  * g - genomic reference sequence
    * ignored if input sequence is in g.
  * c  - coding DNA reference sequence
  * p  - protein reference sequence, 1-letter coding
  * pp - protein reference sequence, 3-letter coding

DEFAULTS TO: 'g' or 'p' if input sequence is in g.

#### Example, output modifier 'c'

```bash
python gnott.py 'NM_000492.3:p.Gly480Cys' -o c
chr7:c.1438G>T
```

### Input level detection

#### Example with cDNA input, output modifier 'p'

```bash
python gnott.py 'NM_000492.3:c.1438G>T' -o p
chr7:p.G480C
```

INPUT TYPE (g/c/p) is detected automatically. See above for c/p type input examples.

If the input is genomic level annotation (g),then the output is HGVS coded protein and mutation.

In this case, output modifier -o can only be c or p, and defaults to p. If modifier g is passed, it will be ignored.

#### Example with protein level input, output modifier 'c' 

```bash
python gnott.py 'chr7:g.117199563G>T' -o c
NM_000492:c.1438G>T
```
## Batch processing
Script gnottFile.py automatically reads lines in a file and calls gnott with the correct input. This script expects the first line in supplied file to be an HGVS protein code, and variants on next lines.

Example of a valid input file:
```bash
NM_000314
L70V
D326N
N276S
G132D
```
### Usage of gnottFile.py
Arguments are similar to gnott.py, with extra -i argument:
usage: gnottFile.py \[-h] \[-i {g,c,p}] \[-o {g,c,p,pp}] [-debug] filename

-i {g,c,p}     Denotes what format are the variants in.
-o {g,c,p,pp}  Denotes what format should the output string be in.
-debug         Runs debug mode, shows more details about progress and
                 errrors.
