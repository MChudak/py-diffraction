"""
2D Diffraction on a single linear shutter

Created on Sun Jul 31 10:34:16 2011

@author: macioosch
"""

from math import sin, sqrt, pi
import os
import Gnuplot     # you may comment that, also look on the last lines below


def findfreeindex(path,name):
    i=0
    
    if os.path.exists(path+'/.'+name):
        with open(path+'/.'+name,'r') as lastindex:
            i=int(lastindex.read())+1
    
    while i<1000 and os.path.exists(path+'/'+name+str(i).zfill(3)):
        i+=1
    
    with open(path+'/.'+name,'w') as lastindex:
        lastindex.write(str(i))
        
    return path+'/'+name+str(i).zfill(3)
        


# file settings:

myname='shutter'            # whatever you like

dir = os.path.dirname(__file__)

mypath=dir+'/output'        # files will be written to 'output' folder

if not os.path.exists(mypath):
    os.makedirs(mypath)
    
outputpath=findfreeindex(mypath,myname)
    
output=open(outputpath, 'w\n')

                            # every distance is in meters

lamb=5.*10**-7              # len :wavelength is 500nm (visible light)

d=1.*10**-5                 # len of the shutter
h=1.*10**+0                 # len from shutter to screen

ct=0.*10**+0                # len that light passed during time t (phase)

test_start=0.*10**+0        # len from across the middle of the shutter
                            #     to first computed point
test_len=2.*10**-1          # len from first to last computed point

n=1001                      # num of computed component waves
points=20001                # num of computed intensities

output.write('### settings:\n')
output.write('###\n')
output.write('### wavelength = '+str(lamb)+' m\n')
output.write('### len to first point = '+str(test_start)+' m\n')
output.write('### len from first to last point = '+str(test_len)+' m\n')
output.write('### len of the shutter = '+str(d)+' m\n')
output.write('### len from shutter to screen = '+str(h)+' m\n')
output.write('### len that light passed during time t (phase) = '+str(ct)+' m\n')
output.write('### num of analysed component waves = '+str(n)+'\n')
output.write('### num of computed points = '+str(points)+'\n')
output.write('###\n')
output.write('### [format: $value1 $value2, where:\n')
output.write('###  $value1 is distance from the point across the middle of shutter,\n')
output.write('###  and $value2 is the computed wave intensity]\n')
output.write('###\n')
output.write('### data start:\n')
output.write('###\n')

for point in range(points):
    p_x=float(point*test_len/(points-1)+test_start)
    A=0.
    
    for wave in range(n):
        w_x=float(wave*d/(n-1))
        L=sqrt((d/2-w_x-p_x)**2+h**2)
        A+=sin(2*pi*(L+ct)/lamb)/L # A isn't Amplitude until multiplied by h/n...
    
    I=(h*A/n)**2                  #...which is done here (because h,n=const)
    
    proc='(%03d%%)' % round(100*(point+1)/points, 0)
    print proc, p_x, I
    output.write(str(p_x)+' '+str(I)+'\n')
    # p_x is in meters,
    # I is in relative power per area units (real k*watts/m**2)

output.close()


# IF YOU DON'T HAVE Gnuplot just comment all this below
# (and the import statement at the beggining):

myplot = Gnuplot.Gnuplot(persist=1)
myplot.xlabel('distance [m]')
myplot.ylabel('wave intensity [relative units]')
myplot.plot('\''+outputpath+'\' w l')
