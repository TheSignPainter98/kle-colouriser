from os import walk as owalk
from os.path import exists, join, splitext
from sys import stderr

def get_json_and_yaml_files(directory:str) -> [str]:
    if not exists(directory):
        print('Could not find directory "%s"' % directory, file=stderr)
        exit(-1)
    return list(filter(lambda f: splitext(f)[1].lower() in ['.yml', '.yaml', '.json'], walk(directory)))

def walk(dname:str) -> [str]:
    ret:[str] = []
    for (r,_,fs) in owalk(dname):
        ret.extend(map(lambda f: join(r,f), fs))
    return ret
