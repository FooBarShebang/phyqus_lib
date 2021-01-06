#usr/bin/python3
"""
Module phyqus_lib.base_classes

Implements class to store a 2-tuple of the mean value of a measurement and its
associated uncertainty as well as basic arithmetics with this new data type.

Classes:
    MeasuredValueABC
    MeasuredValue
"""

__version__= '1.0.0.0'
__date__ = '06-01-2021'
__status__ = 'Development'

#imports

#+ standard library

import sys
import os
import abc
import copy
import math

from typing import Union, Optional, Any

#+ custom modules

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(MODULE_PATH)
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual import

from introspection_lib.base_exceptions import UT_TypeError, UT_ValueError

#types

TReal = Union[int, float]

#classes

class MeasuredValueABC(abc.ABC):
    """
    Prototype class for implementation of the 'real life measurement' data type.
    Added mostly for the benefit of type hints. Implements the read-only data
    access properties and the 'magic' methods for str() and repr() funcitons
    hooking. Cannot be instantiated.

    Properties:
        Value: int OR float; the mean value of a measurement
        SE: int >= 0 OR float >= 0; the measurement uncertainty
    
    Version 1.0.0.0
    """

    #special methods

    @abc.abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        """
        Stub initializer. Does nothing. Added to disable the instantiation of
        the class.

        Signature:
            /.../ -> None
        
        Version 1.0.0.0
        """
        pass

    def __str__(self) -> str:
        """
        Returns a string representation of the stored data as (Value +/- SE).

        Signature:
            None -> str
        
        Version 1.0.0.0
        """
        return '({} +/- {})'.format(self.Value, self.SE)
    
    def __repr__(self) -> str:
        """
        Returns a string representation of the stored data as 'Type(Value, SE)'.

        Signature:
            None -> str
        
        Version 1.0.0.0
        """
        return "'{}({},{})'".format(self.__class__.__name__, self.Value,
                                                                        self.SE)
    
    #public API

    #+ read-only properties

    @property
    def Value(self) -> TReal:
        """
        Read-only access property to the stored mean value of a measurement.

        Signature:
            None -> int OR float
        
        Version 1.0.0.0
        """
        return self._Value
    
    @property
    def SE(self) -> TReal:
        """
        Read-only access property to the stored measurement uncertainty.

        Signature:
            None -> int >= 0 OR float >= 0
        
        Version 1.0.0.0
        """
        return self._SE

