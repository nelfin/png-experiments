# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "pypng",
# ]
# ///
"""
pngtext
~~~~~~~

Insert or extract a custom file into a PNG .iTXt chunk

Usage:

    pngtext graph.png < graphviz.dot
    pngtext -x application/graphviz graph.png | dot -Tsvg

"""

import argparse
import sys
import zlib
from functools import partial

import png

def info(tag, chunk):
    if tag in (b"tEXt", b"iTXt", b"zTXt"):
        mimetype = chunk[:chunk.find(b"\x00")].decode("latin-1")
        return tag, mimetype, len(chunk)

def info_all(tag, chunk):
    return tag, len(chunk)

def dump(tag, chunk, matching_tag=b'IDAT'):
    if tag == matching_tag:
        return chunk

def process(tag, chunk, target_mimetype="text/plain"):
    mimetype, idx = "", chunk.find(b"\x00")
    if tag == b"tEXt" or tag == b"iTXt":
        mimetype, data = chunk[:idx], chunk[idx+1:]
        mimetype = mimetype.decode("latin-1")
    if tag == b"zTXt":
        mimetype, method, zdata = chunk[:idx], chunk[idx+1], chunk[idx+2:]
        assert method == 0, f"Method {method} unknown (0=DEFLATE)"
        mimetype = mimetype.decode("latin-1")
        func = zlib.decompress
    if mimetype == target_mimetype:
        if tag == b"tEXt":
            return data.decode("latin-1")
        elif tag == b"iTXt":
            return data.decode("utf-8")
        elif tag == b"zTXt":
            return func(zdata).decode("latin-1")


parser = argparse.ArgumentParser()
parser.add_argument('image', type=argparse.FileType('rb'), help="PNG image")
parser.add_argument('text', type=argparse.FileType('rb'), nargs='?', default="-")
parser.add_argument('-x', '--extract', metavar="MIME", default='text/plain', help="Extract this mimetype")
parser.add_argument("-l", "--list", action="store_true", help="List all text chunks")
parser.add_argument("--list-all", action="store_true", help="List all chunks")
parser.add_argument("--extract-raw", help="Dump the bytes of this chunk")

args = parser.parse_args()

if args.list:
    func = info
elif args.list_all:
    func = info_all
elif args.extract_raw:
    func = partial(dump, matching_tag=args.extract_raw.encode("latin-1"))
else:
    func = partial(process, target_mimetype=args.extract)

# actually this is probably a waste of time, ref pngtools e.g. pngchunks(1) instead
# pngcrush can insert zTXt no problem, easy Python utils? What about PIL?

im = png.Reader(args.image)
for tag, data in im.chunks():
    if (result := func(tag, data)):
        if isinstance(result, bytes):
            sys.stdout.buffer.write(result)
        else:
            print(result)
