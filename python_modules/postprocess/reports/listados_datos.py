# -*- coding: utf-8 -*-

# Obtiene un listado de los puntos del conjunto cuyo nombre se pasa como parámetro.
def listaKPtsSet(preprocessor,nmbSet, nmbArchivo, fmt):
  caption= "Puntos del conjunto: "+nmbSet
  defCampos= "|r|r|r|r|"
  idsCampos= "Id & x & y & z"
  cabeceraSupertabular(nmbArchivo,4,defCampos,idsCampos,caption)
  setPuntos= preprocessor.getSetLoader.getSet(nmbSet)
  puntos= setPuntos.getPoints()
  for p in puntos:
    nmbArchivo.write(p.tag," & ",fmt.format(p.pos.x)," & ",fmt.format(p.pos.y)," & ",fmt.format(p.pos.z),"\\\\\n")
  cierraSupertabular(nmbArchivo) 

# Obtiene un listado de los elementos del conjunto cuyo nombre se pasa como parámetro.
def listaLineasSet(nmbSet, nmbArchivo):
  caption= "Lineas del conjunto: "+nmbSet
  defCampos= "|r|r|c|"
  idsCampos= "Id & nDiv & Puntos"
  cabeceraSupertabular(nmbArchivo,3,defCampos,idsCampos,caption) 
  setLineas= preprocessor.getSetLoader.getSet(nmbSet)
  lineas= setLineas.getLines()
  for l in lineas:
    nmbArchivo.write(l.tag," & ",l.ndiv," & ",l.kPts,"\\\\\n")
  cierraSupertabular(nmbArchivo)

# Obtiene un listado de los nodos del conjunto cuyo nombre se pasa como parámetro.
def listaNodosSet(preprocessor, nmbSet, nmbArchivo, fmt):
  caption= "Nodos del conjunto: "+nmbSet
  defCampos= "|r|r|r|r|"
  idsCampos= "Id & x & y & z"
  cabeceraSupertabular(nmbArchivo,4,defCampos,idsCampos,caption) 
  s= preprocessor.getSetLoader.getSet(nmbSet)
  nodes= s.getNodes()
  for n in nodes:
    pos= n.getPos()
    nmbArchivo.write(n.tag," & ",fmt.format(pos.x)," & ",fmt.format(pos.y)," & ",fmt.format(pos.z),"\\\\\n")
  cierraSupertabular(nmbArchivo) 

# Obtiene un listado de los elementos del conjunto cuyo nombre se pasa como parámetro.
def listaElementosSet(preprocessor, nmbSet, nmbArchivo):
  nmbArchivo.write("Elementos del conjunto: ",nmbSet,"\n")
  s= preprocessor.getSetLoader.getSet(nmbSet)
  elems= s.getElements()
  for e in elems:
    nmbArchivo.write(e.tag," & ",e.nod(0).tag," & ",e.nod(1).tag,"\\\\\n")

# Obtiene un listado de los elementos del conjunto cuyo nombre se pasa como parámetro.
def listaElementosTrussSet(preprocessor, nmbSet, nmbArchivo, fmt):
  caption= "Elementos del conjunto: "+nmbSet
  defCampos= "|r|r|r|r|"
  idsCampos= "Id & nI & nJ & Mater."
  cabeceraSupertabular(nmbArchivo,4,defCampos,idsCampos,caption) 
  s= preprocessor.getSetLoader.getSet(nmbSet)
  elems= s.getElements()
  for e in elems:
    nmbArchivo.write(e.tag," & ",e.nod(0).tag," & ",e.nod(1).tag," & ",e,getMaterial().tag,"\\\\\n")
  cierraSupertabular(nmbArchivo) 

# Obtiene un listado de los elementos del conjunto cuyo nombre se pasa como parámetro.
def listaElementosBarraSet(preprocessor, nmbSet, fName, fmt):
  caption= "Elementos del conjunto: "+nmbSet
  defCampos= "|r|r|r|r|r|r|r|r|r|r|r|"
  idsCampos= " Id & nI  & nJ  &Sc.&  E     &  G     & Area   & alpha &    J     &   Iy    &    Iz  \\\\\n -  &     &  -  & - & GPa    & GPa    &  cm2   &   -   &   cm4    &  cm4    &   cm4"
  cabeceraSupertabular(nmbArchivo,11,defCampos,idsCampos,caption) 
  s= preprocessor.getSetLoader.getSet(nmbSet)
  elems= s.getElements()
  for e in elems:
    str= str(e.tag)+" & "+str(e.nod(0).tag)+" & "+str(e.nod(1).tag)+" & "
    k= 0
    secciones= e.getSections()
    for s in secciones:
      fName.write(str,k," & ")
      fName.write(fmt.format(s.getE()/1e9)," & ",fmt.format(s.getG()/1e9)," & ",fmt.format(s.getA()*1e4)," & ",fmt.format(s.getAlpha())," & ")
      fName.write(fmt.format(s.getJ()*1e6)," & ",fmt.format(s.getIy()*1e6)," & ",fmt.format(s.getIz()*1e6),"\\\\\n")
      k+=1

  cierraSupertabular(nmbArchivo) 


# Obtiene un listado de las entidades del conjunto cuyo nombre se pasa como parámetro.
def listaEntidadesSet(preprocessor, nmbSet, nmbArchivo, nmbProcLstElementos, fmt, encab, tit):
  nmbArchivo.write("\\twocolumn\n")
  nmbArchivo.write("\\",encab,"{",tit,"}\n")
  listaKPtsSet(preprocessor, nmbSet,nmbArchivo,fmt) 
  listaLineasSet(preprocessor, nmbSet,nmbArchivo) 
  listaNodosSet(preprocessor, nmbSet,nmbArchivo,fmt) 
  nmbArchivo.write("\\onecolumn\n")
  nmbProcLstElementos(preprocessor, nmbSet,nmbArchivo,fmt) 


# Obtiene un listado de las entidades de la linea cuyo nombre se pasa como parámetro.
def listaEntidadesLinea(preprocessor, nmbSet, nmbArchivo, nmbProcLstElementos, fmt, encab, tit):
  nmbArchivo.write("\\",encab,"{",tit,"}\n")
  listaNodosSet(preprocessor, nmbSet,nmbArchivo,fmt)
  nmbProcLstElementos(nmbSet,nmbArchivo,fmt) 

