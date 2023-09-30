import sys
from typing import Tuple, Union

import pygame
import numpy as np


# TODO: may need to change this such that it takes in an entire array and vectorize it.
def cartesian_to_pygame(coordinates: np.ndarray, screen_height: int, ) -> np.ndarray:
    """
    Turn a point defined using the bottom left corner of the pygame window as the origin to those in pygame's coordinate
    system.
    :param coordinates: n x 2 matrix of vertices with bottom left corner of the PyGame window as origin
    :param screen_height: height of the PyGame window
    :return: points in pygame's coordinate system
    """
    result = coordinates.copy()
    result[:, 1] *= -1
    result[:, 1] += screen_height
    return result


def rotation_about_x(center: np.ndarray, vertices: np.ndarray, degree: float) -> None:
    """
    Rotate (and mutate) vertices about the x-axis.
    :param center: 3D array of the center of the object vertices represent
    :param vertices: v x 3 matrix of vertices
    :param degree: degree in radian to rotate
    :return: None
    """
    vertices -= center
    vertices @= np.array([[1, 0, 0],
                          [0, np.cos(degree), -np.sin(degree)],
                          [0, np.sin(degree), np.cos(degree)]])
    vertices += center


def rotation_about_y(center: np.ndarray, vertices: np.ndarray, degree: float) -> None:
    """
    Rotate (and mutate) vertices about the y-axis.
    :param center: 3D array of the center of the object vertices represent
    :param vertices: v x 3 matrix of vertices
    :param degree: degree in radian to rotate
    :return: None
    """
    vertices -= center
    vertices @= np.array([[np.cos(degree), 0, np.sin(degree)],
                          [0, 1, 0],
                          [-np.sin(degree), 0, np.cos(degree)]])
    vertices += center


def rotation_about_z(center: np.ndarray, vertices: np.ndarray, degree: float) -> None:
    """
    Rotate (and mutate) vertices about the z-axis.
    :param center: 3D array of the center of the object vertices represent
    :param vertices: v x 3 matrix of vertices
    :param degree: degree in radian to rotate
    :return: None
    """
    vertices -= center
    vertices @= np.array([[np.cos(degree), -np.sin(degree), 0],
                          [np.sin(degree), np.cos(degree), 0],
                          [0, 0, 1]])
    vertices += center


def translation(vertices: np.ndarray, step: Union[int, float], axis: int) -> None:
    """
    Translate (and mutate) vertices along an axis in the positive direction if step is positive, and vice versa.
    :param vertices: n x 3 matrix of vertices in world cartesian coordinate
    :param step: number to translate by
    :param axis: axis along which to translate
    """
    assert len(vertices.shape) == 2
    assert vertices.shape[1] == 3
    assert 0 <= axis <= 2

    vertices[:, axis] += step


def uniform_scale(center: np.ndarray, vertices: np.ndarray, scale: Union[int, float]) -> None:
    """
    Uniformly scale (and mutate) vertices.
    :param center: center of the object 'vertices' represents
    :param vertices: v x 3 matrix of vertices
    :param scale: scale factor
    :return: None
    """
    vertices -= center
    vertices *= scale
    vertices += center



def init_cuboid(center: np.ndarray, half_width: float, half_height: float, half_depth: float) \
        -> Tuple[np.ndarray, np.ndarray]:
    """
    Initialize a 3D cuboid.
    :param center: length 3 array of the center of the cuboid
    :param half_width: half of the width of the cuboid, i.e. length in x
    :param half_height: half of the height of the cuboid, i.e. length in y
    :param half_depth: half of the depth of the cuboid, i.e. length in z
    :return: 8 x 3 matrix of vertices of the cuboid, 6 x 4 matrix of face indices
    """
    assert len(center.shape) == 1
    assert len(center) == 3
    assert center.dtype == np.float64

    x, y, z = np.meshgrid((center[0] + half_width, center[0] - half_width),
                          (center[1] + half_height, center[1] - half_height),
                          (center[2] + half_depth, center[2] - half_depth), copy=True)

    return (np.column_stack((x.flatten(), y.flatten(), z.flatten())),
            np.array([[0, 4, 6, 2],
                      [1, 3, 7, 5],
                      [0, 2, 3, 1],
                      [0, 1, 5, 4],
                      [1, 3, 7, 5],
                      [2, 6, 7, 3]]))


