import xml.etree.cElementTree as ET
import glob, os
os.chdir("PATH_TO_SYNSET")
for file in glob.glob("*.txt"):
	input_file = open(file, "r") 
	synset_name = input_file.readline()
	image_name = input_file.readline()
	width = input_file.readline()
	height = input_file.readline()
	depth = input_file.readline()
	xmin = input_file.readline()
	ymin = input_file.readline()
	xmax = input_file.readline()
	ymax = input_file.readline()
	
	xmin = xmin.rstrip('\n')
	xmin = float(xmin)
	xmin = int(xmin)
	#print type(xmin)
		
	ymin = ymin.rstrip('\n')
	ymin = float(ymin)
	ymin = int(ymin)
	#print type(ymin)
		
	xmax = xmax.rstrip('\n')
	xmax = float(xmax)
	xmax = int(xmax)
	#print type(xmax)
	
	ymax = ymax.rstrip('\n')
	ymax = float(ymax)
	ymax = int(ymax)
	
	#print type(ymax)
	
	
	root = ET.Element("annotation")

	ET.SubElement(root, "folder").text = synset_name.rstrip('\n') #synset name
	ET.SubElement(root, "filename").text = image_name.rstrip('\n') #image name

	source = ET.SubElement(root, "source")
	ET.SubElement(source, "database").text = "ImageNet database" #lasciare cosi

	size = ET.SubElement(root, "size")
	ET.SubElement(size, "width").text = width.rstrip('\n')
	ET.SubElement(size, "height").text = height.rstrip('\n')
	ET.SubElement(size, "depth").text = depth.rstrip('\n')

	ET.SubElement(root, "segmented").text = "0" #lasciare cosi

	obj = ET.SubElement(root, "object")
	ET.SubElement(obj, "name").text = synset_name.rstrip('\n') #synset name
	ET.SubElement(obj, "pose").text = "Unspecified" #lasciare cosi
	ET.SubElement(obj, "truncated").text = "0" #lasciare cosi
	ET.SubElement(obj, "difficult").text = "0" #lasciare cosi

	bb = ET.SubElement(obj, "bndbox")
	ET.SubElement(bb, "xmin").text = str(xmin)
	ET.SubElement(bb, "ymin").text = str(ymin)
	ET.SubElement(bb, "xmax").text = str(xmax)
	ET.SubElement(bb, "ymax").text = str(ymax)


	#salva
	tree = ET.ElementTree(root)
	xml = image_name.rstrip('\n')+".xml" #rstrip toglie \n
	print file, "-->", xml
	tree.write(xml)
