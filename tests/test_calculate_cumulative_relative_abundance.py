#!/usr/bin/env python3
from pl_curve import calculate_cumulative_relative_abundance
import pandas
import numpy as np


def test_calculate_cumulative_relative_abundance():

    data1 = np.array([['', 'Step I'],
                     ['219', 0.239709],
                     ['218', 0.190986]])

    data2 = np.array([['', 'Step II'],
                     ['219', 0.434289],
                     ['218', 0.193835]])

    # create a dataframe, each sub list is one row
    df1 = pandas.DataFrame(data=data1[1:, 1:], index=data1[1:, 0],
                           columns=data1[0, 1:]).astype(np.dtype(np.float64))

    df2 = pandas.DataFrame(data=data2[1:, 1:], index=data2[1:, 0],
                           columns=data2[0, 1:]).astype(np.dtype(np.float64))

    samples = [df1, df2]

    result = calculate_cumulative_relative_abundance(samples)

    df1_res = result[0]
    df2_res = result[1]

    assert 'Cum Rel Abund' in df1_res.columns
    assert 'Cum Rel Abund' in df2_res.columns

    assert df1_res.loc['219', 'Cum Rel Abund'] == 0.239709
    assert df1_res.loc['218', 'Cum Rel Abund'] == 0.430695

    assert df2_res.loc['219', 'Cum Rel Abund'] == 0.434289
    assert df2_res.loc['218', 'Cum Rel Abund'] == 0.628124
