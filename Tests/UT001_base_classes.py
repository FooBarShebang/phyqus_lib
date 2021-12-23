#usr/bin/python3
"""
Module phyqus_lib.Tests.UT001_base_classes

Set of unit tests on the module phyqus_lib.base_classes.
"""

__version__= '1.1.0.0'
__date__ = '23-12-2021'
__status__ = 'Testing'

#imports

#+ standard library

import sys
import os
import unittest
import random
import operator
import math

#+ custom modules

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(os.path.dirname(MODULE_PATH))
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual import

from phyqus_lib.base_classes import MeasuredValue

#globals

DEF_PRECISION = 8

#classes

#+ helper classes

class HelperClass:

    def __init__(self, Value, SE):
        self.Value = Value
        self.SE = SE

#+ test cases

class Test_Init(unittest.TestCase):
    """
    Test cases for the class phyqus_lib.base_classes.MeasuredValue. Checks the
    implementation of the __init__() method.
    
    Implements tests: TEST-T-100.
    Covers the requirements REQ-FUN-100, REQ-AWM-100 and REQ-AWM-101.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.BadCases = [int, float, str, '1', [1], (1, '1'), ['1'], {'1' : 1}]
        cls.Randoms = [
                (random.randrange(-100, 100), random.randrange(0, 10)),
                (random.uniform(-10.0, 10.0), random.random())
            ]
    
    def test_operation_Ok(self):
        """
        Checks that the instance is created as expected.

        REQ-FUN-100
        """
        for _ in range(100):
            for Mean, Error in self.Randoms:
                gTemp = MeasuredValue(Mean)
                self.assertEqual(gTemp.Value, Mean)
                self.assertEqual(gTemp.SE, 0)
                del gTemp
                gTemp = MeasuredValue(Mean, Error)
                self.assertEqual(gTemp.Value, Mean)
                self.assertEqual(gTemp.SE, Error)
                del gTemp
                gTemp = MeasuredValue(HelperClass(Mean, Error))
                self.assertEqual(gTemp.Value, Mean)
                self.assertEqual(gTemp.SE, Error)
                del gTemp
                gTemp = MeasuredValue(HelperClass(Mean, Error), 0)
                self.assertEqual(gTemp.Value, Mean)
                self.assertEqual(gTemp.SE, 0)
                del gTemp
                gTemp = MeasuredValue(MeasuredValue(Mean, Error))
                self.assertEqual(gTemp.Value, Mean)
                self.assertEqual(gTemp.SE, Error)
                del gTemp
                gTemp = MeasuredValue(MeasuredValue(Mean, Error), 0)
                self.assertEqual(gTemp.Value, Mean)
                self.assertEqual(gTemp.SE, 0)
                del gTemp
    
    def test_TypeError(self):
        """
        Tests that the TypeError sub-clas exception is raised if the arguments
        of the initialization method are of improper types.

        REQ-AWM-100
        """
        for Item in self.BadCases:
            strMessage = 'from {}'.format(Item)
            with self.assertRaises(TypeError, msg = strMessage):
                MeasuredValue(Item)
            strMessage = 'from {}, 0.1'.format(Item)
            with self.assertRaises(TypeError, msg = strMessage):
                MeasuredValue(Item, 0.1)
            strMessage = 'from HelperClass({}, 0.1)'.format(Item)
            with self.assertRaises(TypeError, msg = strMessage):
                MeasuredValue(HelperClass(Item, 0.1))
            strMessage = 'from HelperClass(1, {})'.format(Item)
            with self.assertRaises(TypeError, msg = strMessage):
                MeasuredValue(HelperClass(1, Item))
            strMessage = 'from HelperClass({}, 0.1), 0.1'.format(Item)
            with self.assertRaises(TypeError, msg = strMessage):
                MeasuredValue(HelperClass(Item, 0.1), 0.1)
            strMessage = 'from HelperClass(1, {}), 0.1'.format(Item)
            with self.assertRaises(TypeError, msg = strMessage):
                MeasuredValue(HelperClass(1, Item), 0.1)
        strMessage = 'HelperClass(1, -1)'
        with self.assertRaises(TypeError, msg = strMessage):
            MeasuredValue(HelperClass(1, -1))
        strMessage = 'HelperClass(1, -1), 0.1'
        with self.assertRaises(TypeError, msg = strMessage):
            MeasuredValue(HelperClass(1, -1), 0.1)
    
    def test_ValueError(self):
        """
        Tests that the ValueError sub-class exception is raised if the passed
        SE argument is a negative real number.

        REQ-AWM-101
        """
        with self.assertRaises(ValueError, msg = '1, -0.1'):
            MeasuredValue(1, -0.1)
        with self.assertRaises(ValueError, msg = '0.1, -1'):
            MeasuredValue(0.1, -1)
        with self.assertRaises(ValueError, msg = 'HelperClass(1,1), -0.1'):
            MeasuredValue(HelperClass(1,1), -0.1)
        with self.assertRaises(ValueError, msg = 'MeasuredValue(1,1), -1'):
            MeasuredValue(MeasuredValue(1,1), -1)

class Test_Add(unittest.TestCase):
    """
    Test cases for the class phyqus_lib.base_classes.MeasuredValue. Checks the
    implementation of the __add__(), __radd__() and __iadd__() methods.
    
    Implements tests: TEST-T-101.
    Covers the requirements REQ-FUN-102, REQ-AWM-102 and REQ-AWM-103.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.BadCases = [int, float, str, '1', [1], (1, '1'), ['1'], {'1' : 1},
                        HelperClass(1, -1), HelperClass('1', 1),
                        HelperClass(1, '1')]
        cls.Randoms = [
                (random.randrange(-100, 100), random.randrange(0, 10)),
                (random.uniform(-10.0, 10.0), random.random())
            ]
        cls.Precision = DEF_PRECISION
        cls.Operation = staticmethod(operator.add)
        cls.AugOperation = staticmethod(operator.iadd)
        cls.CheckReverse = True
    
    def test_TypeError(self):
        """
        Tests that the operation raises TypeError if an improper second operand
        is used.

        REQ-AWM-102
        """
        Temp = MeasuredValue(1, 0.1)
        for Item in self.BadCases:
            #direct
            with self.assertRaises(TypeError,
                                        msg = 'direct with {}'.format(Item)):
                gTemp = self.Operation(Temp, Item)
            #reversed
            if self.CheckReverse:
                with self.assertRaises(TypeError,
                                        msg = 'reversed with {}'.format(Item)):
                    gTemp = self.Operation(Item, Temp)
            #augmented assignment
            with self.assertRaises(TypeError,
                                        msg = 'augmented with {}'.format(Item)):
                self.AugOperation(Temp, Item)
    
    def test_normal(self):
        """
        Checks that the __add__() operation works as expected.

        REQ-FUN-102
        """
        for _ in range(1000):
            Value1 = random.uniform(-100.0, 100.0)
            SE1 = random.random() * 11
            Value2 = random.uniform(-100.0, 100.0)
            SE2 = random.random() * 11
            #with real numbers
            for Other in [Value2 , int(Value2)]:
                Temp = MeasuredValue(Value1, SE1)
                Value3 = Value1 + Other
                Test = Temp + Other
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE1, places = self.Precision)
                del Test
                Test = self.Operation(Temp, Other)
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE1, places = self.Precision)
                del Temp
                del Test
                Temp = MeasuredValue(int(Value1), int(SE1))
                Value3 = int(Value1) + Other
                Test = Temp + Other
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, int(SE1),
                                                    places = self.Precision)
                del Test
                Test = self.Operation(Temp, Other)
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, int(SE1),
                                                    places = self.Precision)
                del Temp
                del Test
            #with other measurement with uncertainty
            lstOthers = [HelperClass(Value2, SE2),
                            HelperClass(int(Value2), int(SE2)),
                            MeasuredValue(Value2, SE2),
                            MeasuredValue(int(Value2), int(SE2))]
            for Other in lstOthers:
                Temp = MeasuredValue(Value1, SE1)
                Value3 = Value1 + Other.Value
                SE3 = math.sqrt(SE1**2 + (Other.SE)**2)
                Test = Temp + Other
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE3, places = self.Precision)
                del Test
                Test = self.Operation(Temp, Other)
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE3, places = self.Precision)
                del Temp
                del Test
                Temp = MeasuredValue(int(Value1), int(SE1))
                Value3 = int(Value1) + Other.Value
                SE3 = math.sqrt((int(SE1))**2 + (Other.SE)**2)
                Test = Temp + Other
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE3, places = self.Precision)
                del Test
                Test = self.Operation(Temp, Other)
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE3, places = self.Precision)
                del Test
                del Temp
            #special case - with itself
            Temp = MeasuredValue(Value1, SE1)
            Test = Temp + Temp
            self.assertIsInstance(Test, MeasuredValue)
            self.assertAlmostEqual(Test.Value, 2 * Value1,
                                                    places = self.Precision)
            self.assertAlmostEqual(Test.SE, 2 * SE1, places = self.Precision)
            del Test
            Test = self.Operation(Temp, Temp)
            self.assertIsInstance(Test, MeasuredValue)
            self.assertAlmostEqual(Test.Value, 2 * Value1,
                                                    places = self.Precision)
            self.assertAlmostEqual(Test.SE, 2 * SE1, places = self.Precision)
            del Test
            del Temp
            Temp = MeasuredValue(int(Value1), int(SE1))
            Test = Temp + Temp
            self.assertIsInstance(Test, MeasuredValue)
            self.assertEqual(Test.Value, 2 * int(Value1))
            self.assertEqual(Test.SE, 2 * int(SE1))
            del Test
            Test = self.Operation(Temp, Temp)
            self.assertIsInstance(Test, MeasuredValue)
            self.assertEqual(Test.Value, 2 * int(Value1))
            self.assertEqual(Test.SE, 2 * int(SE1))
            del Test
            del Temp
    
    def test_augmented(self):
        """
        Checks that the __iadd__() operation works as expected.

        REQ-FUN-102
        """
        for _ in range(1000):
            Value1 = random.uniform(-100.0, 100.0)
            SE1 = random.random() * 11
            Value2 = random.uniform(-100.0, 100.0)
            SE2 = random.random() * 11
            #with real numbers
            for Other in [Value2 , int(Value2)]:
                Temp = MeasuredValue(Value1, SE1)
                Value3 = Value1 + Other
                Temp += Other
                self.assertIsInstance(Temp, MeasuredValue)
                self.assertAlmostEqual(Temp.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Temp.SE, SE1, places = self.Precision)
                del Temp
                Temp = MeasuredValue(Value1, SE1)
                self.AugOperation(Temp, Other)
                self.assertIsInstance(Temp, MeasuredValue)
                self.assertAlmostEqual(Temp.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Temp.SE, SE1, places = self.Precision)
                del Temp
                Temp = MeasuredValue(int(Value1), int(SE1))
                Value3 = int(Value1) + Other
                Temp += Other
                self.assertIsInstance(Temp, MeasuredValue)
                self.assertAlmostEqual(Temp.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Temp.SE, int(SE1),
                                                    places = self.Precision)
                del Temp
                Temp = MeasuredValue(int(Value1), int(SE1))
                self.AugOperation(Temp, Other)
                self.assertIsInstance(Temp, MeasuredValue)
                self.assertAlmostEqual(Temp.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Temp.SE, int(SE1),
                                                    places = self.Precision)
                del Temp
            #with other measurement with uncertainty
            lstOthers = [HelperClass(Value2, SE2),
                            HelperClass(int(Value2), int(SE2)),
                            MeasuredValue(Value2, SE2),
                            MeasuredValue(int(Value2), int(SE2))]
            for Other in lstOthers:
                Temp = MeasuredValue(Value1, SE1)
                Value3 = Value1 + Other.Value
                SE3 = math.sqrt(SE1**2 + (Other.SE)**2)
                Temp += Other
                self.assertIsInstance(Temp, MeasuredValue)
                self.assertAlmostEqual(Temp.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Temp.SE, SE3, places = self.Precision)
                del Temp
                Temp = MeasuredValue(Value1, SE1)
                self.AugOperation(Temp, Other)
                self.assertIsInstance(Temp, MeasuredValue)
                self.assertAlmostEqual(Temp.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Temp.SE, SE3, places = self.Precision)
                del Temp
                Temp = MeasuredValue(int(Value1), int(SE1))
                Value3 = int(Value1) + Other.Value
                SE3 = math.sqrt((int(SE1))**2 + (Other.SE)**2)
                Temp += Other
                self.assertIsInstance(Temp, MeasuredValue)
                self.assertAlmostEqual(Temp.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Temp.SE, SE3, places = self.Precision)
                del Temp
                Temp = MeasuredValue(int(Value1), int(SE1))
                self.AugOperation(Temp, Other)
                self.assertIsInstance(Temp, MeasuredValue)
                self.assertAlmostEqual(Temp.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Temp.SE, SE3, places = self.Precision)
                del Temp
            #special case - with itself
            Temp = MeasuredValue(Value1, SE1)
            Temp += Temp
            self.assertIsInstance(Temp, MeasuredValue)
            self.assertAlmostEqual(Temp.Value, 2 * Value1,
                                                    places = self.Precision)
            self.assertAlmostEqual(Temp.SE, 2 * SE1, places = self.Precision)
            del Temp
            Temp = MeasuredValue(Value1, SE1)
            self.AugOperation(Temp, Temp)
            self.assertIsInstance(Temp, MeasuredValue)
            self.assertAlmostEqual(Temp.Value, 2 * Value1,
                                                    places = self.Precision)
            self.assertAlmostEqual(Temp.SE, 2 * SE1, places = self.Precision)
            del Temp
            Temp = MeasuredValue(int(Value1), int(SE1))
            Temp += Temp
            self.assertIsInstance(Temp, MeasuredValue)
            self.assertEqual(Temp.Value, 2 * int(Value1))
            self.assertEqual(Temp.SE, 2 * int(SE1))
            del Temp
            Temp = MeasuredValue(int(Value1), int(SE1))
            self.AugOperation(Temp, Temp)
            self.assertIsInstance(Temp, MeasuredValue)
            self.assertEqual(Temp.Value, 2 * int(Value1))
            self.assertEqual(Temp.SE, 2 * int(SE1))
            del Temp
    
    def test_reversed(self):
        """
        Checks that the __radd__() operation works as expected.

        REQ-FUN-102
        """
        for _ in range(1000):
            Value1 = random.uniform(-100.0, 100.0)
            SE1 = random.random() * 11
            Value2 = random.uniform(-100.0, 100.0)
            SE2 = random.random() * 11
            #with real numbers
            for Other in [Value2 , int(Value2)]:
                Temp = MeasuredValue(Value1, SE1)
                Value3 = Value1 + Other
                Test = Other + Temp
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE1, places = self.Precision)
                del Test
                Test = self.Operation(Other, Temp)
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE1, places = self.Precision)
                del Temp
                del Test
                Temp = MeasuredValue(int(Value1), int(SE1))
                Value3 = int(Value1) + Other
                Test = Other + Temp
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, int(SE1),
                                                    places = self.Precision)
                del Test
                Test = self.Operation(Other, Temp)
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, int(SE1),
                                                    places = self.Precision)
                del Temp
                del Test

