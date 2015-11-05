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
//MapEnt.h

#ifndef MAPENT_H
#define MAPENT_H

#include "preprocessor/cad/MapCadMember.h"
#include "EntMdlr.h"
#include <map>
#include "xc_utils/src/base/any_const_ptr.h"

namespace XC {

//! @ingroup Cad
//
//! @brief Contenedor de entidades de CAD (puntos, líneas, superficies,...).
template <class T>
class MapEnt: public MapCadMember<T>
  {
  protected:
    virtual bool procesa_comando(CmdStatus &status);
  public:
    typedef typename MapCadMember<T>::iterator iterator;
    typedef typename MapCadMember<T>::const_iterator const_iterator;

    MapEnt(Cad *cad= NULL);

    T *getNearest(const Pos3d &p);
    const T *getNearest(const Pos3d &p) const;

    void EjecutaBloqueForEach(CmdStatus &status,const std::string &bloque);

    void numera(void);
  };

//! @brief Constructor.
template <class T>
MapEnt<T>::MapEnt(Cad *cad)
  : MapCadMember<T>(cad) {}

//! @brief Lee un objeto Edge desde el archivo de entrada.
template <class T>
bool MapEnt<T>::procesa_comando(CmdStatus &status)
  {
    const std::string cmd= this->deref_cmd(status.Cmd());
    const std::string str_err= "(MapEnt) Procesando comando: " + cmd;
    if(this->verborrea>2)
      std::clog << str_err << std::endl;

    if(cmd == "for_each")
      {
        const std::string bloque= status.GetBloque();
        EjecutaBloqueForEach(status,bloque);
        return true;
      }
    else
      return MapCadMember<T>::procesa_comando(status);
  }

//! @brief Devuelve el objeto más cercano a la posición que se pasa como parámetro.
template <class T>
T *MapEnt<T>::getNearest(const Pos3d &p)
  {
    //El código comentado da problemas (recursión infinita) si
    //se llama a la función desde boost.python
    /* MapEnt<T> *this_no_const= const_cast<MapEnt<T> *>(this); */
    /* return const_cast<T *>(this_no_const->getNearest(p)); */
    T *retval= NULL;
    if(!this->empty())
      {
	iterator i= this->begin();
        double d2= (*i).second->DistanciaA2(p);
        retval= (*i).second; i++;
        double tmp;
        for(;i!=this->end();i++)
          {
            tmp= (*i).second->DistanciaA2(p);
            if(tmp<d2)
              {
                d2= tmp;
                retval= (*i).second;
              }
          }
      }
    return retval;
  }

//! @brief Devuelve el objeto más cercano a la posición que se pasa como parámetro.
template <class T>
const T *MapEnt<T>::getNearest(const Pos3d &p) const
  {
    const T *retval= NULL;
    if(!this->empty())
      {
	const_iterator i= this->begin();
        double d2= (*i).second->DistanciaA2(p);
        retval= (*i).second; i++;
        double tmp;
        for(;i!=this->end();i++)
          {
            tmp= (*i).second->DistanciaA2(p);
            if(tmp<d2)
              {
                d2= tmp;
                retval= (*i).second;
              }
          }
      }
    return retval;
  }

//!  @brief Asigna índices a los objetos de la lista para poder emplearlos en VTK.
template <class T>
void MapEnt<T>::numera(void)
  {
    size_t idx= 0;
    for(iterator i= this->begin();i!=this->end();i++,idx++)
      {
        EntMdlr *ptr= (*i).second;
        ptr->set_indice(idx);
      }
  }

//! @brief Solicita a cada entidad del contenedor que ejecute
//! el bloque de código que se le pasa como parámetro.
template <class T>
void MapEnt<T>::EjecutaBloqueForEach(CmdStatus &status,const std::string &bloque)
  {
    const std::string nmbBlq= this->nombre_clase()+":for_each";
    std::string tmp;
    for(iterator i=this->begin();i!= this->end();i++)
      {
        tmp= nmbBlq+":"+(*i).second->GetNombre();
        (*i).second->EjecutaBloque(status,bloque,tmp);
      }
  }

} //fin namespace XC
#endif