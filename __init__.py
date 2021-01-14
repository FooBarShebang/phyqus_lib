#!/usr/bin/python3
"""
Library phyqus_lib

Implements the 'real life measurements', i.e. 2-tuple values of the most probale
(or mean) value and the asssociated uncertainty / standard error, which can be
generic or specific type (i.e. with the associated 'dimension' / physical
quantity like meters, gramms, amperes, etc.). Also implements the 'typed'
arithmetic, e.g. one can multiply and divide meters and seconds but not add or
subtract, whereas addition and subtraction are allowed for the same quantities
(meters and miles, for instance).

Modules:
    base_classes: arithmetics and data type to store a measurement with an
        uncertainty values

"""

__project__ = 'Real life measurements arithmetics with dimensions and errors'
__version_info__= (0, 1, 0)
__version_suffix__= '-dev1'
__version__= ''.join(['.'.join(map(str, __version_info__)), __version_suffix__])
__date__ = '14-01-2021'
__status__ = 'Development'
__author__ = 'Anton Azarov'
__maintainer__ = 'a.azarov@diagnoptics.com'
__license__ = 'Public Domain'
__copyright__ = 'Diagnoptics Technologies B.V.'

__all__ = ['base_classes']