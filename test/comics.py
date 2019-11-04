import glob
from PIL import Image
import sys

failures = []

for filename in glob.glob('data/comics/chars/*'):
    try:
        i = Image.open(filename).convert("RGBA")
    except Exception as e:
        failures.append(filename)
        print(e)

for filename in glob.glob('data/comics/backgrounds/*'):
    try:
        i = Image.open(filename).convert("RGBA")
    except Exception as e:
        failures.append(filename)
        print(e)
        
if len(failures) > 0:
    print("Following images failed to open:\n{}".format("\n".join(failures)))
    sys.exit(1)
else:
    sys.exit(0)
