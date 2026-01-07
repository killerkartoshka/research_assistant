import os, sys
from matplotlib.pylab import *

def LOC_read_spectra_3D(filename):
    """
    Read spectra written by LOC.py (LOC_OT.py; 3D models)
    Usage:
        V, S = LOC_read_spectra_3D(filename)
    Input:
        filename = name of the spectrum file
    Return:
        V  = vector of velocity values, one per channel
        S  = spectra as a cube S[NRA, NDE, NCHN] for NRA
             times NDE points on the sky,
             NCHN is the number of velocity channels
    """
    fp              =  open(filename, 'rb')
    NRA, NDE, NCHN  =  fromfile(fp, int32, 3)
    V0, DV          =  fromfile(fp, float32, 2)
    SPE             =  fromfile(fp, float32).reshape(NRA, NDE,2+NCHN)
    OFF             =  SPE[:,:,0:2].copy()
    SPE             =  SPE[:,:,2:]
    fp.close()
    return V0+arange(NCHN)*DV, SPE
    
    
def LOC_read_Tex_3D(filename):
    """
    Read excitation temperatures written by LOC.py (LOC_OT.py) -- in case of
    a Cartesian grid (no hierarchical discretisation).
    Usage:
        TEX = LOC_read_Tex_3D(filename)
    Input:
        filename = name of the Tex file written by LOC1D.py
    Output:
        TEX = Vector of Tex values [K], one per cell.
    Note:
        In case of octree grids, the returned vector must be
        compared to hierarchy information (e.g. from the density file)
        to know the locations of the cells.
        See the routine OT_GetCoordinatesAllV()
    """
    fp    =  open(filename, 'rb')
    NX, NY, NZ, dummy  =  fromfile(fp, int32, 4)
    TEX                =  fromfile(fp, float32).reshape(NZ, NY, NX)
    fp.close()
    return TEX                                                                                


V, T10 = LOC_read_spectra_3D('test_CO_01-00.spe')
V, T21 = LOC_read_spectra_3D('test_CO_02-01.spe')
Tex10  = LOC_read_Tex_3D('test_CO_01-00.tex')
Tex21  = LOC_read_Tex_3D('test_CO_02-01.tex')
NY, NX, NCHN = T10.shape  # number of pixels and channels

# One spectrum from (about) the model centre
subplot(221)
plot(V, T10[NY//2, NX//2, :], 'b-', label='T(1-0)')
plot(V, T21[NY//2, NX//2, :], 'r-', label='T(2-1)')
legend(loc='lower center')
title("Centre spectra (K)")
xlabel(r'$v \/ \/ \rm (km s^{-1})$')
ylabel(r'$T \rm _A \/ \/ (K)$')

# Cross section of the Tex(1-0) cube
subplot(222)
imshow(Tex10[:,:, Tex10.shape[2]//2])
title("J=1-0 excitation temperature (K)")
colorbar()

# Cross section of the Tex(2-1) cube
subplot(223)
imshow(Tex21[:,:, Tex21.shape[2]//2])
title("J=2-1 excitation temperature (K)")
colorbar()

# J=1-0 line area
subplot(224)
W     =  (V[1]-V[0])*sum(T10, axis=2)
imshow(W)
title("Line Area W(1-0) (K km/s)")
colorbar()

show()
