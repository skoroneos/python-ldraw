#!/usr/bin/env python

import math

class MatrixError(Exception):

    pass


class Axis:
    pass

class XAxis(Axis):
    pass

class YAxis(Axis):
    pass

class ZAxis(Axis):
    pass

class AngleUnits:
    pass

class Radians(AngleUnits):
    pass

class Degrees(AngleUnits):
    pass

class Colour:
    def __init__(self, value):
        self.value = value

Black = Colour(0)
Blue = Colour(1)
Green = Colour(2)
Red = Colour(4)
DarkOrange = Colour(6)
Grey = Colour(7)
DarkGrey = Colour(8)
LightRed = Colour(12)
Pink = Colour(13)
Yellow = Colour(14)
White = Colour(15)
LightGreen = Colour(17)
DarkPurple = Colour(22)
Orange = Colour(25)
Purple = Colour(26)

class Matrix:

    def __init__(self, rows):
    
        self.rows = rows
    
    def __repr__(self):
    
        values = reduce(lambda x, y: x + y, self.rows)
        format = ("((%f, %f, %f),\n"
                  " (%f, %f, %f),\n"
                  " (%f, %f, %f))")
        return format % tuple(values)
    
    def ___mul___(self, r1, r2):
    
        rows = [[r1[0][0]*r2[0][0] + r1[0][1]*r2[1][0] + r1[0][2]*r2[2][0],
                 r1[0][0]*r2[0][1] + r1[0][1]*r2[1][1] + r1[0][2]*r2[2][1],
                 r1[0][0]*r2[0][2] + r1[0][1]*r2[1][2] + r1[0][2]*r2[2][2]],
                [r1[1][0]*r2[0][0] + r1[1][1]*r2[1][0] + r1[1][2]*r2[2][0],
                 r1[1][0]*r2[0][1] + r1[1][1]*r2[1][1] + r1[1][2]*r2[2][1],
                 r1[1][0]*r2[0][2] + r1[1][1]*r2[1][2] + r1[1][2]*r2[2][2]],
                [r1[2][0]*r2[0][0] + r1[2][1]*r2[1][0] + r1[2][2]*r2[2][0],
                 r1[2][0]*r2[0][1] + r1[2][1]*r2[1][1] + r1[2][2]*r2[2][1],
                 r1[2][0]*r2[0][2] + r1[2][1]*r2[1][2] + r1[2][2]*r2[2][2]]]
        
        return rows
    
    def __mul__(self, other):
    
        if isinstance(other, Matrix):
        
            r1 = self.rows
            r2 = other.rows
            return Matrix(self.___mul___(r1, r2))
        
        elif isinstance(other, Vector):
        
            r = self.rows
            x, y, z = other.x, other.y, other.z
            return Vector(r[0][0] * x + r[0][1] * y + r[0][2] * z,
                          r[1][0] * x + r[1][1] * y + r[1][2] * z,
                          r[2][0] * x + r[2][1] * y + r[2][2] * z)
        else:
            raise MatrixError
    
    def __rmul__(self, other):
    
        if isinstance(other, Matrix):
        
            r1 = other.rows
            r2 = self.rows
            return Matrix(self.___mul___(r1, r2))
        
        elif isinstance(other, Vector):
        
            r = self.rows
            x, y, z = other.x, other.y, other.z
            return Vector(x * r[0][0] + y * r[1][0] + z * r[2][0],
                          x * r[0][1] + y * r[1][1] + z * r[2][1],
                          x * r[0][2] + y * r[1][2] + z * r[2][2])
        else:
            raise MatrixError
    
    def copy(self):
    
        return Matrix(copy.deepcopy(self.rows))
    
    def rotate(self, angle, axis, units = Degrees):
    
        if units == Degrees:
            c = math.cos(angle/180.0 * math.pi)
            s = math.sin(angle/180.0 * math.pi)
        else:
            c = math.cos(angle)
            s = math.sin(angle)
        
        if axis == XAxis:
            rotation = Matrix([[1, 0, 0], [0, c, -s], [0, s, c]])
        elif axis == YAxis:
            rotation = Matrix([[c, 0, -s], [0, 1, 0], [s, 0, c]])
        elif axis == ZAxis:
            rotation = Matrix([[c, -s, 0], [s, c, 0], [0, 0, 1]])
        else:
            raise MatrixError, "Invalid axis specified."
        
        return rotation * self


def Identity():

    return Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])


class Vector:

    def __init__(self, x, y, z):
    
        self.x, self.y, self.z = x, y, z
    
    def __repr__(self):
    
        return "<Vector: (%f, %f, %f)>" % (self.x, self.y, self.z)
    
    def __add__(self, other):
    
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        
        # Return a new object.
        return Vector(x, y, z)
    
    __radd__ = __add__
    
    def __sub__(self, other):
    
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        
        # Return a new object.
        return Vector(x, y, z)
    
    def __rsub__(self, other):
    
        x = other.x - self.x
        y = other.y - self.y
        z = other.z - self.z
        
        # Return a new object.
        return Vector(x, y, z)
    
    def __cmp__(self, other):
    
        # This next expression will only return zero (equals) if all
        # expressions are false.
        return self.x == other.x or self.y == other.y or self.z == other.z
    
    def __abs__(self):
    
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5
    
    def copy(self):
    
        """vector = copy(self)
        
        Copy the vector so that new vectors containing the same values
        are passed around rather than references to the same object.
        """
        
        return Vector(self.x, self.y, self.z)


