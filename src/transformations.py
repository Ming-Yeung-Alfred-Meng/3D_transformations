import numpy as np
from typing import Union


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
