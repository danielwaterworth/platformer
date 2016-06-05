class HLine(object):
    def __init__(self, x0, x1, y):
        self.x0 = x0
        self.x1 = x1
        assert x0 <= x1
        self.y = y

    def collide_hline(self, hline):
        if self.y != hline.y:
            return False
        return not (self.x1 < hline.x0 or hline.x1 < self.x0)

    @property
    def p0(self):
        return (self.x0, self.y)

    @property
    def p1(self):
        return (self.x1, self.y)

#
#    x1 x0  w
# y0     *-----*
#       /     /
#      /     /
#     /     /
# y1 *-----*
#

class HParallelogram(object):
    def __init__(self, x0, x1, w, y0, y1):
        self.x0 = x0
        self.x1 = x1
        self.w = w
        self.y0 = y0
        self.y1 = y1
        if y0 > y1:
            self.x0, self.x1 = self.x1, self.x0
            self.y0, self.y1 = self.y1, self.y0
        assert w >= 0

    @property
    def points(self):
        return [
            (self.x0, self.y0),
            (self.x0 + self.w, self.y0),
            (self.x1 + self.w, self.y1),
            (self.x1, self.y1)
        ]

    def collide_hline(self, hline):
        if hline.y > self.y1 or hline.y < self.y0:
            return False

        x0 = self.x0 + int((hline.y - self.y0)*(self.x1 - self.x0)/(self.y1 - self.y0))
        x1 = x0 + self.w
        return hline.collide_hline(HLine(x0, x1, hline.y))
