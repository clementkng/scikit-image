from __future__ import print_function, division

import numpy as np

from ._set_metrics import hausdorff_distance_onesided


def hausdorff_distance(a, b):
    """
    Calculate the Hausdorff distance [1]_ between two sets of points.

    The Hausdorff distance is the maximum distance between any point on
    ``a`` and its nearest point on ``b``, and vice-versa.

    Parameters
    ----------
    a, b : ndarray, dtype=bool
        Arrays where ``True`` represents a point that is included in a
        set of points. Both arrays must have the same shape.

    Returns
    -------
    distance : float
        The Hausdorff distance between sets ``a`` and ``b``, using
        Euclidian distance to calculate the distance between points in ``a``
        and ``b``.

    References
    ----------
    .. [1] http://en.wikipedia.org/wiki/Hausdorff_distance
    """
    if a.dtype != np.bool or b.dtype != np.bool:
        raise ValueError('Arrays must have dtype = \'bool\'')
    if a.shape != b.shape:
        raise ValueError('Array shapes must be identical')

    a_points = np.transpose(np.nonzero(a))
    b_points = np.transpose(np.nonzero(b))

    if a_points.ndim != 2 or b_points.ndim != 2:
        raise ValueError('Both input arrays must be two-dimensional')
    if a_points.shape[1] != b_points.shape[1]:
        raise ValueError('Second dimension of the arrays must be equal')

    # Handle empty sets properly
    if a_points.shape[0] == 0 or b_points.shape[0] == 0:
        if a_points.shape[0] == b_points.shape[0]:
            # Both sets are empty and thus the distance is zero
            return 0.
        else:
            # Exactly one set is empty; the distance is infinite
            return np.inf

    a_points = np.require(a_points, np.float64, ['C'])
    b_points = np.require(b_points, np.float64, ['C'])
    return max(hausdorff_distance_onesided(a_points, b_points),
               hausdorff_distance_onesided(b_points, a_points))
