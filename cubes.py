# -*- coding: utf-8 -*-

''' Script to solve a particular puzzle with 4 cubes
    that have different colours on each side, and where
    the solutions is to align the cubes in a single row
    with unique colors showing on all the 4 long sides '''

from colorama import Back
import itertools


class Cube(object):
    'A single cube with different coloured faces'

    # cube faces
    face_keys = ('U', 'R', 'F', 'D', 'L', 'B', )

    # face colours
    cW, cB, cO, cG = range(4)

    # display colors
    colours = {cW: Back.WHITE,
               cB: Back.BLUE,
               cO: '\033[43m',
               cG: Back.GREEN
               }

    def __init__(self, cube_name, cube_faces):
        ''' cube_name: string to identify cube by
            cube_faces: dict with 6 entries, one per face, specifying color
                {'U' : W, 'L' : B, ..}
        '''

        assert isinstance(cube_name, str), \
            "cube_name is not a string: %s" % cube_name

        assert isinstance(cube_faces, dict), \
            "cube_faces must be a dict: %s" % cube_faces

        assert (len(cube_faces) == 6), \
            "cube_faces must be a dict of exactly 6 faces: %d" \
            % len(cube_faces)

        assert (set(cube_faces.keys()) == set(Cube.face_keys)), \
            "cube_faces must be exactly one of each from: %s" % Cube.face_keys

        self.cube_name = cube_name
        self.cube_faces = cube_faces

    def __repr__(self):
        BR = Back.RESET
        s = BR + self.cube_name + "\n"
        s = s + BR + "  "
        s = s + BR + Cube.colours[self.cube_faces['U']] + "  " + BR + "\n"
        s = s + BR + Cube.colours[self.cube_faces['L']] + "  "
        s = s + BR + Cube.colours[self.cube_faces['F']] + "  "
        s = s + BR + Cube.colours[self.cube_faces['R']] + "  "
        s = s + BR + Cube.colours[self.cube_faces['B']] + "  " + BR + "\n"
        s = s + BR + "  " + Cube.colours[self.cube_faces['D']] + "  "
        s = s + BR + "\n "
        s = s + BR
        return s


class Puzzle(object):
    'Represents the specific puzzle with 4 coloured cubes'

    CUBE_0 = Cube('CUBE_0', {'L': Cube.cW,
                             'F': Cube.cB,
                             'R': Cube.cB,
                             'B': Cube.cO,
                             'U': Cube.cG,
                             'D': Cube.cG,
                             })

    CUBE_1 = Cube('CUBE_1', {'L': Cube.cO,
                             'F': Cube.cO,
                             'R': Cube.cO,
                             'B': Cube.cG,
                             'U': Cube.cW,
                             'D': Cube.cB,
                             })

    CUBE_2 = Cube('CUBE_2', {'L': Cube.cG,
                             'F': Cube.cG,
                             'R': Cube.cW,
                             'B': Cube.cO,
                             'U': Cube.cW,
                             'D': Cube.cB,
                             })

    CUBE_3 = Cube('CUBE_3', {'L': Cube.cO,
                             'F': Cube.cO,
                             'R': Cube.cB,
                             'B': Cube.cW,
                             'U': Cube.cG,
                             'D': Cube.cW,
                             })

    CUBES = (CUBE_0,
             CUBE_1,
             CUBE_2,
             CUBE_3,
             )

    def __repr__(self):
        s = ''
        s = s + "- T - -\n"
        s = s + "L F R B\n"
        s = s + "- D - -\n"
        s = s + "\n"
        for c in self.CUBES:
            s = s + str(c) + "\n"
        return s

    def _cube_rots(self, cube):
        ''' returns all the possible rotations of the cube about axes
            passing through the 3 pairs of opposing faces
        '''

        def shift(seq, n=0):
            ''' shifts array elements N positions '''
            a = n % len(seq)
            return seq[-a:] + seq[:-a]

        rots = []
        rots.append(cube)

        # rotating about L-R axis
        mov = (cube.cube_faces['F'],
               cube.cube_faces['U'],
               cube.cube_faces['B'],
               cube.cube_faces['D'],
               )

        for i in range(1, 4):
            r = shift(mov, i)
            rCube = Cube(cube.cube_name + "_x_" + str(i),
                         {'L': cube.cube_faces['L'],
                          'R': cube.cube_faces['R'],
                          'F': r[0],
                          'U': r[1],
                          'B': r[2],
                          'D': r[3],
                          })
            rots.append(rCube)

        # rotating about F-B axis
        mov = (cube.cube_faces['L'],
               cube.cube_faces['U'],
               cube.cube_faces['R'],
               cube.cube_faces['D'],
               )

        for i in range(1, 4):
            r = shift(mov, i)
            rCube = Cube(cube.cube_name + "_z_" + str(i),
                         {'F': cube.cube_faces['F'],
                          'B': cube.cube_faces['B'],
                          'L': r[0],
                          'U': r[1],
                          'R': r[2],
                          'D': r[3],
                          })
            rots.append(rCube)

        # rotating around U-D axis
        mov = (cube.cube_faces['L'],
               cube.cube_faces['F'],
               cube.cube_faces['R'],
               cube.cube_faces['B'],
               )

        for i in range(1, 4):
            r = shift(mov, i)
            rCube = Cube(cube.cube_name + "_y_" + str(i),
                         {'U': cube.cube_faces['U'],
                          'D': cube.cube_faces['D'],
                          'L': r[0],
                          'F': r[1],
                          'R': r[2],
                          'B': r[3],
                          })
            rots.append(rCube)
        return rots

    def _all_rotations(self):
        ''' Prepares the lists of all the possible rotations of the cubes,
            but not the actual permutations.
        '''
        rotations = {}
        for cube in self.CUBES:
            rotations[cube.cube_name] = self._cube_rots(cube)
        return rotations

    def permutations(self):
        rots = self._all_rotations()
        from pprint import pprint
        pprint(rots)


if __name__ == '__main__':
    puzz = Puzzle()
    rots = puzz.permutations()
