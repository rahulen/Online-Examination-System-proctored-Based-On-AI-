
import numpy as np
from keras.layers import Conv2D, Input, BatchNormalization, MaxPooling2D, Activation, Flatten, Dense, Dropout
from keras.models import Model
from keras.preprocessing import image
import cv2

class EmotionRecognitionModel:
    def __init__(self, input_shape):
        self.model = self._build_model(input_shape)
        self.model.load_weights('models\image\model_weights.hdf5')
        self.face_cascade = cv2.CascadeClassifier('models/image//haarcascade_frontalface_default.xml')
        self.label_dict = {0: 'Angry', 1: 'Disgusting', 2: 'Fear', 3: 'Happy', 4: 'Sad', 5: 'Surprise', 6: 'Neutral'}

    def _build_model(self, input_shape):
        X_input = Input((48,48,1))

        X = Conv2D(32, kernel_size=(3,3), strides=(1,1), padding='valid')(X_input)
        X = BatchNormalization(axis=3)(X)
        X = Activation('relu')(X)


        X = Conv2D(64, (3,3), strides=(1,1), padding = 'same')(X)
        X = BatchNormalization(axis=3)(X)
        X = Activation('relu')(X)

        X = MaxPooling2D((2,2))(X)

        X = Conv2D(64, (3,3), strides=(1,1), padding = 'valid')(X)
        X = BatchNormalization(axis=3)(X)
        X = Activation('relu')(X)

        X = Conv2D(128, (3,3), strides=(1,1), padding = 'same')(X)
        X = BatchNormalization(axis=3)(X)
        X = Activation('relu')(X)


        X = MaxPooling2D((2,2))(X)

        X = Conv2D(128, (3,3), strides=(1,1), padding = 'valid')(X)
        X = BatchNormalization(axis=3)(X)
        X = Activation('relu')(X)

        

        X = MaxPooling2D((2,2))(X)
        X = Flatten()(X)
        X = Dense(200, activation='relu')(X)
        X = Dropout(0.6)(X)
        X = Dense(7, activation = 'softmax')(X)

        model = Model(inputs=X_input, outputs=X)
        return model

    def detect_emotion_in_frame(self, cap_image):
        cap_img_gray = cv2.cvtColor(cap_image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(cap_img_gray, 1.3, 5)
        emotion_predictions = []

        if len(faces) == 0:
            return cap_image, ""

        for (x, y, w, h) in faces:
            cv2.rectangle(cap_image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = cap_img_gray[y:y + h, x:x + w]
            roi_gray = cv2.resize(roi_gray, (48, 48))
            img_pixels = image.img_to_array(roi_gray)
            img_pixels = np.expand_dims(img_pixels, axis=0)

            predictions = self.model.predict(img_pixels)
            emotion_label = np.argmax(predictions)
            emotion_prediction = self.label_dict[emotion_label]
            emotion_predictions.append(emotion_prediction)

            cv2.putText(cap_image, emotion_prediction, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        print(emotion_predictions)

        return cap_image, emotion_prediction
    



# Importing required packages
from keras.models import load_model
import numpy as np
import argparse
import dlib
import cv2


emotion_offsets = (20, 40)
emotions = {
    0: {
        "emotion": "Angry",
        "color": (193, 69, 42)
    },
    1: {
        "emotion": "Disgust",
        "color": (164, 175, 49)
    },
    2: {
        "emotion": "Fear",
        "color": (40, 52, 155)
    },
    3: {
        "emotion": "Happy",
        "color": (23, 164, 28)
    },
    4: {
        "emotion": "Sad",
        "color": (164, 93, 23)
    },
    5: {
        "emotion": "Suprise",
        "color": (218, 229, 97)
    },
    6: {
        "emotion": "Neutral",
        "color": (108, 72, 200)
    }
}


def shapePoints(shape):
    coords = np.zeros((68, 2), dtype="int")
    for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)
    return coords


def rectPoints(rect):
    x = rect.left()
    y = rect.top()
    w = rect.right() - x
    h = rect.bottom() - y
    return (x, y, w, h)


faceLandmarks = "models\shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(faceLandmarks)

emotionModelPath = 'models\emotionModel.hdf5'  # fer2013_mini_XCEPTION.110-0.65
emotionClassifier = load_model(emotionModelPath, compile=False)
emotionTargetSize = emotionClassifier.input_shape[1:3]


def identify_emotion(frame):
    
    frame = cv2.resize(frame, (720, 480))

    detected_emotion = ""

    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(grayFrame, 0)
    for rect in rects:
        # shape = predictor(grayFrame, rect)
        # points = shapePoints(shape)
        (x, y, w, h) = rectPoints(rect)
        # grayFace = grayFrame[y:y + h, x:x + w]
        # try:
        #     grayFace = cv2.resize(grayFace, (emotionTargetSize))
        # except:
        #     continue

        color = (255, 255, 255)
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

        # grayFace = grayFace.astype('float32')
        # grayFace = grayFace / 255.0
        # grayFace = (grayFace - 0.5) * 2.0
        # grayFace = np.expand_dims(grayFace, 0)
        # grayFace = np.expand_dims(grayFace, -1)
        # emotion_prediction = emotionClassifier.predict(grayFace)
        # emotion_probability = np.max(emotion_prediction)
        # if (emotion_probability > 0.36):
        #     emotion_label_arg = np.argmax(emotion_prediction)
        #     color = emotions[emotion_label_arg]['color']
        #     cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        #     cv2.line(frame, (x, y + h), (x + 20, y + h + 20),
        #              color,
        #              thickness=2)
        #     cv2.rectangle(frame, (x + 20, y + h + 20), (x + 110, y + h + 40),
        #                   color, -1)
        #     cv2.putText(frame, emotions[emotion_label_arg]['emotion'],
        #                 (x + 25, y + h + 36), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
        #                 (255, 255, 255), 1, cv2.LINE_AA)
            
        #     detected_emotion  =emotions[emotion_label_arg]['emotion']
        # else:
        #     color = (255, 255, 255)
        #     cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

        

    
    return frame,detected_emotion
 