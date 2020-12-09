from .util import flatten, iconcat, rotation
from .yaml_io import read_yaml
from numpy import array as Vector
from types import SimpleNamespace
from typing import List, Tuple, Union

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
    'r': 0.0,
    'x': 0.0,
    'y': 0.0,
    'rotmat': rotation(0.0),
    'pos': Vector((0.0, 0.0)),
    'origin': Vector((0.0, 0.0)),
    'offset': Vector((0.0, 0.0)),
}
parser_state_keys:[dict] = parser_initial_state.keys()
parser_state_reset_keys:[str] = ['d', 'w', 'h', 'w2', 'h2', 'l', 'n', 'x', 'y']
parser_state_output_keys:[str] = ['p', 'w', 'h', 'w2', 'h2', 'l', 'n', 'r', 'x', 'y', 'r', 'rx', 'ry']

def parse_kle(fname:str) -> [dict]:
    return parse_kle_raw(read_yaml(fname))

def parse_kle_raw(layout:Union[Union[str,dict],str]) -> [dict]:
    parser_state:SimpleNamespace = SimpleNamespace(**parser_initial_state)

    # Flatten and parse the structure
    parsed_layout:[[dict]] = []
    for row in layout:
        parsed_layout_row:[dict] = []
        if type(row) == list:
            for cap in row:
                # Update parser state
                if type(cap) == dict:
                    # Update regular parser state
                    for cap_key in cap.keys():
                        if cap_key in parser_state_keys:
                            setattr(parser_state, cap_key, cap[cap_key])

                    # Update the positioning information
                    if 'rx' in cap:
                        parser_state.origin[0] = parser_state.rx
                    if 'ry' in cap:
                        parser_state.origin[1] = parser_state.ry
                    if 'x' in cap:
                        parser_state.offset[0] += parser_state.x
                    if 'y' in cap:
                        parser_state.offset[1] += parser_state.y
                    if 'r' in cap:
                        parser_state.rotmat = rotation(parser_state.r)

                elif type(cap) == str:
                    parser_state.offset[0] += 1.0
                    if not parser_state.d and not parser_state.g:
                        # Apply cap position
                        parser_state.pos = parser_state.origin + parser_state.rotmat @ parser_state.offset

                        # Duplicate the cap and apply name and position fields
                        parsed_cap:dict = copy_output_keys(parser_state, parser_state_output_keys)
                        parsed_cap['~raw-key'] = cap
                        parsed_cap['~key'] = sanitise_cap_name(cap)
                        parsed_cap['~pos'] = parser_state.pos
                        parsed_layout_row.append(parsed_cap)
                    # Reset parser state
                    for reset_key in parser_state_reset_keys:
                        setattr(parser_state, reset_key, parser_initial_state[reset_key])
            parsed_layout.append(parsed_layout_row)
            parser_state.offset[1] += 1.0

    return parsed_layout

def copy_output_keys(state:SimpleNamespace, output_keys:[str]) -> dict:
    return { k:v for k,v in state.__dict__.items() if k in output_keys }

def sanitise_cap_name(s:str) -> str:
    return s.replace('\n', '-')
