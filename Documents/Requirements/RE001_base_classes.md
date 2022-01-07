# RE001 Requirements for the Module phyqus_lib.base_functions

## Conventions

Requirements listed in this document are constructed according to the following structure:

**Requirement ID:** REQ-UVW-XYZ

**Title:** Title / name of the requirement

**Description:** Description / definition of the requirement

**Verification Method:** I / A / T / D

The requirement ID starts with the fixed prefix 'REQ'. The prefix is followed by 3 letters abbreviation (in here 'UVW'), which defines the requiement type - e.g. 'FUN' for a functional and capability requirement, 'AWM' for an alarm, warnings and operator messages, etc. The last part of the ID is a 3-digits *hexadecimal* number (0..9|A..F), with the first digit identifing the module, the second digit identifing a class / function, and the last digit - the requirement ordering number for this object. E.g. 'REQ-FUN-112'. Each requirement type has its own counter, thus 'REQ-FUN-112' and 'REQ-AWN-112' requirements are different entities, but they refer to the same object (class or function) within the same module.

The verification method for a requirement is given by a single letter according to the table below:

| **Term**          | **Definition**                                                               |
| :---------------- | :--------------------------------------------------------------------------- |
| Inspection (I)    | Control or visual verification                                               |
| Analysis (A)      | Verification based upon analytical evidences                                 |
| Test (T)          | Verification of quantitative characteristics with quantitative measurement   |
| Demonstration (D) | Verification of operational characteristics without quantitative measurement |

## Functional and capability requirements

**Requirement ID:** REQ-FUN-100

**Title:** Measurement with uncertainty data type - instantiation

**Description:** The module should provide a class implementing a data type to store and perform arithmetics with a measurement with the associated uncertainty of the measured value. This class should support the following modes of instantiation:

* From a single real number - as the 'mean' value, the uncertainty is zero
* From two real numbers - as the 'mean' and unceratinty values respectively, the second number should be non-negative
* From another measurement with uncertainty object - 'mean' and uncertainty are copied

**Note**: a class is considered to be API compatible with the **MeasuredValue** class (i.e. being a measurement with uncertainty) if it has:

* *Value* attribute, which is a real number, AND
* *SE* attribute, which is a non-begative real number

**Verification Method:** T

___

**Requirement ID:** REQ-FUN-101

**Title:** Basic arithmetic operations

**Description:** The defined new data type should support the addition, subtraction, multiplication and division operations with the second operand (left or right) being either another instance of the same new data type or a real number. The augment assignment versions of the same operations should be supported as well. The calculations should conform the 'normal error propagation model'.

**Verification Method:** T

___

**Requirement ID:** REQ-FUN-102

**Title:** Exponentiation

**Description:** The defined new data type should support the exponentiation with the second operand (left or right) being a real number or another instance of the same new data type. The augment assignment version of the same operation should be supported as well. The calculations should conform the 'normal error propagation model' as well as the standard conventions / limitations on Python *pow*() function.

**Verification Method:** T

## Alarms, warnings and operator messages

**Requirement ID:** REQ-AWM-100

**Title:** Instantiation - TypeError

**Description:** The instantiation of the new defined data type class should result in the **TypeError** (or its sub-class) exception if:

* The 'mean' value is not passed as a real number or via another measurement with uncertainty object, OR
* The uncertainty' value is not passed as a real number or via another measurement with uncertainty object

**Verification Method:** T

___

**Requirement ID:** REQ-AWM-101

**Title:** Instantiation - ValueError

**Description:** The instantiation of the new defined data type class should result in the **ValueError** (or its sub-class) exception if the uncertainty' value is passed as a real number, but its value is negative

**Verification Method:** T

___

**Requirement ID:** REQ-AWM-102

**Title:** Arithemtics - TypeError

**Description:** The arithmetic operations with this new type should result in the **TypeError** (or its sub-class) exception if the second operand is neither a real number, nor via another measurement with uncertainty object

**Verification Method:** T

___

**Requirement ID:** REQ-AWM-103

**Title:** Arithmetics - ValueError

**Description:** The instantiation of the new defined data type class should result in the **ValueError** (or its sub-class) exception if

* Division - the second operand (divider) is either a real number zero or has the zero 'mean', except for the case than an object is divided by itself
* Exponentiation:
  * The 'mean' of the base is zero and the exponent is negative - as int or float, or has negative mean (as with uncertainty instance)
  * The 'mean' of the base is negative and the exponent is non-zero, non-integer real number or another value with uncertainty
  * The base is int or float, which is zero or negative, and the exponent is the value with uncertainty

**Verification Method:** T
