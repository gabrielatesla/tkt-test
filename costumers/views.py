from costumers.models import CostumerElement, Result, CostumerModel


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
            results = from_union([lambda x: from_list(Result.from_dict, x)], obj.get("results"))
            costumer = CostumerModel(
                name=obj.get("name"),
                sector=obj.get("sector"),
                siren=obj.get("siren"),
                results=results
            )
            costumer.save()
        except Exception as e:
            raise e
