import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.inception_v3 import InceptionV3

def create_model(classes):

    model = InceptionV3(
        input_shape=tf.keras.Input(shape=(150, 150, 3)).shape[1:],
        include_top=False,
    )

    for layer in model.layers:
        layer.trainable = False

    last_layers = model.get_layer('mixed7')
    last_output = last_layers.output

    x = tf.keras.layers.Flatten()(last_output)
    x_dense = tf.keras.layers.Dense(128, activation='relu')(x)
    x_dropout = tf.keras.layers.Dropout(0.2)(x_dense)
    output = tf.keras.layers.Dense(len(classes), activation='softmax')(x_dropout)

    model_keras = tf.keras.Model(model.input, output)

    return model_keras

def run():
    train_dir = './files/TumorClassification/train'
    test_dir = './files/TumorClassification/test'

    # Data Image Generators
    train_datage = ImageDataGenerator(rescale=1./255)
    test_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

    train_generator = train_datage.flow_from_directory(
        train_dir,
        target_size=(150, 150),
        batch_size=128,
        class_mode='categorical',
        color_mode='rgb',
        subset = 'training'
    )
    validation_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=(150, 150),
        batch_size=128,
        class_mode='categorical',
        color_mode='rgb',
        subset = 'validation'
    )
    test_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=(150, 150),
        batch_size=128,
        class_mode='categorical',
        color_mode='rgb',
    )

    classes = ["BENIGN", "MALIGNANT", "NORMAL"]

    model = create_model(classes)

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(train_generator, epochs=10, validation_data=validation_generator)

    try:
        model.save('./models/model-inception.h5')
        print("Model saved")
    except:
        print("Error saving model")

    print(model.evaluate(test_generator))

if __name__ == "__main__":
    run()