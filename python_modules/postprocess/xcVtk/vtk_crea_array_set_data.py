# -*- coding: utf-8 -*-

def VtkCreaStrArraySetData(preprocessor,setName,entTypeName,nmbArray,data):
  ''' Creates an array of character strings with the data of the
      points defined in the set.'''
  #Creamos el actor para las líneas.
  st= preprocessor.getSets.getSet(setName)
  
    # \preprocessor{\cad{\sets{\@setName
    #   {
    #     # Define matrix
    #     \vtk{ \define["vtkShStrArray",@nmbArray]{} }
    #     \numera{}
    #     #Put the values in the matrix
    #     \def_var["tmp","string"]{}
    #     \@entTypeName{\for_each
    #       {
    #         \set{tmp= @eval(@data)}
    #         \vtk{\@nmbArray{ \insert_value{getIdx,@tmp} }}
    #       }}
    #   }}}}
