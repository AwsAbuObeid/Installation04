import csv
import numpy as np
from sklearn.model_selection import train_test_split
import statistics
from sklearn import preprocessing
from sklearn.neural_network import MLPClassifier


# this function will open the CSV file and get the selected columns,
# cast them to floats and return the data as a numpy array
def getDataFromFile(path, cols):
    file = open(path)
    rawData = csv.reader(file)
    next(rawData)
    newData = []

    for row in rawData:
        newRow = []
        for index in cols:
            newRow.append(float(row[index]))
        newData.append(newRow)

    return np.array(newData)


# HLRV will  take a period of prices and volumes and return high low ret vol of that period
def HLRV(period):
    # ignoring unix and date
    high = period[:, 1].max()
    low = period[:, 1].min()
    ret = (period[-1, 1] - period[0, 1]) / period[0, 1]
    vol = period[:, 2].sum()
    return [high, low, ret, vol]


# this function will take the raw price and volume data and create features on specific intervals
# at each point (based on the jump value ) it will take a number of past periods, each with a specific
# size based on the PeriodStartingSize and the increment.
# it will also add a Y value at the end column of each row indicating price movement based on the
# horizon.
def priceFeature(rawData, PeriodCount, PeriodStartingSize, increment, horizon, jump):
    feat = []
    Y = []

    # finding starting pos
    InitStartPos = int(
        (((PeriodCount - 1) * (PeriodCount - 1) + (PeriodCount - 1)) / 2) * increment + (
                    PeriodStartingSize * PeriodCount))
    startPos = InitStartPos + (jump - InitStartPos % jump)
    # _____

    for i in range(startPos, len(rawData) - horizon, jump):
        # create Ys
        if float(rawData[i, 1]) > float(rawData[i + horizon, 1]):
            Y.append([rawData[i, 0], 0])
        else:
            Y.append([rawData[i, 0], 1])
        # _____
        x = []
        size = PeriodStartingSize + 0.0
        start = i - int(size) + 1
        for j in range(PeriodCount):
            x.append(HLRV(rawData[start:start + int(size)]))
            size += increment
            start = start - int(size)

        f = [rawData[i, 0], rawData[i, 1]]

        for j in x:
            f = f + j
        feat.append(f)
    featnp = np.array(feat)
    Y = np.array(Y)
    return featnp, Y


# this function will take the raw technical data every 15 mins and add values on each
# row representing previous values.
def simpleFeature(n_p,prev):
    unix=n_p[:,0]
    n_p=n_p[:,1]
    n_p=n_p.flatten()
    feat=[]
    for i in range(prev,len(n_p)) :
        x=[]
        for j in range(0,prev+1):
            x.append(n_p[i-j])
        feat.append([unix[i]]+x)
    return np.array(feat)

# [0] is the time in unix
# price features
price_min = getDataFromFile(r'G:\...\BTCUSD_2021_minute.csv',[0, 2, 3]) #time,price,volume
# technical features
btc_mem = getDataFromFile(r'G:\...\Mem_Data.csv', [0, 2])
btc_tps = getDataFromFile(r'G:\...\TPS_Data.csv', [0, 2])
# stock features
oil = getDataFromFile(r'G:\...\Stock_Data.csv', [0, 2])
msci = getDataFromFile(r'G:\...\Stock_Data.csv', [0, 3])
gld = getDataFromFile(r'G:\...\Stock_Data.csv', [0, 4])
snp = getDataFromFile(r'G:\...\Stock_Data.csv', [0, 5])
btc_tweets = getDataFromFile(r'G:\...\N_Tweets_Data.csv', [0, 2])


# setting the values for the below variables sets the training data
hor = 60                # prediction horizon minutes
usedFeatures = "prices" # what features to use, "prices" ,"no stock" , "all"
p_start = 30            # starting period size for price features
p_count = 40            # number of periods for price features
inc = 60                # increment for period size for price features
tec = 50                # number of past values in the technical features
stoc = 4                # number of past days in the stock features
trainingSetSize = 1     # what fraction of the data set to use
hid = 3                # number of hidden layers for NN
alpha = 0.001           # alpha for NN

# create training data set
Price_feat, output = priceFeature(price_min, p_count, p_start, inc, hor, 10)
# arrays containing all the starting and ending times of the data for sync purposes
allDataStartingTimes = [Price_feat[0, 0], output[0, 0]]
allDataEndingTimes = [Price_feat[-1, 0], output[-1, 0]]

