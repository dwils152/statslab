#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  12 18:41:17 2021

@author: dwils152
"""

#load_dataset() 

import numpy as np
import pandas as pd

def load_dataset():

    data = pd.read_csv('GSE135769_CTCF_TPM.txt', sep= '\t', header=0, index_col=0)

    data = data.iloc[:, 0:48]

    return data.to_numpy().T