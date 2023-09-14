"""main module source code
"""
import xml.etree.ElementTree as ET


tree = ET.parse('map.osm')
root = tree.getroot()


def _get_metadata() -> tuple:
    return float(root.find(".//bounds").attrib['minlat']) , float(root.find(".//bounds").attrib['minlon'])

def get_center():
    minlat = float(root.find(".//bounds").attrib['minlat']) % 1
    maxlat = float(root.find(".//bounds").attrib['maxlat']) % 1
    minlon = float(root.find(".//bounds").attrib['minlon']) % 1
    maxlon = float(root.find(".//bounds").attrib['maxlon']) % 1 
    maxvalue = max((maxlat - minlat) , (maxlon - minlon)) * 1000000
    print((maxlat - minlat) *  1000000)
    return (maxlat - minlat) /  2  *  1000000, (maxlon - minlon) / 2  *  1000000, maxvalue

def get_coords(node_tag) -> tuple:
    meta = _get_metadata()
    lat = float(node_tag.attrib['lat']) % 1 * 1000000
    lon = float(node_tag.attrib['lon']) % 1 * 1000000
    return normolize(lat ,lon)

def normolize(lat , lon):
    center = get_center()
    return (lat - center[0]) / center[2], (lon - center[1]) / center[2]


def get_polygon_from_relation(relation_id) -> list:
    result = []
    relation = root.find(".//relation[@id='{}']".format(relation_id))
    for way in relation:
        if way.tag == 'member':
            result.append(way.attrib['ref'])
    return result

def get_ways_from_polygon(members):
    for member in members:
        way = root.find(".//way[@id='{}']".format(member))
        for tag in way:
            coords = get_coords(root.find(".//node[@id='{}']".format(tag.attrib['ref'])))
            print(coords)

# get_ways_from_polygon(get_polygon_from_relation('9592022'))
print(get_center())