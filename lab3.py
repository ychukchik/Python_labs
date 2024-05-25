import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pickle

from scipy import interp
from itertools import cycle
from sklearn import svm, datasets
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import label_binarize
from tensorflow.keras.preprocessing import image
from sklearn.multiclass import OneVsRestClassifier
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator

#train_dandelion_dir = input("Введите расположение тренировочных картинок коровы: ")
#train_grass_dir = input("Введите расположение тренировочных картинок человека: ")
#valid_dandelion_dir = input("Введите расположение тестовых картинок коровы: ")
#valid_grass_dir = input("Введите расположение тестовых картинок человека: ")

train_dandelion_dir = os.path.join('train1/cow')

train_grass_dir = os.path.join('train1/human')

valid_dandelion_dir = os.path.join('valid1/cow')

valid_grass_dir = os.path.join('valid1/human')

train_dandelion_names = os.listdir(train_dandelion_dir)

train_grass_names = os.listdir(train_grass_dir)

validation_grass_names = os.listdir(valid_grass_dir)

print('total training cow images:', len(os.listdir(train_dandelion_dir)))
print('total training human images:', len(os.listdir(train_grass_dir)))
print('total validation cow images:', len(os.listdir(valid_dandelion_dir)))
print('total validation human images:', len(os.listdir(valid_grass_dir)))

"""nrows = 4
ncols = 4

pic_index = 0

fig = plt.gcf()
fig.set_size_inches(ncols * 4, nrows * 4)

pic_index += 8
next_dandelion_pic = [os.path.join(train_dandelion_dir, fname)
                for fname in train_dandelion_names[pic_index-8:pic_index]]
next_grass_pic = [os.path.join(train_grass_dir, fname)
                for fname in train_grass_names[pic_index-8:pic_index]]

for i, img_path in enumerate(next_dandelion_pic + next_grass_pic):
  sp = plt.subplot(nrows, ncols, i + 1)
  sp.axis('Off')

  img = mpimg.imread(img_path)
  plt.imshow(img)

#plt.show()"""

train_datagen = ImageDataGenerator(rescale=1/255)
validation_datagen = ImageDataGenerator(rescale=1/255)

train_generator = train_datagen.flow_from_directory(
        'train1/',
        classes = ['cow', 'human'],
        target_size=(200, 200),
        batch_size=657,
        class_mode='binary')

validation_generator = validation_datagen.flow_from_directory(
        'valid1/',
        classes = ['cow', 'human'],
        target_size=(200, 200),
        batch_size=10,
        class_mode='binary',
        shuffle=False)
flag = 1
model = tf.keras.models.load_model('model.h5')
if model:
   flag = 0


if (flag):
    model = tf.keras.models.Sequential([tf.keras.layers.Flatten(input_shape = (200,200,3)),
                                    tf.keras.layers.Dense(128, activation=tf.nn.relu),
                                    tf.keras.layers.Dense(1, activation=tf.nn.sigmoid)])


    model.summary()

    model.compile(optimizer = tf.keras.optimizers.Adam(),
              loss = 'binary_crossentropy',
              metrics=['accuracy'])

    history = model.fit(train_generator,
          steps_per_epoch=8,
          epochs=15,
          verbose=1,
          validation_data = validation_generator,
          validation_steps=8)


uploaded = ['test2.jpg']

if flag:
    model.save('model.h5')

#content_dir = input("Введите расположение файла для распознавания: ")
#uploaded = [input("Введите название файла: ")]


choice = int(input("Введите количество картинок: "))
if choice == 1:
    way = input("Напишите путь к файлу: ")
    path = fr"{way}"
    img = image.load_img(path, target_size=(200, 200))
    x = image.img_to_array(img)
    plt.imshow(x / 255.)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    classes = model.predict(images, batch_size=10)
    print(classes[0])
    if classes[0] < 0.5:
        print("Это коровка")
    else:
        print("Это человек")
else:
    path = r'test1'
    count_cow = 0
    count_human = 0
    file_names = os.listdir(path)
    for file_name in file_names:
        fullpath = os.path.join(path, file_name)
        img = image.load_img(fullpath, target_size=(200, 200))
        x = image.img_to_array(img)
        plt.imshow(x / 255.)
        x = np.expand_dims(x, axis=0)
        images = np.vstack([x])
        classes = model.predict(images, batch_size=10)
        print(classes[0])
        if classes[0] < 0.5:
            count_cow += 1
        else:
            count_human += 1
