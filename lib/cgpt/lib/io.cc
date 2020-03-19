/*
  CGPT

  Authors: Christoph Lehner 2020
*/
#include "lib.h"
#include "io/nersc.h"

EXPORT(load,{
    PyObject* ret;
    
    if (ret = load_nersc(args))
      return ret;
    
    Py_RETURN_NONE;
    
  });