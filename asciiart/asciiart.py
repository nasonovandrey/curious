import numpy as np
from PIL import Image
from fire import Fire

default_gscale="$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`. "


def asciify(filename, columns=60, gscale=default_gscale, save='NO', savepath='asciiart.txt'):
    image = Image.open(filename).convert('L')
    width, height = image.size[0], image.size[1]
    rows = int(columns*height/width)
    image = image.resize((columns, rows), Image.ANTIALIAS)
    imarr = np.asarray(image)
    average = np.average(imarr)
    imascii = np.array(list(map(lambda row : [gscale[int(x*(len(gscale)-1)/255)] for x in row],imarr)))

    accstr = ''
    for row in imascii:
        for sym in row:
            accstr += sym
        accstr += '\n'
    print(accstr)

    if save.upper() in ('Y','YES'):
        with open(savepath,'w') as f:
            np.savetxt(f, imascii, delimiter='', fmt='%s')

if __name__=='__main__':
    Fire(asciify)
