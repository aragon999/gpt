/*
    GPT - Grid Python Toolkit
    Copyright (C) 2020  Christoph Lehner (christoph.lehner@ur.de, https://github.com/lehner/gpt)

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
*/

template<typename T>
PyObject* cgpt_lattice_slice(Lattice<T>& l,int dim) {
  typedef typename Lattice<T>::vector_object vobj;
  typedef typename vobj::scalar_object sobj;

  std::vector<sobj> c;
  sliceSum(l,c,dim);

  PyObject* ret=PyList_New(c.size());
  for (size_t i=0; i<c.size(); i++) {
    PyList_SET_ITEM(ret,i,cgpt_numpy_export(c[i]));
  }
  return ret;
}
