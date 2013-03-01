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
        self.assertEqual(str(self.l1.getBBox()),str(geobo3.BBox(0.0,0.0,10.0,0.0)),'')
        #Get WKT
        self.assertEqual(str(self.l1.getWkt()),'LINESTRING (0 0, 1 0, 10 0)','')
        #revert
        self.l1.reverse()
        self.assertEqual(str(self.l1.getWkt()),'LINESTRING (10 0, 1 0, 0 0)','')
        #Set WKT
        l2 = geobo3.Line()
        l2.setFromWkt(' LINESTRING (3 3, 10 5,-6.4 -8.001) ')
        l2.reverse()
        #TODO issue #2: Somehow all coords are converted to float, shouldn't they be converted to int when the end with .0?
        self.assertEqual(str(l2.getWkt()),'LINESTRING (-6.4 -8.001, 10 5, 3 3)','')
        
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
        #TODO issue #1: Inner is not processed correctly when generating wkt
        pg1.addInner(h1)
        
        self.assertEqual(pg1.getBBox().getArea(),20,'')
        self.assertEqual(str(pg1.getWkt()),'POLYGON ((0 0, 4 3, 2 5, 0 0))','')
        self.assertEqual(pg1.getArea(),6,'')
        #TODO: Somehow the polygon is invalid
        self.assertEqual(pg1.isValid(),False,'')

        pg2 = geobo3.Polygon()
        pg2.setFromWkt('POLYGON((-2 2, 1 4, 3 3, 2 2, 4 1, 4 -1, 1 -2, -1 -2, -1 0),(-1 2, 2 3, 1 1, 0 1), (2 -1, 3 -1, 3 1, 2 1))')
        #TODO issue #3: Somehow generating a POLYGON with inner(s) is not working
        self.assertEqual(pg2.getArea(),21.5,'')

    def test_stArea(self):
        #select i.pand, i.opp_pand, st_area(p.geovlak), st_astext(st_force_2d(p.geovlak))from infofolio_utrecht i join pand p on i.pand = p.identificatie limit 3;
        #305100000000003;180.843199999797;180.843199999797;"POLYGON((125061.08 474625.44,125051.76 474628.12,125046.6 474610.2,125055.92 474607.52,125061.08 474625.44))"
        #100000000004;206.016000000266;206.016000000266;"POLYGON((125075 474538.44,125065.56 474542.28,125057.96 474523.48,125067.36 474519.68,125075 474538.44))"
        #305100000000005;221.587019999572;221.587019999572;"POLYGON((125085.695 474532.234,125086.28 474533.72,125077.04 474537.6,125068.88 474517.04,125078.24 474513.28,125085.695 474532.234))"
        pg3 = geobo3.Polygon()
        pg3.setFromWkt('POLYGON((125061.08 474625.44,125051.76 474628.12,125046.6 474610.2,125055.92 474607.52,125061.08 474625.44))')
        #self.assertEqual(str(pg3.getWkt()),'POLYGON((125061.08 474625.44,125051.76 474628.12,125046.6 474610.2,125055.92 474607.52,125061.08 474625.44))','')
        self.assertEqual(pg3.getArea(), 180.84320000000298,'')

        pg4 = geobo3.Polygon()
        pg4.setFromWkt('POLYGON((125075 474538.44,125065.56 474542.28,125057.96 474523.48,125067.36 474519.68,125075 474538.44))')
        #self.assertEqual(str(pg4.getWkt()),'POLYGON((125075 474538.44,125065.56 474542.28,125057.96 474523.48,125067.36 474519.68,125075 474538.44))','')
        self.assertEqual(pg4.getArea(),206.01599999982864,'')
        
        pg5 = geobo3.Polygon()
        pg5.setFromWkt('POLYGON((125085.695 474532.234,125086.28 474533.72,125077.04 474537.6,125068.88 474517.04,125078.24 474513.28,125085.695 474532.234))')
        #self.assertEqual(str(pg5.getWkt()),'POLYGON((125085.695 474532.234,125086.28 474533.72,125077.04 474537.6,125068.88 474517.04,125078.24 474513.28,125085.695 474532.234))','')
        self.assertEqual(pg5.getArea(),221.58701999904588,'')

        
suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
unittest.TextTestRunner(verbosity=2).run(suite)
