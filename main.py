import pygame
import numpy as np
import sys
from typing import Tuple

# TODO: may need to change this such that it takes in an entire array and vectorize it.
def cartesian_to_pygame(window_height: int, coordinates: Tuple[float, float]) -> Tuple[float, float]:
    """
    Turn a point defined using the bottom left corner of the pygame window as the origin to those in pygame's coordinate
    system.
    :param window_height:
    :param coordinates:
    :return: points in pygame's coordinate system
    """
    return coordinates[0], window_height - coordinates[1]


def rotation():
    pass


def translation():
    pass


def scale():
    pass


def init_cube(center: np.ndarray, half_width: float, half_height: float, half_depth: float) -> Tuple[np.ndarray, np.ndarray]:
    assert len(center.shape) == 3

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


def project_onto_screen(camera_location: np.ndarray, vertices: np.ndarray):
    assert len(vertices.shape) == 2, "Dimension of the array of vertices must be 2."
    assert vertices.shape[1] == 4, "Second dimension of the array of vertices must be 4."

    return vertices @ np.array([[-camera_location[2], 0, 0],
                                [0, -camera_location[2], 0],
                                [camera_location[0], camera_location[1], 1],
                                [0, 0, -camera_location[2]]])


def draw_cuboid(screen: pygame.Surface, vertices: np.ndarray, faces: np.ndarray, screen_height: int):
    assert vertices.shape[1] == 2
    assert vertices.dtype == np.float64


    for face in faces:
        for i in range(face.shape[0]):
            pygame.draw.aaline(screen, (0, 0, 0),
                               cartesian_to_pygame(screen_height, vertices[face[i]]),
                               cartesian_to_pygame(screen_height, vertices[face[(i + 1) % face.shape[0]]]))


def cartesian_to_homogeneous(vertices: np.ndarray):
    return np.concatenate((vertices, np.ones((vertices.shape[0], 1))), axis=1)


def homogeneous_to_cartesian(vertices: np.ndarray):
    return vertices /


def start_environment(screen_width, screen_height, vertices, faces):
    vertices = cartesian_to_homogeneous(vertices)

    screen_vertices = project_onto_screen(camera_location, vertices)

    pygame.init()

    screen = pygame.display.set_mode((screen_width, screen_height))

    screen.fill((255, 255, 255))

    draw_cuboid(screen, screen_vertices, faces, screen_height)

    pygame.display.update()


def run(screen_width, screen_height):
    vertices, faces = init_cube(np.array([300, 300, 300]), 50, 50, 50)
    start_environment(screen_width, screen_height, vertices, faces)


if __name__ == '__main__':
    run()
