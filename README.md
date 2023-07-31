# <center>OsmParser 🗿</center>
## About
Osm parser is simple OpenStreetMap xml output parser. It's guided by official [OpenStreatMap](https://wiki.openstreetmap.org/wiki/) documentation and
consist of a little amount of simple classes that represent specific entity of OpenStreetMap

# Map
Class Map represent an object that contains all the entities parsed from osm file. It also have special methods for computing some math
```python
def get_bounds() -> tuple[float]
"""Return the coordinates of sides from current map frame in this order. (All values are float)
(left , right , top , bottom)
"""
```
```python
def get_size() -> float
"""Return the area of current map frame
"""
```
```python
def get_center() -> tuple[float]
"""Return coordinates of center point of current map frame (latitude , longtitute)
"""
```
```python
def get_ways() -> osmparser.Way
"""Return all map ways
"""

def get_routes() -> osmparser.Route
"""Return all map routes
"""

def get_relations() -> osmparser.Relation
"""Return all map relations
"""

```


# Relation [here](https://wiki.openstreetmap.org/wiki/Types_of_relation)



# Way [here](https://wiki.openstreetmap.org/wiki/Way)