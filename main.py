"""
Main Script for DNS Data Processing
===================================

Author: Stijn Schepers
Contact: stijn.schepers.snj@gmail.com
Date: January 28, 2025

Description:
------------
This script reads DISCO binary output files, extracts flow, species, and other fields, 
and exports them in VTK format for visualization in Paraview.

Usage and Installation:
-----------------------
See README.md for installation and usage instructions.
"""

import numpy as np
import pyvista as pv
import gc
import sys

from chemistry.ReadTrotDatmod  import ReadTrotDatmod
from utils import *

def main():

    # Locations and file name
    input_directory  = '/mnt/d/DNS+DC/ref/'
    file_name        = '00012000'
    output_directory = '/mnt/d/DNS+DC/ref/VTK/'

    # Write booleans
    write_flow        = False
    write_species     = False
    write_source      = True
    write_enthalpy    = False

    # Grid parameters
    xmin = 0        # Minimum x-coordinate
    xmax = 8e-3     # Maximum x-coordinate
    ymin = -4e-3    # Minimum y-coordinate
    ymax = 4e-3     # Maximum y-coordinate
    zmin = -4e-3    # Minimum z-coordinate
    zmax = 4e-3     # Maximum z-coordinate
    dx   = 0.025e-3 # Grid spacing
    nx   = 320      # Number of grid points in x-direction
    ny   = 320      # Number of grid points in y-direction
    nz   = 320      # Number of grid points in z-direction

    # Read the mechanism
    _, Sp, _, _, Nsp, _ = ReadTrotDatmod("chemistry/Burke-H2-2012-N2.trot")

    # Read the DNS data
    data_v   = read4Dfile(input_directory +'v'   + file_name + '.bin' ,nx,ny,nz,15)
    data_st  = read4Dfile(input_directory +'st'  + file_name + '.bin' ,nx,ny,nz,9 )
    data_hh  = read4Dfile(input_directory +'hh'  + file_name + '.bin' ,nx,ny,nz,9 )
    data_mu  = read3Dfile(input_directory +'mu'  + file_name + '.bin' ,nx,ny,nz)
    data_eps = read3Dfile(input_directory +'eps' + file_name + '.bin' ,nx,ny,nz)
    data_hrr = read3Dfile(input_directory +'hrr' + file_name + '.bin' ,nx,ny,nz)
    data_k   = read3Dfile(input_directory +'k'   + file_name + '.bin' ,nx,ny,nz)

    # Extract DNS data
    U   = data_v[:,:,:,0:3]      # Velocity vector          [m/s]
    rho = data_v[:,:,:,3]        # Density                  [kg/m^3]
    p   = data_v[:,:,:,4]        # Pressure                 [Pa]
    T   = data_v[:,:,:,5]        # Temperature              [K]
    Ysp = data_v[:,:,:,6:6+Nsp]	 # Species mass fractions   [-]
    Ssp = data_st	             # Species source terms     [kg/(m^3 s)]
    hsp = data_hh                # Enthalpy                 [J/kg]
    mu  = data_mu                # Dynamic viscosity        [Pa s]
    eps = data_eps               # Eddy dissipation rate    [m^2/s^3]
    hrr = data_hrr               # Heat release rate        [W/m^3]
    k   = data_k                 # Turbulent kinetic energy [m^2/s^2]

    # Remove data from memory
    del data_v, data_st, data_hh, data_mu, data_eps, data_hrr, data_k
    gc.collect() # Force garbage collection

    # Create grid for pyvista
    xrng = np.arange(xmin, xmax, dx, dtype=np.float32) # x-coordinate range
    yrng = np.arange(ymin, ymax, dx, dtype=np.float32) # y-coordinate range
    zrng = np.arange(zmin, zmax, dx, dtype=np.float32) # z-coordinate range
    x, y, z = np.meshgrid(xrng, yrng, zrng, indexing='ij') # Create the grid

    # Only write the data if requested
    if write_flow:

        print("Writing flow data to VTK file...")

        # Create grid to store the data
        grid = pv.StructuredGrid(x, y, z)

        # Add the data to the grid
        grid.point_data["U"]    = U.reshape(-1, 3, order="F") # Velocity vector
        grid.point_data["rho"]  = rho.flatten(order="F")      # Density
        grid.point_data["p"]    = p.flatten(order="F")        # Pressure
        grid.point_data["T"]    = T.flatten(order="F")        # Temperature
        grid.point_data["mu"]   = mu.flatten(order="F")       # Dynamic viscosity
        grid.point_data["eps"]  = eps.flatten(order="F")      # Eddy dissipation rate
        grid.point_data["k"]    = k.flatten(order="F")        # Turbulent kinetic energy
        grid.point_data["hrr"]  = hrr.flatten(order="F")      # Heat release rate

        # Write the grid to a VTK file
        grid.save(output_directory+'flow_data_'+file_name+'.vtk')

        print('Flow data written to flow_data_'+file_name+'.vtk')

        # Remove the grid from memory
        del grid
        gc.collect() # Force garbage collection

    # Only write the data if requested
    if write_species:

        print("Writing species data to VTK file...")
    
        # Create grid to store the data
        grid = pv.StructuredGrid(x, y, z)

        # Add the data to the grid
        for i in range(Nsp): # Species mass fractions
            grid.point_data[Sp[i]["Name"]] = Ysp[:,:,:,i].flatten(order="F")

        # Write the grid to a VTK file
        grid.save(output_directory+'species_data_'+file_name+'.vtk')

        print('Species data written to species_data_'+file_name+'.vtk')

        # Remove the grid from memory
        del grid
        gc.collect() # Force garbage collection

    # Only write the data if requested
    if write_source:

        print("Writing source data to VTK file...")

        # Create grid to store the data
        grid = pv.StructuredGrid(x, y, z)

        # Add the data to the grid
        for i in range(Nsp): # Species source terms
            grid.point_data['source_'+Sp[i]["Name"]] = Ssp[:,:,:,i].flatten(order="F")

        # Write the grid to a VTK file
        grid.save(output_directory+'source_data_'+file_name+'.vtk')

        print('Source data written to source_data_'+file_name+'.vtk')

        # Remove the grid from memory
        del grid
        gc.collect() # Force garbage collection

    # Only write the data if requested
    if write_enthalpy:

        print("Writing enthalpy data to VTK file...")

        # Create grid to store the data
        grid = pv.StructuredGrid(x, y, z)

        # Add the data to the grid
        for i in range(Nsp): # Species enthalpies
            grid.point_data['h_'+Sp[i]["Name"]] = hsp[:,:,:,i].flatten(order="F")

        # Write the grid to a VTK file
        grid.save(output_directory+'enthalpy_data_'+file_name+'.vtk')

        print('Enthalpy data written to enthalpy_data_'+file_name+'.vtk')

        # Remove the grid from memory
        del grid
        gc.collect() # Force garbage collection

    sys.exit(0)

if __name__ == "__main__":  
    main()
