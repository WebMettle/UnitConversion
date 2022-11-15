#
# Copyright (c) 2022 by Salvatore Saieva.
#

class UnitConversion(object):

    def __init__(self):
        self.__Facts = []
        self.addFact(["m", 3.28, "ft"])
        self.addFact(["ft", 12, "in"])
        self.addFact(["hr", 60, "min"])
        self.addFact(["min", 60, "sec"])

    def addFact(self, fact):
        self.Facts.append(fact)

    @property
    def Facts(self):
        return self.__Facts

    @property
    def InverseFacts(self):
        return [ [fact[2], 1/fact[1], fact[0]] for fact in self.Facts ]

    def getFact(self, facts, queryUnit):
        fact = [ fact for fact in facts if fact[0] == queryUnit ]
        return fact[0] if self._isDefined(fact) else []

    def _isDefined(self, fact):
        return len(fact) > 0

    def _isNotDefined(self, fact):
        return len(fact) == 0

    def convert(self, query):
        conversionResult = self._computeConversion(self.Facts, query)
        if conversionResult is None:
            conversionResult = self._computeConversion(self.InverseFacts, query)
        return "not convertible!" if conversionResult is None else conversionResult

    def _computeConversion(self, facts, query):
        queryValue = query[0]
        queryUnit = query[1]
        conversionUnit = query[2]
        conversionValue = None

        if queryUnit == conversionUnit:
            return [queryValue, conversionUnit]

        fact = self.getFact(facts, queryUnit)
        if self._isNotDefined(fact):
            return conversionValue
        value = fact[1]
        unit = fact[2]

        conversionValue = self._computeConversion(facts, [queryValue * value, unit, conversionUnit ])

        return conversionValue
