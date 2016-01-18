function [predicted_label, accuracy]=knn_classifier(train_data,test_data,train_label,test_label,K)
% K-Nearest Neighbors Classifier
%
% By Mohammad Rastegari
% Modified by Jonghyun Choi

[m_tr n_tr]=size(train_data);
[m_te n_te]=size(test_data);

nCat=length(unique(train_label));
ret_idx=knn(test_data,train_data,K);

for i=1:n_te   
    NN_L(i,:)=train_label(ret_idx(i,:));
    predicted_label(i) = mode( NN_L(i,:) );
    % H=hist(NN_L(i,:),1:nCat);
    % [~, m_idx]=max(H);
    % predicted_label(i)=m_idx(1);
    
end
accuracy = sum(predicted_label==test_label)/numel(test_label);

