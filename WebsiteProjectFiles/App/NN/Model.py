import numpy as np
import json
from joblib import load


class Model:
    model = 0
    scaler = 0
    config = 0
    PeriodCount = 0
    PeriodStartingSize = 0
    inc = 0.0
    hor = ""
    sampleLength = 0
    coin = ""

    def __init__(self, dir):
        self.dir = dir
        self.model = load(dir + '/NNmodel.joblib')
        self.scaler = load(dir + '/scaler.joblib')
        with open(dir + '/config.txt') as f:
            data = f.read()
        self.config = json.loads(data)

        self.PeriodCount = int(self.config["PeriodCount"])
        self.PeriodStartingSize = int(self.config["PeriodStartingSize"])
        self.sampleLength = int(self.config["sampleLength"])
        self.inc = float(self.config["inc"])
        self.hor = self.config["hor"]
        self.coin = self.config["coin"]

    def HLRV(self, arr):
        high = arr[:, 1].max()
        low = arr[:, 1].min()
        ret = (arr[-1, 1] - arr[0, 1]) / arr[0, 1]
        vol = arr[:, 2].sum()
        return [high, low, ret, vol]

    def sampleOf(self, n_p):
        if len(n_p) != int(
                (((self.PeriodCount - 1) * (self.PeriodCount - 1) + (self.PeriodCount - 1)) / 2) * self.inc + (
                        self.PeriodStartingSize * self.PeriodCount)):
            print(int(
                (((self.PeriodCount - 1) * (self.PeriodCount - 1) + (self.PeriodCount - 1)) / 2) * self.inc + (
                        self.PeriodStartingSize * self.PeriodCount)))
            err = " Model expected a sample of size :" + str(len(n_p)) + " but got :" + str(len(n_p))
            print("Model couldnt predict, " + err)
            # raise Exception(err)
        i = len(n_p) - 1
        x = []
        size = self.PeriodStartingSize + 0.0
        start = i - int(size) + 1
        for j in range(self.PeriodCount):
            x.append(self.HLRV(n_p[start:start + int(size)]))
            size += self.inc
            start = start - int(size)

        f = [n_p[i, 0], n_p[i, 1]]

        for j in x:
            f = f + j
        return np.array(f)

    def predict(self, n_p):
        sample = self.sampleOf(n_p).reshape(1, -1)
        sample = self.scaler.transform(sample)
        pred = int(self.model.predict(sample)[0])
        print(self.coin, self.hor, "Model is predicting...")
        return pred
