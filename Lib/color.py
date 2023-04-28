import colorsys
import numpy as np


def generate_color(num_Color:int) -> list:
    """ https://github.com/qqwweee/keras-yolo3/blob/master/yolo.py#L82-L91  """
    hsv_tuples = [(x / num_Color, 1., 1.) for x in range(num_Color)]
    colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
    colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), colors))
    np.random.seed(10101)       # Fixed seed for consistent colors across runs.
    np.random.shuffle(colors)   # Shuffle colors to decorrelate adjacent classes.
    np.random.seed(None)        # Reset seed to default

    return colors
