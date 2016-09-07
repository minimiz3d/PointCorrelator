from math import sqrt, fabs

def distPointToPoint(p0, p1):
    x0, y0 = [float(n) for n in p0]
    x1, y1 = [float(n) for n in p1]
    d = sqrt((x1 - x0)**2 + (y1 - y0)**2)
    return d

def distPointToLine(point, line):
    start, end = [(float(x), float(y)) for x,y in line]
    l2 = distPointToPoint(start, end)**2
    if l2 == 0:
        return distPointToPoint(point, start)
    t = ((point[0] - start[0]) * \
         (end[0] - start[0]) + \
         (point[1] - start[1]) * \
         (end[1] - start[1])) / l2
    t = max(0, min(1, t))
    return distPointToPoint(point, \
           (start[0] + t*(end[0] - start[0]),\
            start[1] + t*(end[1] - start[1])))

