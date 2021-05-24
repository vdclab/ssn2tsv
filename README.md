# ssn2tsv

Script that allows to transform SSN XGMML to tabulated format file

```
Convert xgmml from SSN to table

optional arguments:
  -h, --help            show this help message and exit

General input dataset options:
  -g <XGMML>, --xgmml <XGMML>
                        XGMML file from the analysis of EFI-EST : https://efi.igb.illinois.edu/efi-est/
  -o <OUTPUT>, --output <OUTPUT>
                        Name of the output file (default: [NAME_OF_XGMML]_table.tsv)
```

Example :

```
python3 ssn2tsv.py -g mySSN.xgmml -o mySSN.tsv
```
