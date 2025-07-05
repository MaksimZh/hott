from core.base_types import *


class LoopCount:
    
    def __init__(self, count):
        self.count = count

    def __neg__(self):
        return LoopCount(-self.count)

    def __add__(self, other):
        if not isinstance(other, LoopCount):
            return NotImplemented
        return LoopCount(self.count) + other.count
    
    def __eq__(self, other):
        """Check equality between two counts."""
        if not isinstance(other, LoopCount):
            return False
        return self.count == other.count


class LoopPath(Path):
    
    def __init__(self, start, count):
        super().__init__(start, start)
        self.count = count
        # Need this to avoid error in circle:
        self._trans_components = []

    def trans(self, other):
        if not isinstance(other, LoopPath):
            return super().trans(other)
            # NOTE: special case when `other` adds another loop turn?
        if other.start != self.start:
            raise ValueError("Composed loops must have same start point")
        result = LoopPath(self.start, self.count + other.count)
        result._trans_components = [self, other]
        return result

    def sym(self):
        return LoopPath(self.start, -self.count)
    
    def __eq__(self, other):
        """Check equality between two loops."""
        if not isinstance(other, LoopPath):
            return False
        return (self.start == other.start and 
                self.count == other.count)


class CircleLoop(LoopPath):
    
    def __init__(self, count=1):
        super().__init__(unit, count)

    def trans(self, other):
        if not isinstance(other, CircleLoop):
            return super().trans(other)
        return CircleLoop(self.count + other.count)

    def sym(self):
        return CircleLoop(-self.count)
