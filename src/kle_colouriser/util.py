from functools import reduce

def dict_union(*ds:[dict]) -> dict:
    def _dict_union(a:dict, b:dict) -> dict:
        return dict(a, **b)
    return dict(reduce(_dict_union, ds, {}))

def flatten(obj:object) -> [object]:
    if type(obj) == list:
        return reduce(iconcat, map(flatten, obj), [])
    else:
        return [obj]

def iconcat(a:list, b:list) -> list:
    a.extend(b)
    return a

