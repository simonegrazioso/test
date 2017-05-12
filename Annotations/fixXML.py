import xml.etree.cElementTree as ET
import glob, os
from xml.dom import minidom

pathAnnot = "Annotations/"
syn = "hand"
os.chdir(pathAnnot + syn)
for file in glob.glob("*.xml"):
	doc = minidom.parse(file)

	# load old file with float values
	synset_name = doc.getElementsByTagName("folder")[0]
	synset_name = str(synset_name.firstChild.data)

	if synset_name is None:
		print synset_name

	image_name = doc.getElementsByTagName("filename")[0]
	image_name = str(image_name.firstChild.data)

	if image_name is None:
		print image_name

	width = doc.getElementsByTagName("width")[0]
	width = float(width.firstChild.data)

	if width is None:
		print width

	height = doc.getElementsByTagName("height")[0]
	height = float(height.firstChild.data)

	if height is None:
		print height

	depth = doc.getElementsByTagName("depth")[0]
	depth = float(depth.firstChild.data)

	if depth is None:
		print depth

	xmin = doc.getElementsByTagName("xmin")[0]
	xmin = float(xmin.firstChild.data)

	if xmin is None:
		print xmin

	xmax = doc.getElementsByTagName("xmax")[0]
	xmax = float(xmax.firstChild.data)

	if xmax is None:
		print xmax

	ymin = doc.getElementsByTagName("ymin")[0]
	ymin = float(ymin.firstChild.data)

	if ymin is None:
		print ymin

	ymax = doc.getElementsByTagName("ymax")[0]
	ymax = float(ymax.firstChild.data)

	if ymax is None:
		print ymax


	if 0 <= xmin and xmax >= width:
		print xmin, xmax, width

	if 0 <= ymin and ymax >= height:
		print ymin, ymax, height

	if xmin > xmax:
		print "problem"

	if ymin > ymax:
		print "y problem"

	if width <= xmin:
		print file, " width ", width, " xmin", xmin
		xmin = width - 1
	if width <= xmax:
		print file, " width ", width, " xmax", xmax
		xmax = width - 1
	if height <= ymin:
		print file, " height ", height, " ymin", ymin
		ymin = height - 1
	if height <= ymax:
		print file, " height ", height, " ymax", ymax
		ymax = height - 1

	if xmin <= 0:
		print file, " xmin ", xmin, " minore di 0"
		xmin = 1
	if xmax <= 0:
		print file, " xmax ", xmax, " minore di 0"
		xmax = 1
	if ymin <= 0:
		print file, " ymin ", ymin, " minore di 0"
		ymin = 1
	if ymax <= 0:
		print file, " ymax ", ymax, " minore di 0"
		ymax = 1

	#create fixed XML with integer values
	
	root = ET.Element("annotation")

	ET.SubElement(root, "folder").text = synset_name #synset name
	ET.SubElement(root, "filename").text = image_name #image name

	source = ET.SubElement(root, "source")
	ET.SubElement(source, "database").text = "ImageNet database" #lasciare cosi

	size = ET.SubElement(root, "size")
	ET.SubElement(size, "width").text = str(int(width))
	ET.SubElement(size, "height").text = str(int(height))
	ET.SubElement(size, "depth").text = str(int(depth))

	ET.SubElement(root, "segmented").text = "0" #lasciare cosi

	obj = ET.SubElement(root, "object")
	ET.SubElement(obj, "name").text = synset_name #synset name
	ET.SubElement(obj, "pose").text = "Unspecified" #lasciare cosi
	ET.SubElement(obj, "truncated").text = "0" #lasciare cosi
	ET.SubElement(obj, "difficult").text = "0" #lasciare cosi

	bb = ET.SubElement(obj, "bndbox")
	ET.SubElement(bb, "xmin").text = str(int(xmin))
	ET.SubElement(bb, "ymin").text = str(int(ymin))
	ET.SubElement(bb, "xmax").text = str(int(xmax))
	ET.SubElement(bb, "ymax").text = str(int(ymax))


	#save
	tree = ET.ElementTree(root)
	xml = str(image_name)+".xml" #rstrip toglie \n
	#print file, "-->", xml
	#d = "../" + "" + syn
	#os.chdir(d)
	tree.write(xml)
	#os.chdir("../" + pathAnnot + syn)


