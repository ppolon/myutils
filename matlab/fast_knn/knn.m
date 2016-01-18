function ret_idx = knn(query,dataset,k)
% Finding K-Nearest Neighbors
%  ret_idx = knn(query, dataset, k)
%
% input:
%  query  : DxN: D: feature dimension, N: #query samples
%  dataset: DxM: D: feature dimension, N: #samples in target dataset (Training data)
%  k      : 1x1: K
%
% output:
%  ret_idx: NxK: K-NN index of dataset

% By Mohammad Rastegari and Jonghyun Choi

[mq nq]=size(query);
[md nd]=size(dataset);
D=dist2(query',dataset');
[sD,s_idx]=sort(D,2);
ret_idx=s_idx(:,1:k);

