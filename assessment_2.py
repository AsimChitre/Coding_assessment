"""Finding the area of quadrilateral as well as which is the given quadrilateral"""

# importing libraries
import numpy as np
from numpy.linalg import norm
from ast import literal_eval


def get_area(ordered_coordinate):
    vertices = ordered_coordinate.T     # taking transpose of matrix
    intermediate = vertices[0, 0] * vertices[1, 1] + vertices[0, 1] * vertices[1, 2] + vertices[0, 2] * vertices[1, 3] + vertices[0, 3] * vertices[1, 0]
    intermediate_2 = vertices[0, 1] * vertices[1, 0] + vertices[0, 2] * vertices[1, 1] + vertices[0, 3] * vertices[1, 2] + vertices[0, 0] * vertices[1, 3]
    return 0.5 * np.abs(intermediate - intermediate_2)


def get_ordering_of_points(x, y):

    # get centroid
    x0 = np.mean(x)
    y0 = np.mean(y)

    # finding polar coordinates
    r = np.sqrt((x - x0) ** 2 + (y - y0) ** 2)

    angles = np.where(
        (y - y0) > 0, np.arccos((x - x0) / r), 2 * np.pi - np.arccos((x - x0) / r)
    )

    mask = np.argsort(angles)

    x_sorted = x[mask]
    y_sorted = y[mask]

    ordered_coords = np.hstack([x_sorted.reshape(-1, 1), y_sorted.reshape(-1, 1)])  # combining x and y
    ordered_coords = ordered_coords[::-1, :]   # clockwise order
    return ordered_coords


def get_shape(ordered_coord):
    homogeneous = np.hstack([ordered_coordinates, np.ones((4, 1))])  # 4 is number of points (4,1) matrix

    # create diagonal line equations
    diagonal_line_1 = np.cross(homogeneous[0], homogeneous[2])  # 2 homogenous equation cross product - line equation
    diagonal_line_2 = np.cross(homogeneous[1], homogeneous[3])

    diagonal_1_length = norm(ordered_coord[0] - ordered_coord[2])
    diagonal_2_length = norm(ordered_coord[1] - ordered_coord[3])

    diagonal_intersection_pt = np.cross(diagonal_line_1, diagonal_line_2)
    # retrieve intersection point coordinates by dividing scale from first 2 coordinates
    diagonal_intersection_pt = diagonal_intersection_pt / diagonal_intersection_pt[-1]
    # to get original co-ordinates , divide by last entry in the homogenous coordinate

    # find distances from diagonal intersection point to 4 vertices
    intersection_to_1_len = norm(diagonal_intersection_pt[:2] - ordered_coord[0])
    intersection_to_3_len = norm(diagonal_intersection_pt[:2] - ordered_coord[2])
    intersection_to_2_len = norm(diagonal_intersection_pt[:2] - ordered_coord[1])
    intersection_to_4_len = norm(diagonal_intersection_pt[:2] - ordered_coord[3])

    # find angle between diagonal lines
    diagonal_intersection_angle = np.arccos(
        np.dot(ordered_coord[0] - ordered_coord[2], ordered_coord[1] - ordered_coord[3])
        / (
            norm(ordered_coord[0] - ordered_coord[2])
            * norm(ordered_coord[1] - ordered_coord[3])
        )
    )

#line equation of all sides of a quadrilateral
    side_eq_1 = np.cross(homogeneous[0], homogeneous[1])
    side_eq_2 = np.cross(homogeneous[1], homogeneous[2])
    side_eq_3 = np.cross(homogeneous[2], homogeneous[3])
    side_eq_4 = np.cross(homogeneous[3], homogeneous[0])

    # conditions for different shapes
    if (
        np.cross(side_eq_1, side_eq_3)[-1] == 0
        and np.cross(side_eq_2, side_eq_4)[-1] == 0
        and intersection_to_1_len == intersection_to_3_len
        and intersection_to_2_len == intersection_to_4_len
    ):  # check if bisects
        if diagonal_1_length == diagonal_2_length:
            if diagonal_intersection_angle == np.pi / 2:
                return "Square"
            return "Rectangle"
        else:
            if diagonal_intersection_angle == np.pi / 2:
                return "Rhombus"
            return "Parallelogram"
    elif (
        intersection_to_1_len == intersection_to_3_len
        or intersection_to_2_len == intersection_to_4_len
    ):
        return "Kite"
    elif (
        np.cross(side_eq_1, side_eq_3)[-1] == 0
        and np.cross(side_eq_2, side_eq_4)[-1] != 0
    ) or (
        np.cross(side_eq_1, side_eq_3)[-1] != 0
        and np.cross(side_eq_2, side_eq_4)[-1] == 0
    ):
        return "Trapezoid"
    else:
        return "Other"


if __name__ == '__main__':
    user_input = input().split()
    coordinates = np.array([literal_eval(coords) for coords in user_input])
    ordered_coordinates = get_ordering_of_points(coordinates[:,0], coordinates[:,1])
    get_shape_of_quad = get_shape(ordered_coordinates)
    if get_shape_of_quad == 'Other':
        print("Other -1")
    else:
        area = get_area(ordered_coordinates)
        print("{} {:.0f}".format(get_shape_of_quad,area))


