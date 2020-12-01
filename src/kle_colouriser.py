#!/usr/bin/env python3

from json import dumps as jdump
from kle_colouriser.args import parse_args, Namespace
from kle_colouriser.colour_map_parser import parse_colour_map
from kle_colouriser.parse_kle import parse_kle
from kle_colouriser.path import get_json_and_yaml_files
from os import mkdir
from os.path import basename, exists, join, splitext
from sys import argv, exit
from yaml import dump as ydump

def main(args:[str]) -> int:
    pargs:SimpleNamespace = parse_args(args)

    # Parse colour-map file
    colour_map:[dict] = parse_colour_map(pargs.colour_map)

    # Get and parse KLE inputs
    kle_input_names:[str] = get_json_and_yaml_files(pargs.kle_in_dir)
    kle_inputs:List[Tuple[str, str, List[dict]]] = list(map(lambda f: (splitext(basename(f))[0], f, parse_kle(f)), kle_input_names))

    # Apply colour-map rules
    colour_mapped_data:List[Tuple[str, str, List[dict]]] = kle_inputs

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
            oname:str = join(pargs.output_dir, n + output_formatter[pargs.output_format][0])
            with open(oname, 'w+') as f:
                print(output_formatter[pargs.output_format][1](d), file=f)

    return 0

if __name__ == '__main__':
    exit(main(argv))
