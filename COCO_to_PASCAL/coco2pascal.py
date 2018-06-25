#!/usr/bin/python -tt

# python code to convert coco val2014 JSON file to PASCAL XML.

import sys
import numpy as np 
from lxml import etree as ET
from shutil import copyfile

	
def main():
	if len(sys.argv) != 3:
		print 'usage: python convert_to_pascalformat.py coco_dataDir coco_dataType'
		print 'for example: python coco2pascal.py ../ train2014'
		sys.exit(1)

	dataDir = sys.argv[1]
	dataType = sys.argv[2]

	from pycocotools.coco import COCO
	import os

	annFile='%s/annotations/instances_%s.json'%(dataDir,dataType)

	coco=COCO(annFile)
	
	#load all categories
	cats = coco.loadCats(coco.getCatIds())
	#Modify the category list according to your need
	catNms=['scissors','suitcase','toilet','laptop','umbrella']
	cat_Ids = coco.getCatIds(catNms)
	print "Category Ids: " + str(cat_Ids)

    # get all the Image Ids of provided categories
	imgIds=[]
	for cat in cat_Ids:
		imgIds.extend(coco.getImgIds(catIds=cat))
	
	print "Total Images : " + str(len(imgIds))
	
	# Create directory for Pascal VOC annotation
	directory_annotation = '../annotations_pascalformat/'
	if not os.path.exists(directory_annotation):
	    os.makedirs(directory_annotation)
	    
	#Creating ImageSet directory for Pascal VOC format    
	imageset_directory = '../ImageSets/Main/'
	if not os.path.exists(imageset_directory):
	    os.makedirs(imageset_directory)
	    
	#Creating JPEG Images directory for Pascal VOC format 
	src_img_directory = '%s/images/%s/'%(dataDir,dataType)   
	dst_img_directory = '../JPEGImages/'
	if not os.path.exists(dst_img_directory):
	    os.makedirs(dst_img_directory)
	
	
	file_names = []	
	print "Conversion in Progress....."
	#Iterate through Image and generate xml and copy image to JPEG directory
	for n in xrange(len(imgIds)):
		img = coco.loadImgs(imgIds[n])[0]
		annIds = coco.getAnnIds(imgIds=img['id'], iscrowd=None)
		anns = coco.loadAnns(annIds)

		root = ET.Element('annotation')	
	
		ET.SubElement(root,'folder').text = 'COCO2014pascalformat'	
		ET.SubElement(root,'filename').text = img['file_name']	
	
		source = ET.SubElement(root, 'source')
		ET.SubElement(source, 'database').text = 'COCO2014 Pascal VOC format'
	
		size = ET.SubElement(root, 'size')
		ET.SubElement(size, 'width').text = str(img['width'])
		ET.SubElement(size, 'height').text = str(img['height'])
		ET.SubElement(size, 'depth').text = str(3)
	
		ET.SubElement(root,'segmented').text = str(0)
	
		for i in xrange(len(anns)):
			bbox = anns[i]['bbox']
		
			for cat in cat_Ids:
				if cat ==  anns[i]['category_id']:
			
					object = ET.SubElement(root, 'object')
		
					for cat in cats:
						if cat['id'] == anns[i]['category_id']:
							ET.SubElement(object, 'name').text = cat['name']
		
					bndbox = ET.SubElement(object, 'bndbox')
					ET.SubElement(bndbox, 'xmin').text = str(int(round(bbox[0])))
					ET.SubElement(bndbox, 'ymin').text = str(int(round(bbox[1])))
					ET.SubElement(bndbox, 'xmax').text = str(int(round(bbox[0] + bbox[2])))
					ET.SubElement(bndbox, 'ymax').text = str(int(round(bbox[1] + bbox[3])))
					ET.SubElement(bndbox, 'truncated').text = str(0)
					ET.SubElement(bndbox, 'difficult').text = str(0)
		
		tree = ET.ElementTree(root)
	
		f_xml = open(directory_annotation + img['file_name'].split('.jpg')[0] + '.xml', 'w')
		tree.write(f_xml, pretty_print=True, xml_declaration=True)
		f_xml.close()
	
		file_names.append(img['file_name'].split('.jpg')[0])
		#copy image from source to destination
		copyfile(src_img_directory + img['file_name'], dst_img_directory + img['file_name'])
	
	#Generate val.txt/train.txt     
	f_txt = open(imageset_directory + dataType[:-4] + '.txt', 'w');	
	
	unique_names = set(file_names)
		
	for name in unique_names:
		f_txt.write(name + "\n")
	f_txt.close()		
	
	print "Conversion Completed."	
	
if __name__ == '__main__':
  main()
