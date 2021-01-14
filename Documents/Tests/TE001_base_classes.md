# Test Report on the Module phyqus_lib.base_classes

## Conventions

Each test is defined following the same format. Each test receives a unique test identifier and a reference to the ID(s) of the requirements it covers (if applicable). The goal of the test is described to clarify what is to be tested. The test steps are described in brief but clear instructions. For each test it is defined what the expected results are for the test to pass. Finally, the test result is given, this can be only pass or fail.

The test format is as follows:

**Test Identifier:** TEST-\[I/A/D/T\]-XYZ

**Requirement ID(s)**: REQ-uvw-xyz

**Verification method:** I/A/D/T

**Test goal:** Description of what is to be tested

**Expected result:** What test result is expected for the test to pass

**Test steps:** Step by step instructions on how to perform the test

**Test result:** PASS/FAIL

The test ID starts with the fixed prefix 'TEST'. The prefix is followed by a single letter, which defines the test type / verification method. The last part of the ID is a 3-digits *hexadecimal* number (0..9|A..F), with the first digit identifing the module, the second digit identifing a class / function, and the last digit - the test ordering number for this object. E.g. 'TEST-T-112'. Each test type has its own counter, thus 'TEST-T-112' and 'TEST-A-112' tests are different entities, but they refer to the same object (class or function) within the same module.

The verification method for a requirement is given by a single letter according to the table below:

| **Term**          | **Definition**                                                               |
| :---------------- | :--------------------------------------------------------------------------- |
| Inspection (I)    | Control or visual verification                                               |
| Analysis (A)      | Verification based upon analytical evidences                                 |
| Test (T)          | Verification of quantitative characteristics with quantitative measurement   |
| Demonstration (D) | Verification of operational characteristics without quantitative measurement |

## Test preparation

Define a helper class **HelperClass**, which must be instantiated with two arbitrary arguments, which are stored as the instance attributes *Value* and *SE* respectively.

## Tests definition (Test)

**Test Identifier:** TEST-T-100

**Requirement ID(s)**: REQ-FUN-100, REQ-AWM-100, REQ-AWM-101

**Verification method:** T

**Test goal:** Correctness of implementation of instantiation of measurement with uncertanty data type class

**Expected result:** The defined class can instantiated with:

* One real number argument, which is treated as the 'mean' value, whereas the uncertainty is set to zero
* Two real number arguments - the first one is treated as the 'mean', and the second - as the uncertainty, whereas the second argument is non-negative
* One argument - instance of a class having *Value* and *SE* attributes (fields or properties) - which values are copied as the 'mean' and unceratinty respectively
* The first argument as an instance of a class having *Value* and *SE* attributes (fields or properties), and the second - as a non-negative real number; the value of the *Value* attribute of the first argument is copied as the 'mean', and the second argument is set as the uncertainty

Upon instantion the attributes (properties) *Value* and *SE* have the expected values.

An exception sub-classing **TypeError** is raised if:

* The first argument is neither integer, nor real, not having both *Value* and *SE* attributes
* The first argument has *Value* attribute, but it is not a real number
* The first argument has *SE* attribute, but it is not a real number, or it is negative
* The second attribute, if provided, is neither integer, nor real, nor None (which is ignored)

An exception sub-classing **ValueError** is raised if the second argument is provided, but it is a negative real number.

**Test steps:** Use the following procedure:

Normal instantiation

* Generate a random integer number as *Mean* and a random, non-negative integer number as *Error*
  * Instantiate **MeasuredValue** class only with *Mean*, check that the instance *Value* = *Mean* and *SE* = 0
  * Instantiate **MeasuredValue** class with both *Mean* and *Error*, check that the instance *Value* = *Mean* and *SE* = *Error*
  * Instantiate **HelperClass** with *Mean* and *Error*, instantiate **MeasuredValue** class from this instance, check the second instance *Value* = *Mean* and *SE* = *Error*
  * Instantiate **HelperClass** with *Mean* and 0, instantiate **MeasuredValue** class from this instance, check the second instance *Value* = *Mean* and *SE* = 0
  * Instantiate **MeasuredValue** class with both *Mean* and *Error*, create another instance of **MeasuredValue** class from it, check the second instance *Value* = *Mean* and *SE* = *Error*
  * Instantiate **MeasuredValue** class with both *Mean* and *Error*, create another instance of **MeasuredValue** class from it and use 0 as the second argument, check the second instance *Value* = *Mean* and *SE* = 0
