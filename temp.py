import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

json_file=open("model-11.4.json", "r")#v=make,y=anything
model_json=json_file.read()
json_file.close()
model=tf.keras.models.model_from_json(model_json)
model.load_weights("model-11.4.h5")
sz=200
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1./255)

training_set = train_datagen.flow_from_directory('data2/train',
                                                 target_size=(sz, sz),
                                                 batch_size=5,
                                                 color_mode='grayscale',
                                                 class_mode='categorical')

test_set = test_datagen.flow_from_directory('data2/test',
                                            target_size=(sz , sz),
                                            batch_size=5,
                                            color_mode='grayscale',
                                            class_mode='categorical')
res=model.evaluate(test_set)
model.summary()
print(res)
#99.43% and 94.06%
