import math
import copy
import string
class BBox():

    def __init__(self, minx, miny, maxx, maxy):
        self.minx = min(minx, maxx)
        self.miny = min(miny, maxy)
        self.maxx = max(minx, maxx)
        self.maxy = max(miny, maxy)
    
    def __str__(self):
        return 'BBox[' + str(self.minx) + \
            ', ' + str(self.miny) + \
            ', ' + str(self.maxx) + \
            ', ' + str(self.maxy) + ']'
    
    def extendByBBox(self, bbox):
        self.minx = min(self.minx, bbox.minx)
        self.miny = min(self.miny, bbox.miny)
        self.maxx = max(self.maxx, bbox.maxx)
        self.maxy = max(self.maxy, bbox.maxy)
    
    def __add__(self, bbox):
        result = copy.copy(self)
        result.extendByBBox(bbox)
        return result
    
    def __iadd__(self, bbox):
        self.extendByBBox(bbox)
    
    def getArea(self):
        return (self.maxx - self.minx) * (self.maxy - self.miny)

    def contains(self, bbox):
        return self.minx <= bbox.minx and \
            self.miny <= bbox.miny and \
            self.maxx >= bbox.maxx and \
            self.maxy >= bbox.maxy


class Point():

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
    
    def __str__(self):
        return 'Point[' + str(self.x) + ',' + str(self.y) + ']'
        
    def __eq__(self, p2):
        if self.x == p2.x and self.y == p2.y:
            return True
        else:
            return False
    
    def distanceTo(self, p2):
        dx = p2.x - self.x
        dy = p2.y - self.y
        return math.sqrt((dx ** 2) + (dy ** 2))

    def setFromWkt(self, wkt):
        #sets x and y from well known text string
        result = False
        wkt = wkt.strip().upper()
        if wkt[:5] == 'POINT':
            wkt = wkt[5:].strip()
            wkt = wkt[1:-1]
            coords = wkt.split(' ')
            if len(coords) == 2:
                try:
                    x = float(coords[0])
                    y = float(coords[1])
                    self.x = x
                    self.y = y
                    result = True
                except:
                    pass
        return result

    def getWkt(self):
        strx = Util().formatNumber(self.x)
        stry = Util().formatNumber(self.y)
        return 'POINT (' + strx + ' ' + stry + ')'
    
        
    def getBBox(self):
        return BBox(self.x, self.y, self.x, self.y)
    
class Line():

    def __init__(self, points = None):
        if points:
            self.points = points
        else:
            self.points = []

    def __str__(self):
        return 'Line[' + str(len(self.points)) + ' points]'
    
    def addPoint(self, point):
        self.points.append(point)
    
    def addXy(self, x, y):
        self.points.append(Point(x, y))
        
    def getLength(self):
        result = 0
        if len(self.points) > 1:
            for i in range(0, len(self.points) - 1):
                result += self.points[i].distanceTo(self.points[i+1])
        return result

    def getBBox(self):
        result = None
        if len(self.points) > 0:
            minx = self.points[0].x
            miny = self.points[0].y
            maxx = minx
            maxy = miny
            if len(self.points) > 1:
                for p in self.points:
                    minx = min(minx, p.x)
                    miny = min(miny, p.y)
                    maxx = max(maxx, p.x)
                    maxy = max(maxy, p.y)
            return BBox(minx, miny, maxx, maxy)
        else:
            return None

    def __len__(self):
        return len(self.points)

    def getWkt(self):
        result = "LINESTRING ("
        result += ', '.join(self._getWktCoords())
        result += ')'
        return result

    def setFromWkt(self, wkt):
        self.points = []
        #sets points from well known text (wkt) string
        result = False
        wkt = wkt.strip().upper()
        if wkt[:10] == 'LINESTRING':
            self.points = Util().wktPartToPoints(wkt[10:].strip())
        else:
            raise Exception('Invalid WKT for LINESTRING')
        return result
        
        
    
    def _getWktCoords(self, closed=False):
        result = []
        for p in self.points:
            strx = Util().formatNumber(p.x)
            stry = Util().formatNumber(p.y)
            result.append(strx + ' ' + stry)
        if not closed:
            return result
        else:
            result.append(result[0])
            return result
            
    def _getRingArea(self):
        result = 0
        if len(self) > 2:
            for i in range(0,len(self)-1):
                dx = self.points[i + 1].x - self.points[i].x
                ay = (self.points[i + 1].y + self.points[i].y) / 2.0
                result += (dx * ay)
            dx = self.points[0].x - self.points[len(self)-1].x
            ay = (self.points[0].y + self.points[len(self)-1].y) / 2.0
            result += (dx * ay)
        return result
    
    def _isRingClockwise(self):
        if self._getRingArea() > 0:
            return True
        else:
            return False

    def reverse(self):
        self.points = self.points[::-1]

