# Assembly H1 Linker
Assembly project where we convert a C++ linker to Python.  Whoever completes the assignment receives 3 points on her/his average.

Uses Anthony J. Dos Reis's H1 Assembler.

Symbmolic Assembly Code: *.mas <br/>
Linkable Module: *.mob <br />
Machine Code: *.mac <br />

## Usage
To use the linker, you first need two .mob files assembled with Anthony Dos Reis's assembler (./mas).

```
$ python linv1.py module1.mob module2.mob
```

## .mob Files

A mob file is the result of assembling a symbolic assembly file (.mas file) that either declares a public or extern symbol.  

.mob files are broken up into two sections: 

1. Header
  1. Contains entries, data values, and symbols (when applicable)
2. Text
  1. Contains instructions to run

.mob files store and format information from the .mas file by separating each type of data into different entires:

### P Entry
P Entries contain symbols and the addresses where they were declared

**module1.mas**:
```
public  x  	    ; declare public symbol x               
extern  y        ; declare external symbol y             
0:     ld      x        ; load value at address x (to ac register)
1:     st      y        ; store value to external address y 
2:     halt             ; stop
3: x:  dw      5        ; declare dataword value 5
```
P Entry for **module1.mas**:
```
Type  Address   Symbol 
P     0003       x
```

### E Entry
E Entries contain symbols and the addresses where they are used

E Entry for **module1.mas**:
```
Type  Address   Symbol 
E     0001       y
```

### R Entry
R Entries are entries for relative/relocatable symbols.  An R Entry contains the address of where a symbol is used (similar to an E Entry), but does not contain the symbol itself because once the two modules are linked, the R Entry will only be an absolute address (due to the fact that it does not affect the addresses of another module).

**module2.mas**:
```
public  y  	    ; declare public symbol y               
extern  x        ; declare external symbol x             
0:     ld      x        ; load value at address x (to ac register)
1:     add    @1        ; add value at address @1 to ac register
2:     st      x        ; st value in ac register to x
3: y:  dw      3        ; declare dataword value 3
4: @1: dw      1        ; declare dataword value 1
```
R Entry for **module2.mas**:
```
Type  Address   Symbol 
R     0001       
```



