# -*- coding: utf-8 -*-
# home made test
from __future__ import division
import xc_base
import geom
import xc
from solution import predefined_solutions
from model import predefined_spaces
from materials import typical_materials

# Problem type
prueba= xc.ProblemaEF()
preprocessor=  prueba.getPreprocessor   
nodos= preprocessor.getNodeLoader
predefined_spaces.gdls_resist_materiales3D(nodos)
nodos.defaultTag= 1 #First node number.
nod= nodos.newNodeXYZ(0,0,0)
nod= nodos.newNodeXYZ(5,5,5)

# Definimos transformaciones geométricas
trfs= preprocessor.getTransfCooLoader
lin= trfs.newPDeltaCrdTransf3d("lin")
lin.xzVector= xc.Vector([0,1,0])

# Materials
seccion= typical_materials.defElasticSection3d(preprocessor, "seccion",1,1,1,1,1,1)
   
# Elements definition
elementos= preprocessor.getElementLoader

elementos.defaultTransformation= "lin" # Transformación de coordenadas para los nuevos elementos
elementos.defaultTag= 1 #Tag for the next element.
elementos.defaultMaterial= "seccion"
beam3d= elementos.newElement("elastic_beam_3d",xc.ID([1,2]))

crdTransf= beam3d.getCoordTransf

# print "vector I:",getIVector
# print "vector J:",getJVector
# print "vector K:",getKVector
vILocal= crdTransf.getVectorLocalCoordFromGlobal(crdTransf.getIVector)
vJLocal= crdTransf.getVectorLocalCoordFromGlobal(crdTransf.getJVector)
vKLocal= crdTransf.getVectorLocalCoordFromGlobal(crdTransf.getKVector)
# print "vector I en locales:",vILocal
# print "vector J en locales:",vJLocal
# print "vector K en locales:",vJLocal
ratio1= (vILocal-xc.Vector([1,0,0])).Norm()
ratio2= (vJLocal-xc.Vector([0,1,0])).Norm()
ratio3= (vKLocal-xc.Vector([0,0,1])).Norm()




    


import os
fname= os.path.basename(__file__)
if (abs(ratio1)<1e-12) & (abs(ratio2)<1e-12) & (abs(ratio3)<1e-12):
  print "test ",fname,": ok."
else:
  print "test ",fname,": ERROR."
