#!/usr/bin/env python3

from functools import partial
from json import dumps as jdump
from kle_colouriser.args import parse_args, Namespace
from kle_colouriser.colour_map_applicator import apply_colour_map
from kle_colouriser.colour_map_parser import parse_colour_map
from kle_colouriser.parse_kle import parse_kle
from kle_colouriser.path import get_json_and_yaml_files
from os import mkdir
from os.path import basename, exists, join, splitext
from sys import argv, exit
from typing import Callable, List, Tuple, Union
from yaml import dump as ydump

printi:Callable = None

def main(args:[str]) -> int:
    global printi
    pargs:SimpleNamespace = parse_args(args)
    printi = partial(cond_print, pargs.quiet)

    # Parse colour-map file
    colour_map:[dict] = parse_colour_map(pargs.colour_map)

    # Get and parse KLE inputs
    printi('Getting input files from directory "%s"...' % pargs.kle_in_dir)
    kle_input_names:[str] = get_json_and_yaml_files(pargs.kle_in_dir)
    kle_inputs:List[Tuple[str, str, List[dict]]] = list(map(lambda f: (splitext(basename(f))[0], f, parse_kle(f)), kle_input_names))

    # Apply colour-map rules
    apply_inputted_colour_map:Callable = partial(apply_colour_map, printi, colour_map)
    #  colour_mapped_data:List[Tuple[str, str, List[dict]]] = list(map(apply_inputted_colour_map, kle_inputs))
    colour_mapped_data:List[Tuple[str, str, List[dict]]] = []
    for kle_input in kle_inputs:
        printi('Applying colour map to "%s"...' % kle_input[0])
        colour_mapped_data.append(apply_inputted_colour_map(kle_input))

    # Sanitise before output
    remove_private_data(colour_mapped_data)

    # Output
    if pargs.output_format != 'none':
        # Ensure output directory actually exists
        if not exists(pargs.output_dir):
            mkdir(pargs.output_dir)

        # File extensions and data-formatters
        output_formatter:dict = {
                'none': (None, lambda _: ''),
                'json': ('.json', jdump),
                'yaml': ('.yaml', ydump),
            }

        # Iterate over results, writing them
        for n,_,d in colour_mapped_data:
            oname:str = join(pargs.output_dir, n + pargs.output_suffix + output_formatter[pargs.output_format][0])
            printi('Writing output "%s"' % oname)
            with open(oname, 'w+') as f:
                print(output_formatter[pargs.output_format][1](d), file=f)

    printi('All done.')

    return 0

def remove_private_data(data:Union[dict, list]) -> Union[dict,list]:
    if type(data) == dict:
        keys_to_remove:[str] = list(filter(lambda k: type(k) == str and k.startswith('~'), data.keys()))
        for rkey in keys_to_remove:
            del data[rkey]
        for key in data.keys():
            data[key] = remove_private_data(data[key])
    elif type(data) in [list, tuple]:
        data = list(map(remove_private_data, data))
    return data

def cond_print(q:bool, *args, **kwargs):
    if not q:
        print(*args, **kwargs)

if __name__ == '__main__':
    exit(main(argv))
