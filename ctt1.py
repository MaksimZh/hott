def test_interaction() -> bool:
    try:
        d0 = Direction(0)
        d1 = Direction(1)
        f00 = Face(d0, 0)
        f01 = Face(d0, 1)
        f10 = Face(d1, 0)
        f11 = Face(d1, 1)
        i = Interval()
        # Test 1: path values on faces
        deg = i.degeneracy(5)
        assert deg(f00.value) == 5, "degeneracy for f00.value"
        assert deg(f01.value) == 5, "degeneracy for f01.value"
        p = i.path(10, 20)
        assert p(f00.value) == 10, "path f00.value"
        assert p(f01.value) == 20, "path f01.value"
        # Test 2: path between faces
        assert i.path(f00.value, f01.value)(0.25) == 0.25, "path for direction 0"
        assert i.path(f10.value, f11.value)(0.25) == 0.25, "path for direction 1"
        # Test 3: path to opposite faces
        oppath = lambda f: i.path(f.value, f.opposite().value)
        assert oppath(f00)(0.25) == 0.25, "path to opposite of f00"
        assert oppath(f01)(0.25) == 0.75, "path to opposite of f01"
        assert oppath(f10)(0.25) == 0.25, "path to opposite of f10"
        assert oppath(f11)(0.25) == 0.75, "path to opposite of f11"
        # Test 4: degenerate paths
        degpath = lambda f: i.path(f.value, f.value)
        assert degpath(f00)(0.25) == 0, "degenerte path of f00"
        assert degpath(f01)(0.25) == 1, "degenerte path of f01"
        assert degpath(f10)(0.25) == 0, "degenerte path of f10"
        assert degpath(f11)(0.25) == 1, "degenerte path of f11"
        # Test 5: paths for directions
        class DirVal:
            def __init__(self, d, v):
                self.direction = d
                self.value = v
            def __eq__(self, other):
                if not isinstance(other, DirVal):
                    return False
                return self.direction == other.direction and \
                       self.value == other.value
            
            def __add__(self, other):
                if not isinstance(other, DirVal) or \
                   other.direction != self.direction:
                    return NotImplemented
                return DirVal(self.direction, self.value + other.value)
            
            def __mul__(self, other):
                return DirVal(self.direction, self.value * other)
        
        assert i.path(DirVal(d0, 10), DirVal(d0, 30))(0.25) == DirVal(d0, 15), \
               "DirVal path"
        assert i.degeneracy(DirVal(d0, 10))(0.25) == DirVal(d0, 10), \
               "DirVal degeneracy"
        # Test 6: face directions
        assert f00.direction == d0
        assert f01.direction == d0
        assert f10.direction == d1
        assert f11.direction == d1
        assert f00.opposite().direction == d0
        assert f01.opposite().direction == d0
        assert f10.opposite().direction == d1
        assert f11.opposite().direction == d1
    
        print("All interaction tests passed successfully!")
        return True
    except Exception as e:
        print(f"Interaction test failed: {str(e)}")
        return False
