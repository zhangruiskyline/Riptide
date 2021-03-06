import os
import tensorflow as tf
from riptide.binary import binary_layers as nn


class alexnet(tf.keras.Model):
    def __init__(self, classes=1000):
        super(alexnet, self).__init__()
        self.conv1 = nn.NormalConv2D(
            filters=64,
            kernel_size=11,
            strides=4,
            padding='same',
            activation='relu',
            use_bias=True)
        self.bn1 = nn.NormalBatchNormalization(center=False, scale=False)
        self.pool1 = nn.NormalMaxPool2D(pool_size=2, strides=2)
        self.enter_int = nn.EnterInteger(scale=1.0)

        self.conv2 = nn.BinaryConv2D(
            filters=192,
            kernel_size=5,
            strides=1,
            padding='same',
            activation='relu',
            use_bias=False)
        self.bn2 = nn.BatchNormalization(self.conv2)
        self.pool2 = nn.MaxPool2D(pool_size=2, strides=2)

        self.conv3 = nn.BinaryConv2D(
            filters=384,
            kernel_size=3,
            strides=1,
            padding='same',
            activation='relu',
            use_bias=False)
        self.bn3 = nn.BatchNormalization(self.conv3)

        self.conv4 = nn.BinaryConv2D(
            filters=384,
            kernel_size=3,
            strides=1,
            padding='same',
            activation='relu',
            use_bias=False)
        self.bn4 = nn.BatchNormalization(self.conv4)

        self.conv5 = nn.BinaryConv2D(
            filters=256,
            kernel_size=3,
            strides=1,
            padding='same',
            activation='relu',
            use_bias=False)
        self.bn5 = nn.BatchNormalization(self.conv5)
        self.pool5 = nn.MaxPool2D(pool_size=2, strides=2)
        self.exit_int = nn.ExitInteger()

        self.flatten = nn.Flatten()
        self.dense6 = nn.NormalDense(4096, use_bias=True, activation='relu')
        self.bn6 = nn.NormalBatchNormalization()
        self.dense7 = nn.NormalDense(4096, use_bias=True, activation='relu')
        self.bn7 = nn.NormalBatchNormalization()
        self.dense8 = nn.NormalDense(classes, use_bias=True)
        #self.scalu = nn.Scalu()
        self.softmax = nn.Activation('softmax')

    def call(self, inputs, training=None):
        x = self.conv1(inputs)
        x = self.bn1(x)
        x = self.pool1(x)
        x = self.enter_int(x)

        x = self.conv2(x)
        x = self.bn2(x, training=training)
        x = self.pool2(x)

        x = self.conv3(x)
        x = self.bn3(x, training=training)

        x = self.conv4(x)
        x = self.bn4(x, training=training)

        x = self.conv5(x)
        x = self.bn5(x, training=training)
        x = self.pool5(x)
        x = self.exit_int(x)

        x = self.flatten(x)
        x = self.dense6(x)
        x = self.bn6(x, training=training)
        x = self.dense7(x)
        x = self.bn7(x, training=training)
        x = self.dense8(x)
        #x = self.scalu(x)
        x = self.softmax(x)

        return x
