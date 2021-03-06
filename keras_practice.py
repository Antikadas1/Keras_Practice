# -*- coding: utf-8 -*-
"""Keras_practice.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1M1vnKodGsSl5SB33ySZzzlftGI4Pux_I

# Import Libraries
"""

import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras import layers

"""# Keras Functional API"""

inputs=keras.Input(784)
dense1=layers.Dense(64,'relu',name="dense1")(inputs)
dense2=layers.Dense(32,'relu')(dense1)
outputs = layers.Dense(10)(dense2)

model=keras.Model(inputs=inputs,outputs=outputs,name="practice")

model.summary()

keras.utils.plot_model(model,"my_model.png")

keras.utils.plot_model(model,"my_model.png",show_shapes=True)

(x_train,y_train),(x_test,y_test)=keras.datasets.mnist.load_data()

x_train.shape

x_train=x_train.reshape(60000,784).astype("float32")/255
x_test=x_test.reshape(10000,784).astype("float32")/255

"""# Some important features like learning rate scheduling, different types of optimzer,loss functions"""

#easy way && default parameter
# model.compile(optimizer="adam",loss="SparseCategoricalCrossentropy")
#scheduler :
    #1. exponential decay
lr_schedule=keras.optimizers.schedules.ExponentialDecay(0.01,10000,0.9,True)


opt=keras.optimizers.Adam(learning_rate=lr_schedule) 

loss_fn=keras.losses.SparseCategoricalCrossentropy(from_logits=True)
#more than one metrices can be used to monitor training ex. AUC, categoricalaccuracy etc.
model.compile(optimizer=opt,loss=loss_fn,metrics=["accuracy"],)

# model.compile(
#     loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
#     optimizer=opt,
#     metrics=["accuracy"],
# )


history=model.fit(x_train,y_train,batch_size=64,epochs=30,verbose=2,validation_split=0.2)
model.evaluate(x_test,y_test)

"""# Define functional API and compiling in form of "function" , use customized loss functions"""

#define model using function to use with different data set

(x_train,y_train),(x_test,y_test)=keras.datasets.mnist.load_data()
x_train=x_train.reshape(60000,784).astype("float32")/255
x_test=x_test.reshape(10000,784).astype("float32")/255

def network_layers():
    inputs = keras.Input(shape=(784,), name="digits")
    x1 = layers.Dense(64, activation="relu", name="dense_1")(inputs)
    x2 = layers.Dense(64, activation="relu", name="dense_2")(x1)
    outputs = layers.Dense(10, activation="softmax", name="predictions")(x2)
    model = keras.Model(inputs=inputs, outputs=outputs)
    # model.add_loss(tf.math.square(x1)*0.1)
    # model.add_metric(keras.backend.std(x1), name="std_of_activation", aggregation="mean")
    return model

def custom_losses(y_true,y_pred):
  return tf.math.reduce_mean(tf.square(y_true - y_pred))

#use custom losses with extra parameter
class custom_loss_class(keras.losses.Loss):
  def __init__(self,regularization_factor=0.1,name="custom_mse"):
    super().__init__(name=name)
    self.regularization_factor=regularization_factor

    def cus_loss_func(self,y_pred,y_true):
      mse=tf.math.reduce_mean(tf.square(y_true,y_pred))
      reg=tf.math.reduce_mean(tf.square(0.5 - y_pred))
    return mse + reg * self.regularization_factor

def compiled_model():
  model=network_layers()
  model.compile(
        optimizer="rmsprop",
        loss="SparseCategoricalCrossentropy", #or custom_loss_class()
        metrics=["accuracy"],
    )
  return model

model = compiled_model()
# model.compile(optimizer=keras.optimizers.Adam(), loss=)

model.summary()

# one hot encoding
# y_train_one_hot=tf.one_hot(y_train,depth=10)
#tf has math library we can use tf for mathematical computation instaed of numpy

model.fit(x_train,y_train,epochs=5,verbose=2)

model.evaluate(x_test,y_test)

"""# Sequential API"""

(x_train,y_train),(x_test,y_test)=keras.datasets.mnist.load_data()
x_train=x_train.reshape(60000,784).astype("float32")/255
x_test=x_test.reshape(10000,784).astype("float32")/255

x_val = x_train[-10000:]
y_val = y_train[-10000:]
x_train = x_train[:-10000]
y_train = y_train[:-10000]


sequential=keras.models.Sequential(
    [keras.layers.Input(shape=(784)),
     keras.layers.Dense(64,activation="relu"),
     keras.layers.Dense(64, activation="relu", name="dense_2"),
     keras.layers.Dense(10, name="predictions"),     
    ]
)

sequential.compile(
        optimizer="rmsprop",
        loss="SparseCategoricalCrossentropy", #or custom_loss_class()
        metrics=["accuracy"],
    )

sequential.fit(x_train,y_train,epochs=5,verbose=2,validation_data=(x_val,y_val))

sequential.evaluate(x_test,y_test)

"""# Saving/loading models"""

sequential.save("sequential_save")

model_seq=keras.models.load_model("sequential_save")

model_seq.summary()

# load as .h5
sequential.save("sequential_save.h5")

#json load
sequential_json=sequential.to_json()

sequential_json

model_seq.get_config()

model_seq.get_weights()

model_seq.optimizer

model_seq.get_layer("dense_2")

"""# CallBack API -- Modelcheckpoint,Earlycallback,Tensorboard"""

filepath="weights-improvement-{epoch:02d}-{val_accuracy:.2f}.hdf5"
checkpoint = keras.callbacks.ModelCheckpoint(filepath, monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')
early_stopping=keras.callbacks.EarlyStopping(monitor='val_loss',min_delta=0.5,patience=3)
callbacks_list = [checkpoint,early_stopping]
# Fit the model
sequential.fit(x_train, y_train, validation_split=0.33, epochs=20, batch_size=10, callbacks=callbacks_list, verbose=0)

"""# Loading the check points

```
# This is formatted as code
```


"""

sequential.load_weights("weights-improvement-01-0.20.hdf5")

