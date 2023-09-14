import xml.etree.ElementTree as ET

tree = ET.parse('map.osm')
root = tree.getroot()