class Piece:

    def __init__(self, colour, position, matrix, part):
    
        self.position = position
        self.colour = colour
        self.matrix = matrix
        self.part = part.upper()
    
    def __repr__(self):
    
        return ("1 %i " % self.colour.value) + \
                ("%f " * 3) % (self.position.x, self.position.y, self.position.z) + \
                ("%f " * 9) % tuple(reduce(
                    lambda row1, row2: row1 + row2, self.matrix.rows
                    )) + \
                ("%s.DAT" % self.part)

class Person:

    def __init__(self, position = None, matrix = None):
    
        self.position = position or Vector(0, 0, 0)
        self.matrix = matrix or Identity()
        self.pieces_info = {}
    
    def head(self, colour, part = "3626BPS5"):
    
        # Displacement from torso
        displacement = self.matrix * Vector(0, -24, 0)
        return Piece(colour, self.position + displacement, self.matrix, part)
    
    def torso(self, colour, part = "973"):
    
        return Piece(colour, self.position, self.matrix, part)
    
    def hips_and_legs(self, colour, part = "970C00"):
    
        # Displacement from torso
        displacement = self.matrix * Vector(0, 32, 0)
        return Piece(colour, self.position + displacement, self.matrix, part)
    
    def hips(self, colour, part = "970"):
    
        # Displacement from torso
        displacement = self.matrix * Vector(0, 32, 0)
        return Piece(colour, self.position + displacement, self.matrix, part)
    
    def left_arm(self, colour, angle, part = "981"):
    
        self.pieces_info["left arm"] = angle
        
        # Displacement from torso
        displacement = self.matrix * Vector(15, 8, 0)
        return Piece(colour, self.position + displacement,
                     self.matrix * Identity().rotate(-10, ZAxis) *
                     Identity().rotate(angle, XAxis), part)
    
    def left_hand(self, colour, angle, part = "983"):
    
        try:
            arm_angle = self.pieces_info["left arm"]
        except KeyError:
            return
        
        # Displacement from torso
        displacement = self.matrix * Vector(19, 8, 0) + (
            self.matrix * Identity().rotate(-10, ZAxis) *
            Identity().rotate(arm_angle, XAxis) * Vector(0, 17, -9)
            )
        return Piece(colour, self.position + displacement,
                     self.matrix * Identity().rotate(-10, ZAxis) *
                     Identity().rotate(arm_angle + 40, XAxis) *
                     Identity().rotate(angle, ZAxis), part)
    
    def right_arm(self, colour, angle, part = "982"):
    
        self.pieces_info["right arm"] = angle
        
        # Displacement from torso
        displacement = self.matrix * Vector(-15, 8, 0)
        return Piece(colour, self.position + displacement,
                     self.matrix * Identity().rotate(10, ZAxis) *
                     Identity().rotate(angle, XAxis), part)
    
    def right_hand(self, colour, angle, part = "983"):
    
        try:
            arm_angle = self.pieces_info["right arm"]
        except KeyError:
            return
        
        # Displacement from torso
        displacement = self.matrix * Vector(-19, 8, 0) + (
            self.matrix * Identity().rotate(10, ZAxis) *
            Identity().rotate(arm_angle, XAxis) * Vector(0, 17, -9)
            )
        return Piece(colour, self.position + displacement,
                     self.matrix * Identity().rotate(10, ZAxis) *
                     Identity().rotate(arm_angle + 40, XAxis) *
                     Identity().rotate(angle, ZAxis), part)
    
    def left_leg(self, colour, angle, part = "972"):
    
        # Displacement from torso
        displacement = self.matrix * Vector(0, 44, 0)
        return Piece(colour, self.position + displacement,
                     self.matrix * Identity().rotate(angle, XAxis), part)
    
    def right_leg(self, colour, angle, part = "971"):
    
        # Displacement from torso
        displacement = self.matrix * Vector(0, 44, 0)
        return Piece(colour, self.position + displacement,
                     self.matrix * Identity().rotate(angle, XAxis), part)


def test():

    import random
    random.seed()
    
    for x in range(-100, 200, 100):
        for z in range(-100, 200, 100):
        
            orientation = Identity()
            orientation = orientation.rotate(random.randrange(0, 360), XAxis)
            orientation = orientation.rotate(random.randrange(0, 360), YAxis)
            orientation = orientation.rotate(random.randrange(0, 360), ZAxis)
            
            figure = Person(Vector(x, 0, z), orientation)
            print figure.head(Yellow)
            print figure.torso(LightGreen, "973P90")
            print figure.hips(Blue)
            angle = random.randrange(-90, 60)
            print figure.left_leg(Red, angle)
            angle = random.randrange(-90, 60)
            print figure.right_leg(Green, angle)
            angle = random.randrange(-120, 60)
            print figure.left_arm(Red, angle)
            angle = random.randrange(-90, 90)
            print figure.left_hand(Yellow, angle)
            angle = random.randrange(-120, 60)
            print figure.right_arm(Green, angle)
            angle = random.randrange(-90, 90)
            print figure.right_hand(Yellow, angle)
            print


if __name__ == "__main__":

    test()