#!/usr/bin/env python3
import pandas
import numpy as np
from pl_curve import calculate_cumulative_relative_abundance
from pl_curve import remove_cumulative_abundance_over_one


def setup_data():
    ''' setup some test data and
    remove all rows cumulative relative abundance has gone over 1
    '''
    # this should get the last item truncated
    data1 = np.array([['', 'Step I'],
                     ['219', 0.7],
                     ['218', 0.3],
                     ['217', 0.1]])

    # this should get no items truncacted as it adds to exactly 1
    data2 = np.array([['', 'Step II'],
                     ['219', 0.4],
                     ['218', 0.2],
                     ['217', 0.2]])

    # this should get no items truncated as it never reaches 1
    data3 = np.array([['', 'Step III'],
                     ['219', 0.1],
                     ['218', 0.2],
                     ['217', 0.2]])

    # create a dataframe, each sub list is one row
    df1 = pandas.DataFrame(data=data1[1:, 1:], index=data1[1:, 0],
                           columns=data1[0, 1:]).astype(np.dtype(np.float64))

    df2 = pandas.DataFrame(data=data2[1:, 1:], index=data2[1:, 0],
                           columns=data2[0, 1:]).astype(np.dtype(np.float64))

    df3 = pandas.DataFrame(data=data3[1:, 1:], index=data3[1:, 0],
                           columns=data3[0, 1:]).astype(np.dtype(np.float64))

    samples = [df1, df2, df3]

    samples = calculate_cumulative_relative_abundance(samples)
    result = remove_cumulative_abundance_over_one(samples)

    return result


def test_remove_cumulative_abundance_over_one_toolong():
    '''test the scenario where one item was removed'''
    result = setup_data()

    assert len(result[0]['Cum Rel Abund']) == 2


def test_remove_cumulative_abundance_over_one_justright():
    '''test the scenario where everything addedto exactly one,
    nothing should be removed'''
    result = setup_data()

    assert len(result[1]['Cum Rel Abund']) == 3


def test_remove_cumulative_abundance_over_one_toofew():
    '''test the scenario where everything added to less than one,
    nothing should be removed'''
    result = setup_data()

    assert len(result[2]['Cum Rel Abund']) == 3
