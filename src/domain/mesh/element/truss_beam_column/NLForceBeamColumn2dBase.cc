//----------------------------------------------------------------------------
//  XC program; finite element analysis code
//  for structural analysis and design.
//
//  Copyright (C)  Luis Claudio Pérez Tato
//
//  This program derives from OpenSees <http://opensees.berkeley.edu>
//  developed by the  «Pacific earthquake engineering research center».
//
//  Except for the restrictions that may arise from the copyright
//  of the original program (see copyright_opensees.txt)
//  XC is free software: you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation, either version 3 of the License, or 
//  (at your option) any later version.
//
//  This software is distributed in the hope that it will be useful, but 
//  WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details. 
//
//
// You should have received a copy of the GNU General Public License 
// along with this program.
// If not, see <http://www.gnu.org/licenses/>.
//----------------------------------------------------------------------------
//NLForceBeamColumn2dBase.cpp

#include <domain/mesh/element/truss_beam_column/NLForceBeamColumn2dBase.h>
#include <material/section/PrismaticBarCrossSection.h>

#include "utility/actor/actor/MatrixCommMetaData.h"

XC::Matrix XC::NLForceBeamColumn2dBase::theMatrix(6,6);
XC::Vector XC::NLForceBeamColumn2dBase::theVector(6);
double XC::NLForceBeamColumn2dBase::workArea[100];

//! @brief Allocate section flexibility matrices and section deformation vectors
void XC::NLForceBeamColumn2dBase::resizeMatrices(const size_t &nSections)
  {
    fs.resize(nSections);
    vs.resize(nSections);
    Ssr.resize(nSections);
    vscommit.resize(nSections);
  }

// constructor:
// invoked by a FEM_ObjectBroker, recvSelf() needs to be invoked on this object.
XC::NLForceBeamColumn2dBase::NLForceBeamColumn2dBase(int tag,int classTag,int numSec)
  : BeamColumnWithSectionFDTrf2d(tag,classTag,numSec),
    rho(0), maxIters(10), tol(1e-8), initialFlag(0),
    kv(NEBD,NEBD), Se(NEBD), kvcommit(NEBD,NEBD), Secommit(NEBD),
    fs(numSec), vs(numSec), Ssr(numSec), vscommit(numSec), p0()
  {}

// constructor:
// invoked by a FEM_ObjectBroker, recvSelf() needs to be invoked on this object.
XC::NLForceBeamColumn2dBase::NLForceBeamColumn2dBase(int tag,int classTag,int numSec,const Material *m,const CrdTransf *coordTransf)
  : BeamColumnWithSectionFDTrf2d(tag,classTag,numSec,m,coordTransf),
    rho(0), maxIters(10), tol(1e-8), initialFlag(0),
    kv(NEBD,NEBD), Se(NEBD), kvcommit(NEBD,NEBD), Secommit(NEBD),
    fs(numSec), vs(numSec), Ssr(numSec), vscommit(numSec), p0()
  {}

//! @brief Copy constructor.
XC::NLForceBeamColumn2dBase::NLForceBeamColumn2dBase(const NLForceBeamColumn2dBase &other)
  : BeamColumnWithSectionFDTrf2d(other), rho(other.rho), maxIters(other.maxIters), tol(other.tol), initialFlag(other.initialFlag),
    kv(other.kv), Se(other.Se), kvcommit(other.kvcommit), Secommit(other.Secommit),
    fs(other.fs), vs(other.vs), Ssr(other.Ssr), vscommit(other.vscommit), sp(other.sp), p0(other.p0), Ki(other.Ki)
  {}

//! @brief Assignment operator.
XC::NLForceBeamColumn2dBase &XC::NLForceBeamColumn2dBase::operator=(const NLForceBeamColumn2dBase &)
  {
    std::cerr << "NLForceBeamColumn2dBase: No se debe llamar al operador de asignación."
              << std::endl;
    return *this;
  }

// ~NLForceBeamColumn2dBase():
//         destructor
//      delete must be invoked on any objects created by the object
XC::NLForceBeamColumn2dBase::~NLForceBeamColumn2dBase(void)
  {}


