import os
import pdb
from StreamSageDeepMetadataAWS import StreamSageDeepMetadataAWS

if __name__ == "__main__":
    sss = StreamSageDeepMetadataAWS()
    rootdirname = '/Volumes/MrVideo/mraptis'

    for root, dirs, files in os.walk(rootdirname):
        subdirname = root[root.find(rootdirname)+len(rootdirname):]
        print 'subdirname:',subdirname
        for fn in files:
            srcfn = root+'/'+fn
            tgtfn = 'data/jchoi'+subdirname+'/'+fn
            print root+'/'+fn,'==>','data/jchoi'+subdirname+'/'+fn
            sss.upload(srcfn, tgtfn)
            # pdb.set_trace()