* Repeat the procedure with the floating point *Mean* and *Error*
* Repeat the steps above multiples times (N ~ 1000) with new random values

TypeError

* Create a list of wrong type values: **int** and **float** (as types, not instances!), string literal, sequences of arbitrary type values, a dictionary, etc.
* For each element *Item* in this list perform *assertRaises* test with catching by TypeError using the following instantiation calls:
  * MeasuredValue(Item)
  * MeasuredValue(Item, 0.1)
  * MeasuredValue(HelperClass(Item, 0.1))
  * MeasuredValue(HelperClass(1, Item))
  * MeasuredValue(HelperClass(Item, 0.1), 0.1)
  * MeasuredValue(HelperClass(1, Item), 0.1)
* Try also MeasuredValue(HelperClass(1, -1)) and MeasuredValue(HelperClass(1, -0.1), 0.1)

ValueError

* Within the *assertRaises* with catching by ValueError context try the following instantations:
  * MeasuredValue(1, -0.1)
  * MeasuredValue(0.1, -1)
  * MeasuredValue(HelperClass(1,1), -0.1)
  * MeasuredValue(MeasuredValue(1,1), -1)

The test cases are implemented within the module [UT001_base_classes](../../Tests/UT001_base_classes.py), see class **Test_Init**.

**Test result:** PASS

___

**Test Identifier:** TEST-T-101

**Requirement ID(s)**: REQ-FUN-101, REQ-FUN-102, REQ-AWM-102, REQ-AWM-103

**Verification method:** T

**Test goal:** Correctness of implementation of instantiation of measurement with uncertanty data type class

**Expected result:** The calculations (normal error propagation model via measurements with uncertainties arithmetics) are performed according the formulas given in the design / reference document [UD001](../References/UD001_base_classes.md), including the special cases of the second operand being the same object. The TypeError sub-class exception is raised if the second argument is incompatible data type, and ValueError sub-class exception is raised if division by zero is bound to occur or a negative 'mean' value is raised into non-integer power.

**Test steps:**

Correctness of calculations - performed separately for each of the test suits for a specific arithmetic operation:

* Instance of the tested class as a left operand of '+', '-', '*', '/' and '**'
  * Instantiate the **MeasuredValue** class with the random floating point numbers - both the 'mean' and uncertainty
    * Perform the operation directly (e.g. as 'a + b') and using a functional wrapper (e.g. *operator.add*(a, b) from the standard library) with a random integer and a random floating point right operand. Compare the results with the expected 'mean' and uncertainty (acoording to the formulas). **Note** in case of the division the right operand should not be zero; in case of the exponentiation the 'mean' value should also satisfy conditions discussed in the exponentiaion operation definition (see UD001 document).
    * Except the exponentiation! Perform the same operation directly and via a functional call wrapper using another instance of **MeasuredValue** class and an instance of **HelperClass** as the right operand, with the second operand being instantiated with integer and floating point values. **Note** in case of the division the 'mean' value of the right operand should not be zero.
    * Except the exponentiation! Check the special case, when the second operand is the same object as the left one.
  * Repeat the process with the random integer values of the 'mean' and uncertainty
  * For division only. Check that the division of an instance with a zero 'mean' by itself results in (1, 0) and ValueError is not raised.
* Augmented assigment: '+=', '-=', '*=', '/=' and '**=' to an instance of the tested class
  * Instantiate the **MeasuredValue** class with the random floating point numbers - both the 'mean' and uncertainty
    * Perform the operation directly (e.g. as 'a += b') and using a functional wrapper (e.g. *operator.iadd*(a, b) from the standard library) with a random integer and a random floating point right operand. Compare the results with the expected 'mean' and uncertainty (acoording to the formulas). **Note** in case of the division the right operand should not be zero; in case of the exponentiation the 'mean' value should also satisfy conditions discussed in the exponentiaion operation definition (see UD001 document).
    * Except the exponentiation! Perform the same operation directly and via a functional call wrapper using another instance of **MeasuredValue** class and an instance of **HelperClass** as the right operand, with the second operand being instantiated with integer and floating point values. **Note** in case of the division the 'mean' value of the right operand should not be zero.
    * Except the exponentiation! Check the special case, when the second operand is the same object as the left one.
  * Repeat the process with the random integer values of the 'mean' and uncertainty
  * For division only. Check that the augmented division assignemnt to an instance with a zero 'mean' with the right operand being the same object results in (1, 0) and ValueError is not raised.
