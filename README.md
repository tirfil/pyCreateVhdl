
Create VHDL module and testbench skeleton (Python)

VHDL langage syntax is strict and wordy. 
We need to write again and again almost same code in entity, component and portmap. 
It's a waste of time and energy before starting main code write !

This tool helps designer in the very first step to create module (entity) and testbench (component, portmap) skeleton code.

Design have to write a simple text file using simple syntax rules and execute the python script on it.
The script produces two files: a first with a vhdl module template and another with a testbench template.

Simple file syntax:
Each line is word separated by space. First word is the keyword , others are arguments.

| syntax                                  | notes                   |
| --------------------------------------  | ----------------------- |
| entity module-name                      |                         |                     
| architecture arch-name                  | default is rtl          |        
| end                                     | end of file             |
| in signal-name bus-width           | bus-witdh is optional |
| out signal-name bus-width          | bus-witdh is optional |
| inout signal-name bus-width         | bus-witdh is optional |
| clock clock-name edge-value        | edge-value default 1 is positive edge |
| reset async-reset-name active-value | active-value default 0 is active low |

Using clock and reset is recommended for full features.

For an example, see register8.txt in example/input. example/output contains generated files.







