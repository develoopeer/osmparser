import pprint
import xml.etree.ElementTree as ET


def pairwise(iterable):
    result = []
    for _ in range(len(iterable) - 1):
        result.append([iterable[_] , iterable[_ + 1]])

    result.append([iterable[0] , iterable[-1]])
    return result


class Map:
    def __init__(self , root) -> None:
        self.root = root
    
    def get_relations(self) -> None:
        _relations = self.root.findall(".//relation")
        result = []
        for _relation in _relation:
            result.append(Relation(_relation))

        return result

    def get_bounds(self) -> list:
        return list(map(float , self.root.find('.//bounds').attrib.values()))

    def get_center(self) -> tuple:
        bounds = self.get_bounds()
        x_center = bounds[0] + (bounds[2] - bounds[0])
        y_center = bounds[1] + (bounds[3] - bounds[1])
        return x_center , y_center

    @property
    def size(self) -> float:
        # https://www.sco.wisc.edu/2022/01/21/how-big-is-a-degree/#:~:text=Therefore%20we%20can%20easily%20compute,69.4%20miles%20(111.1%20km).
        long_const = [
            (0  , 15 , 111.1),
            (15 , 30 , 107.3),
            (30 , 45 , 96.2),
            (45 , 60 , 78.6),
            (60 , 75 , 55.6),
            (75 , 90 , 28.8)
        ]
        bounds = self.get_bounds()
        long = 0
        _width  = bounds[2] - bounds[0]
        for _ in long_const:
            if int(bounds[2]) in range(_[0] , _[1]):
                long = _[2]
        _height = bounds[3] - bounds[1]
        return round(_width * 111.1 * _height * long , 2)
    
    @property
    def ways_cound(self) -> int:
        return len(self.get_ways())

    def get_ways(self):
        return self.root.findall('.//way')

    def get_routes(self):
        return self.root.findall(".//tag[@v='route']...")

    def get_relation(self , relation_id):
        return Relation(self.root.findall(".//relation[@id='{}']".format(relation_id))[0])


class MemberWay():
    def __init__(self , member) -> None:
        self.member_struct = member
        self._serial_nodes , self._serial_tags = self._serialize()

    def _serialize(self) -> tuple:
        nodes = []
        tags  = {}
        for tag in self.member_struct:
            if tag.tag == 'nd':
                nodes.append(tag)
            elif tag.tag == 'tag':
                tags[tag.attrib['k']] = tag.attrib['v']
        return nodes , tags

    @property
    def tags(self) -> dict:
        return self._serial_tags

    @property
    def is_closed(self) -> bool:
        if self._serial_nodes[-1].attrib['ref'] == self._serial_nodes[0].attrib['ref']:
            return True
        return False
    
    def pair_nodes(self) -> list:
        pass
    
    def dots(self) -> list:
        # Return list of dots to connect with line to render current feature
        result = []
        for node in self._serial_nodes:
            result.append([
                float(node.attrib['lat']),
                float(node.attrib['lon'])
            ])
        return result


class Relation:
    def __init__(self , relation_struct) -> None:
        self.relation_struct = relation_struct
        self.ways , self.tags = self._serialize()

    def _serialize(self) -> None:
        ways = []
        tags = {}
        for tag in self.relation_struct:
            if tag.tag == 'member' and tag.attrib['type'] == 'way':
                ways.append(tag.attrib['ref'])
            elif tag.tag == 'tag':
                tags[tag.attrib['k']] = tag.attrib['v']

        return ways , tags

    def print(self) -> None:
        pprint.pprint(self.tags)

    @property
    def is_multipolygon(self) -> bool:
        if self.tags.get('type') == 'multipolygon':
            return True
        return False
    
    def is_route(self) -> bool:
        if self.tags.get('type') == 'route':
            return True
        return False

    @property
    def type(self) -> str:
        return self.tags['type']