class MeasuredValue(MeasuredValueABC):
    """
    Implements the data type to store a measurement mean value and the bound
    uncertainty as well as the basic arithmetic operations, including the
    augmented assignments.
    
    The addition, subtraction, multiplication and division are supported for
    both operands having uncertainty as well as only one operand having it and
    the second operand being a plain real number. The power operation is
    implemented only for the real number exponent, whereas the base being an
    instance of this class.

    Avoids ZeroDivisionError by checking operands and raising UT_ValueError
    instead.
    
    Also supports the data conversion into int and float (i.e., lossing SE
    information), the abs() and round() standard functions support as well as
    math.tunc(). math.ceil() and math.floor().
    
    Note that this data type does not support comparison operations.
    
    Sub-classes MeasuredValueABC.

    Properties:
        Value: int OR float; the mean value of a measurement
        SE: int >= 0 OR float >= 0; the measurement uncertainty
    
    Version 1.0.0.0
    """

    #'private' helper methods

    def _checkInput(self, Value: Any) -> None:
        """
        Helper 'private' method to check the input for instantiation or
        arithmetics methods, which raises an custom TypeError type exception
        with 2 frames skipped if the input is not acceptable.

        Signature:
            type A -> None
        
        Args:
            Value: type A; the value to be checked
        
        Raises:
            UT_TypeError: the passed argument is not int, float ('is a' check)
                or instance of MeasuredValueABC sub-class, which is checked as
                'has a'
        
        Version 1.0.0.0
        """
        bCond1 = isinstance(Value, (int, float))
        bCond2 = hasattr(Value, 'Value') and hasattr(Value, 'SE')
        if not (bCond1 or bCond2):
            raise UT_TypeError(Value, (int, float, MeasuredValueABC),
                                                                SkipFrames = 2)

    #special methods

    def __init__(self, Value: Union[TReal, MeasuredValueABC],
                                            SE: Optional[TReal] = None) -> None:
        """
        Initializer. Supports four modes of call:
            * single argument of int or float type - passed value is set as the
                mean, whereas the SE is set to zero
            * single argument as instance of sub-class of MeasuredValueABC
                (checked as 'has a') - the mean and SE value are copied
            * two arguments of int or float type - copied as the mean and SE
                values respectevely
            * first argument of MeasuredValueABC sub-class type and the second
                of int or float type - the mean value of the first argument is
                copied as the mean, the second argument is copied as SE

        Signature:
            int OR float OR MeasuredValueABC /, int OR float OR None/ -> None
        
        Args:
            Value: int OR float OR MeasuredValueABC; the mean value of the
                measurement with optional uncertainty (if instance of sub-class
                of MeasuredValueABC is passed)
            SE: (optional) int OR float; the associated measurement uncertainty,
                if provided (not None), overwrites the value assigned based on
                the first argument
        
        Raises:
            UT_TypeError: the first argument is not int, float or instance of
                MeasuredValueABC sub-class, which is checked as 'has a' not
                'is a', OR the second argument is not int, float or None
            UT_ValueError: the second argument is negative
        
        Version 1.0.0.0
        """
        self._checkInput(Value)
        if isinstance(Value, (int, float)):
            self._Value = copy.copy(Value)
            self._SE = 0
        else:
            self._Value = copy.copy(Value.Value)
            self._SE = copy.copy(Value.SE)
        if not (SE is None):
            if not isinstance(SE, (int, float)):
                raise UT_TypeError(SE, (int, float, None), SkipFrames = 1)
            elif SE < 0:
                raise UT_ValueError(SE, '>= 0', SkipFrames = 1)
            self._SE = copy.copy(SE)
    
    def __int__(self) -> int:
        """
        Returns the stored mean value of the measurement converted into int
        data type.

        Signature:
            None -> int
        
        Version 1.0.0.0
        """
        return int(self.Value)
    
    def __float__(self) -> float:
        """
        Returns the stored mean value of the measurement converted into float
        data type.

        Signature:
            None -> int
        
        Version 1.0.0.0
        """
        return float(self.Value)
    
    def __trunc__(self) -> int:
        """
        Returns the stored mean value of the measurement converted into int
        data type - same as simple int() conversion

        Signature:
            None -> int
        
        Version 1.0.0.0
        """
        return int(self.Value)
    
    def __floor__(self) -> int:
        """
        Returns the stored mean value of the measurement converted into int
        data type using math.floor() - hook for the same function call!

        Signature:
            None -> int
        
        Version 1.0.0.0
        """
        return math.floor(self.Value)
    
    def __ceil__(self) -> int:
        """
        Returns the stored mean value of the measurement converted into int
        data type using math.ceil() - hook for the same function call!

        Signature:
            None -> int
        
        Version 1.0.0.0
        """
        return math.ceil(self.Value)
    
    def __round__(self, NDigits: Optional[int] = None) -> TReal:
        """
        Returns the stored mean value of the measurement rounded to int or float
        with the requested number of the digits after comma. Hooks the round()
        function.

        Signature:
            None -> int OR float

        Args:
            NDigits: (optional) int; the desired precision of the rounding,
                defaults to None, in which case the rounding is done to an int
        
        Version 1.0.0.0
        """
        return round(self.Value, NDigits)
    
    def __abs__(self) -> TReal:
        """
        Returns the absolute of the stored mean value of the measurement.

        Signature:
            None -> int or float
        
        Version 1.0.0.0
        """
        return abs(self.Value)
    
    def __pos__(self) -> MeasuredValueABC:
        """
        Implements an unitary plus operation, returns a copy of itself.

        Signature:
            None -> MeasuredValue
        
        Version 1.0.0.0
        """
        return MeasuredValue(self)
    
    def __neg__(self) -> MeasuredValueABC:
        """
        Implements an unitary minus, i.e. negation operation.

        Signature:
            None -> MeasuredValue
        
        Version 1.0.0.0
        """
        return MeasuredValue(- self.Value, self.SE)

    def __add__(self,
                    Other: Union[TReal, MeasuredValueABC]) -> MeasuredValueABC:
        """
        Implements the addition operation with the current instance being the
        left operand.

        Signature:
            int OR float OR MeasuredValueABC -> MeasuredValue
        
        Args:
            Other: int OR float OR MeasuredValueABC; the right operand
        
        Raises:
            UT_TypeError: the passed argument is not int, float ('is a' check)
                or instance of MeasuredValueABC sub-class, which is checked as
                'has a'
        
        Version 1.0.0.0
        """
        self._checkInput(Other)
        if isinstance(Other, (int, float)):
            Mean = self.Value + Other
            SE = self.SE
        elif Other is self:
            Mean = 2 * self.Value
            SE = 2 * self.SE
        else:
            Mean = self.Value + Other.Value
            SE = math.sqrt(pow(self.SE, 2) + pow(Other.SE, 2))
        return MeasuredValue(Mean, SE)
    
    def __radd__(self,
                    Other: Union[TReal, MeasuredValueABC]) -> MeasuredValueABC:
        """
        Implements the addition operation with the current instance being the
        right operand.

        Signature:
            int OR float OR MeasuredValueABC -> MeasuredValue
        
        Args:
            Other: int OR float OR MeasuredValueABC; the left operand
        
        Raises:
            UT_TypeError: the passed argument is not int, float ('is a' check)
                or instance of MeasuredValueABC sub-class, which is checked as
                'has a'
        
        Version 1.0.0.0
        """
        self._checkInput(Other)
        return self.__add__(Other)
    
    def __iadd__(self,
                    Other: Union[TReal, MeasuredValueABC]) -> MeasuredValueABC:
        """
        Implements the augmented addition assignment to current instance.

        Signature:
            int OR float OR MeasuredValueABC -> MeasuredValue
        
        Args:
            Other: int OR float OR MeasuredValueABC; the second operand
        
        Raises:
            UT_TypeError: the passed argument is not int, float ('is a' check)
                or instance of MeasuredValueABC sub-class, which is checked as
                'has a'
        
        Version 1.0.0.0
        """
        self._checkInput(Other)
        Temp = self.__add__(Other)
        self._Value = copy.copy(Temp.Value)
        self._SE = copy.copy(Temp.SE)
        del Temp
        return self
    
    def __sub__(self,
                    Other: Union[TReal, MeasuredValueABC]) -> MeasuredValueABC:
        """
        Implements the subtraction operation with the current instance being the
        left operand.

        Signature:
            int OR float OR MeasuredValueABC -> MeasuredValue
        
        Args:
            Other: int OR float OR MeasuredValueABC; the right operand
        
        Raises:
            UT_TypeError: the passed argument is not int, float ('is a' check)
                or instance of MeasuredValueABC sub-class, which is checked as
                'has a'
        
        Version 1.0.0.0
        """
        self._checkInput(Other)
        if isinstance(Other, (int, float)):
            Mean = self.Value - Other
            SE = self.SE
        elif Other is self:
            Mean = 0
            SE = 0
        else:
            Mean = self.Value - Other.Value
            SE = math.sqrt(pow(self.SE, 2) + pow(Other.SE, 2))
        return MeasuredValue(Mean, SE)
    
    def __rsub__(self,
                    Other: Union[TReal, MeasuredValueABC]) -> MeasuredValueABC:
        """
        Implements the subtraction operation with the current instance being the
        right operand.

        Signature:
            int OR float OR MeasuredValueABC -> MeasuredValue
        
        Args:
            Other: int OR float OR MeasuredValueABC; the left operand
        
        Raises:
            UT_TypeError: the passed argument is not int, float ('is a' check)
                or instance of MeasuredValueABC sub-class, which is checked as
                'has a'
        
        Version 1.0.0.0
        """
        self._checkInput(Other)
        return (- self.__sub__(Other))
    
    def __isub__(self,
                    Other: Union[TReal, MeasuredValueABC]) -> MeasuredValueABC:
        """
        Implements the augmented subtraction assignment to current instance.

        Signature:
            int OR float OR MeasuredValueABC -> MeasuredValue
        
        Args:
            Other: int OR float OR MeasuredValueABC; the second operand
        
        Raises:
            UT_TypeError: the passed argument is not int, float ('is a' check)
                or instance of MeasuredValueABC sub-class, which is checked as
                'has a'
        
        Version 1.0.0.0
        """
        self._checkInput(Other)
        Temp = self.__sub__(Other)
        self._Value = copy.copy(Temp.Value)
        self._SE = copy.copy(Temp.SE)
        del Temp
        return self
    
    def __mul__(self,
                    Other: Union[TReal, MeasuredValueABC]) -> MeasuredValueABC:
        """
        Implements the multiplication operation with the current instance being
        the left operand.

        Signature:
            int OR float OR MeasuredValueABC -> MeasuredValue
        
        Args:
            Other: int OR float OR MeasuredValueABC; the right operand
        
        Raises:
            UT_TypeError: the passed argument is not int, float ('is a' check)
                or instance of MeasuredValueABC sub-class, which is checked as
                'has a'
        
        Version 1.0.0.0
        """
        self._checkInput(Other)
        if isinstance(Other, (int, float)):
            Mean = self.Value * Other
            SE = self.SE * abs(Other)
        elif Other is self:
            Mean = self.Value**2
            SE = 2 * self.SE * abs(self.Value)
        else:
            Mean = self.Value * Other.Value
            SE = math.sqrt(pow(self.SE * Other.Value, 2)
                                                + pow(Other.SE * self.SE, 2))
        return MeasuredValue(Mean, SE)
    
    def __rmul__(self,
                    Other: Union[TReal, MeasuredValueABC]) -> MeasuredValueABC:
        """
        Implements the multiplication operation with the current instance being
        the right operand.

        Signature:
            int OR float OR MeasuredValueABC -> MeasuredValue
        
        Args:
            Other: int OR float OR MeasuredValueABC; the left operand
        
        Raises:
            UT_TypeError: the passed argument is not int, float ('is a' check)
                or instance of MeasuredValueABC sub-class, which is checked as
                'has a'
        
        Version 1.0.0.0
        """
        self._checkInput(Other)
        return self.__mul__(Other)
    
    def __imul__(self,
                    Other: Union[TReal, MeasuredValueABC]) -> MeasuredValueABC:
        """
        Implements the augmented multiplication assignment to current instance.

        Signature:
            int OR float OR MeasuredValueABC -> MeasuredValue
        
        Args:
            Other: int OR float OR MeasuredValueABC; the second operand
        
        Raises:
            UT_TypeError: the passed argument is not int, float ('is a' check)
                or instance of MeasuredValueABC sub-class, which is checked as
                'has a'
        
        Version 1.0.0.0
        """
        self._checkInput(Other)
        Temp = self.__mul__(Other)
        self._Value = copy.copy(Temp.Value)
        self._SE = copy.copy(Temp.SE)
        del Temp
        return self
    
    def __truediv__(self,
                    Other: Union[TReal, MeasuredValueABC]) -> MeasuredValueABC:
        """
        Implements the division operation with the current instance being the
        left operand.

        Signature:
            int OR float OR MeasuredValueABC -> MeasuredValue
        
        Args:
            Other: int OR float OR MeasuredValueABC; the right operand
        
        Raises:
            UT_TypeError: the passed argument is not int, float ('is a' check)
                or instance of MeasuredValueABC sub-class, which is checked as
                'has a'
            UT_ValueError: the passed argument is zero or has zero mean value
        
        Version 1.0.0.0
        """
        self._checkInput(Other)
        if isinstance(Other, (int, float)):
            if not Other:
                raise UT_ValueError(Other, '!= 0', SkipFrames = 1)
            Mean = self.Value / Other
            SE = self.SE / abs(Other)
        elif Other is self:
            Mean = 1
            SE = 0
        else:
            if not Other.Value:
                raise UT_ValueError(Other, '!= 0', SkipFrames = 1)
            Mean = self.Value / Other.Value
            SE = math.sqrt(pow(self.SE / Other.Value, 2)
                        + pow((Other.SE * self.Value) / (Other.Value**2), 2))
        return MeasuredValue(Mean, SE)
    
    def __rtruediv__(self,
                    Other: Union[TReal, MeasuredValueABC]) -> MeasuredValueABC:
        """
        Implements the division operation with the current instance being the
        right operand.

        Signature:
            int OR float OR MeasuredValueABC -> MeasuredValue
        
        Args:
            Other: int OR float OR MeasuredValueABC; the left operand
        
        Raises:
            UT_TypeError: the passed argument is not int, float ('is a' check)
                or instance of MeasuredValueABC sub-class, which is checked as
                'has a'
            UT_ValueError: the current mean value stored is zero
        
        Version 1.0.0.0
        """
        self._checkInput(Other)
        if isinstance(Other, (int, float)):
            if not self.Value:
                raise UT_ValueError(self, '!= 0', SkipFrames = 1)
            Mean = Other / self.Value
            SE = self.SE * abs(Other) / (self.Value**2)
        elif Other is self:
            Mean = 1
            SE = 0
        else:
            if not self.Value:
                raise UT_ValueError(self, '!= 0', SkipFrames = 1)
            Mean = Other.Value / self.Value
            SE = math.sqrt(pow(Other.SE / self.Value, 2)
                        + pow((self.SE * Other.Value) / (self.Value**2), 2))
        return MeasuredValue(Mean, SE)
    
    def __itruediv__(self,
                    Other: Union[TReal, MeasuredValueABC]) -> MeasuredValueABC:
        """
        Implements the augmented division assignment to current instance.

        Signature:
            int OR float OR MeasuredValueABC -> MeasuredValue
        
        Args:
            Other: int OR float OR MeasuredValueABC; the second operand
        
        Raises:
            UT_TypeError: the passed argument is not int or float ('is a' check)
                or instance of MeasuredValueABC sub-class, which is checked as
                'has a'
            UT_ValueError: the passed argument is zero or has zero mean value
        
        Version 1.0.0.0
        """
        self._checkInput(Other)
        Temp = self.__truediv__(Other)
        self._Value = copy.copy(Temp.Value)
        self._SE = copy.copy(Temp.SE)
        del Temp
        return self
    
    def __pow__(self, Other: TReal) -> MeasuredValueABC:
        """
        Implements the power operation with the current instance being the left
        operand.

        Signature:
            int OR float -> MeasuredValue
        
        Args:
            Other: int OR float; the right operand
        
        Raises:
            UT_TypeError: the passed argument is not int or float ('is a' check)
            UT_ValueError: raising negative mean to a fractional, not integer
                power; raising zero mean to negative power
        
        Version 1.0.0.0
        """
        if not isinstance(Other, (int, float)):
            raise UT_TypeError(Other, (int, float), SkipFrames = 1)
        elif (not isinstance(Other, int)) and (self.Value < 0):
            raise UT_ValueError(self, '>= 0', SkipFrames = 1)
        elif (Other < 0) and (not self.Value):
            raise UT_ValueError(self, '!= 0', SkipFrames = 1)
        elif not Other:
            Mean = 1
            SE = 0
        else:
            Mean = self.Value ** Other
            if self.Value:
                SE = self.SE * abs(Other * Mean / self.Value)
            else:
                SE = self.SE ** Other
        return MeasuredValue(Mean, SE)
    
    def __ipow__(self, Other: TReal) -> MeasuredValueABC:
        """
        Implements the augmented power assignment to current instance.

        Signature:
            int OR float -> MeasuredValue
        
        Args:
            Other: int OR float; the second operand
        
        Raises:
            UT_TypeError: the passed argument is not int or float ('is a' check)
            UT_ValueError: raising negative mean to a fractional, not integer
                power; raising zero mean to negative power
        
        Version 1.0.0.0
        """
        if not isinstance(Other, (int, float)):
            raise UT_TypeError(Other, (int, float), SkipFrames = 1)
        elif (not isinstance(Other, int)) and (self.Value < 0):
            raise UT_ValueError(self, '>= 0', SkipFrames = 1)
        elif (Other < 0) and (not self.Value):
            raise UT_ValueError(self, '!= 0', SkipFrames = 1)
        Temp = self.__pow__(Other)
        self._Value = copy.copy(Temp.Value)
        self._SE = copy.copy(Temp.SE)
        del Temp
        return self