class Test_Sub(Test_Add):
    """
    Test cases for the class phyqus_lib.base_classes.MeasuredValue. Checks the
    implementation of the __sub__(), __rsub__() and __isub__() methods.
    
    Implements tests: TEST-T-101.
    Covers the requirements REQ-FUN-102, REQ-AWM-102 and REQ-AWM-103.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.Operation = staticmethod(operator.sub)
        cls.AugOperation = staticmethod(operator.isub)
    
    def test_normal(self):
        """
        Checks that the __sub__() operation works as expected.

        REQ-FUN-102
        """
        for _ in range(1000):
            Value1 = random.uniform(-100.0, 100.0)
            SE1 = random.random() * 11
            Value2 = random.uniform(-100.0, 100.0)
            SE2 = random.random() * 11
            #with real numbers
            for Other in [Value2 , int(Value2)]:
                Temp = MeasuredValue(Value1, SE1)
                Value3 = Value1 - Other
                Test = Temp - Other
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE1, places = self.Precision)
                del Test
                Test = self.Operation(Temp, Other)
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE1, places = self.Precision)
                del Temp
                del Test
                Temp = MeasuredValue(int(Value1), int(SE1))
                Value3 = int(Value1) - Other
                Test = Temp - Other
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, int(SE1),
                                                    places = self.Precision)
                del Test
                Test = self.Operation(Temp, Other)
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, int(SE1),
                                                    places = self.Precision)
                del Temp
                del Test
            #with other measurement with uncertainty
            lstOthers = [HelperClass(Value2, SE2),
                            HelperClass(int(Value2), int(SE2)),
                            MeasuredValue(Value2, SE2),
                            MeasuredValue(int(Value2), int(SE2))]
            for Other in lstOthers:
                Temp = MeasuredValue(Value1, SE1)
                Value3 = Value1 - Other.Value
                SE3 = math.sqrt(SE1**2 + (Other.SE)**2)
                Test = Temp - Other
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE3, places = self.Precision)
                del Test
                Test = self.Operation(Temp, Other)
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE3, places = self.Precision)
                del Test
                del Temp
                Temp = MeasuredValue(int(Value1), int(SE1))
                Value3 = int(Value1) - Other.Value
                SE3 = math.sqrt((int(SE1))**2 + (Other.SE)**2)
                Test = Temp - Other
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE3, places = self.Precision)
                del Test
                Test = self.Operation(Temp, Other)
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE3, places = self.Precision)
                del Test
                del Temp
            #special case - with itself
            Temp = MeasuredValue(Value1, SE1)
            Test = Temp - Temp
            self.assertIsInstance(Test, MeasuredValue)
            self.assertEqual(Test.Value, 0)
            self.assertEqual(Test.SE, 0)
            del Test
            Test = self.Operation(Temp, Temp)
            self.assertIsInstance(Test, MeasuredValue)
            self.assertEqual(Test.Value, 0)
            self.assertEqual(Test.SE, 0)
            del Test
            del Temp
            Temp = MeasuredValue(int(Value1), int(SE1))
            Test = Temp - Temp
            self.assertIsInstance(Test, MeasuredValue)
            self.assertEqual(Test.Value, 0)
            self.assertEqual(Test.SE, 0)
            del Test
            Test = self.Operation(Temp, Temp)
            self.assertIsInstance(Test, MeasuredValue)
            self.assertEqual(Test.Value, 0)
            self.assertEqual(Test.SE, 0)
            del Test
            del Temp
    
    def test_augmented(self):
        """
        Checks that the __isub__() operation works as expected.

        REQ-FUN-102
        """
        for _ in range(1000):
            Value1 = random.uniform(-100.0, 100.0)
            SE1 = random.random() * 11
            Value2 = random.uniform(-100.0, 100.0)
            SE2 = random.random() * 11
            #with real numbers
            for Other in [Value2 , int(Value2)]:
                Temp = MeasuredValue(Value1, SE1)
                Value3 = Value1 - Other
                Temp -= Other
                self.assertIsInstance(Temp, MeasuredValue)
                self.assertAlmostEqual(Temp.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Temp.SE, SE1, places = self.Precision)
                del Temp
                Temp = MeasuredValue(Value1, SE1)
                self.AugOperation(Temp, Other)
                self.assertIsInstance(Temp, MeasuredValue)
                self.assertAlmostEqual(Temp.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Temp.SE, SE1, places = self.Precision)
                del Temp
                Temp = MeasuredValue(int(Value1), int(SE1))
                Value3 = int(Value1) - Other
                Temp -= Other
                self.assertIsInstance(Temp, MeasuredValue)
                self.assertAlmostEqual(Temp.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Temp.SE, int(SE1),
                                                    places = self.Precision)
                del Temp
                Temp = MeasuredValue(int(Value1), int(SE1))
                self.AugOperation(Temp, Other)
                self.assertIsInstance(Temp, MeasuredValue)
                self.assertAlmostEqual(Temp.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Temp.SE, int(SE1),
                                                    places = self.Precision)
                del Temp
            #with other measurement with uncertainty
            lstOthers = [HelperClass(Value2, SE2),
                            HelperClass(int(Value2), int(SE2)),
                            MeasuredValue(Value2, SE2),
                            MeasuredValue(int(Value2), int(SE2))]
            for Other in lstOthers:
                Temp = MeasuredValue(Value1, SE1)
                Value3 = Value1 - Other.Value
                SE3 = math.sqrt(SE1**2 + (Other.SE)**2)
                Temp -= Other
                self.assertIsInstance(Temp, MeasuredValue)
                self.assertAlmostEqual(Temp.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Temp.SE, SE3, places = self.Precision)
                del Temp
                Temp = MeasuredValue(Value1, SE1)
                self.AugOperation(Temp, Other)
                self.assertIsInstance(Temp, MeasuredValue)
                self.assertAlmostEqual(Temp.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Temp.SE, SE3, places = self.Precision)
                del Temp
                Temp = MeasuredValue(int(Value1), int(SE1))
                Value3 = int(Value1) - Other.Value
                SE3 = math.sqrt((int(SE1))**2 + (Other.SE)**2)
                Temp -= Other
                self.assertIsInstance(Temp, MeasuredValue)
                self.assertAlmostEqual(Temp.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Temp.SE, SE3, places = self.Precision)
                del Temp
                Temp = MeasuredValue(int(Value1), int(SE1))
                self.AugOperation(Temp, Other)
                self.assertIsInstance(Temp, MeasuredValue)
                self.assertAlmostEqual(Temp.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Temp.SE, SE3, places = self.Precision)
                del Temp
            #special case - with itself
            Temp = MeasuredValue(Value1, SE1)
            Temp -= Temp
            self.assertIsInstance(Temp, MeasuredValue)
            self.assertEqual(Temp.Value, 0)
            self.assertEqual(Temp.SE, 0)
            del Temp
            Temp = MeasuredValue(Value1, SE1)
            self.AugOperation(Temp, Temp)
            self.assertIsInstance(Temp, MeasuredValue)
            self.assertEqual(Temp.Value, 0)
            self.assertEqual(Temp.SE, 0)
            del Temp
            Temp = MeasuredValue(int(Value1), int(SE1))
            Temp -= Temp
            self.assertIsInstance(Temp, MeasuredValue)
            self.assertEqual(Temp.Value, 0)
            self.assertEqual(Temp.SE, 0)
            del Temp
            Temp = MeasuredValue(int(Value1), int(SE1))
            self.AugOperation(Temp, Temp)
            self.assertIsInstance(Temp, MeasuredValue)
            self.assertEqual(Temp.Value, 0)
            self.assertEqual(Temp.SE, 0)
            del Temp
    
    def test_reversed(self):
        """
        Checks that the __rsub__() operation works as expected.

        REQ-FUN-102
        """
        for _ in range(1000):
            Value1 = random.uniform(-100.0, 100.0)
            SE1 = random.random() * 11
            Value2 = random.uniform(-100.0, 100.0)
            SE2 = random.random() * 11
            #with real numbers
            for Other in [Value2 , int(Value2)]:
                Temp = MeasuredValue(Value1, SE1)
                Value3 = Other - Value1
                Test = Other - Temp
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE1, places = self.Precision)
                del Test
                Test = self.Operation(Other, Temp)
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE1, places = self.Precision)
                del Temp
                del Test
                Temp = MeasuredValue(int(Value1), int(SE1))
                Value3 = Other - int(Value1)
                Test = Other - Temp
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, int(SE1),
                                                    places = self.Precision)
                del Test
                Test = self.Operation(Other, Temp)
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, int(SE1),
                                                    places = self.Precision)
                del Temp
                del Test

class Test_Mul(Test_Add):
    """
    Test cases for the class phyqus_lib.base_classes.MeasuredValue. Checks the
    implementation of the __mul__(), __rmul__() and __imul__() methods.
    
    Implements tests: TEST-T-101.
    Covers the requirements REQ-FUN-102, REQ-AWM-102 and REQ-AWM-103.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.Operation = staticmethod(operator.mul)
        cls.AugOperation = staticmethod(operator.imul)
    
    def test_normal(self):
        """
        Checks that the __mul__() operation works as expected.

        REQ-FUN-102
        """
        for _ in range(1000):
            Value1 = random.uniform(-100.0, 100.0)
            SE1 = random.random() * 11
            Value2 = random.uniform(-100.0, 100.0)
            SE2 = random.random() * 11
            #with real numbers
            for Other in [Value2 , int(Value2)]:
                Temp = MeasuredValue(Value1, SE1)
                Value3 = Value1 * Other
                SE3 = SE1 * abs(Other)
                Test = Temp * Other
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE3, places = self.Precision)
                del Test
                Test = self.Operation(Temp, Other)
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE3, places = self.Precision)
                del Temp
                del Test
                Temp = MeasuredValue(int(Value1), int(SE1))
                Value3 = int(Value1) * Other
                Test = Temp * Other
                SE3 = int(SE1) * abs(Other)
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE3, places = self.Precision)
                del Test
                Test = self.Operation(Temp, Other)
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE3, places = self.Precision)
                del Temp
                del Test
            #with other measurement with uncertainty
            lstOthers = [HelperClass(Value2, SE2),
                            HelperClass(int(Value2), int(SE2)),
                            MeasuredValue(Value2, SE2),
                            MeasuredValue(int(Value2), int(SE2))]
            for Other in lstOthers:
                Temp = MeasuredValue(Value1, SE1)
                Value3 = Value1 * Other.Value
                SE3 = math.sqrt(pow(Other.Value * SE1, 2) + 
                                                    pow(Value1 * Other.SE, 2))
                Test = Temp * Other
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE3, places = self.Precision)
                del Test
                Test = self.Operation(Temp, Other)
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE3, places = self.Precision)
                del Test
                del Temp
                Temp = MeasuredValue(int(Value1), int(SE1))
                Value3 = int(Value1) * Other.Value
                SE3 = math.sqrt((Other.Value * int(SE1))**2 + 
                                                (int(Value1) * Other.SE)**2)
                Test = Temp * Other
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE3, places = self.Precision)
                del Test
                Test = self.Operation(Temp, Other)
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE3, places = self.Precision)
                del Test
                del Temp
            #special case - with itself
            Temp = MeasuredValue(Value1, SE1)
            Test = Temp * Temp
            self.assertIsInstance(Test, MeasuredValue)
            self.assertAlmostEqual(Test.Value, Value1**2, places=self.Precision)
            self.assertAlmostEqual(Test.SE, 2 * SE1 * abs(Value1),
                                                        places = self.Precision)
            del Test
            Test = self.Operation(Temp, Temp)
            self.assertIsInstance(Test, MeasuredValue)
            self.assertAlmostEqual(Test.Value, Value1**2, places=self.Precision)
            self.assertAlmostEqual(Test.SE, 2 * SE1 * abs(Value1),
                                                        places = self.Precision)
            del Test
            del Temp
            Temp = MeasuredValue(int(Value1), int(SE1))
            Test = Temp * Temp
            self.assertIsInstance(Test, MeasuredValue)
            self.assertAlmostEqual(Test.Value, (int(Value1))**2, 
                                                        places = self.Precision)
            self.assertAlmostEqual(Test.SE, 2 * int(SE1) * abs(int(Value1)),
                                                        places = self.Precision)
            del Test
            Test = self.Operation(Temp, Temp)
            self.assertIsInstance(Test, MeasuredValue)
            self.assertAlmostEqual(Test.Value, (int(Value1))**2, 
                                                        places = self.Precision)
            self.assertAlmostEqual(Test.SE, 2 * int(SE1) * abs(int(Value1)),
                                                        places = self.Precision)
            del Test
            del Temp
    
    def test_augmented(self):
        """
        Checks that the __imul__() operation works as expected.

        REQ-FUN-102
        """
        for _ in range(1000):
            Value1 = random.uniform(-100.0, 100.0)
            SE1 = random.random() * 11
            Value2 = random.uniform(-100.0, 100.0)
            SE2 = random.random() * 11
            #with real numbers
            for Other in [Value2 , int(Value2)]:
                Temp = MeasuredValue(Value1, SE1)
                Value3 = Value1 * Other
                SE3 = SE1 * abs(Other)
                Temp *= Other
                self.assertIsInstance(Temp, MeasuredValue)
                self.assertAlmostEqual(Temp.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Temp.SE, SE3, places = self.Precision)
                del Temp
                Temp = MeasuredValue(Value1, SE1)
                self.AugOperation(Temp, Other)
                self.assertIsInstance(Temp, MeasuredValue)
                self.assertAlmostEqual(Temp.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Temp.SE, SE3, places = self.Precision)
                del Temp
                Temp = MeasuredValue(int(Value1), int(SE1))
                Value3 = int(Value1) * Other
                Temp *= Other
                SE3 = int(SE1) * abs(Other)
                self.assertIsInstance(Temp, MeasuredValue)
                self.assertAlmostEqual(Temp.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Temp.SE, SE3, places = self.Precision)
                del Temp
                Temp = MeasuredValue(int(Value1), int(SE1))
                self.AugOperation(Temp, Other)
                self.assertIsInstance(Temp, MeasuredValue)
                self.assertAlmostEqual(Temp.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Temp.SE, SE3, places = self.Precision)
                del Temp
            #with other measurement with uncertainty
            lstOthers = [HelperClass(Value2, SE2),
                            HelperClass(int(Value2), int(SE2)),
                            MeasuredValue(Value2, SE2),
                            MeasuredValue(int(Value2), int(SE2))]
            for Other in lstOthers:
                Temp = MeasuredValue(Value1, SE1)
                Value3 = Value1 * Other.Value
                SE3 = math.sqrt(pow(Other.Value * SE1, 2) + 
                                                    pow(Value1 * Other.SE, 2))
                Temp *= Other
                self.assertIsInstance(Temp, MeasuredValue)
                self.assertAlmostEqual(Temp.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Temp.SE, SE3, places = self.Precision)
                del Temp
                Temp = MeasuredValue(Value1, SE1)
                self.AugOperation(Temp, Other)
                self.assertIsInstance(Temp, MeasuredValue)
                self.assertAlmostEqual(Temp.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Temp.SE, SE3, places = self.Precision)
                del Temp
                Temp = MeasuredValue(int(Value1), int(SE1))
                Value3 = int(Value1) * Other.Value
                SE3 = math.sqrt((Other.Value * int(SE1))**2 + 
                                                (int(Value1) * Other.SE)**2)
                Temp *= Other
                self.assertIsInstance(Temp, MeasuredValue)
                self.assertAlmostEqual(Temp.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Temp.SE, SE3, places = self.Precision)
                del Temp
                Temp = MeasuredValue(int(Value1), int(SE1))
                self.AugOperation(Temp, Other)
                self.assertIsInstance(Temp, MeasuredValue)
                self.assertAlmostEqual(Temp.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Temp.SE, SE3, places = self.Precision)
                del Temp
            #special case - with itself
            Temp = MeasuredValue(Value1, SE1)
            Temp *= Temp
            self.assertIsInstance(Temp, MeasuredValue)
            self.assertAlmostEqual(Temp.Value, Value1**2, places=self.Precision)
            self.assertAlmostEqual(Temp.SE, 2 * SE1 * abs(Value1),
                                                        places = self.Precision)
            del Temp
            Temp = MeasuredValue(Value1, SE1)
            self.AugOperation(Temp, Temp)
            self.assertIsInstance(Temp, MeasuredValue)
            self.assertAlmostEqual(Temp.Value, Value1**2, places=self.Precision)
            self.assertAlmostEqual(Temp.SE, 2 * SE1 * abs(Value1),
                                                        places = self.Precision)
            del Temp
            Temp = MeasuredValue(int(Value1), int(SE1))
            Temp *= Temp
            self.assertIsInstance(Temp, MeasuredValue)
            self.assertAlmostEqual(Temp.Value, (int(Value1))**2, 
                                                        places = self.Precision)
            self.assertAlmostEqual(Temp.SE, 2 * int(SE1) * abs(int(Value1)),
                                                        places = self.Precision)
            del Temp
            Temp = MeasuredValue(int(Value1), int(SE1))
            self.AugOperation(Temp, Temp)
            self.assertIsInstance(Temp, MeasuredValue)
            self.assertAlmostEqual(Temp.Value, (int(Value1))**2, 
                                                        places = self.Precision)
            self.assertAlmostEqual(Temp.SE, 2 * int(SE1) * abs(int(Value1)),
                                                        places = self.Precision)
            del Temp
    
    def test_reversed(self):
        """
        Checks that the __rmul__() operation works as expected.

        REQ-FUN-102
        """
        for _ in range(1000):
            Value1 = random.uniform(-100.0, 100.0)
            SE1 = random.random() * 11
            Value2 = random.uniform(-100.0, 100.0)
            SE2 = random.random() * 11
            #with real numbers
            for Other in [Value2 , int(Value2)]:
                Temp = MeasuredValue(Value1, SE1)
                Value3 = Value1 * Other
                SE3 = SE1 * abs(Other)
                Test = Other * Temp
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE3, places = self.Precision)
                del Test
                Test = self.Operation(Other, Temp)
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE3, places = self.Precision)
                del Temp
                del Test
                Temp = MeasuredValue(int(Value1), int(SE1))
                Value3 = int(Value1) * Other
                Test = Other * Temp
                SE3 = int(SE1) * abs(Other)
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE3, places = self.Precision)
                del Test
                Test = self.Operation(Other, Temp)
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE3, places = self.Precision)
                del Temp
                del Test

