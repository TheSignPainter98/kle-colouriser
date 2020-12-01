from .util import flatten, iconcat
from .yaml_io import read_yaml
from types import SimpleNamespace
from typing import Union

parser_initial_state:dict = {
    'p': 'R2',
    'd': False,
    'g': False,
    'h': 1.0,
    'w': 1.0,
    'h2': 1.0,
    'w2': 1.0,
    'l': False,
    'n': False,
}
parser_state_keys:[dict] = parser_initial_state.keys()
parser_state_reset_keys:[str] = ['d', 'w', 'h', 'w2', 'h2', 'l', 'n']
parser_state_output_keys:[str] = ['p', 'w', 'h', 'w2', 'h2', 'l', 'n']

def parse_kle(fname:str) -> [dict]:
    return parse_kle_raw(read_yaml(fname))

def parse_kle_raw(layout:Union[Union[str,dict],str]) -> [dict]:
    parser_state:SimpleNamespace = SimpleNamespace(**parser_initial_state)

    # Flatten and parse the structure
    parsed_layout:[dict] = []
    for cap in flatten(layout):
        # Update parser state
        if type(cap) == dict:
            for cap_key in cap.keys():
                if cap_key in parser_state_keys:
                    setattr(parser_state, cap_key, cap[cap_key])
        elif type(cap) == str:
            if not parser_state.d and not parser_state.g:
                parsed_cap:dict = copy_output_keys(parser_state, parser_state_output_keys)
                parsed_cap['key'] = cap
                parsed_layout.append(parsed_cap)

            # Reset parser state
            for reset_key in parser_state_reset_keys:
                setattr(parser_state, reset_key, parser_initial_state[reset_key])

    return parsed_layout

def copy_output_keys(state:SimpleNamespace, output_keys:[str]) -> dict:
    return { k:v for k,v in state.__dict__.items() if k in output_keys }
