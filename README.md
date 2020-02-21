KiCad sub-PCBs
==========
create sub-pcbs according to sub-schematic file in KiCad 5.x

consider to use the [Replicate layout](https://github.com/MitjaNemec/Kicad_action_plugins#replicate-layout) Action-Plugins of [Mitja Nemec](https://github.com/MitjaNemec) before trying to use this plugin. It serves very similar needs, while providing much more features under a nice user interface.

How to use
==========
* First create a project with a main-schematics file and insert the subcircuit as hierarchical sheet as often as you plan to actually place this file on the PCB
* annotate devices
* save everything
* you should now have a `mySubCircuit.sch` file
* close all KiCad software and only open Eeschema!!
* open the `mySubCircuit.sch` file
* create a netlist
* create a PCB with the name `mySubCircuit.kicad_pcb`
* close `mySubCircuit.sch` file without saving
* import the netlist manually (as its not opened in the project manager) into the PCB
* route everything as desired and save and close PCB file
* call `kicad-sub-pcb.py mySubCircuit.sch`
* you now should have a sub-folder `mySubCircuit.kicad_pcbs` with as many PCB-files inside as there should be subcircuits
* open the main PCB file again without project manager in Pcbnew
* *Append Board...* for each of the PCBs in `mySubCircuit.kicad_pcbs` folder
* save and close PCB
* reopen the project
* open the main PCB file and run *Update PCB from schematic*
* you should now have nice routed subcircuits also on your PCB
