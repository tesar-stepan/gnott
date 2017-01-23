# gnott - WIP
This script takes a string argument in HGVS format, and translates it to genomic notation using transvar (transvar.readthedocs.io).
Useful for cerain use-case specific batch procesing.

## Instalation
Gnott itself is a simple python script - just download and run in python, but it requires that transvar is present in your system.

See: http://transvar.readthedocs.io/en/latest/download_and_install.html

And do these before running gnott: http://transvar.readthedocs.io/en/latest/quick_start.html

## Usage
This scipt can theoretically take any input that Transvar accepts. The only requirement is that the string has a ":x" sequence in it, where the 'x' is one of g/c/p characters, denoting the type of encoding. However, I wrote gnott for a very specific use-case, so only the formats you see below were tested.

Protein level annotation example:

```bash
python gnott.py 'NM_000492.3:p.Gly480Cys'
chr7:g.117199563G>T
```

OUTPUT MODIFIER: -o 

use to modify the output format.

Possible values: 'g', 'c', 'p', 'pp'

  * g - genomic reference sequence
    * ignored if input sequence is in g.
  * c  - coding DNA reference sequence
  * p  - protein reference sequence, 1-letter coding
  * pp - protein reference sequence, 3-letter coding

DEFAULTS TO: 'g' or 'p' if input sequence is in g.

Protein level annotation example, output modifier 'c'

```bash
python gnott.py 'NM_000492.3:p.Gly480Cys' -o c
chr7:c.1438G>T
```

cDNA level annotation example, output modifier 'p'

```bash
python gnott.py 'NM_000492.3:c.1438G>T' -o p
chr7:p.G480C
```

INPUT TYPE (g/c/p) is detected automatically. See above for c/p type input examples.

If the input is genomic level annotation (g),then the output is HGVS coded protein and mutation.

In this case, output modifier -o can only be c or p, and defaults to p. If modifier g is passed, it will be ignored.

Genomic level annotation example:

```bash
python gnott.py 'chr7:g.117199563G>T' -o c
NM_000492:c.1438G>T
```
