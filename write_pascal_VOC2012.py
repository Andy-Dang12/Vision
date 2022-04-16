import os.path
import xml.etree.ElementTree as ET
import numpy as np
    
def save_file_xml(img:np.ndarray, abspath:str, folder_save:str, boxes:list):
    ''' 
    img             opencv
    abspath         đường dẫn đầy đủ của ảnh
    folder_save     là folder để save
    boxes           là list các box theo thứ tự xmin, ymin, xmax, ymax, class_name'''
    
    imgname = os.path.basename(abspath)
    hei, wid, ch = img.shape
    
    annotation = ET.Element("annotation")
    ET.SubElement(annotation, "folder").text = "data_form"
    ET.SubElement(annotation, "filename").text = imgname
    ET.SubElement(annotation, "path").text = abspath
    source = ET.SubElement(annotation, "source")
    ET.SubElement(source, "database").text= "Unknown"
    size = ET.SubElement(annotation, "size")
    ET.SubElement(size, "width").text = str(wid)
    ET.SubElement(size, "height").text = str(hei)
    ET.SubElement(size, "depth").text = str(ch)
    ET.SubElement(annotation, "segmented").text = "0"

    for box in boxes:
        obj = ET.SubElement(annotation, "object")
        ET.SubElement(obj, "name").text = str(box[4])   #FIXME classname
        ET.SubElement(obj, "pose").text = "Unspecified"
        ET.SubElement(obj, "truncated").text = "0"
        ET.SubElement(obj, "difficult").text = "0"
        bndbox = ET.SubElement(obj, "bndbox")
        ET.SubElement(bndbox, "xmin").text = str(box[0])
        ET.SubElement(bndbox, "ymin").text = str(box[1])
        ET.SubElement(bndbox, "xmax").text = str(box[2])
        ET.SubElement(bndbox, "ymax").text = str(box[3])

    tree = ET.ElementTree(annotation)
    tree.write(os.path.join(folder_save, imgname.split(".")[0] + ".xml"))