//----------------------------------------------------------------------------
//  programa XC; cálculo mediante el método de los elementos finitos orientado
//  a la solución de problemas estructurales.
//
//  Copyright (C)  Luis Claudio Pérez Tato
//
//  El programa deriva del denominado OpenSees <http://opensees.berkeley.edu>
//  desarrollado por el «Pacific earthquake engineering research center».
//
//  Salvo las restricciones que puedan derivarse del copyright del
//  programa original (ver archivo copyright_opensees.txt) este
//  software es libre: usted puede redistribuirlo y/o modificarlo 
//  bajo los términos de la Licencia Pública General GNU publicada 
//  por la Fundación para el Software Libre, ya sea la versión 3 
//  de la Licencia, o (a su elección) cualquier versión posterior.
//
//  Este software se distribuye con la esperanza de que sea útil, pero 
//  SIN GARANTÍA ALGUNA; ni siquiera la garantía implícita
//  MERCANTIL o de APTITUD PARA UN PROPÓSITO DETERMINADO. 
//  Consulte los detalles de la Licencia Pública General GNU para obtener 
//  una información más detallada. 
//
// Debería haber recibido una copia de la Licencia Pública General GNU 
// junto a este programa. 
// En caso contrario, consulte <http://www.gnu.org/licenses/>.
//----------------------------------------------------------------------------
/* ****************************************************************** **
**    OpenSees - Open System for Earthquake Engineering Simulation    **
**          Pacific Earthquake Engineering Research Center            **
**                                                                    **
**                                                                    **
** (C) Copyright 1999, The Regents of the University of California    **
** All Rights Reserved.                                               **
**                                                                    **
** Commercial use of this program without express permission of the   **
** University of California, Berkeley, is strictly prohibited.  See   **
** file 'COPYRIGHT'  in main directory for information on usage and   **
** redistribution,  and for a DISCLAIMER OF ALL WARRANTIES.           **
**                                                                    **
** Developed by:                                                      **
**   Frank McKenna (fmckenna@ce.berkeley.edu)                         **
**   Gregory L. Fenves (fenves@ce.berkeley.edu)                       **
**   Filip C. Filippou (filippou@ce.berkeley.edu)                     **
**                                                                    **
** ****************************************************************** */
                                                                        
// $Revision: 1.3 $
// $Date: 2008/08/26 16:49:19 $
// $Source: /usr/local/cvs/OpenSees/SRC/material/section/ElasticShearSection3d.cpp,v $

#include "material/section/elastic_section/ElasticShearSection3d.h"
#include "preprocessor/loaders/MaterialLoader.h"
#include "utility/matrix/Matrix.h"
#include "xc_utils/src/base/CmdStatus.h"
#include "xc_utils/src/base/any_const_ptr.h"
#include "xc_utils/src/base/utils_any.h"
#include <cstdlib>
#include "material/section/ResponseId.h"

XC::Vector XC::ElasticShearSection3d::s(6);
XC::Matrix XC::ElasticShearSection3d::ks(6,6);

XC::ElasticShearSection3d::ElasticShearSection3d(void)
  :BaseElasticSection3d(0, SEC_TAG_Elastic3d,6) {}

XC::ElasticShearSection3d::ElasticShearSection3d(int tag, MaterialLoader *mat_ldr)
  :BaseElasticSection3d(tag, SEC_TAG_Elastic3d,6,mat_ldr) {}

const XC::Vector &XC::ElasticShearSection3d::getStressResultant(void) const
  {
    const Vector &e= getSectionDeformation();
    s(0) = ctes_scc.EA()*e(0);
    s(1) = ctes_scc.EIz()*e(1);
    s(3) = ctes_scc.EIy()*e(3);
    s(5) = ctes_scc.GJ()*e(5);

    const double GA= ctes_scc.GAAlpha();
    s(2)= GA*e(2);
    s(4)= GA*e(4);
    return s;
  }

const XC::Matrix &XC::ElasticShearSection3d::getSectionTangent(void) const
  { return ctes_scc.getSectionTangent6x6(); }

const XC::Matrix &XC::ElasticShearSection3d::getInitialTangent(void) const
  { return ctes_scc.getInitialTangent6x6(); }

