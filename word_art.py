from pathlib import PosixPath as Path

from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap
import numpy as np


FONT = 'comic.ttf'


def h_gradient(to_draw, width, height, *colors):
    n = len(colors)
    sub_height = height // (n - 1)
    for i, (color1, color2) in enumerate(zip(colors, colors[1:])):
        for j in range(sub_height):
            r = int(color1[0]*(1-j/sub_height) + color2[0]*j/sub_height)
            g = int(color1[1]*(1-j/sub_height) + color2[1]*j/sub_height)
            b = int(color1[2]*(1-j/sub_height) + color2[2]*j/sub_height)
            to_draw.line([(0, j+(i*sub_height)), (width, j+(i*sub_height))], fill=(r, g, b))


def box_size(text, font, max_text_length):
    boxed = wrap(text, max_text_length, break_long_words=False)
    size_x, size_y = 0, 0
    sizes = []
    for line in boxed:
        size = font.getsize(line)
        size_x = max(size_x, size[0])
        size_y += size[1]
        sizes.append(size)
    return size_x, size_y, sizes, boxed


def slant(numpy_image):
    t = numpy_image.transpose((1,0,2))
    f = (np.random.random_sample()-.5)*.3
    return np.array([np.concatenate((t[i,int(f*i):,:],t[i,:int(f*i),:])) for i in range(t.shape[0])]).transpose((1,0,2))


def add_shadow(numpy_image):
    shadow_pos = -np.random.randint(5, 10)
    out = np.concatenate([numpy_image[shadow_pos:], numpy_image[:shadow_pos]], axis=0)
    out = np.concatenate([out[:,shadow_pos:], out[:,:shadow_pos]], axis=1)
    out[:,:,:3] = 0
    out *= .5
    out *= numpy_image==0
    return out + numpy_image


def add_borders(numpy_image, x1=0, x2=0, y1=0, y2=0):
    out = numpy_image.transpose((1,0,2))
    if x1 > 0:
        out = np.concatenate([np.zeros([int(x1), *out.shape[1:]]), out], axis=0)
    if x2 > 0:
        out = np.concatenate([out, np.zeros([int(x2), *out.shape[1:]])], axis=0)
    if y1 > 0:
        out = np.concatenate([np.zeros([out.shape[0], int(y1), *out.shape[2:]]), out], axis=1)
    if y2 > 0:
        out = np.concatenate([out, np.zeros([out.shape[0], int(y2), *out.shape[2:]])], axis=1)
    return out.transpose((1,0,2))


def create_text_gradient(text, imgx, imgy, *colors):

    max_len_char = 6

    big_x = 1920
    big_y = 1080
    image_text = Image.new("RGBA", (big_x, big_y), (0, 0, 0, 0))
    draw_text = ImageDraw.Draw(image_text)

    size_x = float('inf')
    size_y = float('inf')
    font_size = 200
    max_len = max_len_char
    while (size_x > imgx or size_y > imgy) and font_size > 40:
        font = ImageFont.truetype(FONT, font_size)
        size_x, size_y, sizes, boxed = box_size(text, font, max_len)
        max_len += 1
        if max_len == 30:
            max_len = max_len_char
            font_size -= 4

    y = 0
    for line, size in zip(boxed, sizes):
        draw_text.text(((big_x - size[0]) // 2, ((big_y - size_y) // 2) + y), line, font=font, fill='white')
        y += size[1]

    pixs_image = np.array(image_text)
    white = np.sum(pixs_image, axis=2)
    pixs_image_crop = pixs_image[:,np.any(white!=0, axis=0),:]
    pixs_image_crop = pixs_image_crop[np.any(white != 0, axis=1),:,:]
    image_gradient = Image.new("RGBA", pixs_image_crop.shape[:2][::-1], (0, 0, 0, 0))
    draw_gradient = ImageDraw.Draw(image_gradient)
    h_gradient(draw_gradient, size_x, size_y, *colors)

    pixs_gradient = np.array(image_gradient)
    pixs_image_crop = (pixs_image_crop/255)*pixs_gradient

    pixs_image_crop = add_borders(pixs_image_crop, x1=10, x2=10, y1=pixs_image_crop.shape[0]*1.5, y2=pixs_image_crop.shape[0]*1.5)
    pixs_image_crop = slant(pixs_image_crop)
    pixs_image_crop = add_shadow(pixs_image_crop)
    pixs_image_crop = pixs_image_crop[np.any(np.sum(pixs_image_crop, axis=2) != 0, axis=1),:,:]

    image_crop = Image.fromarray(pixs_image_crop.astype(np.uint8))
    if pixs_image_crop.shape[1] > imgx:
        image_crop = image_crop.resize((imgx, size_y), Image.ANTIALIAS)
        size_x, size_y = image_crop.size
    if pixs_image_crop.shape[0] > imgy:
        image_crop = image_crop.resize((size_x, imgy), Image.ANTIALIAS)
        size_x, size_y = image_crop.size

    return image_crop


def resize_image_for_sticker(path: Path):
    img = Image.open(str(path))
    ratio = 512/max(img.size)
    new_size = (int(img.size[0]*ratio), int(img.size[1]*ratio))
    img = img.resize(new_size, Image.ANTIALIAS)
    result = path.with_suffix(".png")
    img.save(result, "png")
    return result


if __name__ == '__main__':
    width, height = 512, 512
    im = create_text_gradient('text in wordart', width, height, (255, 0, 255), (255, 255, 0))

    im.save('gradient.webp', method=6, quality=100)