class Test_Div(Test_Add):
    """
    Test cases for the class phyqus_lib.base_classes.MeasuredValue. Checks the
    implementation of the __truediv__(), __rtruediv__() and __itruediv__()
    methods.
    
    Implements tests: TEST-T-101.
    Covers the requirements REQ-FUN-102, REQ-AWM-102 and REQ-AWM-103.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.Operation = staticmethod(operator.truediv)
        cls.AugOperation = staticmethod(operator.itruediv)
    
    def test_ValueError(self):
        """
        Tests that the operation raises ValueError if division by zero is about
        to occur.

        REQ-AWM-103
        """
        Temp = MeasuredValue(1, 0.1)
        Temp2 = MeasuredValue(10.0, 1)
        #direct
        with self.assertRaises(ValueError):
            gTest = Temp / 0
        with self.assertRaises(ValueError):
            gTest = Temp2 / 0.0
        with self.assertRaises(ValueError):
            gTest = Temp / MeasuredValue(0, 0)
        with self.assertRaises(ValueError):
            gTest = Temp2 / MeasuredValue(0.0, 0.1)
        with self.assertRaises(ValueError):
            gTest = Temp / HelperClass(0, 0)
        with self.assertRaises(ValueError):
            gTest = Temp2 / HelperClass(0.0, 0.1)
        with self.assertRaises(ValueError):
            gTest = self.Operation(Temp2, HelperClass(0.0, 0.1))
        #augmented assignment
        with self.assertRaises(ValueError):
            Temp /= 0
        with self.assertRaises(ValueError):
            Temp2 /= 0.0
        with self.assertRaises(ValueError):
            Temp /= MeasuredValue(0, 0)
        with self.assertRaises(ValueError):
            Temp2 /= MeasuredValue(0.0, 0.1)
        with self.assertRaises(ValueError):
            Temp /= HelperClass(0, 0)
        with self.assertRaises(ValueError):
            Temp2 /= HelperClass(0.0, 0.1)
        with self.assertRaises(ValueError):
            Temp2 = self.AugOperation(Temp2, HelperClass(0.0, 0.1))
        del Temp
        del Temp2
        #reversed
        Temp = MeasuredValue(0, 0.1)
        Temp2 = MeasuredValue(0.0, 1)
        with self.assertRaises(ValueError):
            gTest = 1 / Temp
        with self.assertRaises(ValueError):
            gTest = 1.0 / Temp2
        with self.assertRaises(ValueError):
            gTest = MeasuredValue(1, 0) / Temp
        with self.assertRaises(ValueError):
            gTest = MeasuredValue(0.0, 0.1) / Temp2
        with self.assertRaises(ValueError):
            gTest = HelperClass(0, 0) / Temp
        with self.assertRaises(ValueError):
            gTest = HelperClass(1.0, 0.1) / Temp2
        with self.assertRaises(ValueError):
            gTest = self.Operation(HelperClass(1.0, 0.1), Temp2)
        del Temp
        del Temp2
    
    def test_normal(self):
        """
        Checks that the __truediv__() operation works as expected.

        REQ-FUN-102
        """
        for _ in range(1000):
            Value1 = random.uniform(-100.0, 100.0)
            SE1 = random.random() * 11
            Value2 = random.uniform(-100.0, 100.0)
            SE2 = random.random() * 11
            #with real numbers
            for Other in [Value2 , int(Value2)]:
                if not Other:
                    continue
                Temp = MeasuredValue(Value1, SE1)
                Value3 = Value1 / Other
                SE3 = SE1 / abs(Other)
                Test = Temp / Other
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE3, places = self.Precision)
                del Test
                Test = self.Operation(Temp, Other)
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE3, places = self.Precision)
                del Temp
                del Test
                Temp = MeasuredValue(int(Value1), int(SE1))
                Value3 = int(Value1) / Other
                Test = Temp / Other
                SE3 = int(SE1) / abs(Other)
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE3, places = self.Precision)
                del Test
                Test = self.Operation(Temp, Other)
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE3, places = self.Precision)
                del Temp
                del Test
            #with other measurement with uncertainty
            lstOthers = [HelperClass(Value2, SE2),
                            HelperClass(int(Value2), int(SE2)),
                            MeasuredValue(Value2, SE2),
                            MeasuredValue(int(Value2), int(SE2))]
            for Other in lstOthers:
                if not Other.Value:
                    continue
                Temp = MeasuredValue(Value1, SE1)
                Value3 = Value1 / Other.Value
                SE3 = math.sqrt(pow(SE1 / Other.Value, 2) + 
                                pow(Value1 * Other.SE / (Other.Value)**2, 2))
                Test = Temp / Other
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE3, places = self.Precision)
                del Test
                Test = self.Operation(Temp, Other)
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE3, places = self.Precision)
                del Test
                del Temp
                Temp = MeasuredValue(int(Value1), int(SE1))
                Value3 = int(Value1) / Other.Value
                SE3 = math.sqrt(pow(int(SE1) / Other.Value, 2) + 
                            pow(int(Value1) * Other.SE / (Other.Value)**2, 2))
                Test = Temp / Other
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE3, places = self.Precision)
                del Test
                Test = self.Operation(Temp, Other)
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE3, places = self.Precision)
                del Test
                del Temp
            #special case - with itself
            if not Value1:
                continue
            Temp = MeasuredValue(Value1, SE1)
            Test = Temp / Temp
            self.assertIsInstance(Test, MeasuredValue)
            self.assertEqual(Test.Value, 1)
            self.assertEqual(Test.SE, 0)
            del Test
            Test = self.Operation(Temp, Temp)
            self.assertIsInstance(Test, MeasuredValue)
            self.assertEqual(Test.Value, 1)
            self.assertEqual(Test.SE, 0)
            del Test
            del Temp
            if not int(Value1):
                continue
            Temp = MeasuredValue(int(Value1), int(SE1))
            Test = Temp / Temp
            self.assertIsInstance(Test, MeasuredValue)
            self.assertEqual(Test.Value, 1)
            self.assertEqual(Test.SE, 0)
            del Test
            Test = self.Operation(Temp, Temp)
            self.assertIsInstance(Test, MeasuredValue)
            self.assertEqual(Test.Value, 1)
            self.assertEqual(Test.SE, 0)
            del Test
            del Temp
        #very special case - by itself with zero 'mean
        Temp = MeasuredValue(0, 0.1)
        Test = Temp / Temp
        self.assertIsInstance(Test, MeasuredValue)
        self.assertEqual(Test.Value, 1)
        self.assertEqual(Test.SE, 0)
        del Temp
        del Test
        Temp = MeasuredValue(0.0, 0)
        Test = self.Operation(Temp, Temp)
        self.assertIsInstance(Test, MeasuredValue)
        self.assertEqual(Test.Value, 1)
        self.assertEqual(Test.SE, 0)
        del Temp
        del Test
    
    def test_augmented(self):
        """
        Checks that the __itruediv__() operation works as expected.

        REQ-FUN-102
        """
        for _ in range(1000):
            Value1 = random.uniform(-100.0, 100.0)
            SE1 = random.random() * 11
            Value2 = random.uniform(-100.0, 100.0)
            SE2 = random.random() * 11
            #with real numbers
            for Other in [Value2 , int(Value2)]:
                if not Other:
                    continue
                Temp = MeasuredValue(Value1, SE1)
                Value3 = Value1 / Other
                SE3 = SE1 / abs(Other)
                Temp /= Other
                self.assertIsInstance(Temp, MeasuredValue)
                self.assertAlmostEqual(Temp.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Temp.SE, SE3, places = self.Precision)
                del Temp
                Temp = MeasuredValue(Value1, SE1)
                self.AugOperation(Temp, Other)
                self.assertIsInstance(Temp, MeasuredValue)
                self.assertAlmostEqual(Temp.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Temp.SE, SE3, places = self.Precision)
                del Temp
                Temp = MeasuredValue(int(Value1), int(SE1))
                Value3 = int(Value1) / Other
                Temp /= Other
                SE3 = int(SE1) / abs(Other)
                self.assertIsInstance(Temp, MeasuredValue)
                self.assertAlmostEqual(Temp.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Temp.SE, SE3, places = self.Precision)
                del Temp
                Temp = MeasuredValue(int(Value1), int(SE1))
                self.AugOperation(Temp, Other)
                self.assertIsInstance(Temp, MeasuredValue)
                self.assertAlmostEqual(Temp.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Temp.SE, SE3, places = self.Precision)
                del Temp
            #with other measurement with uncertainty
            lstOthers = [HelperClass(Value2, SE2),
                            HelperClass(int(Value2), int(SE2)),
                            MeasuredValue(Value2, SE2),
                            MeasuredValue(int(Value2), int(SE2))]
            for Other in lstOthers:
                if not Other.Value:
                    continue
                Temp = MeasuredValue(Value1, SE1)
                Value3 = Value1 / Other.Value
                SE3 = math.sqrt(pow(SE1 / Other.Value, 2) + 
                                pow(Value1 * Other.SE / (Other.Value)**2, 2))
                Temp /= Other
                self.assertIsInstance(Temp, MeasuredValue)
                self.assertAlmostEqual(Temp.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Temp.SE, SE3, places = self.Precision)
                del Temp
                Temp = MeasuredValue(Value1, SE1)
                self.AugOperation(Temp, Other)
                self.assertIsInstance(Temp, MeasuredValue)
                self.assertAlmostEqual(Temp.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Temp.SE, SE3, places = self.Precision)
                del Temp
                Temp = MeasuredValue(int(Value1), int(SE1))
                Value3 = int(Value1) / Other.Value
                SE3 = math.sqrt(pow(int(SE1) / Other.Value, 2) + 
                            pow(int(Value1) * Other.SE / (Other.Value)**2, 2))
                Temp /= Other
                self.assertIsInstance(Temp, MeasuredValue)
                self.assertAlmostEqual(Temp.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Temp.SE, SE3, places = self.Precision)
                del Temp
                Temp = MeasuredValue(int(Value1), int(SE1))
                self.AugOperation(Temp, Other)
                self.assertIsInstance(Temp, MeasuredValue)
                self.assertAlmostEqual(Temp.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Temp.SE, SE3, places = self.Precision)
                del Temp
            #special case - with itself
            if not Value1:
                continue
            Temp = MeasuredValue(Value1, SE1)
            Temp /= Temp
            self.assertIsInstance(Temp, MeasuredValue)
            self.assertEqual(Temp.Value, 1)
            self.assertEqual(Temp.SE, 0)
            del Temp
            Temp = MeasuredValue(Value1, SE1)
            self.AugOperation(Temp, Temp)
            self.assertIsInstance(Temp, MeasuredValue)
            self.assertEqual(Temp.Value, 1)
            self.assertEqual(Temp.SE, 0)
            del Temp
            if not int(Value1):
                continue
            Temp = MeasuredValue(int(Value1), int(SE1))
            Temp /= Temp
            self.assertIsInstance(Temp, MeasuredValue)
            self.assertEqual(Temp.Value, 1)
            self.assertEqual(Temp.SE, 0)
            del Temp
            Temp = MeasuredValue(int(Value1), int(SE1))
            self.AugOperation(Temp, Temp)
            self.assertIsInstance(Temp, MeasuredValue)
            self.assertEqual(Temp.Value, 1)
            self.assertEqual(Temp.SE, 0)
            del Temp
        #very special case - by itself with zero 'mean
        Temp = MeasuredValue(0, 0.1)
        Temp /= Temp
        self.assertIsInstance(Temp, MeasuredValue)
        self.assertEqual(Temp.Value, 1)
        self.assertEqual(Temp.SE, 0)
        del Temp
        Temp = MeasuredValue(0.0, 0)
        self.AugOperation(Temp, Temp)
        self.assertIsInstance(Temp, MeasuredValue)
        self.assertEqual(Temp.Value, 1)
        self.assertEqual(Temp.SE, 0)
        del Temp
    
    def test_reversed(self):
        """
        Checks that the __rtruediv__() operation works as expected.

        REQ-FUN-102
        """
        for _ in range(1000):
            Value1 = random.uniform(-100.0, 100.0)
            SE1 = random.random() * 11
            Value2 = random.uniform(-100.0, 100.0)
            SE2 = random.random() * 11
            #with real numbers
            for Other in [Value2 , int(Value2)]:
                if not Value1:
                    continue
                Temp = MeasuredValue(Value1, SE1)
                Value3 = Other / Value1
                SE3 = SE1 * abs(Other) / (abs(Value1)**2)
                Test = Other / Temp
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE3, places = self.Precision)
                del Test
                Test = self.Operation(Other, Temp)
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE3, places = self.Precision)
                del Temp
                del Test
                if not int(Value1):
                    continue
                Temp = MeasuredValue(int(Value1), int(SE1))
                Value3 = Other / int(Value1)
                Test = Other / Temp
                SE3 = int(SE1) * abs(Other) / (abs(int(Value1))**2)
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE3, places = self.Precision)
                del Test
                Test = self.Operation(Other, Temp)
                self.assertIsInstance(Test, MeasuredValue)
                self.assertAlmostEqual(Test.Value, Value3,
                                                    places = self.Precision)
                self.assertAlmostEqual(Test.SE, SE3, places = self.Precision)
                del Temp
                del Test

class Test_Pow(Test_Add):
    """
    Test cases for the class phyqus_lib.base_classes.MeasuredValue. Checks the
    implementation of the __pow__(), and __ipow__() methods.
    
    Implements tests: TEST-T-101.
    Covers the requirements REQ-FUN-102, REQ-AWM-102 and REQ-AWM-103.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.Operation = staticmethod(operator.pow)
        cls.AugOperation = staticmethod(operator.ipow)
    
    def test_normal(self):
        """
        Checks that the __pow__() operation works as expected.

        REQ-FUN-102
        """
        #integer exponent
        for _ in range(1000):
            Value1 = random.uniform(-10, 10)
            if not Value1:
                continue
            SE1 = random.random() * 3
            Value2 = random.randrange(1, 5)
            Value = pow(Value1, Value2)
            SE = abs(pow(Value1, Value2 - 1)) * Value2 * SE1
            Temp = MeasuredValue(Value1, SE1)
            gTest = Temp ** Value2
            gTest2 = self.Operation(Temp, Value2)
            self.assertIsInstance(gTest, MeasuredValue)
            self.assertAlmostEqual(gTest.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest.SE, SE, places = self.Precision)
            self.assertIsInstance(gTest2, MeasuredValue)
            self.assertAlmostEqual(gTest2.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest2.SE, SE, places = self.Precision)
            del gTest
            del gTest2
            del Temp
            if not int(Value1):
                continue
            Value = pow(int(Value1), Value2)
            SE = abs(pow(int(Value1), Value2 - 1)) * Value2 * int(SE1)
            Temp = MeasuredValue(int(Value1), int(SE1))
            gTest = Temp ** Value2
            gTest2 = self.Operation(Temp, Value2)
            self.assertIsInstance(gTest, MeasuredValue)
            self.assertAlmostEqual(gTest.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest.SE, SE, places = self.Precision)
            self.assertIsInstance(gTest2, MeasuredValue)
            self.assertAlmostEqual(gTest2.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest2.SE, SE, places = self.Precision)
            del gTest
            del gTest2
            del Temp
        #float exponent
        Value1 = random.uniform(0.1, 10)
        SE1 = random.random() * 3
        for _ in range(1000):
            Value2 = random.uniform(-3.0, 3.0)
            Value = pow(Value1, Value2)
            SE = abs(pow(Value1, Value2 - 1)) * abs(Value2) * SE1
            Temp = MeasuredValue(Value1, SE1)
            gTest = Temp ** Value2
            gTest2 = self.Operation(Temp, Value2)
            self.assertIsInstance(gTest, MeasuredValue)
            self.assertAlmostEqual(gTest.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest.SE, SE, places = self.Precision)
            self.assertIsInstance(gTest2, MeasuredValue)
            self.assertAlmostEqual(gTest2.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest2.SE, SE, places = self.Precision)
            del gTest
            del gTest2
            del Temp
            if not int(Value1):
                continue
            Value = pow(int(Value1), Value2)
            SE = abs(pow(int(Value1), Value2 - 1)) * abs(Value2) * int(SE1)
            Temp = MeasuredValue(int(Value1), int(SE1))
            gTest = Temp ** Value2
            gTest2 = self.Operation(Temp, Value2)
            self.assertIsInstance(gTest, MeasuredValue)
            self.assertAlmostEqual(gTest.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest.SE, SE, places = self.Precision)
            self.assertIsInstance(gTest2, MeasuredValue)
            self.assertAlmostEqual(gTest2.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest2.SE, SE, places = self.Precision)
            del gTest
            del gTest2
            del Temp
        #both base and exponent are with uncertainty
        for _ in range(1000):
            #float base
            Value1 = random.uniform(0.1, 5)
            SE1 = random.random()
            #+positive float exp
            Value2 = random.uniform(0.1, 5)
            SE2 = random.random()
            Value = pow(Value1, Value2)
            Temp1 = pow(Value2 * SE1, 2) * pow(Value1, 2*(Value2 - 1))
            Temp2 = pow(SE2 * math.log(Value1) * pow(Value1, Value2), 2)
            SE = math.sqrt(Temp1 + Temp2)
            TempBase = MeasuredValue(Value1, SE1)
            TempExp = MeasuredValue(Value2, SE2)
            gTest = TempBase ** TempExp
            gTest2 = self.Operation(TempBase, TempExp)
            self.assertIsInstance(gTest, MeasuredValue)
            self.assertAlmostEqual(gTest.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest.SE, SE, places = self.Precision)
            self.assertIsInstance(gTest2, MeasuredValue)
            self.assertAlmostEqual(gTest2.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest2.SE, SE, places = self.Precision)
            del gTest
            del gTest2
            del TempBase
            del TempExp
            #+negative float exp
            Value2 = -Value2
            Value = pow(Value1, Value2)
            Temp1 = pow(Value2 * SE1, 2) * pow(Value1, 2*(Value2 - 1))
            Temp2 = pow(SE2 * math.log(Value1) * pow(Value1, Value2), 2)
            SE = math.sqrt(Temp1 + Temp2)
            TempBase = MeasuredValue(Value1, SE1)
            TempExp = MeasuredValue(Value2, SE2)
            gTest = TempBase ** TempExp
            gTest2 = self.Operation(TempBase, TempExp)
            self.assertIsInstance(gTest, MeasuredValue)
            self.assertAlmostEqual(gTest.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest.SE, SE, places = self.Precision)
            self.assertIsInstance(gTest2, MeasuredValue)
            self.assertAlmostEqual(gTest2.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest2.SE, SE, places = self.Precision)
            del gTest
            del gTest2
            del TempBase
            del TempExp
            #+positive int exp
            Value2 = 1 + int(abs(Value2))
            Value = pow(Value1, Value2)
            Temp1 = pow(Value2 * SE1, 2) * pow(Value1, 2*(Value2 - 1))
            Temp2 = pow(SE2 * math.log(Value1) * pow(Value1, Value2), 2)
            SE = math.sqrt(Temp1 + Temp2)
            TempBase = MeasuredValue(Value1, SE1)
            TempExp = MeasuredValue(Value2, SE2)
            gTest = TempBase ** TempExp
            gTest2 = self.Operation(TempBase, TempExp)
            self.assertIsInstance(gTest, MeasuredValue)
            self.assertAlmostEqual(gTest.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest.SE, SE, places = self.Precision)
            self.assertIsInstance(gTest2, MeasuredValue)
            self.assertAlmostEqual(gTest2.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest2.SE, SE, places = self.Precision)
            del gTest
            del gTest2
            del TempBase
            del TempExp
            #+negative int exp
            Value2 = -Value2
            Value = pow(Value1, Value2)
            Temp1 = pow(Value2 * SE1, 2) * pow(Value1, 2*(Value2 - 1))
            Temp2 = pow(SE2 * math.log(Value1) * pow(Value1, Value2), 2)
            SE = math.sqrt(Temp1 + Temp2)
            TempBase = MeasuredValue(Value1, SE1)
            TempExp = MeasuredValue(Value2, SE2)
            gTest = TempBase ** TempExp
            gTest2 = self.Operation(TempBase, TempExp)
            self.assertIsInstance(gTest, MeasuredValue)
            self.assertAlmostEqual(gTest.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest.SE, SE, places = self.Precision)
            self.assertIsInstance(gTest2, MeasuredValue)
            self.assertAlmostEqual(gTest2.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest2.SE, SE, places = self.Precision)
            del gTest
            del gTest2
            del TempBase
            del TempExp
            #int base
            Value1 = int(random.uniform(0.1, 5) + 1)
            SE1 = random.random()
            #+positive float exp
            Value2 = random.uniform(0.1, 5)
            SE2 = random.random()
            Value = pow(Value1, Value2)
            Temp1 = pow(Value2 * SE1, 2) * pow(Value1, 2*(Value2 - 1))
            Temp2 = pow(SE2 * math.log(Value1) * pow(Value1, Value2), 2)
            SE = math.sqrt(Temp1 + Temp2)
            TempBase = MeasuredValue(Value1, SE1)
            TempExp = MeasuredValue(Value2, SE2)
            gTest = TempBase ** TempExp
            gTest2 = self.Operation(TempBase, TempExp)
            self.assertIsInstance(gTest, MeasuredValue)
            self.assertAlmostEqual(gTest.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest.SE, SE, places = self.Precision)
            self.assertIsInstance(gTest2, MeasuredValue)
            self.assertAlmostEqual(gTest2.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest2.SE, SE, places = self.Precision)
            del gTest
            del gTest2
            del TempBase
            del TempExp
            #+negative float exp
            Value2 = -Value2
            Value = pow(Value1, Value2)
            Temp1 = pow(Value2 * SE1, 2) * pow(Value1, 2*(Value2 - 1))
            Temp2 = pow(SE2 * math.log(Value1) * pow(Value1, Value2), 2)
            SE = math.sqrt(Temp1 + Temp2)
            TempBase = MeasuredValue(Value1, SE1)
            TempExp = MeasuredValue(Value2, SE2)
            gTest = TempBase ** TempExp
            gTest2 = self.Operation(TempBase, TempExp)
            self.assertIsInstance(gTest, MeasuredValue)
            self.assertAlmostEqual(gTest.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest.SE, SE, places = self.Precision)
            self.assertIsInstance(gTest2, MeasuredValue)
            self.assertAlmostEqual(gTest2.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest2.SE, SE, places = self.Precision)
            del gTest
            del gTest2
            del TempBase
            del TempExp
            #+positive int exp
            Value2 = 1 + int(abs(Value2))
            Value = pow(Value1, Value2)
            Temp1 = pow(Value2 * SE1, 2) * pow(Value1, 2*(Value2 - 1))
            Temp2 = pow(SE2 * math.log(Value1) * pow(Value1, Value2), 2)
            SE = math.sqrt(Temp1 + Temp2)
            TempBase = MeasuredValue(Value1, SE1)
            TempExp = MeasuredValue(Value2, SE2)
            gTest = TempBase ** TempExp
            gTest2 = self.Operation(TempBase, TempExp)
            self.assertIsInstance(gTest, MeasuredValue)
            self.assertAlmostEqual(gTest.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest.SE, SE, places = self.Precision)
            self.assertIsInstance(gTest2, MeasuredValue)
            self.assertAlmostEqual(gTest2.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest2.SE, SE, places = self.Precision)
            del gTest
            del gTest2
            del TempBase
            del TempExp
            #+negative int exp
            Value2 = -Value2
            Value = pow(Value1, Value2)
            Temp1 = pow(Value2 * SE1, 2) * pow(Value1, 2*(Value2 - 1))
            Temp2 = pow(SE2 * math.log(Value1) * pow(Value1, Value2), 2)
            SE = math.sqrt(Temp1 + Temp2)
            TempBase = MeasuredValue(Value1, SE1)
            TempExp = MeasuredValue(Value2, SE2)
            gTest = TempBase ** TempExp
            gTest2 = self.Operation(TempBase, TempExp)
            self.assertIsInstance(gTest, MeasuredValue)
            self.assertAlmostEqual(gTest.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest.SE, SE, places = self.Precision)
            self.assertIsInstance(gTest2, MeasuredValue)
            self.assertAlmostEqual(gTest2.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest2.SE, SE, places = self.Precision)
            del gTest
            del gTest2
            del TempBase
            del TempExp
        #special cases
        for _ in range(100): #base and exponent are the same object!
            #+float
            SE1 = random.random()
            Value1 = random.uniform(0.1, 5)
            Value = pow(Value1, Value1)
            SE = Value * SE1 * abs(1 + math.log(Value1))
            Temp = MeasuredValue(Value1, SE1)
            gTest = Temp ** Temp
            gTest2 = self.Operation(Temp, Temp)
            self.assertIsInstance(gTest, MeasuredValue)
            self.assertAlmostEqual(gTest.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest.SE, SE, places = self.Precision)
            self.assertIsInstance(gTest2, MeasuredValue)
            self.assertAlmostEqual(gTest2.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest2.SE, SE, places = self.Precision)
            del gTest
            del gTest2
            del Temp
            #+int
            Value1 = 1 + int(Value1)
            Value = pow(Value1, Value1)
            SE = Value * SE1 * abs(1 + math.log(Value1))
            Temp = MeasuredValue(Value1, SE1)
            gTest = Temp ** Temp
            gTest2 = self.Operation(Temp, Temp)
            self.assertIsInstance(gTest, MeasuredValue)
            self.assertAlmostEqual(gTest.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest.SE, SE, places = self.Precision)
            self.assertIsInstance(gTest2, MeasuredValue)
            self.assertAlmostEqual(gTest2.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest2.SE, SE, places = self.Precision)
            del gTest
            del gTest2
            del Temp
        for _ in range(10):
            Value1 = random.uniform(-10, 10)
            if not Value1:
                continue
            SE1 = random.random()
            Value2 = random.uniform(0.1, 3.0)
            Temp = MeasuredValue(Value1, SE1)
            gTest = Temp ** 0 #raising to (x!=0,y) measured into zero power!
            gTest2 = self.Operation(Temp, 0)
            gTest3 = Temp ** 0.0
            gTest4 = self.Operation(Temp, 0.0)
            self.assertIsInstance(gTest, MeasuredValue)
            self.assertEqual(gTest.Value, 1)
            self.assertEqual(gTest.SE, 0)
            self.assertIsInstance(gTest2, MeasuredValue)
            self.assertEqual(gTest2.Value, 1)
            self.assertEqual(gTest2.SE, 0)
            self.assertIsInstance(gTest3, MeasuredValue)
            self.assertEqual(gTest3.Value, 1)
            self.assertEqual(gTest3.SE, 0)
            self.assertIsInstance(gTest4, MeasuredValue)
            self.assertEqual(gTest4.Value, 1)
            self.assertEqual(gTest4.SE, 0)
            del gTest
            del gTest2
            del gTest3
            del gTest4
            del Temp
            Temp = MeasuredValue(0, SE1)
            gTest = Temp ** Value2 #raising (0, y) to a positive power
            gTest2 = self.Operation(Temp, Value2)
            Value3 = int(1 + Value2)
            gTest3 = Temp**Value3
            gTest4 = self.Operation(Temp, Value3)
            self.assertIsInstance(gTest, MeasuredValue)
            self.assertEqual(gTest.Value, 0)
            self.assertAlmostEqual(gTest.SE, pow(SE1, Value2),
                                                    places = self.Precision)
            self.assertIsInstance(gTest2, MeasuredValue)
            self.assertEqual(gTest2.Value, 0)
            self.assertAlmostEqual(gTest2.SE, pow(SE1, Value2),
                                                    places = self.Precision)
            self.assertIsInstance(gTest3, MeasuredValue)
            self.assertEqual(gTest3.Value, 0)
            self.assertAlmostEqual(gTest3.SE, pow(SE1, Value3),
                                                    places = self.Precision)
            self.assertIsInstance(gTest4, MeasuredValue)
            self.assertEqual(gTest4.Value, 0)
            self.assertAlmostEqual(gTest4.SE, pow(SE1, Value3),
                                                    places = self.Precision)
            del gTest
            del gTest2
            del gTest3
            del gTest4
            del Temp
        Temp = MeasuredValue(0, SE1)
        gTest = Temp ** 0 #raising to (0,y) measured into zero power!
        gTest2 = self.Operation(Temp, 0)
        gTest3 = Temp ** 0.0
        gTest4 = self.Operation(Temp, 0.0)
        self.assertIsInstance(gTest, MeasuredValue)
        self.assertEqual(gTest.Value, 1)
        self.assertEqual(gTest.SE, 0)
        self.assertIsInstance(gTest2, MeasuredValue)
        self.assertEqual(gTest2.Value, 1)
        self.assertEqual(gTest2.SE, 0)
        self.assertIsInstance(gTest3, MeasuredValue)
        self.assertEqual(gTest3.Value, 1)
        self.assertEqual(gTest3.SE, 0)
        self.assertIsInstance(gTest4, MeasuredValue)
        self.assertEqual(gTest4.Value, 1)
        self.assertEqual(gTest4.SE, 0)
        del gTest
        del gTest2
        del gTest3
        del gTest4
        del Temp
    
    def test_augmented(self):
        """
        Checks that the __ipow__() operation works as expected.

        REQ-FUN-102
        """
        #integer exponent
        for _ in range(1000):
            Value1 = random.uniform(-10, 10)
            if not Value1:
                continue
            SE1 = random.random() * 3
            Value2 = random.randrange(1, 5)
            Value = pow(Value1, Value2)
            SE = abs(pow(Value1, Value2 - 1)) * Value2 * SE1
            Temp = MeasuredValue(Value1, SE1)
            Temp **= Value2
            self.assertIsInstance(Temp, MeasuredValue)
            self.assertAlmostEqual(Temp.Value, Value, places = self.Precision)
            self.assertAlmostEqual(Temp.SE, SE, places = self.Precision)
            del Temp
            Temp = MeasuredValue(Value1, SE1)
            self.AugOperation(Temp, Value2)
            self.assertIsInstance(Temp, MeasuredValue)
            self.assertAlmostEqual(Temp.Value, Value, places = self.Precision)
            self.assertAlmostEqual(Temp.SE, SE, places = self.Precision)
            del Temp
            if not int(Value1):
                continue
            Value = pow(int(Value1), Value2)
            SE = abs(pow(int(Value1), Value2 - 1)) * Value2 * int(SE1)
            Temp = MeasuredValue(int(Value1), int(SE1))
            Temp **= Value2
            self.assertIsInstance(Temp, MeasuredValue)
            self.assertAlmostEqual(Temp.Value, Value, places = self.Precision)
            self.assertAlmostEqual(Temp.SE, SE, places = self.Precision)
            del Temp
            Temp = MeasuredValue(int(Value1), int(SE1))
            self.AugOperation(Temp, Value2)
            self.assertIsInstance(Temp, MeasuredValue)
            self.assertAlmostEqual(Temp.Value, Value, places = self.Precision)
            self.assertAlmostEqual(Temp.SE, SE, places = self.Precision)
            del Temp
        #float exponent
        Value1 = random.uniform(0.1, 10)
        SE1 = random.random() * 3
        for _ in range(1000):
            Value2 = random.uniform(-3.0, 3.0)
            Value = pow(Value1, Value2)
            SE = abs(pow(Value1, Value2 - 1)) * abs(Value2) * SE1
            Temp = MeasuredValue(Value1, SE1)
            Temp **= Value2
            self.assertIsInstance(Temp, MeasuredValue)
            self.assertAlmostEqual(Temp.Value, Value, places = self.Precision)
            self.assertAlmostEqual(Temp.SE, SE, places = self.Precision)
            del Temp
            Temp = MeasuredValue(Value1, SE1)
            self.AugOperation(Temp, Value2)
            self.assertIsInstance(Temp, MeasuredValue)
            self.assertAlmostEqual(Temp.Value, Value, places = self.Precision)
            self.assertAlmostEqual(Temp.SE, SE, places = self.Precision)
            del Temp
            if not int(Value1):
                continue
            Value = pow(int(Value1), Value2)
            SE = abs(pow(int(Value1), Value2 - 1)) * abs(Value2) * int(SE1)
            Temp = MeasuredValue(int(Value1), int(SE1))
            Temp **= Value2
            self.assertIsInstance(Temp, MeasuredValue)
            self.assertAlmostEqual(Temp.Value, Value, places = self.Precision)
            self.assertAlmostEqual(Temp.SE, SE, places = self.Precision)
            del Temp
            Temp = MeasuredValue(int(Value1), int(SE1))
            self.AugOperation(Temp, Value2)
            self.assertIsInstance(Temp, MeasuredValue)
            self.assertAlmostEqual(Temp.Value, Value, places = self.Precision)
            self.assertAlmostEqual(Temp.SE, SE, places = self.Precision)
            del Temp
        #special cases
        for _ in range(10):
            Value1 = random.uniform(-10, 10)
            SE1 = random.random()
            Value2 = random.uniform(0.1, 3.0)
            Temp = MeasuredValue(Value1, SE1)
            Temp **= 0
            self.assertIsInstance(Temp, MeasuredValue)
            self.assertEqual(Temp.Value, 1)
            self.assertEqual(Temp.SE, 0)
            del Temp
            Temp = MeasuredValue(Value1, SE1)
            self.AugOperation(Temp, 0)
            self.assertIsInstance(Temp, MeasuredValue)
            self.assertEqual(Temp.Value, 1)
            self.assertEqual(Temp.SE, 0)
            del Temp
            Temp = MeasuredValue(0, SE1)
            Temp **= Value2
            self.assertIsInstance(Temp, MeasuredValue)
            self.assertEqual(Temp.Value, 0)
            self.assertAlmostEqual(Temp.SE, pow(SE1, Value2),
                                                    places = self.Precision)
            del Temp
            Temp = MeasuredValue(0, SE1)
            self.AugOperation(Temp, Value2)
            self.assertIsInstance(Temp, MeasuredValue)
            self.assertEqual(Temp.Value, 0)
            self.assertAlmostEqual(Temp.SE, pow(SE1, Value2),
                                                    places = self.Precision)
            del Temp
    
    def test_reversed(self):
        """
        Checks that the __rpow__() operation works as expected.
        Not implemented - stub for the future possible extention of the
        functionality.

        REQ-FUN-102
        """
        for _ in range(1000):
            Value1 = random.randrange(1, 4) + random.random()
            SE2 = random.random()
            Value2 = random.randrange(1, 4) + random.random()
            Value = pow(Value1, Value2)
            SE = abs(Value * math.log(Value1)) * SE2
            Temp = MeasuredValue(Value2, SE2)
            gTest = Value1 ** Temp
            gTest2 = self.Operation(Value1, Temp)
            self.assertIsInstance(gTest, MeasuredValue)
            self.assertAlmostEqual(gTest.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest.SE, SE, places = self.Precision)
            self.assertIsInstance(gTest2, MeasuredValue)
            self.assertAlmostEqual(gTest2.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest2.SE, SE, places = self.Precision)
            del gTest
            del gTest2
            del Temp
            Value2 = - Value2
            Value = pow(Value1, Value2)
            SE = abs(Value * math.log(Value1)) * SE2
            Temp = MeasuredValue(Value2, SE2)
            gTest = Value1 ** Temp
            gTest2 = self.Operation(Value1, Temp)
            self.assertIsInstance(gTest, MeasuredValue)
            self.assertAlmostEqual(gTest.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest.SE, SE, places = self.Precision)
            self.assertIsInstance(gTest2, MeasuredValue)
            self.assertAlmostEqual(gTest2.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest2.SE, SE, places = self.Precision)
            del gTest
            del gTest2
            del Temp
            Value2 = int(Value2)
            Value = pow(Value1, Value2)
            SE = abs(Value * math.log(Value1)) * SE2
            Temp = MeasuredValue(Value2, SE2)
            gTest = Value1 ** Temp
            gTest2 = self.Operation(Value1, Temp)
            self.assertIsInstance(gTest, MeasuredValue)
            self.assertAlmostEqual(gTest.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest.SE, SE, places = self.Precision)
            self.assertIsInstance(gTest2, MeasuredValue)
            self.assertAlmostEqual(gTest2.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest2.SE, SE, places = self.Precision)
            del gTest
            del gTest2
            del Temp
            Value2 = - Value2
            Value = pow(Value1, Value2)
            SE = abs(Value * math.log(Value1)) * SE2
            Temp = MeasuredValue(Value2, SE2)
            gTest = Value1 ** Temp
            gTest2 = self.Operation(Value1, Temp)
            self.assertIsInstance(gTest, MeasuredValue)
            self.assertAlmostEqual(gTest.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest.SE, SE, places = self.Precision)
            self.assertIsInstance(gTest2, MeasuredValue)
            self.assertAlmostEqual(gTest2.Value, Value, places = self.Precision)
            self.assertAlmostEqual(gTest2.SE, SE, places = self.Precision)
            del gTest
            del gTest2
            del Temp

    def test_ValueError(self):
        """
        Tests that the operation raises ValueError if exponentiation operator
        receives inappropriate values of the proper type arguments.

        REQ-AWM-103
        """
        for _ in range(1000):
            Power = random.uniform(0.1, 0.9) + random.randrange(0, 3)
            #division by zero - direct and augmented - zero to negative power
            for Mean in [0, 0.0]:
                Temp = MeasuredValue(Mean, 0.1)
                with self.assertRaises(ValueError):
                    Test = Temp**(- random.randrange(1, 4))
                with self.assertRaises(ValueError):
                    Temp **= - random.randrange(1, 4)
                with self.assertRaises(ValueError):
                    self.Operation(Temp, - random.randrange(1, 4))
                with self.assertRaises(ValueError):
                    self.AugOperation(Temp, - random.randrange(1, 4))
                with self.assertRaises(ValueError):
                    Test = Temp**(-Power)
                with self.assertRaises(ValueError):
                    Temp **= - Power
                with self.assertRaises(ValueError):
                    Test = self.Operation(Temp, -Power)
                with self.assertRaises(ValueError):
                    self.AugOperation(Temp, -Power)
                with self.assertRaises(ValueError):
                    Test = Temp**MeasuredValue(-random.randrange(1, 4), 0.1)
                with self.assertRaises(ValueError):
                    Test = self.Operation(Temp,
                                MeasuredValue(-random.randrange(1, 4), 0.1))
                with self.assertRaises(ValueError):
                    Temp **= MeasuredValue(-random.randrange(1, 4), 0.1)
                with self.assertRaises(ValueError):
                    self.AugOperation(Temp,
                                MeasuredValue(-random.randrange(1, 4), 0.1))
                with self.assertRaises(ValueError):
                    Test = Temp**MeasuredValue(-random.uniform(0.1, 0.9), 0.1)
                with self.assertRaises(ValueError):
                    Test = self.Operation(Temp,
                                MeasuredValue(-random.uniform(0.1, 0.9), 0.1))
                with self.assertRaises(ValueError):
                    Temp **= MeasuredValue(-random.uniform(0.1, 0.9), 0.1)
                with self.assertRaises(ValueError):
                    self.AugOperation(Temp,
                                MeasuredValue(-random.uniform(0.1, 0.9), 0.1))
                del Temp
            #non-integer power with negative 'mean' of the base
            gMean = random.uniform(-10.0, -1.2)
            for Mean in [gMean, int(gMean)]:
                Temp = MeasuredValue(Mean, random.random())
                with self.assertRaises(ValueError):
                    Test = Temp**Power
                with self.assertRaises(ValueError):
                    Test = Temp**(-Power)
                with self.assertRaises(ValueError):
                    self.Operation(Temp, Power)
                with self.assertRaises(ValueError):
                    self.Operation(Temp, -Power)
                with self.assertRaises(ValueError):
                    self.AugOperation(Temp, Power)
                with self.assertRaises(ValueError):
                    self.AugOperation(Temp, -Power)
                TempExp = MeasuredValue(random.uniform(0.1, 0.9), 0.1)
                with self.assertRaises(ValueError):
                    Test = Temp**TempExp
                with self.assertRaises(ValueError):
                    Temp **= TempExp
                with self.assertRaises(ValueError):
                    self.Operation(Temp, TempExp)
                with self.assertRaises(ValueError):
                    self.AugOperation(Temp, TempExp)
                del TempExp
                TempExp = MeasuredValue(-random.uniform(0.1, 0.9), 0.1)
                with self.assertRaises(ValueError):
                    Test = Temp**TempExp
                with self.assertRaises(ValueError):
                    Temp **= TempExp
                with self.assertRaises(ValueError):
                    self.Operation(Temp, TempExp)
                with self.assertRaises(ValueError):
                    self.AugOperation(Temp, TempExp)
                del TempExp
                TempExp = MeasuredValue(random.randrange(1, 4), 0.1)
                with self.assertRaises(ValueError):
                    Test = Temp**TempExp
                with self.assertRaises(ValueError):
                    Temp **= TempExp
                with self.assertRaises(ValueError):
                    self.Operation(Temp, TempExp)
                with self.assertRaises(ValueError):
                    self.AugOperation(Temp, TempExp)
                del TempExp
                TempExp = MeasuredValue(-random.randrange(1, 4), 0.1)
                with self.assertRaises(ValueError):
                    Test = Temp**TempExp
                with self.assertRaises(ValueError):
                    Temp **= TempExp
                with self.assertRaises(ValueError):
                    self.Operation(Temp, TempExp)
                with self.assertRaises(ValueError):
                    self.AugOperation(Temp, TempExp)
                del TempExp
                del Temp
            #non-positive float or int base with uncertainty exponent
            gMean = random.uniform(1.2, 6.0)
            for Mean in [gMean, int(gMean), -gMean, -int(gMean)]:
                Temp = MeasuredValue(Mean, random.random())
                with self.assertRaises(ValueError):
                    Test = 0 ** Temp
                with self.assertRaises(ValueError):
                    Test = 0.0 ** Temp
                with self.assertRaises(ValueError):
                    self.Operation(0 , Temp)
                with self.assertRaises(ValueError):
                    self.Operation(0.0 , Temp)
                Value = -random.randrange(1, 4)
                with self.assertRaises(ValueError):
                    Test = Value ** Temp
                with self.assertRaises(ValueError):
                    self.Operation(Value , Temp)
                Value -= random.random()
                with self.assertRaises(ValueError):
                    Test = Value ** Temp
                with self.assertRaises(ValueError):
                    self.Operation(Value , Temp)
                del Temp

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_Init)
TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(Test_Add)
TestSuite3 = unittest.TestLoader().loadTestsFromTestCase(Test_Sub)
TestSuite4 = unittest.TestLoader().loadTestsFromTestCase(Test_Mul)
TestSuite5 = unittest.TestLoader().loadTestsFromTestCase(Test_Div)
TestSuite6 = unittest.TestLoader().loadTestsFromTestCase(Test_Pow)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2, TestSuite3, TestSuite4,
                    TestSuite5, TestSuite6])

if __name__ == "__main__":
    sys.stdout.write("Conducting phyqus_lib.base_classes module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)
