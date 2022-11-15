#
# Copyright (c) 2022 by Salvatore Saieva.
#

import unittest
import UnitConversion

class UnitConversionTest(unittest.TestCase):

    def test_whenInstantiated_factsAreLoaded(self):
        uc = UnitConversion.UnitConversion()
        self.assertGreater(len(uc.Facts), 0)
        self.assertGreater(len(uc.InverseFacts), 0)

    def test_whenGetFactIsCalled_correctTupleIsReturned(self):
        uc = UnitConversion.UnitConversion()
        self.assertListEqual(uc.getFact(uc.Facts, "m"), ["m", 3.28, "ft" ])
        self.assertListEqual(uc.getFact(uc.Facts, "ft"), ["ft", 12, "in" ])
        self.assertListEqual(uc.getFact(uc.Facts, "hr"), ["hr", 60, "min" ])
        self.assertListEqual(uc.getFact(uc.Facts, "min"), ["min", 60, "sec" ])

    def test_whenGetFactIsCalledForInverseFacts_correctTupleIsReturned(self):
        uc = UnitConversion.UnitConversion()
        self.assertListEqual(uc.getFact(uc.InverseFacts, "in"), ["in", 1/12, "ft" ])
        self.assertListEqual(uc.getFact(uc.InverseFacts, "ft"), ["ft", 1/3.28, "m" ])
        self.assertListEqual(uc.getFact(uc.InverseFacts, "sec"), ["sec", 1/60, "min" ])
        self.assertListEqual(uc.getFact(uc.InverseFacts, "min"), ["min", 1/60, "hr" ])

    def test_whenFactIsMissing_getFactReturnsAnEmptyTuple(self):
        uc = UnitConversion.UnitConversion()
        self.assertListEqual(uc.getFact(uc.Facts, "in"), [])
        self.assertListEqual(uc.getFact(uc.Facts, "sec"), [])

    def test_whenInverseFactIsMissing_getFactsReturnsAnEmptyTuple(self):
        uc = UnitConversion.UnitConversion()
        self.assertListEqual(uc.getFact(uc.InverseFacts, "m"), [])
        self.assertListEqual(uc.getFact(uc.InverseFacts, "hr"), [])

    def test_whenQueryUnitsAndConversionUnitsAreEqual_correctConversionTupleIsReturned(self):
        uc = UnitConversion.UnitConversion()
        self.assertListEqual(uc.convert([1, "m", "m"]), [1, "m"])
        self.assertListEqual(uc.convert([10, "ft", "ft"]), [10, "ft"])
        self.assertListEqual(uc.convert([20, "min", "min"]), [20, "min"])

        self.assertListEqual(uc.convert([1, "hr", "hr"]), [1, "hr"])
        self.assertListEqual(uc.convert([10, "min", "min"]), [10, "min"])
        self.assertListEqual(uc.convert([20, "sec", "sec"]), [20, "sec"])

    def test_whenConvertingDirectlyFromFacts_correctConversionTupleIsReturned(self):
        uc = UnitConversion.UnitConversion()
        self.assertListEqual(uc.convert([1, "m", "ft"]), [3.28, "ft"])
        self.assertListEqual(uc.convert([1, "ft", "in"]), [12, "in"])
        self.assertListEqual(uc.convert([1, "hr", "min"]), [60, "min"])
        self.assertListEqual(uc.convert([1, "min", "sec"]), [60, "sec"])

        self.assertListEqual(uc.convert([10, "m", "ft"]), [32.8, "ft"])
        self.assertListEqual(uc.convert([10, "ft", "in"]), [120, "in"])
        self.assertListEqual(uc.convert([10, "hr", "min"]), [600, "min"])
        self.assertListEqual(uc.convert([10, "min", "sec"]), [600, "sec"])

    def test_whenConvertingDirectlyFromInverseFacts_correctConversionTupleIsReturned(self):
        uc = UnitConversion.UnitConversion()
        self.assertListEqual(uc.convert([12, "in", "ft"]), [1, "ft"])

        returnTuple = uc.convert([3.28, "ft", "m"])
        self.assertAlmostEqual(returnTuple[0], 1)
        self.assertEqual(returnTuple[1], "m")

        self.assertListEqual(uc.convert([60, "sec", "min"]), [1, "min"])
        self.assertListEqual(uc.convert([60, "min", "hr"]), [1, "hr"])

        self.assertListEqual(uc.convert([120, "in", "ft"]), [10, "ft"])
        returnTuple = uc.convert([32.8, "ft", "m"])
        self.assertAlmostEqual(returnTuple[0], 10)
        self.assertEqual(returnTuple[1], "m")

        self.assertListEqual(uc.convert([600, "sec", "min"]), [10, "min"])
        self.assertListEqual(uc.convert([600, "min", "hr"]), [10, "hr"])

    def test_whenConvertingIndirectlyFromFacts_correctConversionTupleIsReturned(self):
        uc = UnitConversion.UnitConversion()
        self.assertListEqual(uc.convert([1, "m", "in"]), [3.28 * 12, "in"])
        self.assertListEqual(uc.convert([100, "m", "in"]), [100 * 3.28 * 12, "in"])
        self.assertListEqual(uc.convert([1, "hr", "sec"]), [60 * 60, "sec"])
        self.assertListEqual(uc.convert([100, "hr", "sec"]), [100 *60 * 60, "sec"])

    def test_whenConvertingIndirectlyFromInverseFacts_correctConversionTupleIsReturned(self):
        uc = UnitConversion.UnitConversion()
        returnTuple = uc.convert([10 * 12 * 3.28, "in", "m"])
        self.assertAlmostEqual(returnTuple[0], 10)
        self.assertEqual(returnTuple[1], "m")
        
        self.assertListEqual(uc.convert([10 * 60 * 60, "sec", "hr"]), [10, "hr"])

    def test_whenUnitsAreNotConvertible_correctMessageIsReturned(self):
        uc = UnitConversion.UnitConversion()
        for timeUnit in ["hr", "min", "sed"]:
            for lengthUnit in ["m", "ft", "in"]:
                self.assertEqual(uc.convert([1, timeUnit, lengthUnit]), "not convertible!")
                self.assertEqual(uc.convert([1, lengthUnit, timeUnit]), "not convertible!")

    def test_whenFactIsNotDefined_correctMessageIsReturned(self):
        uc = UnitConversion.UnitConversion()
        self.assertEqual(uc.convert([1, "no-unit", "in"]), "not convertible!")
        self.assertEqual(uc.convert([1, "m", "no-unit"]), "not convertible!")

if __name__ == '__main__':
    unittest.main()
