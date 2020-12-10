from argparse import ArgumentError, ArgumentParser, Namespace
from .version import version_notice

def parse_args(args:[str]) -> Namespace:
    ap:ArgumentParser = ArgumentParser(prog=args[0], add_help=False)
    ap.add_argument('-f', '--output-format', metavar='format', type=str, choices=[ 'json', 'none', 'yaml' ], default='json', help='The format to use when writing output')
    ap.add_argument('-h', '--help', action='help', help='Show this help message and exit')
    ap.add_argument('-s', '--output-suffix', metavar='suffix', type=str, default='', help='A suffix to place before the file-extension when outputting')
    ap.add_argument('-v', '--verbosity', action='store', help="Set verbosity from 0 (least) to 2 (most), default is 0", type=int, default=0, choices=[0, 1, 2,])
    ap.add_argument('-V', '--version', dest='version', action='store_true', help='Show version and licensing information')

    ap.add_argument('colour_map', metavar='colour-map', type=str, help='The colour map to apply to the kle layouts')
    ap.add_argument('kle_in_dir', metavar='input-dir', type=str, help='The directory containing the kle files to process')
    ap.add_argument('output_dir', metavar='output-dir', type=str, help='The directory where the colourised layouts will be outputted')

    numMissingMandatoryPositionals:int = 3 - len(list(filter(lambda a: not a.startswith('-'), args[1:])))
    pseudo_args:[str] = args[1:] + [ None for _ in range(numMissingMandatoryPositionals) ]
    pargs:Namespace = ap.parse_args(pseudo_args)

    # Output version
    if pargs.version:
        print(version_notice)
        exit(0)

    # This dumb hacky way of printing out the error information is because the `exit_on_error=False` parameter of ArgumentParser *exits regardless* when a mandatory argument is omitted, instead of raising an exception
    if numMissingMandatoryPositionals > 0:
        ap.parse_args(args[1:])
        exit(1)


    return pargs
