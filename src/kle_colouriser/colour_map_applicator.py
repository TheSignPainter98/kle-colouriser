from .colour_map_parser import ops
from functools import partial
from re import match
from typing import Callable, List, Tuple, Union

def apply_colour_map(printi:Callable, colour_map:List[dict], kle_input:Tuple[str, str, List[List[dict]]]) -> List[List[dict]]:
    context:dict = {
            'short-layout-file-name': kle_input[0],
            'layout-file-name': kle_input[1],
            'printi': printi
        }
    for row in kle_input[2]:
        for cap in row:
            apply_colour_map_to_cap(context, colour_map, cap)
    return kle_input

def apply_colour_map_to_cap(context:dict, colour_map:List[dict], cap:dict) -> dict:
    for rule in colour_map:
        context['printi']('Testing cap "%s" against rule "%s"...' %(cap['~key'], rule['name']))
        if rule_matches(context, cap, rule):
            context['printi']('Cap "%s" matches rule "%s"...' %(cap['~key'], rule['name']))
            cap['c'] = rule['cap-colour']
            cap['t'] = rule['glyph-style']
            cap['appled-colour-rule'] = rule['name']
            return cap

def rule_matches(context, cap:dict, rule:dict) -> bool:
    return all(resolve_matches(context, cap, rule))

def resolve_matches(context:dict, cap:dict, rule:dict) -> [bool]:
    printi:Callable = context['printi']
    printi_name:Callable = partial(printi, '%s:' % context['short-layout-file-name'])
    conds:[bool] = []

    # Resolve conditions at this level
    if 'key-name' in rule:
        printi_name('Checking key name "%s" entirely matches any of' % cap['~key'], end=' ')
        key_name_regexes = rule['key-name'] if type(rule['key-name']) == list else [rule['key-name']]
        printi('[ %s ]...' % ', '.join(list(map(lambda r: '"%s"' % r, key_name_regexes))), end=' ')
        cond_result:bool = any(map(lambda r: match('^%s$' % r, cap['~key']) is not None, key_name_regexes))
        printi('%r' % cond_result)
        conds.append(cond_result)
    if 'parsed-key-pos' in rule:
        printi_name('Checking key position (%.4fu,%.4fu) satisfies condition "%s"...' % (cap['~pos'][0], cap['~pos'][1], rule['key-pos']), end=' ')
        cond_result:bool = eval_maths_cond(cap, rule['parsed-key-pos'])
        printi('%r' % cond_result)
        conds.append(cond_result)
    if 'layout-file-name' in rule:
        printi_name('Checking "%s" entirely matches "%s"...' % (context['layout-file-name'], rule['layout-file-name']), end=' ')
        cond_result:bool = match('^%s$' % rule['layout-file-name'], context['layout-file-name']) is not None
        printi('%r' % cond_result)
        conds.append(cond_result)

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

def eval_maths_cond(cap:dict, pos_cond:Union[str, int, dict]) -> object:
    if type(pos_cond) == int:
        return pos_cond
    elif type(pos_cond) == str:
        return {
            'x': cap['~pos'][0],
            'y': cap['~pos'][1],
        }[pos_cond]
    elif type(pos_cond) == dict:
        eval_cap_cond:Callable = partial(eval_maths_cond, cap)
        return pos_cond['op'](*tuple(map(eval_cap_cond, pos_cond['args'])))

