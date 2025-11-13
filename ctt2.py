def compose_cubes_with_rules(
        cube1: Cube, system1: System, 
        cube2: Cube, system2: System,
        direction: Direction, value: int) -> tuple[Cube, System]:
    face1 = Face(direction, value)
    face2 = face1.opposite()
    cube = cube1.compose(cube2, direction, value)
    system = system1.compose(system2, [face1, face2])
    return cube, system


def test_compose_cubes_with_rules() -> bool:
    try:
        d0 = Direction(0)
        d1 = Direction(1)
        d2 = Direction(2)
        
        f00 = Face(d0, 0)
        f01 = Face(d0, 1)
        f10 = Face(d1, 0)
        f11 = Face(d1, 1)
        f20 = Face(d2, 0)
        f21 = Face(d2, 1)
        
        cube1 = Cube([d0, d1])
        cube1.set_face(f00, "100")
        cube1.set_face(f01, "101")
        cube1.set_face(f10, "110")
        cube1.set_face(f11, "composed")

        system1 = System()
        system1.add_rule([f00, f01], "1-00-01")
        system1.add_rule([f00, f10], "1-00-10")
        system1.add_rule([f00, f11], "1-00-11")
        system1.add_rule([f01, f10], "1-01-10")
        system1.add_rule([f01, f11], "1-01-11")
        system1.add_rule([f10, f11], "10-11")
        system1.add_rule([f00, f01, f10, f11], "10-11+")

        cube2 = Cube([d1, d2])
        cube2.set_face(f10, "composed")
        cube2.set_face(f11, "211")
        cube2.set_face(f20, "220")
        cube2.set_face(f21, "221")
        
        system2 = System()
        system2.add_rule([f10, f11], "10-11")
        system2.add_rule([f10, f20], "2-10-20")
        system2.add_rule([f10, f21], "2-10-21")
        system2.add_rule([f11, f20], "2-11-20")
        system2.add_rule([f11, f21], "2-11-21")
        system2.add_rule([f20, f21], "2-20-21")
        system2.add_rule([f10, f11, f20, f21], "10-11+")
        
        cube, system = compose_cubes_with_rules(
            cube1, system1, cube2, system2,
            d1, 1)

        assert cube.dimension() == 3, "composed dimension"
        assert cube.get_face(f00) == "100", "composed f00"
        assert cube.get_face(f01) == "101", "composed f01"
        assert cube.get_face(f10) == "110", "composed f10"
        assert cube.get_face(f11) == "211", "composed f11"
        assert cube.get_face(f20) == "220", "composed f10"
        assert cube.get_face(f21) == "221", "composed f11"

        assert system([f00, f01]) == "1-00-01", "composed rule [f00, f01]"
        assert system([f00, f10]) is None, "composed rule [f00, f10]"
        assert system([f00, f11]) is None, "composed rule [f00, f11]"
        assert system([f00, f20]) is None, "composed rule [f00, f20]"
        assert system([f00, f21]) is None, "composed rule [f00, f21]"
        assert system([f01, f10]) is None, "composed rule [f01, f10]"
        assert system([f01, f11]) is None, "composed rule [f01, f11]"
        assert system([f01, f20]) is None, "composed rule [f01, f20]"
        assert system([f01, f21]) is None, "composed rule [f01, f21]"
        assert system([f10, f11]) is None, "composed rule [f10, f11]"
        assert system([f10, f20]) is None, "composed rule [f10, f20]"
        assert system([f10, f21]) is None, "composed rule [f10, f21]"
        assert system([f11, f20]) is None, "composed rule [f11, f20]"
        assert system([f11, f21]) is None, "composed rule [f11, f21]"
        assert system([f20, f21]) == "2-20-21", "composed rule [f20, f21]"
        assert system([f00, f01, f20, f21]) == "10-11+", "composed rule [f00, f01, f20, f21]"
        
        print("All tests for composition of cubes and rules passed successfully!")
        return True
    except Exception as e:
        print(f"Tests for composition of cubes and rules failed: {str(e)}")
        return False
