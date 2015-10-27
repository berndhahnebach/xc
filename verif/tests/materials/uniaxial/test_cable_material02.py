# -*- coding: utf-8 -*-
# Test tomado del manual de Ansys
# Referencia:  Strength of Material, Part I, Elementary Theory and Problems, pg. 26, problem 10
import xc_base
import geom
import xc
from solution import predefined_solutions
from model import predefined_spaces
from materials import typical_materials


E= 30e6 # Young modulus (psi)
l= 10 # Longitud del cable en pulgadas
sigmaPret= 1000.0 # Magnitud del pretensado en libras
area= 2.0
fPret= sigmaPret*area # Magnitud del pretensado en libras

# Model definition
prueba= xc.ProblemaEF()
preprocessor=  prueba.getPreprocessor
nodos= preprocessor.getNodeLoader

# Problem type
predefined_spaces.gdls_elasticidad2D(nodos)


nodos.defaultTag= 1 #First node number.
nod= nodos.newNodeXY(0,0)
nod= nodos.newNodeXY(l,0.0)

# Materials definition
mat= typical_materials.defCableMaterial(preprocessor, "cable",E,sigmaPret,0.0)
    
''' Se definen nodos en los puntos de aplicación de
la carga. Puesto que no se van a determinar tensiones
se emplea una sección arbitraria de área unidad '''
    
# Elements definition
elementos= preprocessor.getElementLoader
elementos.defaultMaterial= "cable"
elementos.dimElem= 2
truss= elementos.newElement("corot_truss",xc.ID([1,2]));
truss.area= area
    
# Constraints
coacciones= preprocessor.getConstraintLoader
spc= coacciones.newSPConstraint(1,0,0.0) # Nodo 1
spc= coacciones.newSPConstraint(1,1,0.0)
spc= coacciones.newSPConstraint(2,0,0.0) # Nodo 2
spc= coacciones.newSPConstraint(2,1,0.0)



# Solution
analisis= predefined_solutions.simple_static_linear(prueba)
result= analisis.analyze(1)



nodos.calculateNodalReactions(True)
nodos= preprocessor.getNodeLoader
R1= nodos.getNode(2).getReaction[0] 
R2= nodos.getNode(1).getReaction[0] 


ratio1= (abs(R1-fPret)/fPret)
ratio2= (abs(R2+fPret)/fPret)
    
''' 
print "R1= ",R1
print "fPret= ", fPret
print "ratio1= ",ratio1
print "R2= ",R2
print "ratio2= ",(ratio2)
   '''
    
import os
fname= os.path.basename(__file__)
if (abs(ratio1)<1e-5) & (abs(ratio2)<1e-5):
  print "test ",fname,": ok."
else:
  print "test ",fname,": ERROR."