def perspective_projection(camera_location: np.ndarray, vertices: np.ndarray) -> np.ndarray:
    """
    Perspective projection of 3D vertices in world cartesian coordinate to the frame of the x-y plane.
    :param camera_location: array of camara location in world frame
    :param vertices: n x 3 matrix of vertices in world frame
    :return: n x 2 matrix of vertices in the frame of the x-y plane
    """
    assert len(camera_location.shape) == 1
    assert len(vertices.shape) == 2
    assert vertices.shape[1] == 4
    assert vertices.dtype == np.float64

    return vertices @ np.array([[-camera_location[2], 0, 0],
                                [0, -camera_location[2], 0],
                                [camera_location[0], camera_location[1], 1],
                                [0, 0, -camera_location[2]]])


def orthographic_projection(vertices: np.ndarray) -> np.ndarray:
    """
    Orthographic projection of 3D vertices in world cartesian coordinate to the frame of the x-y plane.
    :param vertices: n x 3 vertices to project
    :return: n x 2 projected vertices, i.e. **VIEW** into first two columns of 'vertices'
    """
    assert len(vertices.shape) == 2
    assert vertices.shape[1] == 3

    return vertices[:, 0:2]


def draw_wireframe(screen: pygame.Surface, vertices: np.ndarray, faces: np.ndarray, screen_height: int) -> None:
    """
    Draw the 2D projected image of the wireframe of a 3D mesh onto the PyGame surface.
    :param screen: pygame Surface
    :param vertices: n x 2 matrix of projected vertices of the wireframe
    :param faces: m x 4 matrix of face indices
    :param screen_height: height of the surface
    :return None
    """
    assert len(vertices.shape) == 2
    assert vertices.shape[1] == 2
    assert vertices.dtype == np.float64

    vertices_to_draw = cartesian_to_pygame(vertices, screen_height)

    for face in faces:
        for i in range(face.shape[0]):
            pygame.draw.aaline(screen, (0, 0, 0),
                               vertices_to_draw[face[i]],
                               vertices_to_draw[face[(i + 1) % face.shape[0]]])


def cartesian_to_homogeneous(vertices: np.ndarray) -> np.ndarray:
    """
    Turn vertices from cartesian to homogeneous representation.
    :param vertices: n x d matrix of vertices in cartesian coordinate
    :return: n x (d + 1) matrix of vertices in homogeneous coordinate
    """
    assert len(vertices.shape) == 2
    assert vertices.dtype == np.float64

    return np.concatenate((vertices, np.ones((vertices.shape[0], 1))), axis=1)


def homogeneous_to_cartesian(vertices: np.ndarray) -> np.ndarray:
    """
    Turn vertices from homogeneous representation to cartesian representation.
    :param vertices: n x d matrix of vertices in homogeneous coordinate
    :return: n x (d - 1) matrix of vertices in cartesian coordinate
    """
    assert len(vertices.shape) == 2
    assert vertices.dtype == np.float64

    return vertices[:, 0:-1] / vertices[:, -1][:, None]


def start_environment(screen_width: int, screen_height: int, vertices: np.ndarray, faces: np.ndarray) -> None:
    """
    Begin the game loop.
    :param screen_width: width of the PyGame screen
    :param screen_height: height of the PyGame screen
    :param vertices: v x 3 matrix of vertices of the object to display
    :param faces: f x 4 matrix of vertices of face indices of the object
    :return: None
    """
    pygame.init()

    screen = pygame.display.set_mode((screen_width, screen_height))

    screen.fill((255, 255, 255))

    draw_wireframe(screen, orthographic_projection(vertices), faces, screen_height)

    pygame.display.update()


def run(screen_width: int, screen_height: int) -> None:
    vertices, faces = init_cuboid(np.array([300, 300, 300]), 50, 50, 50)
    start_environment(screen_width, screen_height, vertices, faces)


if __name__ == '__main__':
    run(800, 800)
