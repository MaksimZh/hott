def segment_kan():
    bottom = CubicalPath(lambda t: (t, 0))
    top = CubicalPath(lambda t: (t, 1))
    filled = fill({'bottom': bottom, 'top': top})
    
    x_direction = Direction(0)
    y_direction = Direction(1)

    lower_face = Face(y_direction, 0)
    upper_face = Face(y_direction, 1)

    lower_cube = Cube([x_direction, y_direction])
    lower_cube.set_face(lower_face, bottom)
    lower_cube.set_face(upper_face, filled)
    
    upper_cube = Cube([x_direction, y_direction])
    upper_cube.set_face(lower_face, filled)
    upper_cube.set_face(upper_face, top)

    composed_cube = lower_cube.compose(upper_cube, y_direction, 1)
    assert composed_cube.get_face(lower_face) == bottom
    assert composed_cube.get_face(upper_face) == top
