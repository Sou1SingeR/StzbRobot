from PIL import Image


def images_concat(images, cols):
    assert len(images) % cols == 0
    col_interval = 100
    row_interval = 50
    width = 0
    height_max = 0
    for i in range(cols):
        width += images[i].size[0] + col_interval
        height_max = max(height_max, images[i].size[1])
    height = len(images) // cols * (height_max + row_interval)
    target = Image.new('RGB', (width, height))

    x = 0
    y = 0
    col = 1
    for img in images:
        target.paste(img, (x, y))
        if col < cols:
            col += 1
            x += img.size[0] + col_interval
        else:
            col = 1
            x = 0
            y += img.size[1] + row_interval
    return target


def image_concat(image_a, image_b):
    width, height = image_a.size
    width2, height2 = image_b.size
    assert(width == width2)

    target = Image.new('RGB', (width, height + height2))
    target.paste(image_a, (0, 0))
    target.paste(image_b, (0, height))

    return target
