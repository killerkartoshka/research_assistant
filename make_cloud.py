from numpy import *
from numpy.random import randn

# allocate the cube containing seven parameters for each cell
NX, NY, NZ = 64, 64, 64
# we have same number of cells along each dimension
# however, note the order of dimensions in the Python array !!
C       = ones((NZ, NY, NX, 7), float32)  # start with values 1.0 for all parameters

# calculate cell distances from the centre
k, j, i = indices((NZ, NY, NX), float32)
c       = 0.5*(NX-1.0)                # coordinate value at the centre (since NX=NY=NZ)
i, j, k = (i-c)/c, (j-c)/c, (k-c)/c   # coordinates in the [-1,1] range
r       = sqrt(i*i+j*j+k*k)           # distance from the centre

# Set the values in the cube
# C[k, j, i, ifield] is an element where the LOC x-coordinate is i, y-coordinate j,
#                    and z-coordinate is k !!
C[:,:,:,0]   = exp(-3.0**r*r)         # density values, 3D Gaussian
C[:,:,:,1]  *= 15.0                   # Tkin=15 K in every cell
C[:,:,:,2]  *=  1.0                   # leave microturbulence at 1 km/s
C[:,:,:,3]   = randn(NZ,NY,NX)        # vx, macroscopic velocity
C[:,:,:,4]   = randn(NZ,NY,NX)        # vy  
C[:,:,:,5]   = randn(NZ,NY,NX)        # vz
C[:,:,:,6]   = 1.0                    # abundance values will be scaled later

# Write the actual file
fp = open('my.cloud', 'wb')
asarray([NX, NY, NZ], int32).tofile(fp)  # note again the order of dimensions !!
C.tofile(fp)  # in the file the x-coordinate changes fastest (C-order)
fp.close()
