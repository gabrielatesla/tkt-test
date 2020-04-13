from enum import Enum
from django.db import models
from rest_framework import serializers
from typing import Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Result:
    ca: int
    margin: int
    ebitda: int
    loss: int
    year: int

    def __init__(self, ca: int, margin: int, ebitda: int, loss: int, year: int) -> None:
        self.ca = ca
        self.margin = margin
        self.ebitda = ebitda
        self.loss = loss
        self.year = year

    @staticmethod
    def from_dict(obj: Any) -> 'Result':
        assert isinstance(obj, dict)
        ca = from_int(obj.get("ca"))
        margin = from_int(obj.get("margin"))
        ebitda = from_int(obj.get("ebitda"))
        loss = from_int(obj.get("loss"))
        year = from_int(obj.get("year"))
        return Result(ca, margin, ebitda, loss, year)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ca"] = from_int(self.ca)
        result["margin"] = from_int(self.margin)
        result["ebitda"] = from_int(self.ebitda)
        result["loss"] = from_int(self.loss)
        result["year"] = from_int(self.year)
        return result


class Sector(Enum):
    ELECTRONIC = "Electronic"
    ENERGY = "Energy"
    LUXURY = "Luxury"
    RETAIL = "Retail"
    SERVICES = "Services"


class CostumerModel(models.Model):
    name = models.CharField(max_length=200)
    sector = models.CharField(max_length=50)
    siren = models.IntegerField()
    results = models.TextField(null=True, blank=True)


class CostumerSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    sector = serializers.CharField(max_length=50)
    siren = serializers.IntegerField()
    results = serializers.CharField()


class CostumerElement(models.Model):
    name: str
    sector: Sector
    siren: int
    results: List[Result]

    def __init__(self, name: str, sector: Sector, siren: int, results: List[Result]) -> None:
        self.name = name
        self.sector = sector
        self.siren = siren
        self.results = results

    @staticmethod
    def from_dict(obj: Any) -> 'CostumerElement':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        sector = Sector(obj.get("sector"))
        siren = from_int(obj.get("siren"))
        results = from_list(Result.from_dict, obj.get("results"))
        return CostumerElement(name, sector, siren, results)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["sector"] = to_enum(Sector, self.sector)
        result["siren"] = from_int(self.siren)
        result["results"] = from_list(lambda x: to_class(Result, x), self.results)
        return result


def data_from_dict(s: Any) -> List[CostumerElement]:
    return from_list(CostumerElement.from_dict, s)


def data_to_dict(x: List[CostumerElement]) -> Any:
    return from_list(lambda x: to_class(CostumerElement, x), x)