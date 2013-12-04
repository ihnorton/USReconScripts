import re

def parse_mha_header(stream):
    spltr = re.compile("\W*=\W*")
    hdr = {}
    while True:
        line = stream.readline()
        a1,a2 = spltr.split(line.strip())
        hdr[a1] = a2
        if (line.startswith("ElementDataFile = LOCAL")):
            break
    return hdr
