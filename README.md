# catoligo

Catoligo is a simple python script for calculating melting temperature of short oligo sequences (e.g. primers) of up to 50 nucloeotides in length.

Sequences may contain up to 3 degenerate bases. (Primers and probes with many degenerate bases are very difficult to optimise and imho, misses the point that it is supposed to have a targeted objective. 

Allowed letters in oligo sequence:

```
A	Adenine 
C	Cytosine
G	Guanine
T	Thymine
U	Uracil
R	Guanine / Adenine (purine)
Y	Cytosine / Thymine (pyrimidine)
K	Guanine / Thymine
M	Adenine / Cytosine
S	Guanine / Cytosine
W	Adenine / Thymine
B	Guanine / Thymine / Cytosine
D	Guanine / Adenine / Thymine
H	Adenine / Cytosine / Thymine
V	Guanine / Cytosine / Adenine
N	Adenine / Guanine / Cytosine / Thymine

```

**Note**: in general degenerate bases, make it very difficult to calculate Tm and downstream more difficult to optimise the assay because of the wide range of possibilities and combination of bases in the oligo sequence pool. Thus it is not advisable to use too many degenerate bases in your primer or probe sequences.

**Formula**:

This formula was published at https://ucmp.berkeley.edu/museum/MPL/oligosinfo.html

> Tm ≈ (81.5 + (16.6 * log10([Na+])) + (0.41 * (%GC))) - (675 / (oligonucleotide length))
> where [Na+] is the molar salt concentration, n = number of bases in the oligonucleotide

This formula is a common empirical approximation used to estimate the melting temperature (Tm) of short DNA oligonucleotides (like primers or probes). It takes into account the length of the oligonucleotide, its GC content, and the salt concentration in the solution. Let's break down each component:

* Tm: This is the melting temperature in degrees Celsius (°C). It represents the temperature at which 50% of the oligonucleotide duplexes are dissociated into single strands. This is a crucial parameter for designing PCR primers and hybridization probes.

* 81.5: This is an empirical constant. It represents a baseline melting temperature estimated for a very long oligonucleotide with 50% GC content in a standard salt concentration (often implicitly assumed to be around 1 M Na+ in some derivations, though the salt correction term adjusts for other concentrations).

* 16.6 * log10([Na+]): This is the salt correction term.

16.6: Another empirical constant that reflects the influence of monovalent cation concentration on DNA stability.
log10([Na+]): The logarithm base 10 of the molar concentration of monovalent cations (primarily sodium ions, Na+) in the solution. Higher salt concentrations stabilize the DNA duplex by neutralizing the negatively charged phosphate backbones, thus increasing the Tm. The logarithm indicates a non-linear relationship – the effect of salt concentration diminishes at higher concentrations.

* 0.41 * (%GC): This is the GC content contribution term.

0.41: An empirical constant representing the approximate increase in Tm per percentage of guanine (G) and cytosine (C) bases.
(%GC): The percentage of guanine and cytosine bases in the oligonucleotide sequence. G-C base pairs have three hydrogen bonds, which are stronger than the two hydrogen bonds in adenine (A) and thymine (T) base pairs. Therefore, a higher GC content leads to a higher melting temperature.

* -675 / (oligonucleotide length): This is the length correction term.

675: An empirical constant related to the energetic cost of initiating helix formation.
(oligonucleotide length): The number of bases in the oligonucleotide sequence. Longer oligonucleotides have more base pairs and thus require more energy (higher temperature) to completely separate. This term accounts for the increased stability with length.

(Explanation of the formula terms were generated using Gemini Flash 2.0, however the formula came from https://ucmp.berkeley.edu/museum/MPL/oligosinfo.html)

There are many oligo melt temperature calculator apps online and they may give different results depending on the formula used. For example, the very simple one that many of us may have learned in school was this one: (Tm = 4(G+C) + 2(A+T)) from 1962 (Marmur and Doty (1962)). And it was the later publications, that melting temperature calculations started taking length and salt concentration into consideration. 

