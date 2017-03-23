#!/usr/bin/env python3
import shutil
import os
import sys
import argparse
import subprocess

parser = argparse.ArgumentParser(description='update-website')
parser.add_argument('built_doc')

args = parser.parse_args()

if not os.path.isdir(args.built_doc):
    print("%s is not a dir" % args.built_doc)
    sys.exit(1)
elif not os.path.isfile(os.path.join(args.built_doc, 'index.html')):
    print("%s does not exist" % os.path.join(args.built_doc, 'index.html'))
    sys.exit(1)

SDIR = os.path.dirname(os.path.realpath(__file__))
for f in os.listdir(args.built_doc):
    ldir = os.path.join(SDIR, f)
    ndir = os.path.join(args.built_doc, f)
    if os.path.isdir(ndir) and f == '.git':
        continue

    if os.path.isdir(ldir):
        shutil.rmtree(ldir)

    print("Copying %s" % f)
    if os.path.isdir(ndir):
        shutil.copytree(ndir, ldir, symlinks=True)
    else:
        shutil.copy(ndir, ldir)

subprocess.check_output(['git', 'add', '*'])
print("Cached changes stats:")
subprocess.check_output(['git', 'diff', '--cached', '--stat'])
