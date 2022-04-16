import os, glob, shutil
import xml.etree.ElementTree as ET
import cv2

    
def save_file_xml(img, link, path, list_result):
    ''' 
    img           opencv
    link          đường dẫn đầy đủ của ảnh
    path          là folder để save
    list_result   là list các box theo thứ tự xmin, ymin, xmax, ymax            '''
    
    annotation = ET.Element("annotation")
    ET.SubElement(annotation, "folder").text = "data_form"
    ET.SubElement(annotation, "filename").text = os.path.basename(link)
    ET.SubElement(annotation, "path").text = link
    source = ET.SubElement(annotation, "source")
    ET.SubElement(source, "database").text= "Unknown"
    size = ET.SubElement(annotation, "size")
    ET.SubElement(size, "width").text = str(img.shape[1])
    ET.SubElement(size, "height").text = str(img.shape[0])
    ET.SubElement(size, "depth").text = str(img.shape[2])
    ET.SubElement(annotation, "segmented").text = "0"

    for result in list_result:
        object = ET.SubElement(annotation, "object")
        ET.SubElement(object, "name").text = 'table'            # classname
        ET.SubElement(object, "pose").text = "Unspecified"
        ET.SubElement(object, "truncated").text = "0"
        ET.SubElement(object, "difficult").text = "0"
        bndbox = ET.SubElement(object, "bndbox")
        ET.SubElement(bndbox, "xmin").text = str(result[0])
        ET.SubElement(bndbox, "ymin").text = str(result[1])
        ET.SubElement(bndbox, "xmax").text = str(result[2])
        ET.SubElement(bndbox, "ymax").text = str(result[3])
    name_xml = os.path.join(path, os.path.basename(link).split(".")[0] + ".xml")
    tree = ET.ElementTree(annotation)
    tree.write(name_xml)