if (usedFeatures == 'no stock' or usedFeatures == 'all'):
    btc_mem_feat = simpleFeature(btc_mem, tec)  # number must div 2
    btc_tps_feat = simpleFeature(btc_tps, tec)  # number must div 2
    btc_tweets_feat = simpleFeature(btc_tweets, tec)

    allDataStartingTimes.append(btc_mem_feat[0, 0])
    allDataStartingTimes.append(btc_tps_feat[0, 0])
    allDataStartingTimes.append(btc_tweets_feat[0, 0])

    allDataEndingTimes.append(btc_mem_feat[-1, 0])
    allDataEndingTimes.append(btc_tps_feat[-1, 0])
    allDataEndingTimes.append(btc_tweets_feat[-1, 0])

    if (usedFeatures == 'all'):
        oil_feat = simpleFeature(oil, stoc * 96)
        gld_feat = simpleFeature(gld, stoc * 96)
        snp_feat = simpleFeature(snp, stoc * 96)
        msci_feat = simpleFeature(msci, stoc * 96)

        allDataStartingTimes.append(oil_feat[0, 0])
        allDataStartingTimes.append(gld_feat[0, 0])
        allDataStartingTimes.append(snp_feat[0, 0])
        allDataStartingTimes.append(msci_feat[0, 0])

        allDataEndingTimes.append(oil_feat[-1, 0])
        allDataEndingTimes.append(gld_feat[-1, 0])
        allDataEndingTimes.append(snp_feat[-1, 0])
        allDataEndingTimes.append(msci_feat[-1, 0])

startingUnix=max(allDataStartingTimes)
endingUnix=min(allDataEndingTimes)
X = Price_feat[np.where(Price_feat[:, 0] == startingUnix)[0][0]:np.where(Price_feat[:, 0] == endingUnix)[0][0]]

if (usedFeatures == 'no stock' or usedFeatures == 'all'):
    X = np.c_[X, btc_mem_feat[np.where(btc_mem_feat[:, 0] == startingUnix)[0][0]:np.where(btc_mem_feat[:, 0] == endingUnix)[0][0]]]
    X = np.c_[X, btc_tps_feat[np.where(btc_tps_feat[:, 0] == startingUnix)[0][0]:np.where(btc_tps_feat[:, 0] == endingUnix)[0][0]]]
    X = np.c_[X, btc_tweets_feat[np.where(btc_tweets_feat[:, 0] == startingUnix)[0][0]:np.where(btc_tweets_feat[:, 0] == endingUnix)[0][0]]]

    if (usedFeatures == 'all'):
        X = np.c_[X, msci_feat[np.where(msci_feat[:, 0] == startingUnix)[0][0]:np.where(msci_feat[:, 0] == endingUnix)[0][0]]]
        X = np.c_[X, oil_feat[np.where(oil_feat[:, 0] == startingUnix)[0][0]:np.where(oil_feat[:, 0] == endingUnix)[0][0]]]
        X = np.c_[X, snp_feat[np.where(snp_feat[:, 0] == startingUnix)[0][0]:np.where(snp_feat[:, 0] == endingUnix)[0][0]]]
        X = np.c_[X, gld_feat[np.where(gld_feat[:, 0] == startingUnix)[0][0]:np.where(gld_feat[:, 0] == endingUnix)[0][0]]]

# what rows to use:
x = X[len(X) - len(X)*trainingSetSize:]
Y = output[np.where(output[:, 0] == startingUnix)[0][0]:np.where(output[:, 0] == endingUnix)[0][0]]
y = Y[len(X) - len(X)*trainingSetSize:, 1:]

# checking the data times are synced
if sum(Y[:, 0] != X[:, 0]) != 0:
    raise Exception("Desync in the data times")

# scaling
scaler = preprocessing.StandardScaler().fit(x)
x = scaler.transform(x)

print("sample size :",int((((p_count - 1) * (p_count - 1) +
                            (p_count - 1)) / 2) * inc + (p_start * p_count)))
y=y.flatten()

# Split the dataset into training and test dataset
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.3,random_state=10)

# unskew the data, making the ups and down data points the same number
if False:
    one=0
    zero=np.count_nonzero(y_train==0)
    ones_del=0
    r0=[]
    for i in range(len(y_train)):
        if y_train[i]==1:
            one=one+1
            if(one>zero):
                r0.append(i)
                ones_del=ones_del+1
    x_train=np.delete(x_train,r0,0)
    y_train=np.delete(y_train,r0,0)

# training
clf = MLPClassifier(solver='adam', alpha=alpha, hidden_layer_sizes=(int(x.shape[1]*2/3), hid), random_state=1, max_iter=10000, shuffle=False)
clf.fit(x_train, y_train)

y_test_pred = clf.predict(x_test)
y_train_pred = clf.predict(x_train)

# results{
# this finds the accuracy of the prediction by comparing it to the real output
test_acc=statistics.mean((y_test_pred==y_test)+0.0)*100
train_acc=statistics.mean((y_train_pred==y_train)+0.0)*100
attr='horizon: '+str(hor)+'h, feats: '+cols+', rows :'+str(rows)+', tec: '+str(tec)+' ,stocdays='+str(stoc) \
     +',\nP_count='+str(p_count)+' ,p_start='+str(p_start) \
     +' ,inc '+str(inc)+' ,alpha='+str(alpha)+' ,hid='+str(hid)

print(attr)
print("train acc: ",train_acc)
print("test acc: ",test_acc)