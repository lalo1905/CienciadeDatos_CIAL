# -*- coding: utf-8 -*-
"""ISABEL JEJE.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1FARc_R7rp50-5X4Y395yo6eo_yrftrdV

# **Importar bibliotecas**
"""

import tensorflow as tf  # IMPORTA TENSORFLOW
from tensorflow.keras import layers, models  # IMPORTA CAPAS Y MODELOS DE KERAS
from tensorflow.keras.preprocessing.image import ImageDataGenerator  # IMPORTA EL GENERADOR DE DATOS PARA AUMENTACIÓN DE IMÁGENES
from tensorflow.keras.optimizers import Adam  # IMPORTA EL OPTIMIZADOR ADAM
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping  # IMPORTA CALLBACKS PARA AJUSTE DE TASA DE APRENDIZAJE Y DETENCIÓN TEMPRANA

"""## **Configuraciones**"""

# CONFIGURACIONES DEL MODELO
batch_size = 64  # DEFINIR EL TAMAÑO DEL LOTE
epochs = 50  # DEFINIR EL NÚMERO DE EPOCAS

"""# **Preprocesamiento de datos y aumentación**"""

# PREPROCESAMIENTO DE DATOS Y AUMENTACIÓN
train_datagen = ImageDataGenerator(  # CREAR UN GENERADOR PARA EL CONJUNTO DE ENTRENAMIENTO
    rescale=1.0/255,  # NORMALIZAR LAS IMÁGENES A UN RANGO DE 0 A 1
    horizontal_flip=True,  # AUMENTAR DATOS MEDIANTE VOLTEO HORIZONTAL
    width_shift_range=0.1,  # DESPLAZAR IMÁGENES HORIZONTALMENTE
    height_shift_range=0.1,  # DESPLAZAR IMÁGENES VERTICALMENTE
    shear_range=0.1,  # APLICAR CORTES A LAS IMÁGENES
    zoom_range=0.1  # APLICAR ZOOM A LAS IMÁGENES
)

test_datagen = ImageDataGenerator(rescale=1.0/255)  # CREAR UN GENERADOR PARA EL CONJUNTO DE PRUEBA CON NORMALIZACIÓN

"""# **Cargar y preprocesar CIFAR-10**"""

# CARGAR Y PREPROCESAR EL CONJUNTO DE DATOS CIFAR-10
train_dataset = tf.keras.datasets.cifar10.load_data()  # CARGAR EL CONJUNTO DE DATOS CIFAR-10
(x_train, y_train), (x_test, y_test) = train_dataset  # SEPARAR LAS IMÁGENES Y LAS ETIQUETAS EN CONJUNTOS DE ENTRENAMIENTO Y PRUEBA

# CREAR GENERADORES DE DATOS PARA EL ENTRENAMIENTO Y PRUEBA
train_generator = train_datagen.flow(x_train, y_train, batch_size=batch_size)  # GENERADOR DE DATOS PARA EL CONJUNTO DE ENTRENAMIENTO
test_generator = test_datagen.flow(x_test, y_test, batch_size=batch_size)  # GENERADOR DE DATOS PARA EL CONJUNTO DE PRUEBA

"""# **Construcción del modelo**"""

