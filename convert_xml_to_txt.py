import glob
import os
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


def xml_to_text(xml_path, class_id_dict, text_path):
    box = [0, 0, 0, 0]
    size = [0, 0]
    for xml_file in glob.glob(xml_path + '{}*.xml'.format(os.sep)):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        file_name = root.find('filename').text
        file_name = file_name.replace(".jpg", ".txt")

        if not os.path.exists(text_path):
            os.makedirs(text_path)
        f = open(os.path.join(text_path, file_name), "w", encoding="utf-8")
        
        for member in root.findall('object'):
            size[0] = int(root.find('size')[0].text)
            size[1] = int(root.find('size')[1].text)
            c = member[0].text
            box[0] = int(member[4][0].text)  # xmin
            box[1] = int(member[4][1].text)  # ymin
            box[2] = int(member[4][2].text)  # xmax
            box[3] = int(member[4][3].text)  # ymax

            bb = coordinateCvt2YOLO(size, box)
            bndbox = "".join(["".join([str(e), " "]) for e in bb])
            contents = "".join([str(class_id_dict[c]), " ", bndbox[:-1], "\n"])
            f.write(contents)



xml_path = r"/home/scratch/Documents/philippines/datasets/data_step3/data_tr"                      # sửa folder chứa file xml
text_path = r"/home/scratch/Documents/philippines/datasets/data_step3/datadata"                        # sửa folder chứa file txt

class_id_dict = {
    'surname': 0,
    'givenname': 1,
    'middlename': 2,
    'birth': 3,
    'ID': 4,
    'sex': 5,
    'home': 6,
    }

xml_to_text(xml_path, class_id_dict, text_path)
print('Successfully converted xml to csv.')
