import os
import random

trainval_percent = 0.9
train_percent = 0.9
txtfilepath = 'WiderPerson/Annotations'  # txt标签文件路径
txtsavepath = 'WiderPerson'              # 数据划分txt文件路径
total_xml = os.listdir(txtfilepath)

num = len(total_xml)
list =[f for f in os.listdir(txtfilepath) if f.endswith(".txt")]
tv = int(num * trainval_percent)
tr = int(tv * train_percent)
trainval = random.sample(list, tv)
train = random.sample(trainval, tr)

ftrainval = open('trainval.txt', 'w')
ftest = open('WiderPerson/test.txt', 'w')
ftrain = open('WiderPerson/train.txt', 'w')
fval = open('WiderPerson/val.txt', 'w')

for i in list:
    name = i.split(".")[0] + '\n'
    if i in trainval:
        ftrainval.write(name)
        if i in train:
            ftrain.write(name)
        else:
            fval.write(name)
    else:
        ftest.write(name)

ftrainval.close()
ftrain.close()
fval.close()
ftest.close()
