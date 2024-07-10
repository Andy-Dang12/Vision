from glob import iglob
import os, re
import os.path as osp
import xml.etree.ElementTree as ET


def coordinateCvt2YOLO(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]

    x = (box[0] + box[2]) / 2.0         # (xmin + xmax / 2)
    y = (box[1] + box[3]) / 2.0         # (ymin + ymax / 2)

    w = box[2] - box[0]                 # (xmax - xmin) = w
    h = box[3] - box[1]                 # (ymax - ymin) = h

    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (round(x, 5), round(y, 5), round(w, 5), round(h, 5))


def xml_to_text(xml_path:str, class_to_idx:dict, text_path:str):
    if not osp.isdir(text_path):
        os.makedirs(text_path)

    for xml in iglob(osp.join(xml_path, '*.xml')):
        root = ET.parse(xml).getroot()

        filename = root.find('filename').text
        filename = re.sub('.jpg$', '.txt', filename)
        width = int(root.find('size/width').text)
        height = int(root.find('size/height').text)

        f = open(osp.join(text_path, filename), 'w', encoding='utf-8')
        objects = root.findall('object')
        for obj in objects:
            class_name = obj.find('name').text
            bndbox = obj.find('bndbox')
            xmin = int(bndbox.find('xmin').text)
            ymin = int(bndbox.find('ymin').text)
            xmax = int(bndbox.find('xmax').text)
            ymax = int(bndbox.find('ymax').text)

            bb = coordinateCvt2YOLO((width, height), (xmin, ymin, xmax, ymax))
            bndbox = ''.join([''.join([str(e), ' ']) for e in bb])
            f.write(''.join((str(class_to_idx[class_name]), ' ', bndbox[:-1], '\n')))
        f.close()


xml_path = r'abs_path folder chứa file xml'
text_path = r'abs_path folder chứa file txt'

class_to_idx = {
    'classname_0': 0,
    'classname_1': 1,
    'classname_2': 2,
}

xml_to_text(xml_path, class_to_idx, text_path)
print('Successfully converted xml to txt.')
