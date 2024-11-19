from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D, BatchNormalization, Input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import regularizers
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint

def create_model(classes):

    input = Input(shape=(124, 124, 1))
    # Second Convolutional Layer
    x1 = Conv2D(75, (3,3), activation='relu', padding='same')(input)
    x1_pool = MaxPooling2D(2, 2)(x1)
    x1_flatten = Flatten()(x1_pool)
    # Dense Layer
    x2 = Dense(512, kernel_regularizer=regularizers.l2(1e-5), activation='relu')(x1_flatten)
    x2_dropout = Dropout(0.2)(x2)
    # Second Dense Layer
    x3 = Dense(128, kernel_regularizer=regularizers.l2(1e-5), activation='relu')(x2_dropout)
    x3_dropout = Dropout(0.2)(x3)
    # Output Layer
    output_layer = Dense(len(classes), activation='softmax')(x3_dropout)
    model = Model(input, output_layer)

    return model

def get_checkpoint():
    checkpoint_path = "./models/checkpoint.weights.keras"
    checkpoint = ModelCheckpoint(filepath=checkpoint_path,
                                save_freq='epoch',
                                save_weights_only = False,
                                monitor = "val_accuracy",
                                save_best_only = True,
                                verbose = 1
                                )
    return checkpoint

def run():
    train_dir = './files/TumorClassification/train'
    test_dir = './files/TumorClassification/test'

    # Data Image Generators
    train_datage = ImageDataGenerator(rescale=1./255)
    test_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

    # Train Generator
    train_generator = train_datage.flow_from_directory(
    train_dir,
    target_size=(124, 124),
    batch_size=128,
    class_mode='categorical',
    color_mode='grayscale',
    subset = 'training'
    )
    # Validation Generator
    validation_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=(124, 124),
        batch_size=128,
        class_mode='categorical',
        color_mode='grayscale',
        subset = 'validation'
    )
    # Test Generator
    test_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=(124, 124),
        batch_size=128,
        class_mode='categorical',
        color_mode='grayscale',
    )

    classes = ["BENIGN", "MALIGNANT", "NORMAL"]

    model = create_model(classes)
    model.summary()

    model.compile(optimizer=Adam(0.001), loss='categorical_crossentropy', metrics=['accuracy'])
    checkpoint = get_checkpoint()

    model.fit(train_generator, epochs=10, validation_data=validation_generator, callbacks=[checkpoint])

    try:
        model.save('./models/model.h5')
        print("Model saved")
    except:
        print("Error saving model")

    print(model.evaluate(test_generator))

if __name__ == "__main__":
    run()