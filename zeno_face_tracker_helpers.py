import os
import numpy as np
import xml.etree.cElementTree as ET


def save_pts(pts_path, pts):
    with open(pts_path, 'w') as pts_file:
        pts_file.write('version: 1\n')
        pts_file.write('n_points: %d\n{\n' % pts.shape[0])
        for idx in range(pts.shape[0]):
            pts_file.write('%.3f %.3f\n' % (pts[idx, 0], pts[idx, 1]))
        pts_file.write('}\n')


def load_pts(pts_path):
    with open(pts_path) as pts_file:
        pts_file_content = pts_file.read().replace('\r', ' ').replace('\n', ' ')
        pts_file_content = pts_file_content[pts_file_content.find('{') + 1:
                                            pts_file_content.find('}')]
        return np.array([float(x) for x in pts_file_content.split(' ') if
                         len(x) > 0]).reshape(-1, 2)


def save_annotation_job(job_path, items, number_of_landmarks):
    root = ET.Element('FaceDataset')
    root.set('xmlns', 'https://github.com/luigivieira/Facial-Landmarks-Annotation-Tool')
    root.set('numberOfFeatures', '%d' % number_of_landmarks)
    samples = ET.SubElement(root, 'Samples')
    job_parent_folder = os.path.dirname(os.path.realpath(job_path))
    for item in items:
        sample = ET.SubElement(samples, 'Sample')
        image_path = os.path.relpath(item[0], job_parent_folder)
        sample.set('fileName', image_path)
        features = ET.SubElement(sample, 'Features')
        for pt_idx, pt in enumerate(item[1]):
            feature = ET.SubElement(features, 'Feature')
            feature.set('x', '%.3f' % pt[0])
            feature.set('y', '%.3f' % pt[1])
            feature.set('id', '%d' % pt_idx)
            connections = ET.SubElement(feature, 'Connections')
            if item[1].shape[0] == 68:
                if pt_idx == 30:
                    target = ET.SubElement(connections, 'Target')
                    target.set('id', '33')
                elif pt_idx == 41:
                    target = ET.SubElement(connections, 'Target')
                    target.set('id', '36')
                elif pt_idx == 47:
                    target = ET.SubElement(connections, 'Target')
                    target.set('id', '42')
                elif pt_idx == 59:
                    target = ET.SubElement(connections, 'Target')
                    target.set('id', '48')
                elif pt_idx == 67:
                    target = ET.SubElement(connections, 'Target')
                    target.set('id', '60')
                elif pt_idx != 16 and pt_idx != 21 and pt_idx != 26 and pt_idx != 35:
                    target = ET.SubElement(connections, 'Target')
                    target.set('id', '%d' % (pt_idx + 1))
    ET.ElementTree(root).write(job_path, encoding='UTF-8', xml_declaration=True)
