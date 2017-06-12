
from svm import *
from svmutil import *

train_label,train_pixel = svm_read_problem('train_pix_feature_xy.txt' )
predict_label,predict_pixel = svm_read_problem('last_test_pix_xy_new.txt')

model = svm_train(train_label, train_pixel)
print("result:")
p_label, p_acc, p_val = svm_predict(predict_label, predict_pixel, model)

print(p_acc)
