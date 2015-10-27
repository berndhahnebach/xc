# -*- coding: utf-8 -*-

import xc_base
import geom
import xc

# Typical material definition.


#Linear elastic uniaxial material.
def defElasticMaterial(preprocessor,name,E):
  materiales= preprocessor.getMaterialLoader
  materiales.newMaterial("elastic_material",name)
  retval= materiales.getMaterial(name)
  retval.E= E
  return retval

def defElasticPPMaterial(preprocessor,name,E,fyp,fyn):
  materiales= preprocessor.getMaterialLoader
  materiales.newMaterial("elasticpp_material",name)
  retval= materiales.getMaterial(name)
  retval.E= E
  retval.fyp= fyp
  retval.fyn= fyn
  return retval

def defElastNoTracMaterial(preprocessor,name,E):
  materiales= preprocessor.getMaterialLoader
  materiales.newMaterial("elast_no_trac_material",name)
  retval= materiales.getMaterial(name)
  retval.E= E
  return retval

#Cable material.
def defCableMaterial(preprocessor,name,E,prestress,rho):
  materiales= preprocessor.getMaterialLoader
  materiales.newMaterial("cable_material",name)
  retval= materiales.getMaterial(name)
  retval.E= E
  retval.prestress= prestress
  retval.rho= rho
  return retval


#Steel 01.
def defSteel01(preprocessor,name,E,fy,b):
  materiales= preprocessor.getMaterialLoader
  materiales.newMaterial("steel01",name)
  retval= materiales.getMaterial(name)
  retval.E= E
  retval.fy= fy
  retval.b= b
  return retval

#Steel 02.
def defSteel02(preprocessor,name,E,fy,b,initialStress):
  materiales= preprocessor.getMaterialLoader
  materiales.newMaterial("steel02",name)
  retval= materiales.getMaterial(name)
  retval.E= E
  retval.fy= fy
  retval.b= b
  retval.initialStress= initialStress
  return retval

#Concrete 01.
def defConcrete01(preprocessor,name,epsc0,fpc,fpcu,epscu):
  materiales= preprocessor.getMaterialLoader
  materiales.newMaterial("concrete01_material",name)
  retval= materiales.getMaterial(name)
  retval.epsc0= epsc0
  retval.fpc= fpc
  retval.fpcu= fpcu
  retval.epscu= epscu
  return retval


#Elastic section 2d.
def defElasticSection2d(preprocessor,name,A,E,I):
  materiales= preprocessor.getMaterialLoader
  materiales.newMaterial("elastic_section_2d",name)
  retval= materiales.getMaterial(name)
  retval.sectionProperties.A= A
  retval.sectionProperties.E= E
  retval.sectionProperties.I= I
  return retval

#Elastic shear section 2d.
def defElasticShearSection2d(preprocessor,name,A,E,G,I,alpha):
  materiales= preprocessor.getMaterialLoader
  materiales.newMaterial("elasticShearSection2d",name)
  retval= materiales.getMaterial(name)
  retval.sectionProperties.A= A
  retval.sectionProperties.E= E
  retval.sectionProperties.G= G
  retval.sectionProperties.I= I
  retval.sectionProperties.Alpha= alpha
  return retval

def defElasticSectionFromMechProp2d(preprocessor,name,mechProp2d):
  return defElasticSection2d(preprocessor,name,mechProp2d.A,mechProp2d.E,mechProp2d.I)

#Elastic section 3d.
def defElasticSection3d(preprocessor,name,A,E,G,Iz,Iy,J):
  materiales= preprocessor.getMaterialLoader
  materiales.newMaterial("elastic_section_3d",name)
  retval= materiales.getMaterial(name)
  retval.sectionProperties.A= A
  retval.sectionProperties.E= E
  retval.sectionProperties.G= G
  retval.sectionProperties.Iz= Iz
  retval.sectionProperties.Iy= Iy
  retval.sectionProperties.J= J
  return retval

def defElasticSectionFromMechProp3d(preprocessor,name,mechProp3d):
  return defElasticSection3d(preprocessor,name,mechProp3d.A,mechProp3d.E,mechProp3d.G,mechProp3d.Iz,mechProp3d.Iy,mechProp3d.J)

#Elastic shear section 3d.
def defElasticShearSection3d(preprocessor,name,A,E,G,Iz,Iy,J,alpha):
  materiales= preprocessor.getMaterialLoader
  materiales.newMaterial("elasticShearSection3d",name)
  retval= materiales.getMaterial(name)
  retval.sectionProperties.A= A
  retval.sectionProperties.E= E
  retval.sectionProperties.G= G
  retval.sectionProperties.Iz= Iz
  retval.sectionProperties.Iy= Iy
  retval.sectionProperties.J= J
  retval.sectionProperties.Alpha= alpha
  return retval


#Linear elastic isotropic plane strain material.
def defElasticIsotropicPlaneStrain(preprocessor,name,E,nu,rho):
  materiales= preprocessor.getMaterialLoader
  materiales.newMaterial("elastic_isotropic_plane_strain_2d",name)
  retval= materiales.getMaterial(name)
  retval.E= E
  retval.nu= nu
  retval.rho= rho
  return retval

#Linear elastic isotropic plane stress material.
def defElasticIsotropicPlaneStress(preprocessor,name,E,nu,rho):
  materiales= preprocessor.getMaterialLoader
  materiales.newMaterial("elastic_isotropic_plane_stress_2d",name)
  retval= materiales.getMaterial(name)
  retval.E= E
  retval.nu= nu
  retval.rho= rho
  return retval

#Linear elastic isotropic 3d material.
def defElasticIsotropic3d(preprocessor,name,E,nu,rho):
  materiales= preprocessor.getMaterialLoader
  materiales.newMaterial("elastic_isotropic_3d",name)
  retval= materiales.getMaterial(name)
  retval.E= E
  retval.nu= nu
  retval.rho= rho
  return retval

#Elastic membrane plate section.
def defElasticPlateSection(preprocessor,name,E,nu,rho,h):
  materiales= preprocessor.getMaterialLoader
  materiales.newMaterial("elastic_membrane_plate_section",name)
  retval= materiales.getMaterial(name)
  retval.E= E
  retval.nu= nu
  retval.rho= rho
  retval.h= h
  return retval

#Elastic membrane plate section.
def defElasticMembranePlateSection(preprocessor,name,E,nu,rho,h):
  materiales= preprocessor.getMaterialLoader
  materiales.newMaterial("elastic_membrane_plate_section",name)
  retval= materiales.getMaterial(name)
  retval.E= E
  retval.nu= nu
  retval.rho= rho
  retval.h= h
  return retval
