import numpy as np

# Function to read 4D binary files
def read4Dfile(fileName,nx,ny,nz,nv):
    f = np.memmap(fileName, dtype=float, mode='r')
    f = np.reshape(f, (nx,ny,nz,nv), order='F')
    return f

# Function to read 3D binary files
def read3Dfile(fileName,nx,ny,nz):
    f = np.memmap(fileName, dtype=float, mode='r')
    f = np.reshape(f, (nx,ny,nz), order='F')
    return f

def listStruc(Struc=None,fieldname=None):
    return [Struc[x][fieldname] for x in range(len(Struc))]

def SpInd(Name,Sp):
    return listStruc(Sp,"Name").index(Name)

def ElInd(Name,El):
    return listStruc(El,"Name").index(Name)