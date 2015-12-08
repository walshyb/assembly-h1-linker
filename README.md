# Assembly H1 Linker
Assembly project where we convert a C++ linker to Python.  Whoever completes the assignment receives 3 points on her/his average.

Uses Anthony J. Dos Reis's H1 Assembler.

Symbmolic Assembly Code: *.mas <br/>
Linkable Module: *.mob <br />
Machine Code: *.mac <br />

## .mob Files

A mob file is the result of assembling a symbolic assembly file (.mas file) that either declares a public or extern symbol.  

.mob files are broken up into two sections: 

1. Header
   - Contains entries, data values, and symbols (when applicable)
2. Text
   - Contains instructions to run

.mob files store and format information from the .mas file by separating each type of data into different entires:

##### P Entry
P Entries contain symbols and the addresses where they were declared

**module1.mas**:
```
	   public  x  	    ; declare public symbol x               
	   extern  y        ; declare external symbol y             
0:     ld      x        ; load value at address x
1:     ld      y        ; load value at external address y 
2:     halt             ; stop
3: x:  dw      5        ; declare dataword value 5
```
P Entry for **module1.mas**:
```
Type  Address   Symbol 
 P     0003       x
```
##### E Entry
E Entries contain symbols and the addresses where they are used

E Entry for **module1.mas**:
```
Type  Address   Symbol 
 E     0001       y
```