* Instance of the tested class as a right operand of '+', '-', '*' and '/' (excluding exponentiation!)
  * Instantiate the **MeasuredValue** class with the random floating point numbers - both the 'mean' and uncertainty
    * Perform the operation directly (e.g. as 'a + b') and using a functional wrapper (e.g. *operator.add*(a, b) from the standard library) with a random integer and a random floating point left operand. Compare the results with the expected 'mean' and uncertainty (acoording to the formulas). **Note** in case of the division the 'mean' of the test instance of the **MeasuredValue** class (being tested) should be mon-zero.
  * Repeat the process with the random integer values of the 'mean' and uncertainty
* Repeat tests multiple time (N ~ 1000) with new random values

TypeError - impoper second operand type tests; performed separately for each of the test suits for a specific arithmetic operation:

* Generate a sequence of improper values of the second operand: **int** and **float** (as data types, not instances!), generic sequences (list, tuple, etc.) of arbitrary elements (including numbers), mapping objects (dictionary, etc.) as well as instances of **HelperClass** with non-numeric values of *Value* and / or *SE* attributes or a negative value of the *SE* attribute.
* For exponentiation only! Include an instance of the **MeasuredValue** into this list.
* Create an instance of the **MeasuredValue** (tested class) with an arbitrary, random values of the 'mean' and the uncertainty
* For each element in the generated list perform the following within *assertRaises*() with catching by TypeError context:
  * the tested operation (as 'a + b') with the test instance being the left operand and the improper type item - the right operand
  * the tested operation with the operand being swapped  - except for the exponentiation
  * the augmented assignment (as 'a += b') to the test instance with the improper type item being the right operand

ValueError - the proper type of the second operand, but either the 'mean' or the second operand have incompatible values (division by zero, etc.). The tests are performed within the *assertRaises*() with catching by ValueError context:

* Division operation
  * Instantiate **MeasuredValue** (tested class) with an arbitrary, random values of the 'mean' and the uncertainty
  * Try to divide it by 0 (integer) and 0.0 (floating point)
  * Create a second instance of **MeasuredValue** with zero 'mean' (try both integer and floating point zeros)
  * Try to divide the first instance by the second
  * Repeat the procedure using the augmented division assigment instead.
* Exponentiation operation
  * Instantiate **MeasuredValue** (tested class) with an arbitrary, random values of the 'mean' and the uncertainty; the 'mean' value should be negative
  * Try to raise this instance into a random non-integer power. Repeat several time with the different powers - both positive and negative.
  * Instantiate **MeasuredValue** (tested class) with an arbitrary, random value of the uncertainty and zero 'mean' (try both integer 0 and floating point 0.0)
  * Try to raise this instance to an arbitrary (integer or floating point) negative power. Repeat several times with the different powers.
  * Repeat the procedure using the augmented expenentiation assigment instead.

The test cases are implemented within the module [UT001_base_classes](../../Tests/UT001_base_classes.py), see classes **Test_Add**, **Test_Sub**, **Test_Mul**, **Test_Div** and **Test_Pow**.

**Test result:** PASS

## Traceability

For traceability the relation between tests and requirements is summarized in the table below:

| **Requirement ID** | **Covered in test(s)** | **Verified \[YES/NO\]**) |
| :----------------- | :--------------------- | :----------------------- |
| REQ-FUN-100        | TEST-T-100             | YES                      |
| REQ-FUN-101        | TEST-T-101             | YES                      |
| REQ-FUN-102        | TEST-T-101             | YES                      |
| REQ-AWM-100        | TEST-T-100             | YES                      |
| REQ-AWM-101        | TEST-T-100             | YES                      |
| REQ-AWM-102        | TEST-T-101             | YES                      |
| REQ-AWM-103        | TEST-T-101             | YES                      |

| **Software ready for production \[YES/NO\]** | **Rationale**        |
| :------------------------------------------: | :------------------- |
| YES                                          | All tests are passed |
