# extractCaffeFeat.py
# Author: Jonghyun Choi (jonghyun.choi@cable.comcast.com)
# Date created: 7/17/2015
# Date last modified: 11/10/2015
# Python ver: 2.7.10

import os, os.path
import numpy as np
import matplotlib.pyplot as pyplot
import scipy.io as sio
import cv2

import sys
import os
import pdb

import caffe
import time

import types

def initCaffe(gpuid):
    caffe_root = '/Users/jchoi206/tmp/caffe/'
    caffe_model_dir = '/Users/jchoi206/libs/caffe/models/vgg_s/'
    caffe_model_fn  = 'VGG_CNN_S.caffemodel'
    caffe_model_mean_fn = 'VGG_mean.mat'
    caffe_momdel_proto_fn = 'VGG_CNN_S_deploy.prototxt'

    # model data check
    if not os.path.isfile(caffe_model_dir+caffe_model_fn) or \
       not os.path.isfile(caffe_model_dir+caffe_model_mean_fn) or \
       not os.path.isfile(caffe_model_dir+caffe_momdel_proto_fn):
       print 'some of the model files are missing. Code terminates'
       return
    
    # CPU mode or GPU mode
    if gpuid < 0:
        #-- CPU mode
        caffe.set_mode_cpu()
    else:
        #-- GPU mode
        caffe.set_device(gpuid)
        caffe.set_mode_gpu()
    #--

    net = caffe.Net(caffe_model_dir + caffe_momdel_proto_fn, \
                    caffe_model_dir + caffe_model_fn, \
                    caffe.TEST)

    # input preprocessing
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2,0,1))
    #
    data_mean = sio.loadmat(caffe_model_dir+caffe_model_mean_fn)['image_mean']
    data_mean = data_mean.swapaxes(0,2).swapaxes(1,2)
    #
    transformer.set_mean('data', data_mean) # mean pixel
    transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
    transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB

    # set net to batch size of 50
    net.blobs['data'].reshape(1,3,224,224)

    return net, transformer 

def extractCaffe(net, transformer, imgfn, layername):
    # do forward prop. only
    # net.blobs['data'].data[...] = transformer.preprocess('data', caffe.io.load_image(caffe_root + 'examples/images/cat.jpg'))
    try:
        net.blobs['data'].data[...] = transformer.preprocess('data', caffe.io.load_image(imgfn))
    except:
        print 'This image file has a problem'
        return -1

    out = net.forward() # 'prob' output 
    if layername == 'prob':
        out = out['prob']
    else:
        out = net.blobs[layername].data
    # %timeit net.forward()

    return out



def extractCaffeImg(net, transformer, imgs, layername = 'prob'):
    """do forward prop. only
    """
    try:
        cnt = 0
        if type(imgs) is types.ListType:
            for img in imgs:
                net.blobs['data'].data[...] = transformer.preprocess('data', img)
                # net.blobs['data'].data[cnt,:,:,:] = transformer.preprocess('data', img)
                cnt += 1
        else:
            net.blobs['data'].data[...] = transformer.preprocess('data', imgs)
            cnt = 1
    
    except:
        print 'Image file has a problem'
        return -1

    out = net.forward() # 'prob' output 
    if layername == 'prob':
        out = out['prob']
    else:
        out = net.blobs[layername].data
    # %timeit net.forward()

    return out



if __name__ == "__main__":
    print 'code begins'
    ipath = '/tmp_datasets/UCF101'
    opath = '/tmp_datasets/UCF101_feat'

    if len(sys.argv) < 2:
        print 'no GPU ID is specified. Default: 0'
        gpuid = 0
    else:
        gpuid = int(sys.argv[1])
    print 'Specified GPU ID:', gpuid

    #
    print 'getting list of videos...',
    videoLists = [name for name in os.listdir(ipath) if os.path.isdir(ipath+'/'+name)]
    print 'done'
    print 'number of entries in ', ipath, ':', len(videoLists)

    # erroneous file list
    ferr = open(opath+'/errorvideos.txt','a+')

    # initialize Caffe
    net, transformer = initCaffe(gpuid)

    # loop over videos
    cnt = 0
    layername = 'fc7'
    ndim = 4096
    print 'begins loop'
    for videoDir in videoLists: #[len(videoLists)/4*gpuid:len(videoLists)/4*(gpuid+1)]:
        print ipath+'/'+videoDir
        print cnt,'/',len(videoLists),':',videoDir
        jpglist = [f for f in os.listdir(ipath+'/'+videoDir) if (f.split('.')[-1] == 'jpg')]
        out = np.empty([len(jpglist), ndim])
        njpg = len(jpglist)
        #
        fnmat = opath+'/'+videoDir+'_'+layername+'.mat'
        if not os.path.isfile(fnmat):
            starttime = time.time()
            cnt2 = 0
            errflag = False
            for fn in jpglist:
                if cnt2%(njpg/10) == 0:
                    endtime = time.time()
                    print '[',cnt2,'/',njpg,']: time elapsed:', endtime-starttime
                    starttime = time.time()
                # read image by cv2 and put it intout extractCaffe(img)
                pathnfn = ipath+'/'+videoDir+'/'+fn
                tmp = extractCaffe(net, transformer, pathnfn, layername) 
                if isinstance(tmp, np.ndarray):
                    out[cnt2,:] = tmp
                else:
                    ferr.write(pathnfn+'\n')
                    errflag = True
                    continue
                cnt2 += 1
            if not errflag:
                matformat = {}
                matformat['feat'] = out
                print 'save frame features...',
                sio.savemat(fnmat, matformat)
                print 'done'
            else:
                print 'Feature saving skipped: '+ipath+'/'+videoDir+'has a problem'
        else:
            print fnmat,'is found. Extracting feature is skipped'
        #
        cnt += 1

    ferr.close()


