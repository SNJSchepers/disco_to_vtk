# DISCO to VTK

A python program that reads DISCO output files and writes them in VTK format to visualise and analyse in Paraview. 

## Requirements
- python 3.x
- pip

## Setup
1. Clone the repository or download the project files
2. Navigate to the project directory
   
   ```bash
   cd disco_to_vtk
3. Create a virtual environment
   ```bash
   python3 -m venv venv
4. Activate the virtual environment
   ```bash
   source venv/bin/activate
5. Install dependencies
   ```bash
   pip3 install -r requirements.txt
6. Create output directory to store the VTK files
   ```bash
   mkdir output

## Usage

1. Change the `directory` and `file_name` variables to your case folder and the desired time step.
2. Set the write booleans, `write_flow`,`write_species`,`write_source` and `write_enthalpy`, to select which variables you want to write.
3. Check if the grid parameters are correct.

Run the program:
```bash
python3 main.py
``` 
The VTK files will be written in the `output/` directory. 

## Note
Make sure to close back ground processes since this program uses quite a bit of RAM. This is also the reason that not all variables are stored in a single VTK file, but they are grouped in seperate VTK files. 

