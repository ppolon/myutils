from boto.s3.connection import S3Connection
import time
import pdb

class StreamSageDeepMetadataAWS():
    """A simple python interface for DeepMetadata AWS S3
       author: Jonghyun Choi (jonghyun_choi@cable.comcast.com)
    """
    s3 = None
    bucket = None

    def get_s3_conn(self):
        return self.s3

    def get_bucket(self):
        return self.bucket

    def __init__(self):
        self.s3 = S3Connection('AKIAILCHW7GN2ZLERG6A', 'PR9+a1BCHE2l+0TUOHn1DE4XB8vqPlTB9C/SmTg1')
        self.bucket = self.s3.get_bucket('compass-research-deepmeta')

    def upload(self, iFn, pathNfn):
        key = self.bucket.new_key(pathNfn)
        startt = time.time()
        fsize = key.set_contents_from_filename(iFn) # TODO: check that the file is in the server, if so, abort it
        key.set_acl('public-read')
        endt = time.time()
        print iFn,'is uploaded to',pathNfn,'(filesize:',fsize,') (',endt-startt,'sec elapsed )'

    def download(self, pathNfn, oFn):
        key = self.bucket.get_key(pathNfn)
        startt = time.time()
        key.get_contents_to_filename(oFn)
        endt = time.time()
        print pathNfn,'is downloaded to',oFn,'(',endt-startt,'sec elapsed )'

    def rls(self, pathname):
        print 'Listing: remote/'+pathname
        print '%5s %15s %s' % ('<Index>', '<Size>', '<Path and name>')
        keynames = self.bucket.list(prefix=pathname)
        retList = [None]*len([keyname for keyname in keynames])
        cnt = 0
        for keyname in keynames:
            pathnfnremote = str(keyname.name)
            # tmpkey = self.bucket.get_key(keyname)
            # # pdb.set_trace()
            # if hasattr(tmpkey,'date'):
            #     datestr = tmpkey.date
            # else:
            #     datestr = ''

            if hasattr(keyname,'size'):
                sizestr = keyname.size
            else:
                sizestr = '0'
            #
            # print '%20s %15s %s' % (datestr, sizestr, pathnfnremote)
            print '%5d %15s %s' % (cnt, sizestr, pathnfnremote)
            retList[cnt] = pathnfnremote
            cnt += 1
        #
        return retList

    def rrm(self, pathNfn):
        key = self.bucket.get_key(pathNfn)
        print 'deleting',pathNfn,'...',
        if key is not None:
            key.delete() # bucket.delete_key(pathNfn)
            print 'done.'
        else:
            print 'already deleted. Nothing is running.'
