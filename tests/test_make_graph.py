#!/usr/bin/env python3
from pl_curve import make_graph
import pandas
import numpy as np
import os


def test_make_graph():
    data1 = np.array([['', 'Step I', 'Cum Prop TRFs', 'Cum Rel Abund'],
                     ['219', 0.239709, 0.5, 0.3],
                     ['218', 0.190986, 1.0, 1.0]])

    data2 = np.array([['', 'Step II', 'Cum Prop TRFs', 'Cum Rel Abund'],
                     ['219', 0.434289, 0.5, 0.4],
                     ['218', 0.193835, 1.0, 1.0]])

    # create a dataframe, each sub list is one row
    df1 = pandas.DataFrame(data=data1[1:, 1:], index=data1[1:, 0],
                           columns=data1[0, 1:]).astype(np.dtype(np.float64))

    df2 = pandas.DataFrame(data=data2[1:, 1:], index=data2[1:, 0],
                           columns=data2[0, 1:]).astype(np.dtype(np.float64))

    samples = [df1, df2]

    # delete test.png if it already exists
    try:
        os.remove("test.png")
    # catch the error if file doesn't exist
    except FileNotFoundError as error:
        pass

    make_graph(samples, "test.png")
    assert os.path.isfile("test.png") is True
