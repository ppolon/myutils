function [ recall, precision, ap, eer ] = myPRcurve2( i, uLabel, conf )
% [ recall, precision, ap, eer ] = myPRcurve( i, uLabel, eLabel )
%
% input:
%  i: target class label
%  uLabel: GND labels of test samples
%  conf: classification confidence test samples
%
% output:
%  recall: recall sequence
%  precision: precision sequence
%  ap: average precision
%  eer: equal error rate
%
% usage:
%  1) plot PR curve
%   [ recall, precision, ap ] = myPRcurve( i, uLabel, eLabel )
%   plot(recall, precision);

% Jonghyun Choi @ UMD, MSR
% Last updated @ 2016.1.17
% History:
%  2016.1.17: + compute equal error rate
%  2016.1.15: clean up code and put usage
%  2014.7.22: add comments and comment out unnecessary parts
%  2013.1: created by modifying PASCAL VOC evaluation scripts

% precision = (#correctly positive)/(#obtained positive)
% recall = (#correctly positive)/(#positive samples)
[ val idx ] = sort( conf, 'descend' );

for iii = 1:numel(idx)
    recall(iii)    = sum(uLabel(idx(1:iii)) == i)/sum(uLabel == i);
    precision(iii) = sum(uLabel(idx(1:iii)) == i)/iii;
end

% compute average precision (based on PASCAL VOC 2007 evaluation code)
ap=0; % average precision
T = linspace(0,1,1000);
for t=T % why so few bins?
    p=max(precision(recall>=t));
    if isempty(p)
        p=0;
    end
    ap=ap+p/length(T);
end

% % PASCAL code for computing precision and recall
% gt(uLabel == i) = 1;
% gt(uLabel ~= i) = -1;
% 
% [so,si]=sort(-conf);
% tp=gt(si)>0;
% fp=gt(si)<0;
% 
% fp=cumsum(fp);
% tp=cumsum(tp);
% rec=tp/sum(gt>0);
% prec=tp./(fp+tp);
% 
% % AP by PASCAL VOC 2010 circa
% ap=VOCap(rec',prec');
% fprintf('PASCAL VOC AP: %.6f\n', ap);


% compute equal error rate (eer)
% eer = when "false positive rate (fpr)" == "false negative rate (fnr)"
% @false positive rate = (false positive)/(#negative samples)
%                      = (1-precision)*(#obtained positive)/(#negative
%                      samples)
% @false negative rate = (false negative)/(#positive samples)
%                      = 1-recall

fpr = (1-precision).*sum(uLabel == i)/(numel(uLabel)-sum(uLabel == i));
fnr = 1-recall;

diff_fpr_fnr = abs(fpr-fnr);
[val, idx] = min(diff_fpr_fnr);

fprintf('tolerance for equal error rate: %f\n', val);
eer = fpr(idx);
