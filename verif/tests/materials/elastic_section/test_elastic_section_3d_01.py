# -*- coding: utf-8 -*-
# Test de funcionamiento de una sección elástica en 3d

import xc_base
import geom
import xc
from solution import predefined_solutions
from model import predefined_spaces
from model import fix_node_6dof
from materials import typical_materials
from materials import parametrosSeccionRectangular
from misc import banco_pruebas_scc3d

prueba= xc.ProblemaEF()
prueba.logFileName= "/tmp/borrar.log" # Para no imprimir mensajes de advertencia.
preprocessor=  prueba.getPreprocessor

# Definición de la sección rectangular
scc10x20=  parametrosSeccionRectangular.RectangularSection("rectang",.10,.20,2.1e6, 0.3)

# Materials definition
matPoteau= scc10x20.defSeccElastica3d(preprocessor)
elemZLS= banco_pruebas_scc3d.modeloSecc3d(preprocessor, scc10x20.nmb)

# Constraints
coacciones= preprocessor.getConstraintLoader

fix_node_6dof.fixNode6DOF(coacciones,1)
fix_node_6dof.Nodo6DOFMovXGiroZLibres(coacciones,2)

# Loads definition
cargas= preprocessor.getLoadLoader
casos= cargas.getLoadPatterns
#Load modulation.
ts= casos.newTimeSeries("constant_ts","ts")
casos.currentTimeSeries= "ts"
#Load case definition
lp0= casos.newLoadPattern("default","0")
#casos.currentLoadPattern= "0"
loadMz= 1e3
lp0.newNodalLoad(2,xc.Vector([0,0,0,0,0,loadMz]))

#We add the load case to domain.
casos.addToDomain("0")


# Solution
analisis= predefined_solutions.simple_static_linear(prueba)
result= analisis.analyze(1)

nodos= preprocessor.getNodeLoader
nodos.calculateNodalReactions(True)
nodos= preprocessor.getNodeLoader

RM= nodos.getNode(1).getReaction[5] 

elementos= preprocessor.getElementLoader
ele1= elementos.getElement(1)
ele1.getResistingForce()
scc0= ele1.getSection()

esfMz= scc0.getStressResultantComponent("Mz")

ratio1= (RM+loadMz)/loadMz
ratio2= (esfMz-loadMz)/loadMz
import os
fname= os.path.basename(__file__)
if (abs(ratio1)<1e-5) & (abs(ratio2)<1e-5) :
  print "test ",fname,": ok."
else:
  print "test ",fname,": ERROR."
