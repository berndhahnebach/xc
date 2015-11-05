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
//MapEsquemas2d.h

#ifndef MAPEsquemas2d_H
#define MAPEsquemas2d_H

#include "preprocessor/cad/MapCadMember.h"
#include "boost/lexical_cast.hpp"
#include "xc_utils/src/base/utils_any.h"

namespace XC {
class MatrizPtrPnt;

//! @ingroup Cad
//
//! @brief Contenedor de puntos del modelo.
class MapEsquemas2d: public MapCadMember<MatrizPtrPnt>
  {
  protected:
    MatrizPtrPnt *Crea(void);

    virtual bool procesa_comando(CmdStatus &status);
  public:
    MapEsquemas2d(Cad *cad= NULL);

    MatrizPtrPnt *makeNew(void);
    MatrizPtrPnt *Nuevo(CmdStatus &);

    any_const_ptr GetProp(const std::string &cod) const;
  };

} //fin namespace XC
#endif