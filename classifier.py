import cv2
import numpy as np
import joblib
import pickle as pk


class RandomForest:
    dictionary = {
        0: 'Apple Braeburn',
        1: 'Apricot',
        2: 'Avocado',
        3: 'Banana',
        4: 'Blueberry',
        5: 'Cantaloupe 2',
        6: 'Carambula',
        7: 'Cherry 1',
        8: 'Cocos',
        9: 'Eggplant',
        10: 'Grape White 3',
        11: 'Grapefruit White',
        12: 'Guava',
        13: 'Kiwi',
        14: 'Kumquats',
        15: 'Limes',
        16: 'Lychee',
        17: 'Mandarine',
        18: 'Mango',
        19: 'Mangostan',
        20: 'Orange',
        21: 'Papaya',
        22: 'Passion Fruit',
        23: 'Peach',
        24: 'Pear',
        25: 'Pineapple',
        26: 'Pitahaya Red',
        27: 'Plum',
        28: 'Pomegranate',
        29: 'Rambutan',
        30: 'Strawberry',
        31: 'Walnut',
        32: 'Watermelon'
    }

    def __init__(self):
        self.scaler = pk.load(open("scaler.pkl", 'rb'))
        self.pca = pk.load(open("pca.pkl", 'rb'))
        self.forest = joblib.load("random_forest.joblib")

    def detect_fruit(self, img):
        img = cv2.resize(img, (45, 45))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        image = [img]
        image = np.array(image)
        # print(image[0].shape)
        image = self.scaler.transform([i.flatten() for i in image])
        pca_result = self.pca.transform(image)
        prediction = self.forest.predict(pca_result)
        return self.dictionary[prediction[0]]


# rf = RandomForest()
# print(rf.detect_fruit(cv2.imread("temp/58_100.jpg", cv2.IMREAD_COLOR)))
# print(rf.detect_fruit(cv2.imread("temp/3_100.jpg", cv2.IMREAD_COLOR)))
