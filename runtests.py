import geobo3
import unittest

class TestSequenceFunctions(unittest.TestCase):
    
    def setUp(self):
        self.bb1 = geobo3.BBox(0,0,2,2)
        self.bb2 = geobo3.BBox(3, 3, 1, 1)
        self.p1 = geobo3.Point(0,0)
        self.p2 = geobo3.Point(1,0)
        self.l1 = geobo3.Line()
        
    def test_bbox(self):
        _area = self.bb1.getArea()
        _area1 = self.bb2.getArea()
        self.assertEqual(_area, 4, 'incorrect area for bb1')
        self.assertEqual(_area1, 4, 'incorrect area for bb2')
        self.assertEqual(_area1, _area, 'bb1 not equal to bb2')
        
    def test_point(self):
        self.assertEqual(str(self.p1),'Point[0,0]','')
        self.assertEqual(self.p1.getWkt(),'POINT (0 0)','')
        self.assertEqual(self.p1.distanceTo(self.p2),1,'')

    def test_line(self):
        #Line holds no point, length equals 0
        self.assertEqual(self.l1.getLength(),0,'')

        #Line holds a single point, length equals 0
        self.l1.addPoint(self.p1)
        self.assertEqual(self.l1.getLength(),0,'')

        #Line holds two points, length equals 1
        self.l1.addPoint(self.p2)
        self.assertEqual(self.l1.getLength(),1,'')

        #Line holds 3 points, length equals 10
        self.l1.addXy(10,0)
        self.assertEqual(self.l1.getLength(),10,'')

        #Get the BBOX for this line
        self.assertEqual(str(self.l1.getBBox()),str(geobo3.BBox(0,0,10,0)),'')
        #Get WKT
        self.assertEqual(str(self.l1.getWkt()),'LINESTRING (0 0, 1 0, 10 0)','')
        #revert
        self.l1.reverse()
        self.assertEqual(str(self.l1.getWkt()),'LINESTRING (10 0, 1 0, 0 0)','')
        #Set WKT
        l2 = geobo3.Line()
        l2.setFromWkt(' LINESTRING (3 3, 10 5,-6.4 -8) ')
        l2.reverse()
        #TODO: Somehow all coords are converted to float, shouldn't they be converted to int when the end with .0?
        self.assertEqual(str(l2.getWkt()),'LINESTRING (-6.4 -8.0, 10.0 5.0, 3.0 3.0)','')
        
    def test_polygon(self):
        pg1 = geobo3.Polygon()

        #Add outer
        pg1.outer.addXy(0, 0)
        pg1.outer.addXy(4, 3)
        pg1.outer.addXy(2, 5)

        #Add inner
        h1 = geobo3.Line()
        h1.addXy(2, 2)
        h1.addXy(3, 3)
        h1.addXy(2, 4)
        #TODO: Inner is not processed correctly when generating wkt
        pg1.addInner(h1)
        
        self.assertEqual(pg1.getBBox().getArea(),20,'')
        self.assertEqual(str(pg1.getWkt()),'POLYGON ((0 0, 4 3, 2 5, 0 0))','')
        self.assertEqual(pg1.getArea(),6,'')
        #TODO: Somehow the polygon is invalid
        self.assertEqual(pg1.isValid(),False,'')

        pg2 = geobo3.Polygon()
        pg2.setFromWkt('POLYGON((-2 2, 1 4, 3 3, 2 2, 4 1, 4 -1, 1 -2, -1 -2, -1 0),(-1 2, 2 3, 1 1, 0 1), (2 -1, 3 -1, 3 1, 2 1))')
        #TODO: Somehow generating a POLYGON with inner(s) is not working
        self.assertEqual(pg2.getArea(),0,'')
    
suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
unittest.TextTestRunner(verbosity=2).run(suite)
