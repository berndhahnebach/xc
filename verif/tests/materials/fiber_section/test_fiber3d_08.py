# -*- coding: utf-8 -*-
# Test de funcionamiento del comando addFiber

import xc_base
import geom
import xc
from model import predefined_spaces
from solution import predefined_solutions
from materials import typical_materials
import math

yF= 2.0 # Fibra en el cuarto cuadrante.
zF= -3.0
F= 2100
MomY= F*zF
MomZ= F*yF
MomYDqFibras= 0.0
MomZDqFibras= 0.0
Es= 2.1e6
Area= 1.0
eps= F/(Area*Es)

# Problem type
prueba= xc.ProblemaEF()
prueba.logFileName= "/tmp/borrar.log" # Para no imprimir mensajes de advertencia.
preprocessor=  prueba.getPreprocessor
nodos= preprocessor.getNodeLoader
predefined_spaces.gdls_resist_materiales3D(nodos)
nodos.defaultTag= 1 #First node number.
nod= nodos.newNodeXYZ(1,0,0)
nod= nodos.newNodeXYZ(1,0,0)


# Definimos materiales
A= 0.0
yG= 0.0
zG= 0.0

IEA= 0.0; IK12= 0.0; IK13= 0.0
IK21= 0.0; IEIy= 0.0; IK23= 0.0
IK31= 0.0; IK32= 0.0; IEIz= 0.0

TEA= 0.0; TK12= 0.0; TK13= 0.0
TK21= 0.0; TEIy= 0.0; TK23= 0.0
TK31= 0.0; TK32= 0.0; TEIz= 0.0

elast0= typical_materials.defElasticMaterial(preprocessor, "elast0",Es)
# Secciones
prb= preprocessor.getMaterialLoader.newMaterial("fiber_section_3d","prb")

prb.addFiber("elast0",Area,xc.Vector([yF,zF]))

A= prb.getArea
yG= prb.getCdgY()
zG= prb.getCdgZ()
IEA= prb.getInitialTangentStiffness().at(1,1)
IK12= prb.getInitialTangentStiffness().at(1,2)
IK13= prb.getInitialTangentStiffness().at(1,3)
IK21= prb.getInitialTangentStiffness().at(2,1)
IEIy= prb.getInitialTangentStiffness().at(2,2)
IK23= prb.getInitialTangentStiffness().at(2,3)
IK31= prb.getInitialTangentStiffness().at(3,1)
IK32= prb.getInitialTangentStiffness().at(3,2)
IEIz= prb.getInitialTangentStiffness().at(3,3)

prb.setTrialSectionDeformation(xc.Vector([eps,0.0,0.0]))
TEA= prb.getTangentStiffness().at(1,1)
TK12= prb.getTangentStiffness().at(1,2)
TK13= prb.getTangentStiffness().at(1,3)
TK21= prb.getTangentStiffness().at(2,1)
TEIy= prb.getTangentStiffness().at(2,2)
TK23= prb.getTangentStiffness().at(2,3)
TK31= prb.getTangentStiffness().at(3,1)
TK32= prb.getTangentStiffness().at(3,2)
TEIz= prb.getTangentStiffness().at(3,3)

R= prb.getStressResultant()
fibras= prb.getFibers()
MomYDqFibras= fibras.getMy(0.0)
MomZDqFibras= fibras.getMz(0.0)




ratio1= R[0]-F
ratio2= R[1]-MomZ
ratio3= R[2]-MomY
ratio4= R[1]-MomZDqFibras
ratio5= R[2]-MomYDqFibras

''' 
print "F= ",F
print "MomY= ",MomY
print "MomZ= ",MomZ
print "MomYDqFibras= ",MomYDqFibras
print "MomZDqFibras= ",MomZDqFibras
print "A= ",A
print "eps= ",eps
print "yG= ",yG
print "zG= ",zG,"\n\n"
print "IEA= ",IEA, " IK12= ",IK12, " IK13= ",IK13
print "IK21= ",IK21, " IEIy= ",IEIy, " IK23= ",IK23
print "IK31= ",IK31, " IK32= ",IK32, " IEIz= ",IEIz,"\n\n"

print "TEA= ",TEA, " TK12= ",TK12, " TK13= ",TK13
print "TK21= ",TK21, " TEIy= ",TEIy, " TK23= ",TK23
print "TK31= ",TK31, " TK32= ",TK32, " TEIz= ",TEIz,"\n\n"

print "R= ",R

print "ratio1= ",(ratio1)
print "ratio2= ",(ratio2)
print "ratio3= ",(ratio3)
print "ratio4= ",(ratio4)
'''

import os
fname= os.path.basename(__file__)
if (abs(ratio1)<1e-15) & (abs(ratio2)<1e-15) & (abs(ratio3)<1e-15) & (abs(ratio4)<1e-15) & (abs(ratio5)<1e-15) :
  print "test ",fname,": ok."
else:
  print "test ",fname,": ERROR."
