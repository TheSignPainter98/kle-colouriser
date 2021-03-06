from os.path import exists
from re import Match, search
from sys import exit, stderr
from yaml import safe_load


##
# @brief Read yaml from a given file or '-' for stdin. Exits on error
#
# @param fname:str Name of the file to use
#
# @return The data present in file fname
def read_yaml(fname: str) -> dict:
    yaml_lines:[str]
    if exists(fname):
        with open(fname, 'r', encoding='utf-8') as f:
            yaml_lines = f.read().split('\n')
    else:
        print('Couldn\'t find or read file "%s"' % fname, file=stderr)
        exit(1)
    sanitised_yaml_string:str = '\n'.join(list(map(sanitise_yaml_line, yaml_lines)))
    return safe_load(sanitised_yaml_string)


def sanitise_yaml_line(line:str) -> str:
    m:Match = search(r'^\t+', line)
    if m is not None:
        span:tuple = m.span()
        num_tabs:int = span[1] - span[0]
        return '  ' * num_tabs + line[num_tabs:]
    else:
        return line


##
# @brief Write a dictionary to a given file, or '-' for stdout
#
# @param fname:str Name of file to write data into or '-' for stdout
# @param data:dict Data to write
#
# @return Nothing
def write_yaml(fname: str, data: dict):
    if fname == '-':
        print(dump(data), end='')
    else:
        with open(fname, 'w+', encoding='utf-8') as f:
            print(dump(data), file=f, end='')
