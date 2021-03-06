# -*- coding: utf-8 -*-

#Based on sXML-master projet on gitHub

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2015 LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

from xml_basics import Container as ctr
from xml_basics import TableXMLNodes  as tb
from xml_basics import Header as hdr
from xml_basics import HeaderItem as hi
from xml_basics import Object as obj
from xml_basics import ObjectItem as oI
from xml_basics import Row as rw
import MaterialProperties as mp
import uuid

idMaterialContainer= mp.containerId
tMaterialContainer= mp.containerProgId

class MaterialTable(tb.TableXMLNodes):
  '''Material XML table.

  Attributes:
    tableId:      Table identifier.
    tableProgId:  Another identifier (redundant?).
  '''
  def __init__(self,matProperties):
    tableId= matProperties.TableId
    tableProgId= matProperties.TableProgId
    super(MaterialTable,self).__init__(tableId,'Materials')
    self.progid= tableProgId
  def populate(self,matDict):
    print "XXX write implementation!"
    

class MaterialContainer(ctr.Container):
  '''Material container.

  Attributes:
    tableGeneric:      Table containing generic materials.
    tableSteelSIA:     Table containing steel material as defined in SIA code.
    tableConcreteSIA:  Table containing concrete material as defined in SIA code.
  '''
  def __init__(self):
    super(MaterialContainer,self).__init__(idMaterialContainer,tMaterialContainer)
    self.tableGeneric= MaterialTable(mp.MaterialProperties.tableGeneric)
    self.tableSteelSIA= MaterialTable(mp.MaterialProperties.tableSteelSIA)
    self.tableConcreteSIA= MaterialTable(mp.MaterialProperties.tableConcreteSIA)

  