class Polygon():

    def __init__(self, outer = None, inner = None):
        if outer:
            self.outer = outer
        else:
            l = Line()
            self.outer = l
        if inner:
            self.inner = inner
        else:
            self.inner = []
            
    def __str__(self):
        return 'Polygon[' + str(len(self.outer)) + ' boundary points, ' + str(len(self.inner)) + ' holes]'
    
    def getBBox(self):
        if len(self.outer) > 0:
            result = self.outer.getBBox()
            for hole in self.inner:
                result.extendByBBox(hole.getBBox())
            return result
        else:
            return None
    
    def getWkt(self):
        result = "POLYGON ("
        outercoords = ', '.join(self.outer._getWktCoords(True))
        result += '(' + outercoords + ')'
        for i in self.inner:
            innercoords = ', '.join(i._getWktCoords(True))
            result + '(' + innercoords + ')'
        result += ')'
        return result
        
    def getArea(self):
        result = 0
        result += abs(self.outer._getRingArea())
        for hole in self.inner:
            result -= abs(hole._getRingArea())
        return result

    def addInner(self, hole):
        self.inner.append(hole)
        
    def isValid(self):
        #outer
        if len(self.outer) < 3:
            #raise Exception('invalid: outer boundary has less than 3 points')
            return False
        outerBBox = self.outer.getBBox()
        if outerBBox.getArea() <= 0:
            #raise Exception('invalid: outer boundary\'s bbox-area <= 0')
            return False
        if not self.outer._isRingClockwise():
            #raise Exception('invalid: outer boundary is counter clockwise')
            return False
        for hole in self.inner:
            if len(hole) < 3:
                return False
            innerBBox = hole.getBBox()
            if innerBBox.getArea() <= 0:
                #raise Exception('invalid: inner boundary\'s bbox-area <= 0')
                return False
            if hole._isRingClockwise():
                #raise Exception('invalid: inner boundary is counter clockwise')
                return False
            if not outerBBox.contains(innerBBox):
                #raise Exception('invalid: inner bbox is not contained by outer bbox')
                return False
        return True

    def setFromWkt(self, wkt):
        self.outer = Line()
        self.inner = []
        #sets boundaries from well known text (wkt) string
        result = False
        wkt = wkt.strip().upper()
        if wkt[:7] == 'POLYGON':
            #remove 'POLYGON' and first and last brackets
            wkt = wkt[7:].strip()
            firstbracket = wkt.find('(')
            lastbracket = Util()._findBackward(wkt, ')')
            wkt = wkt[firstbracket+1:lastbracket]
            boundarylist = []
            
            #self.points = wktPartToPoints(wkt[7:])
        else:
            raise Exception('Invalid WKT for POLYGON')
        return result


# functionality
class Util():
    def wktPartToPoints(self,part):
        points = []
        if part.count('(') == part.count(')'):
            part = part.replace('(','').replace(')','')
            for wktp in part.split(','):
                strp = wktp.strip().split(' ')
                if len(strp) == 2:
                    x = float(strp[0])
                    y = float(strp[1])
                    p = Point(x,y)
                    points.append(p)
                    
        return points
    
    def formatNumber(self,num):
        #num to string
        strnum = str(num)
        #check if there is a . inside
        if strnum.find('.') > -1:
            #remove trailing zeros
            strnum2 = strnum.rstrip('0')
            strnum3 = strnum2.rstrip('.')
            return strnum3
        else:        
            return strnum
    
    def _findBackward(self,s,subs):
        result = -1
        index = s[::-1].find(subs)
        if index > -1:
            result = len(s) - index - 1

        return result 
