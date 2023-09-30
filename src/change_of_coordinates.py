import numpy as np


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


def cartesian_to_pygame(coordinates: np.ndarray, screen_height: int) -> np.ndarray:
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
