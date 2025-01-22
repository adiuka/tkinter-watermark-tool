import os, sys

print(im.size, im.width, im.height)
print(im.format, im.info)
print(im.mode)

# Converts for to jpeg
for infile in sys.argv[1:]: # Creates a list with command line arguments. We start at 1 because we do not need the name of the script with is indexed as [0]
    f, e = os.path.splittext(infile) # is an os function that splits a pathname into it's base name and extension (.jpeg for e.g.)
    outfile = f + '.jpg'
    if infile != outfile:
        try:
            with Image.open(infile) as im:
                im.save(outfile)
        except OSError:
            print("cannot convert", infile)

size = (1280, 1280)

for infile in sys.argv[1:]:
    outfile = os.path.splitext(infile)[0] + ".thumbnail"
    if infile != outfile:
        try:
            with Image.open(infile) as im:
                im.thumbnail(size)
                im.save(outfile, "JPEG")
        except OSError:
            print("cannot create thumbnail for", infile)

im.show()

im.save("Tkinter-build/created_images/audrius-new.bmp", "BMP") # Allows you to save an image in a new format.