# CONSTRUCCIÓN DEL MODELO
def create_model():  # DEFINIR UNA FUNCIÓN PARA CREAR EL MODELO
    model = models.Sequential()  # INICIALIZAR UN MODELO SECUENCIAL

    # PRIMERA CAPA CONVOLUCIONAL
    model.add(layers.Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=(32, 32, 3)))  # CAPA CONVOLUCIONAL CON 32 FILTRAS Y FUNCIÓN DE ACTIVACIÓN RELU
    model.add(layers.BatchNormalization())  # NORMALIZACIÓN POR LOTE PARA ESTABILIZAR EL APRENDIZAJE
    model.add(layers.Conv2D(32, (3, 3), activation='relu'))  # OTRA CAPA CONVOLUCIONAL
    model.add(layers.BatchNormalization())  # OTRA NORMALIZACIÓN POR LOTE
    model.add(layers.MaxPooling2D((2, 2)))  # CAPA DE MAX POOLING PARA REDUCIR LA DIMENSIÓN
    model.add(layers.Dropout(0.2))  # CAPA DE DROPOUT PARA PREVENIR EL SOBREAJUSTE

    # SEGUNDA CAPA CONVOLUCIONAL
    model.add(layers.Conv2D(64, (3, 3), padding='same', activation='relu'))  # CAPA CONVOLUCIONAL CON 64 FILTRAS
    model.add(layers.BatchNormalization())  # NORMALIZACIÓN POR LOTE
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))  # OTRA CAPA CONVOLUCIONAL
    model.add(layers.BatchNormalization())  # OTRA NORMALIZACIÓN POR LOTE
    model.add(layers.MaxPooling2D((2, 2)))  # MAX POOLING
    model.add(layers.Dropout(0.3))  # DROPOUT

    # TERCERA CAPA CONVOLUCIONAL
    model.add(layers.Conv2D(128, (3, 3), padding='same', activation='relu'))  # CAPA CONVOLUCIONAL CON 128 FILTRAS
    model.add(layers.BatchNormalization())  # NORMALIZACIÓN POR LOTE
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))  # OTRA CAPA CONVOLUCIONAL
    model.add(layers.BatchNormalization())  # OTRA NORMALIZACIÓN POR LOTE
    model.add(layers.MaxPooling2D((2, 2)))  # MAX POOLING
    model.add(layers.Dropout(0.4))  # DROPOUT

    # CAPA Densa
    model.add(layers.Flatten())  # APLANAR LA SALIDA PARA LA CAPA Densa
    model.add(layers.Dense(128, activation='relu'))  # CAPA Densa CON 128 NEURONAS Y ACTIVACIÓN RELU
    model.add(layers.Dropout(0.5))  # DROPOUT
    model.add(layers.Dense(10, activation='softmax'))  # CAPA DE SALIDA PARA CLASIFICACIÓN CON 10 CLASES (CIFAR-10)

    return model  # DEVOLVER EL MODELO CREADO

model = create_model()  # CREAR EL MODELO LLAMANDO A LA FUNCIÓN

"""# **Compilación del modelo**"""

# COMPILACIÓN DEL MODELO
model.compile(optimizer=Adam(learning_rate=0.001),  # COMPILAR EL MODELO UTILIZANDO EL OPTIMIZADOR ADAM CON UNA TASA DE APRENDIZAJE DE 0.001
              loss='sparse_categorical_crossentropy',  # FUNCIÓN DE PÉRDIDA PARA CLASIFICACIÓN MULTICLASSE
              metrics=['accuracy'])  # MÉTRICAS A SEGUIR DURANTE EL ENTRENAMIENTO

"""# **Callbacks para ajuste dinámico del learning rate**"""

# CALLBACKS PARA AJUSTE DINÁMICO DEL LEARNING RATE
callbacks = [  # CREAR UNA LISTA DE CALLBACKS
    ReduceLROnPlateau(monitor='val_accuracy', factor=0.5, patience=5, verbose=1),  # REDUCIR LA TASA DE APRENDIZAJE SI LA PRECISIÓN DE VALIDACIÓN NO MEJORA
    EarlyStopping(monitor='val_accuracy', patience=10, restore_best_weights=True)  # DETENER EL ENTRENAMIENTO TEMPRANAMENTE SI NO HAY MEJORAS
]

"""# **Entrenamiento del modelo**"""

# ENTRENAMIENTO DEL MODELO
history = model.fit(  # INICIAR EL PROCESO DE ENTRENAIMIENTO DEL MODELO
    train_generator,  # GENERADOR DE DATOS PARA EL CONJUNTO DE ENTRENAMIENTO
    epochs=epochs,  # NÚMERO DE EPOCAS DEFINIDO ANTERIORMENTE
    validation_data=test_generator,  # GENERADOR DE DATOS PARA VALIDACIÓN
    callbacks=callbacks  # INCLUIR LOS CALLBACKS DEFINIDOS
)

"""# **Evaluación final en el conjunto de prueba**"""

# GUARDAR EL MODELO ENTRENADO
model.save('cifar10_model.h5')

# MODO TEST: CARGAR Y EVALUAR EL MODELO GUARDADO
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# CARGAR EL MODELO ENTRENADO
model = tf.keras.models.load_model('cifar10_model.h5')

# PREPROCESAMIENTO PARA EL MODO DE PRUEBA
# Se usa el generador sin aumentación, sólo reescalado
test_datagen = ImageDataGenerator(rescale=1.0/255)
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()

# CONFIGURAR EL GENERADOR DE TEST
test_generator = test_datagen.flow(x_test, y_test, batch_size=64, shuffle=False)

# EVALUAR EL MODELO EN EL CONJUNTO DE PRUEBA
test_loss, test_accuracy = model.evaluate(test_generator)
print(f"Test Accuracy: {test_accuracy:.2f}")