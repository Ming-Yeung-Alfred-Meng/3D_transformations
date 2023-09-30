import sys
from typing import Tuple, Union

import pygame
import numpy as np

from src.change_of_coordinates import cartesian_to_pygame


def init_cuboid(center: np.ndarray,
                half_width: Union[int, float],
                half_height: Union[int, float],
                half_depth: Union[int, float]) -> Tuple[np.ndarray, np.ndarray]:
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

    vertices_to_draw = cartesian_to_pygame(vertices, screen_height)

    for face in faces:
        for i in range(face.shape[0]):
            pygame.draw.aaline(screen, (0, 0, 0),
                               vertices_to_draw[face[i]],
                               vertices_to_draw[face[(i + 1) % face.shape[0]]])


def start_environment(screen_width: int, screen_height: int, vertices: np.ndarray, faces: np.ndarray) -> None:
    """
    Begin the game loop.
    :param screen_width: width of the PyGame screen
    :param screen_height: height of the PyGame screen
    :param vertices: v x 3 matrix of vertices of the object to display
    :param faces: f x 4 matrix of vertices of face indices of the object
    :return: None
    """
    assert len(vertices.shape) == 2
    assert vertices.shape[1] == 3
    assert len(faces.shape) == 2
    assert faces.shape[1] == 4

    pygame.init()

    screen = pygame.display.set_mode((screen_width, screen_height))

    screen.fill((255, 255, 255))

    draw_wireframe(screen, orthographic_projection(vertices), faces, screen_height)

    pygame.display.update()


def run(screen_width: int, screen_height: int) -> None:
    vertices, faces = init_cuboid(np.array([300, 300, 300]), 50, 50, 50)
    start_environment(screen_width, screen_height, vertices, faces)
