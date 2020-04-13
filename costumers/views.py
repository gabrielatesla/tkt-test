from costumers.models import CostumerElement, Result, CostumerModel, CostumerSerializer
import json
from django import db


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_list(f, x):
    assert isinstance(x, list)
    return [f(y) for y in x]


class Costumers:

    @staticmethod
    def save(obj):
        try:
            CostumerModel.objects.get_or_create(
                name=obj.get("name"),
                sector=obj.get("sector"),
                siren=obj.get("siren"),
                results=json.dumps(obj.get("results"))
            )

        except Exception as e:
            raise e