const XC::Matrix &XC::ElasticShearSection3d::getSectionFlexibility(void) const
  { return ctes_scc.getSectionFlexibility6x6(); }

const XC::Matrix &XC::ElasticShearSection3d::getInitialFlexibility(void) const
  { return ctes_scc.getInitialFlexibility6x6(); }

XC::SectionForceDeformation *XC::ElasticShearSection3d::getCopy(void) const
  { return new ElasticShearSection3d(*this); }

const XC::ResponseId &XC::ElasticShearSection3d::getType(void) const
  { return RespElasticShSection3d; }

int XC::ElasticShearSection3d::getOrder(void) const
  { return 6; }

//! @brief Envía los miembros del objeto a través del canal que se pasa como parámetro.
int XC::ElasticShearSection3d::sendData(CommParameters &cp)
  {
    int res= BaseElasticSection3d::sendData(cp);
    setDbTagDataPos(9,parameterID);
    return res;
  }

//! @brief Recibe los miembros del objeto a través del canal que se pasa como parámetro.
int XC::ElasticShearSection3d::recvData(const CommParameters &cp)
  {
    int res= BaseElasticSection3d::recvData(cp);
    parameterID= getDbTagDataPos(9);
    return res;
  }

int XC::ElasticShearSection3d::sendSelf(CommParameters &cp)
  {
    setDbTag(cp);
    const int dataTag= getDbTag();
    inicComm(3);
    int res= sendData(cp);

    res+= cp.sendIdData(getDbTagData(),dataTag);
    if(res < 0)
      std::cerr << nombre_clase() << "sendSelf() - failed to send data\n";
    return res;
  }

int XC::ElasticShearSection3d::recvSelf(const CommParameters &cp)
  {
    inicComm(3);
    const int dataTag= getDbTag();
    int res= cp.receiveIdData(getDbTagData(),dataTag);

    if(res<0)
      std::cerr << nombre_clase() << "::recvSelf - failed to receive ids.\n";
    else
      {
        setTag(getDbTagDataPos(0));
        res+= recvData(cp);
        if(res<0)
          std::cerr << nombre_clase() << "::recvSelf - failed to receive data.\n";
      }
    return res;
  }
 
void XC::ElasticShearSection3d::Print(std::ostream &s, int flag) const
  {
    if(flag == 2)
     {}
    else
     {
       s << "ElasticShearSection3d, tag: " << this->getTag() << std::endl;
       ctes_scc.Print(s);
     }
  }

int XC::ElasticShearSection3d::setParameter(const std::vector<std::string> &argv, Parameter &param)
  {
    if(argv.size() < 1)
      return -1;
    else
      return ctes_scc.setParameter(argv,param,this);
  }

int XC::ElasticShearSection3d::updateParameter(int paramID, Information &info)
  { return ctes_scc.updateParameter(paramID,info); }

int XC::ElasticShearSection3d::activateParameter(int paramID)
  {
    parameterID = paramID;
    return 0;
  }

const XC::Vector &XC::ElasticShearSection3d::getStressResultantSensitivity(int gradIndex, bool conditional)
  {
    s.Zero();

//     if(parameterID == 1) { // E
//     s(0) = A*e(0);
//     s(1) = Iz*e(1);
//     s(3) = Iy*e(3);
//   }
//   if (parameterID == 2) { // A
//     s(0) = E*e(0);
//     double Galpha = G*alpha;
//     s(2) = Galpha*e(2);
//     s(4) = Galpha*e(4);
//   }
//   if (parameterID == 3) // Iz
//     s(1) = E*e(1);
//   if (parameterID == 4) // Iy
//     s(3) = E*e(3);
//   if (parameterID == 5) { // G
//     double Aalpha = A*alpha;
//     s(2) = Aalpha*e(2);
//     s(4) = Aalpha*e(4);
//     s(5) = J*e(5);
//   }
//   if (parameterID == 6) // J
//     s(5) = G*e(5);
//   if (parameterID == 7) { // alpha
//     double GA = G*A;
//     s(2) = GA*e(2);
//     s(4) = GA*e(4);
//   }

  return s;
}

const XC::Matrix &XC::ElasticShearSection3d::getInitialTangentSensitivity(int gradIndex)
  {
    ks.Zero();
    return ks;
  }