int XC::NLForceBeamColumn2dBase::getNumDOF(void) const
  { return NEGD; }


const XC::Matrix &XC::NLForceBeamColumn2dBase::getTangentStiff(void) const
  {
    // Will remove once we clean up the corotational 2d transformation -- MHS
    theCoordTransf->update();
    static Matrix K;
    K= theCoordTransf->getGlobalStiffMatrix(kv, Se);
    if(isDead())
      K*=dead_srf;
    return K;
  }


const XC::Vector &XC::NLForceBeamColumn2dBase::getResistingForce(void) const
  {
    // Will remove once we clean up the corotational 2d transformation -- MHS
    theCoordTransf->update();
    Vector p0Vec= p0.getVector();
    static Vector retval;
    retval= theCoordTransf->getGlobalResistingForce(Se, p0Vec);
    if(isDead())
      retval*=dead_srf;
    return retval;
  }


void XC::NLForceBeamColumn2dBase::initializeSectionHistoryVariables(void)
  {
    const size_t nSections= getNumSections();
    for(size_t i= 0;i<nSections; i++)
      {
        int order = theSections[i]->getOrder();

        fs[i] = Matrix(order,order);
        vs[i] = Vector(order);
        Ssr[i] = Vector(order);

        vscommit[i] = Vector(order);
      }
  }

//! @brief Send members through the channel being passed as parameter.
int XC::NLForceBeamColumn2dBase::sendData(CommParameters &cp)
  {
    int res= BeamColumnWithSectionFDTrf2d::sendData(cp);
    res+= cp.sendDoubles(rho,tol,getDbTagData(),CommMetaData(12));
    res+= cp.sendInts(maxIters,initialFlag,getDbTagData(),CommMetaData(13));
    res+= cp.sendMatrix(kv,getDbTagData(),CommMetaData(14));
    res+= cp.sendVector(Se,getDbTagData(),CommMetaData(15));
    res+= cp.sendMatrix(kvcommit,getDbTagData(),CommMetaData(16));
    res+= cp.sendVector(Secommit,getDbTagData(),CommMetaData(17));
    res+= cp.sendMatrices(fs,getDbTagData(),CommMetaData(18));;
    res+= cp.sendVectors(vs,getDbTagData(),CommMetaData(19));
    res+= cp.sendVectors(Ssr,getDbTagData(),CommMetaData(20));
    res+= cp.sendVectors(vscommit,getDbTagData(),CommMetaData(21));
    res+= cp.sendMatrix(sp,getDbTagData(),CommMetaData(22));
    res+= p0.sendData(cp,getDbTagData(),CommMetaData(23));
    return res;
  }

//! @brief Receives members through the channel being passed as parameter.
int XC::NLForceBeamColumn2dBase::recvData(const CommParameters &cp)
  {
    int res= BeamColumnWithSectionFDTrf2d::recvData(cp);
    res+= cp.receiveDoubles(rho,tol,getDbTagData(),CommMetaData(12));
    res+= cp.receiveInts(maxIters,initialFlag,getDbTagData(),CommMetaData(13));
    res+= cp.receiveMatrix(kv,getDbTagData(),CommMetaData(14));
    res+= cp.receiveVector(Se,getDbTagData(),CommMetaData(15));
    res+= cp.receiveMatrix(kvcommit,getDbTagData(),CommMetaData(16));
    res+= cp.receiveVector(Secommit,getDbTagData(),CommMetaData(17));
    res+= cp.receiveMatrices(fs,getDbTagData(),CommMetaData(18));;
    res+= cp.receiveVectors(vs,getDbTagData(),CommMetaData(19));
    res+= cp.receiveVectors(Ssr,getDbTagData(),CommMetaData(20));
    res+= cp.receiveVectors(vscommit,getDbTagData(),CommMetaData(21));
    res+= cp.receiveMatrix(sp,getDbTagData(),CommMetaData(22));
    res+= p0.receiveData(cp,getDbTagData(),CommMetaData(23));
    return res;
  }
