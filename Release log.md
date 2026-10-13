# Release log of library phyqus_lib

## 2026-10-13 v0.1.2-dev1

Added walk-around into MeasuredValue's class arithmetics to support statistics_lib.data_classes.Statistics1D class instances. Basically, if API compatible class is detected, the \_\_add\_\_(), \_\_sub\_\_(), \_\_mul\_\_() and \_\_truediv\_\_() methods re-delegate the calculations to the respective methods \_\_radd\_\_(), \_\_rsub\_\_(), \_\_rmul\_\_() and \_\_rtruediv\_\_() of the second (right) operand.

## 2023-04-19 v0.1.1-dev1

Code clean-up.

## 2021-01-14 v0.1.0-dev1

Implemented, tested and documented module *base_clases* - normal error propagation model arithmetics and 'measurements with uncertainties' data type class.
