# ssn2tsv

Script that allows to transform SSN XGMML to tabulated format file

```
Convert xgmml from SSN to table

optional arguments:
  -h, --help            show this help message and exit

General input dataset options:
  -g <XGMML>, --xgmml <XGMML>
                        XGMML file from the analysis of EFI-EST : https://efi.igb.illinois.edu/efi-est/
  -f, --full            Option that allows to have a table with all the columns that appear in the xgmml. Default columns are : ???
  -t, --taxonomy        Add the taxonomy if present in the file, to have the best result of this feature please use the full network not a reduced/concatenated one. Else only unique field will be written
  -o <OUTPUT>, --output <OUTPUT>
                        Name of the output file (default: [NAME_OF_XGMML]_table.tsv)
```

Example :

```
python3.8 ssn2tsv.py -g mySSN.xgmml -o mySSN.tsv
```
