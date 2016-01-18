function plotConfusionMat(C)
% plotConfusionMat(C)
%
% Input: C (NxM)
% Output: Plot

% Written by Jonghyun Choi @ UMD, UMIACS

imagesc(C);
colormap(gray);
colorbar;
