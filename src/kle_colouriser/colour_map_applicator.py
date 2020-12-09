from .colour_map_parser import ops
from functools import partial
from re import match
from typing import Callable, List, Tuple, Union

def apply_colour_map(printi:Callable, colour_map:List[dict], kle_input:Tuple[str, str, List[List[dict]]]) -> List[List[dict]]:
    context:dict = {
            'layout-file-name': kle_input[0],
        }
    for row in kle_input[2]:
        for cap in row:
            apply_colour_map_to_cap(context, colour_map, cap)
    return kle_input

def apply_colour_map_to_cap(context:dict, colour_map:List[dict], cap:dict) -> dict:
    for rule in colour_map:
        if rule_matches(context, cap, rule):
            cap['c'] = rule['cap-colour']
            cap['t'] = rule['glyph-style']
            cap['appled-colour-rule'] = rule['name']

def rule_matches(context, cap:dict, rule:dict) -> bool:
    return all(resolve_matches(context, cap, rule))

def resolve_matches(context:dict, cap:dict, rule:dict) -> [bool]:
    conds:[bool] = []

    # Resolve conditions at this level
    if 'key-name' in rule:
        key_name_regexes = rule['key-name'] if type(rule['key-name']) == list else [rule['key-name']]
        conds.append(any(map(lambda r: match('^%s$' % r, cap['~key']) is not None, key_name_regexes)))
    if 'key-pos' in rule:
        conds.append(eval_cond(cap, rule['key-pos']))
    if 'layout-file-name' in rule:
        conds.append(match('^%s$' % rule['layout-file-name'], context['layout-file-name']) is not None)

    # Resolve sub-conditions
    if 'any' in rule:
        conds.append(any(resolve_matches(context, cap, rule['any'])))
    if 'all' in rule:
        conds.append(all(resolve_matches(context, cap, rule['all'])))
    if 'not-all' in rule:
        conds.append(not all(resolve_matches(context, cap, rule['not-all'])))
    if 'not-any' in rule:
        conds.append(not any(resolve_matches(context, cap, rule['not-any'])))

    return conds

def eval_cond(cap:dict, pos_cond:Union[str, int, dict]) -> object:
    if type(pos_cond) == int:
        return pos_cond
    elif type(pos_cond) == str:
        return {
            'x': cap['~pos'][0],
            'y': cap['~pos'][1],
        }[pos_cond]
    elif type(pos_cond) == dict:
        eval_cap_cond:Callable = partial(eval_cond, cap)
        return pos_cond['op'](*tuple(map(eval_cap_cond, pos_cond['args'])))

