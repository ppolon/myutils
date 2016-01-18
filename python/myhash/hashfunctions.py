# hashfunctions.py
# Author: Jonghyun Choi (jonghyun.choi@cable.comcast.com)
# Date created: 11/16/2015
# Date last modified: 11/16/2015
# Python ver: 2.7.10

import os, os.path
import numpy as np

import sys
import os
import pdb

import time

import types
import scipy.io as sio
import math


def bin2intFromNP(a):
    a = a.flatten()
    if a.shape[0] == 0:
        return a

    la = a.shape[0]
    out = np.zeros(la/32)
    b = a
    for i in range(la-1,-1,-1):
        c = a[i]
        if c != 0 and c != 1:
            print 'error: input should only contain 0 or 1'
            return -1
        out[(la-1-i)/32] += c*(2**(i%32))

    return out


def bin2intFromBinInt(a):
    if a == 0:
        return a

    la = int(math.log10(a))+1
    out = 0
    b = a
    for i in range(0,la):
        c = b % 10
        if c != 0 and c != 1:
            print 'error: input should only contain 0 or 1'
            return -1
        out += c*(2**i)
        b = int(b / 10)

    return out

def gaussianHash(inputFeat, outDim):
    # inputFeat: DxN
    # D: dimension
    # N: number of samples
    d, n = inputFeat.shape

    fn = './gaussianHash.mat'
    aa = {}
    if os.path.isfile(fn):
        aa = sio.loadmat(fn)
        gaussHashMat = aa['mat']
    else:
        # TODO: if the dimension is bigger than stored, make the gaussHashMat bigger by concatenate it more
        gaussHashMat = np.random.randn(5000,10000)
        aa['mat'] = gaussHashMat
        sio.savemat(fn, aa)
    hashMat = gaussHashMat[0:outDim,0:d]

    outbin = 1*(np.dot(hashMat, inputFeat) > 0)
    out = np.empty([outDim/32,n])
    for i in range(0,n):
        out[:,i] = bin2intFromNP(outbin[:,i])

    return out


def test():
    print 'test code begins'

    outdim = 64
    infeat = np.random.rand(4096, 10)
    print gaussianHash(infeat, outdim)


if __name__ == "__main__":
    test()

