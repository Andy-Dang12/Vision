import os
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET
from os.path import basename, join

import cv2
import numpy as np


def write_xml(img:np.ndarray, abspath:str, folder_save:str, boxes:list) -> None:
    r''' 
        img           opencv
        abspath       đường dẫn đầy đủ của ảnh
        folder_save   là folder để save file xml
        list result   là list các box theo thứ tự xmin, ymin, xmax, ymax, class_name
    '''
    imgname = basename(abspath)
    
    annotation = ET.Element("annotation")
    # ET.SubElement(annotation, "folder").text = basename(folder_save)
    ET.SubElement(annotation, "filename").text = imgname
    
    #NOTE <source>
    # source = ET.SubElement(annotation, "source")
    # ET.SubElement(source, "database").text= "The VOC2007 Database"
    # ET.SubElement(source, "annotation").text= "PASCAL VOC2007"
    # ET.SubElement(source, "image").text= "flickr"
    
    #NOTE <size>
    # size = ET.SubElement(annotation, "size")
    # hei, wid, ch = img.shape
    # ET.SubElement(size, "width").text = str(wid)
    # ET.SubElement(size, "height").text = str(hei)
    # ET.SubElement(size, "depth").text = str(ch)
    
    #NOTE <segmented>
    # ET.SubElement(annotation, "segmented").text = "0"

    for box in boxes:
        obj = ET.SubElement(annotation, "object")
        ET.SubElement(obj, "name").text = str(box[4]).strip()
        
        #NOTE <actions>
        # actions = ET.SubElement(obj, "actions")
        # ET.SubElement(actions, "jumping").text = '0'
        # ET.SubElement(actions, "other").text = '0'
        # ET.SubElement(actions, "phoning").text = '1'
        # ET.SubElement(actions, "playinginstrument").text = '0'
        # ET.SubElement(actions, "reading").text = '0'
        # ET.SubElement(actions, "ridingbike").text = '0'
        # ET.SubElement(actions, "ridinghorse").text = '0'
        # ET.SubElement(actions, "running").text = '0'
        # ET.SubElement(actions, "takingphoto").text = '0'
        # ET.SubElement(actions, "usingcomputer").text = '0'
        # ET.SubElement(actions, "walking").text = '1'

        # ET.SubElement(obj, "truncated").text = "0"
        # ET.SubElement(obj, "difficult").text = "0"
        # ET.SubElement(obj, "pose").text = "Unspecified"
        #NOTE <point>
        point = ET.SubElement(obj, "point")
        ET.SubElement(point, "x").text = '260'  # example
        ET.SubElement(point, "y").text = '135'  # example

        
        #NOTE <bndbox>
        bndbox = ET.SubElement(obj, "bndbox")
        ET.SubElement(bndbox, "xmin").text = str(box[0]).strip()
        ET.SubElement(bndbox, "ymin").text = str(box[1]).strip()
        ET.SubElement(bndbox, "xmax").text = str(box[2]).strip()
        ET.SubElement(bndbox, "ymax").text = str(box[3]).strip()
    
    abspath_xml = join(folder_save, basename.split(".")[0] + ".xml")
    # tree = ET.ElementTree(annotation)
    # ET.indent(tree, space="\t", level=0)
    # tree.write(name_xml)
    dom = minidom.parseString(ET.tostring(annotation))
    xmlstr = dom.toprettyxml(indent='\t')
    
    # remove <?xml version="1.0" ?>
    xmlstr = '\n'.join(xmlstr.splitlines()[1:])
    with open(abspath_xml, 'w') as f:
        f.write(xmlstr)


def read(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    folder = root.find('folder').text
    file_name= root.find('filename').text
    path = root.find('path').text

    source = root.find('source')
    database = source[0].text

    size = root.find('size')
    width = int(size[0].text)
    height = int(size[1].text)
    depth = int(size[0].text)

    segmented = root.find('segmented').text

    objects = root.findall('object')
    for obj in objects:
        name = obj[0].text
        pose = obj[1].text
        truncated = obj[2].text
        difficult = objects
    # print(source.text)
    obj = root.findall('object')
    class_name =[]
    # for name in obj:
    #     a = name[0].text
    return None


def get_bndbox(xml_path) -> list:
    root = ET.parse(xml_path).getroot()

    list_box = []
    for obj in root.findall('object'):

        class_name = obj.find('name').text
        
        bndbox = obj.find('bndbox')
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)
        box = (xmin, ymin, xmax, ymax, class_name)
        list_box.append(box)
    return list_box


if __name__ == '__main__':
    bndbox = get_bndbox('data/2012_0001.xml')
    print(bndbox)
