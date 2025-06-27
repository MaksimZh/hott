from core.base_types import *

# 1 - 2
# |   |
# 3 - 4

p12 = Path(1, 2)
p24 = Path(2, 4)
p13 = Path(1, 3)
p34 = Path(3, 4)
pa = p12.trans(p24)
pb = p13.trans(p34)
assert pa.start == pb.start
assert pa.end == pb.end
p = pa.trans(pb.sym())
assert p.start == p.end


# 1  - 10
# V     V
# 2  -  5

p = Path(1, 10)
twice = lambda x: x * 2
half = lambda x: x // 2
p1 = p.map_both(twice, half)
assert p1.start == twice(p.start)
assert p1.end == half(p.end)
