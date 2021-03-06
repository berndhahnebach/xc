# -*- coding: utf-8 -*-
# Taken from page 114 of the article Development of Membrane, Plate and
# Flat Shell Elements in Java

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AOO)"
__copyright__= "Copyright 2015, LCPT and AOO"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

L= 6.0 # Beam length expressed in inches.
h= 0.8 # Beam cross-section depth expressed in inches.
t= 1 # Beam cross-section width expressed in inches. In the article t= 0.2 was written by mistake.
E= 30000 # Young modulus of the material expressed in ksi.
nu= 0.3 # Poisson's ratio.
# Load
F= 10 # Load magnitude en kips

import xc_base
import geom
import xc
from model import predefined_spaces
from solution import predefined_solutions
from materials import typical_materials

# Problem type
feProblem= xc.FEProblem()
preprocessor=  feProblem.getPreprocessor
nodes= preprocessor.getNodeHandler

modelSpace= predefined_spaces.SolidMechanics2D(nodes)

nodes.defaultTag= 1; nodes.newNodeXY(0,0)
nodes.defaultTag= 2; nodes.newNodeXY(L/3,0)
nodes.defaultTag= 3; nodes.newNodeXY(2*L/3,0)
nodes.defaultTag= 4; nodes.newNodeXY(L,0)
nodes.defaultTag= 5; nodes.newNodeXY(0,h)
nodes.defaultTag= 6; nodes.newNodeXY(L/3,h)
nodes.defaultTag= 7; nodes.newNodeXY(2*L/3,h)
nodes.defaultTag= 8; nodes.newNodeXY(L,h)


# Materials definition
elast2d= typical_materials.defElasticIsotropicPlaneStress(preprocessor, "elast2d",E,nu,0.0)

elements= preprocessor.getElementHandler
elements.defaultMaterial= "elast2d"
quad1= elements.newElement("FourNodeQuad",xc.ID([1,2,6,5]))
quad1.thickness= t
quad2= elements.newElement("FourNodeQuad",xc.ID([2,3,7,6]))
quad2.thickness= t
quad3= elements.newElement("FourNodeQuad",xc.ID([3,4,8,7]))
quad3.thickness= t

# Constraints
constraints= preprocessor.getBoundaryCondHandler

spc= constraints.newSPConstraint(1,0,0.0)
spc= constraints.newSPConstraint(1,1,0.0)
spc= constraints.newSPConstraint(5,0,0.0)
spc= constraints.newSPConstraint(5,1,0.0)

# Loads definition
loadHandler= preprocessor.getLoadHandler

lPatterns= loadHandler.getLoadPatterns

#Load modulation.
ts= lPatterns.newTimeSeries("constant_ts","ts")
lPatterns.currentTimeSeries= "ts"
#Load case definition
lp0= lPatterns.newLoadPattern("default","0")
lp0.newNodalLoad(8,xc.Vector([0,-F]))

#We add the load case to domain.
lPatterns.addToDomain("0")


# Solution
analisis= predefined_solutions.simple_static_linear(feProblem)
analOk= analisis.analyze(1)


nodes.calculateNodalReactions(True,1e-7)
 
nod1= nodes.getNode(1)


# print "reac node 1: ",reac
Fx= nod1.getReaction[0]
Fy= nod1.getReaction[1]
# \print{"Fx= ",Fx
#print "Fy= ",Fy}

nod3= nodes.getNode(3)
disp= nod3.getDisp
UX3= disp[0] # Node 3 xAxis displacement
UY3= disp[1] # Node 3 yAxis displacement


nod5= nodes.getNode(5)


# print "reac node 5: ",reac
Fx= (Fx+nod5.getReaction[0])
Fy= (Fy+nod5.getReaction[1])
# \print{"Fx= ",Fx
#print "Fy= ",Fy}

nod8= nodes.getNode(8)

# print .getDisp
                     
UX8= nod8.getDisp[0] # Node 8 xAxis displacement
UY8= nod8.getDisp[1] # Node 8 yAxis displacement


UX8SP2K= 0.016110
UY8SP2K= -0.162735
UX3SP2K= -0.014285
UY3SP2K= -0.084652


# Differences from the results attributed to SAP-2000 in that article.
ratio1= abs(((UX8-UX8SP2K)/UX8SP2K))
ratio2= abs(((UY8-UY8SP2K)/UY8SP2K))
ratio3= abs(((UX3-UX3SP2K)/UX3SP2K))
ratio4= abs(((UY3-UY3SP2K)/UY3SP2K))
ratio5= abs(((Fy-F)/F))

''' 
print "Fx= ",Fx
print "Fy= ",Fy
print "UX8= ",UX8
print "UX8SP2K= ",UX8SP2K
print "UY8= ",UY8
print "UY8SP2K= ",UY8SP2K
print "UX3= ",UX3
print "UX3SP2K= ",UX3SP2K
print "UY3= ",UY3
print "UY3SP2K= ",UX3SP2K

print "ratio1= ",ratio1
print "ratio2= ",ratio2
print "ratio3= ",ratio3
print "ratio4= ",ratio4
print "ratio5= ",ratio5
print "analOk= ",analOk
 '''

import os
from miscUtils import LogMessages as lmsg
fname= os.path.basename(__file__)
if (abs(ratio1)<1e-5) & (abs(ratio2)<1e-5) & (abs(ratio3)<1e-5) & (abs(ratio4)<1e-5) & (abs(ratio5)<1e-12) & (analOk == 0.0):
  print "test ",fname,": ok."
else:
  lmsg.error(fname+' ERROR.')
