from math import ceil
import copy


def rotate_90_degree_clckwise(matrix):
    """ Get a matrix rotated 90 degrees clockwise. """
    rot_matrix = []
    for i in range(len(matrix[0])):
        li = list(map(lambda x: x[i], matrix))
        li.reverse()
        rot_matrix.append(li)

    return rot_matrix


def x_symmetry(matrix):
    """ Get reflection of matrix in the x-axis. """
    sym_matrix = [x[:] for x in matrix]
    height = len(matrix)
    start = ceil(height/2)
    reflect = start - 1 - height % 2
    for i in range(start, height):
        sym_matrix[i] = matrix[reflect]
        reflect -= 1
    return sym_matrix


def y_symmetry(matrix):
    """ Get reflection of matrix in the y-axis. """
    # sym_matrix = copy.deepcopy(matrix)
    sym_matrix = [x[:] for x in matrix]
    width = len(sym_matrix[0])
    start = ceil(width/2)
    reflect = start - 1 - width % 2
    for i in range(start, width):
        reflect_column = get_column(sym_matrix, reflect)
        sym_matrix = set_column(sym_matrix, i, reflect_column)
        reflect -= 1
    return sym_matrix


def show_rows(matrix):
    """ Print matrix. """
    string = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*string)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in string]
    print('\n'.join(table))


def get_matrix(array):
    """ Return 3x3 matrix based on pattern array. """
    return [array[0:3], [array[3], ' ', array[4]], array[5:8]]


def get_column(matrix, i):
    """ Return column of matrix. """
    return [row[i] for row in matrix]


def set_column(m, i, v):
    """ Return matrix with a replaced column. """
    for x, row in enumerate(m):
        row[i] = v[x]
    return m
