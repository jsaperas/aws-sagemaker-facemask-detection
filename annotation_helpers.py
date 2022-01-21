import json

def get_image_dimensions(xml):
    
    dim = xml.find('size')
    image_dim = {}
    for d in ['width', 'height', 'depth']:
        image_dim[d] = int(dim.find(d).text)
    
    return image_dim

def get_annotations(xml):
    
    image_name = xml.find('filename').text
    image_size = get_image_dimensions(xml)
    
    class_map = {'without_mask': 0, 'with_mask': 1, 'mask_weared_incorrect': 2}
    annotations = []
    for obj in xml.iter('object'):
        _annot = get_bbox(obj, class_map)
        annotations.append(_annot)
    
    record = {}
    record['source-ref'] = image_name
    record['bounding-box'] = {
        'image_size': [image_size],
        'annotations': annotations
    }
    
    return record
        
    
def get_bbox(obj, class_map):
    
    annot = {}
    
    label = obj.find('name').text
    bndbox = obj.find('bndbox')
    xmin = int(bndbox.find('xmin').text)
    xmax = int(bndbox.find('xmax').text)
    ymin = int(bndbox.find('ymin').text)
    ymax = int(bndbox.find('ymax').text)

    annot['class_id'] = class_map[label]
    annot['left'] = xmin
    ## This is key - ymin is really the top of the bbox since the origin (0, 0)
    ## is the upper-left corner of the entire image.
    annot['top'] = ymin 
    annot['width'] = xmax - xmin
    annot['height'] = ymax - ymin
    
    return annot

def save_augmented_manifest(annotations, file):
    with open(file, 'w') as f:
        for ann in annotations:
            json.dump(ann, f)
            f.write('\n')