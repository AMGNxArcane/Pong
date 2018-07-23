import tensorflow as tf
from tensorflow import keras
import numpy as np
import random
import os
import csv

fileList = os.listdir("data/")
print(len(fileList))

labels = {
    "-1": [1,0,0],
    "0":  [0,1,0],
    "1":  [0,0,1]
}

def getBatch(fileList,size):
    """returns the content of <size> files"""
    input = []
    target = []
    for i in range(size):
        with open("data/"+fileList[i]) as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row)!=7:
                    continue
                inp = [float(x) for x in row[2:7]]
                #print(inp)
                input.append(inp)
                target.append(int(row[1])+1)

    return input,target


input,target = getBatch(fileList,1000)


model = tf.keras.Sequential([
    keras.layers.Dense(10,input_shape=[5],activation="relu"),
    keras.layers.Dense(3,activation="softmax")
])

model.compile(optimizer=keras.optimizers.Adam(),loss='categorical_crossentropy',
              metrics=['accuracy'])

#model.fit(xs,ys,epochs=3,steps_per_epoch=10000)
inp = np.array(input)
print(inp.shape)

tar = []
for y in target:
    onehot = [0,0,0]
    onehot[y]=1
    tar.append(onehot)
tar = np.array(tar)
print(tar.shape)
model.fit(inp,tar,epochs=4)
model.save('model.h5')
