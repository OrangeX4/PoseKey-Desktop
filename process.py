import numpy as np

with open('autodata.json', 'r', encoding='utf-8') as f:
    data = []
    label = []
    for i in range(800):
        label_stand = 0
        label_run = 0
        dataArray = []
        for j in range(24):
            print(24 * i + j)
            json = eval(f.readline().strip())  # eval
            if json['label'] == 0:
                label_stand += 1
            else:
                label_run += 1
            array = []
            for point in json['keyPoints'].values():
                array.append([point['score'], point['position']
                              ['x'] / 300, point['position']['y'] / 300])
            dataArray.append(array)
        if label_stand >= label_run:
            label.append(0)
        else:
            label.append(1)
        data.append(dataArray)
    print(np.array(data).shape)
    np.savez('autodata.npz', data=np.array(data), label=np.array(label))

