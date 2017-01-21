# gnott
This script takes a string argument in HGVS format, and translates it to genomic notation using transvar (transvar.readthedocs.io)

Note - this scipt can theoretically take any input that Transvar accepts. The only requirement is that the string has a ":x" sequence in it, where the 'x' is one of g/c/p characters, denoting the type of encoding.

Protein level annotation example:

input  : $python gnott.py 'NM_000492.3:p.Gly480Cys'

output : chr7:g.117199563G>T

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

INPUT TYPE (g/c/p) is detected automatically. See above for c/p type input examples.

If the input is genomic level annotation (g),then the output is HGVS coded protein and mutation.

In this case, OUTPUT MODIFIER can only be c or p, and defaults to p. If modifier g is passesd it will be ignored.

Genomic level annotation example:

input  : $python gnott.py 'chr7:g.117199563G>T' c

output : NM_000492:c.1438G>T
