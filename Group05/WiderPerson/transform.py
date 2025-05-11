import os

otxt_path = "WiderPerson/label/val"
ntxt_path = "../dataset/labels/val"
if not os.path.exists(ntxt_path):
    os.makedirs(ntxt_path)

filer = []
for root, dirs, files in os.walk(otxt_path):
    for i in files:
        otxt = os.path.join(otxt_path, i)
        ntxt = os.path.join(ntxt_path, i)
        f = open(otxt, 'r', encoding='utf-8')
        for line in f.readlines():
            if line == '\n':
                continue
            cls = line.split(" ")
            # cls = '%s'%(int(cls[0])-1) + " " + cls[1]+ " " + cls[2]+ " " + cls[3]+ " " + cls[4]
            cls = '0' + " " + cls[1]+ " " + cls[2]+ " " + cls[3]+ " " + cls[4]
            filer.append(cls)
        with open(ntxt,"a") as f:
            for i in filer:
                f.write(i)
        filer = []

otxt_path = "WiderPerson/label/train"
ntxt_path = "../dataset/labels/train"
if not os.path.exists(ntxt_path):
    os.makedirs(ntxt_path)

filer = []
for root, dirs, files in os.walk(otxt_path):
    for i in files:
        otxt = os.path.join(otxt_path, i)
        ntxt = os.path.join(ntxt_path, i)
        f = open(otxt, 'r', encoding='utf-8')
        for line in f.readlines():
            if line == '\n':
                continue
            cls = line.split(" ")
            # cls = '%s'%(int(cls[0])-1) + " " + cls[1]+ " " + cls[2]+ " " + cls[3]+ " " + cls[4]
            cls = '0' + " " + cls[1]+ " " + cls[2]+ " " + cls[3]+ " " + cls[4]
            filer.append(cls)
        with open(ntxt,"a") as f:
            for i in filer:
                f.write(i)
        filer = []