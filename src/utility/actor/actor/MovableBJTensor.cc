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
//MovableBJTensor.cc

#include "MovableBJTensor.h"

#include "utility/actor/channel/Channel.h"
#include "utility/actor/objectBroker/FEM_ObjectBroker.h"
#include "utility/matrix/ID.h"
#include "CommParameters.h"
#include "CommMetaData.h"

//! @brief Constructor.
XC::MovableBJTensor::MovableBJTensor(const int &rank,const double &initval)
  :BJtensor(rank,initval),MovableObject(TENSOR_TAG_BJtensor) {}

//! @brief Constructor.
XC::MovableBJTensor::MovableBJTensor(const BJtensor &v)
  :BJtensor(v),MovableObject(TENSOR_TAG_BJtensor) {}


//! @brief Asigna el vector.
void XC::MovableBJTensor::setBJTensor(const BJtensor &v)
  { BJtensor::operator=(v); }

//! @brief Envia el vector through the channel being passed as parameter.
int XC::MovableBJTensor::sendSelf(CommParameters &cp)
  {
    std::cerr << "MovableBJTensor::sendSelf() - not implemented.\n";
    return 0;
  }

//! @brief Recibe el vector through the channel being passed as parameter.
int XC::MovableBJTensor::recvSelf(const CommParameters &cp)
  {
    std::cerr << "MovableBJTensor::recvSelf() - not implemented.\n";
    return 0;
  }

