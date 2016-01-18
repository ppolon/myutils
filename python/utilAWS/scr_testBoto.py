from StreamSageDeepMetadataAWS import StreamSageDeepMetadataAWS

sss = StreamSageDeepMetadataAWS()
# sss.upload('/Users/jchoi206/Desktop/v_BaseballPitch_g01_c02_fc7.mat','data/jchoi/tmp.mat')
remoteList = sss.ls_remote('data/jchoi')
print len(remoteList)

# for fn in remoteList:
#     print fn

for fn in remoteList:
    sss.delete_remote(fn)