from argparse import ArgumentParser, Namespace

def parse_args(args:[str]) -> Namespace:
    ap:ArgumentParser = ArgumentParser(add_help=False)
    ap.add_argument('-h', '--help', action='help', help='Show this help message and exit')
    ap.add_argument('-v', '--verbosity', action='store', help="Set verbosity from 0 (least) to 2 (most), default is 0", type=int, default=0, choices=[0, 1, 2,])
    ap.add_argument('colour_map', metavar='colour-map', type=str, help='The colour map to apply to the kle layouts')
    ap.add_argument('kle_in_dir', metavar='input-dir', type=str, help='The directory containing the kle files to process')
    ap.add_argument('output_dir', metavar='input-dir', type=str, help='The directory where the colourised layouts will be outputted')
    ap.add_argument('-f', '--output-format', metavar='format', type=str, choices=[ 'json', 'none', 'yaml' ], default='json', help='The format to use when writing output')
    ap.add_argument('-s', '--output-suffix', metavar='suffix', type=str, default='', help='A suffix to place before the file-extension when outputting')

    return ap.parse_args()
