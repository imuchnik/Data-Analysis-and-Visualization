import os
import pandas as pd
import matplotlib.pyplot as plt
import LinRegLearner as lrl
import KNNLearner as knn
import numpy as np
import csv


#HERE IS ALL PRELIMINARY METHODS FOR GETTING THE PRICES DATA, ETC.
#Get the relevant data into a data frame
def symbol_to_path(symbol, base_dir="data"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))

def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols.insert(0, 'SPY')

    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date',
                parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])
        df_temp = df_temp.rename(columns={'Adj Close': symbol})
        df = df.join(df_temp)
        if symbol == 'SPY':  # drop dates SPY did not trade
            df = df.dropna(subset=["SPY"])

    return df

#CALCULATE THE INDICATORS

#Calculate the bollinger values
def getBollingerVals(df):
    sma = pd.rolling_mean(df, window=10)
    std = pd.rolling_std(df, window = 10)
    bb = df.copy()
    for i in df.index:
        bb.ix[i]=(bb.ix[i]-sma.ix[i])/(2*std.ix[i])
    bbVals = bb.ix[:,0]
    return bbVals


#Calculate the momentum
def getMomentum(df):
    prices = df.ix[:,0]
    newPrices = (prices/prices.shift(10))-1
    return newPrices


#Calculate the volatility
def getVolatility(prices):
    dr = (prices/prices.shift(1))-1
    vol = pd.rolling_std(dr, window = 10)
    return vol

#Calculate the five day returns
def getYVal(df):
    prices = df.ix[:,0]
    pricesB = prices.copy()
    newPrices = (pricesB.shift(-5)/pricesB)-1
    return newPrices

#Get data frame with all four columns
def getAllData(symbols, dates):
    df = get_data(symbols, dates)
    dfPrices = df.ix[:,1]
    dfUse = pd.DataFrame(data = dfPrices, index = df.index)
    df2 = pd.DataFrame(index = df.index, columns = ['BollingerVal', 'Momentum', 'Volatility', 'YVal', 'PRICE'])
    df2['BollingerVal']=getBollingerVals(dfUse)
    df2['Momentum']=getMomentum(dfUse)
    df2['Volatility']=getVolatility(dfUse)
    df2['YVal']=getYVal(dfUse)
    df2['PRICE'] = dfPrices
    return df2

#Get the xTrain data
def getXTrain(df):
    df2 = df[['BollingerVal', 'Momentum', 'Volatility']]
    return df2

#Get the yTrain data
def getYTrain(df):
    df2 = df['YVal']
    return df2

#Plot a dataframe
def plot_chart(prices, title="Chart One"):
    ax = prices.plot(title=title, label="Prices")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc='upper left')
    plt.show()

#Strategy
def myStrategy(df, predictedDf, symbol, fileName, title):
    ax = df['PRICE'].plot(title=title, label=symbol, color = 'blue')
    # Add axis labels and legend
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc='upper left')

    allDates = df.index

    longs = pd.DataFrame(index = df.index, columns = ['EN', 'EX'])
    shorts = pd.DataFrame(index = df.index, columns = ['EN', 'EX'])
    holdingStock = pd.DataFrame(index = df.index, columns = ['HOLDING'])
    holdingStock = holdingStock.fillna(0)

    predicted = predictedDf['PRED']

    for x in range(1, allDates.size-7):
        yesterday = allDates[x-1]
        today = allDates[x]
        hold1 = allDates[x+1]
        hold2 = allDates[x+2]
        exitDate = allDates[x+3]

        numLong = .01
        numShort = -.01

        if predicted[today]>=numLong and holdingStock.ix[today, 'HOLDING'] == 0:

            #Long Entry
            longs.ix[today, 'EN'] = 1
            longs.ix[today, 'EX'] = 0

            #Hold for two days, sell at end of third
            holdingStock.ix[today, 'HOLDING'] = 1
            holdingStock.ix[hold1, 'HOLDING'] = 1
            holdingStock.ix[hold2, 'HOLDING'] = 1

            longs.ix[exitDate, 'EN'] = 0
            longs.ix[exitDate, 'EX'] = 1
            holdingStock.ix[exitDate, 'HOLDING'] = 1

        #Now do the shorts
        if predicted[today]<=numShort and holdingStock.ix[today, 'HOLDING'] == 0:
            #Short entry
            shorts.ix[today, 'EN'] = 1
            shorts.ix[today, 'EX'] = 0

            #Hold for two days, sell at end of third
            holdingStock.ix[today, 'HOLDING'] = 1
            holdingStock.ix[hold1, 'HOLDING'] = 1
            holdingStock.ix[hold2, 'HOLDING'] = 1

            #Exit
            shorts.ix[exitDate, 'EN'] = 0
            shorts.ix[exitDate, 'EX'] = 1
            holdingStock.ix[exitDate, 'HOLDING'] = 1



    c = csv.writer(open(fileName, "wb"))
    c.writerow(["Date","Symbol","Order","Shares"])

    for y in range (0, allDates.size-1, 1):
        date = allDates[y]
        dateString = str(date)[:10]
        numLongShares = "5000"
        numShortShares = "5000"

        # if predicted[today]>=.05:
        #     numLongShares = "5000"
        # elif predicted[today]>.04:
        #     numLongShares = "4000"
        # elif predicted[today]>=.03:
        #     numLongShares = "3000"
        # elif predicted[today]>=.02:
        #     numLongShares = "2000"
        # elif predicted[today]>=.01:
        #     numLongShares = "100"
        #
        # if predicted[today]<=-.05:
        #     numShortShares = "5000"
        # elif predicted[today]<=-.04:
        #     numShortShares = "4000"
        # elif predicted[today]<=-.03:
        #     numShortShares = "3000"
        # elif predicted[today]<=-.02:
        #     numShortShares = "2000"
        # elif predicted[today]<=-.01:
        #     numShortShares = "100"


        if longs.ix[date, 'EN']==1:
           plt.axvline(date, color = 'green')
           c.writerow([dateString, symbol, "BUY", numLongShares])
        if longs.ix[date, 'EX']==1:
           plt.axvline(date, color = 'black')
           c.writerow([dateString, symbol, "SELL", numLongShares])
        if shorts.ix[date, 'EN']==1:
            plt.axvline(date, color = 'red')
            c.writerow([dateString, symbol, "SELL", numShortShares])
        if shorts.ix[date, 'EX']==1:
            plt.axvline(date, color = 'black')
            c.writerow([dateString, symbol, "BUY", numShortShares])
    plt.show()

#IN SAMPLE SINE DATA, STRATEGY TEST
def inSampleSineTest():

    #Get the data
    dates = pd.date_range('2007-12-31', '2009-12-31')
    symbols = ['ML4T-399']
    prices = get_data(symbols, dates)
    df = getAllData(symbols, dates)

    #Get the xTrain and yTrain values
    xTrain=getXTrain(df)
    yTrain = getYTrain(df)

    #Create the learner
    learner = knn.KNNLearner(k=3)

    #Train the learner
    learner.addEvidence(xTrain.values, yTrain.values)

    #Query the learner ON THE IN SAMPLE DATA
    predicted = learner.query(xTrain.values)
    predictedDf = pd.DataFrame(data=predicted, index = prices.index, columns = ['PRED'])

    #Call the strategy. Args to pass it are:
    #The df with the prices data for the test year, for the plot
    #The df with the predictions for the test year, for the strategy
    #The symbol
    myStrategy(df, predictedDf, "ML4T-399", "inSampleSine.csv", "IN SAMPLE 399")

#IN SAMPLE IBM DATA, STRATEGY TEST
def inSampleIbmTest():
    #Get the data
    dates = pd.date_range('2007-12-31', '2009-12-31')
    symbols = ['IBM']
    prices = get_data(symbols, dates)
    df = getAllData(symbols, dates)

    #Get the xTrain and yTrain values
    xTrain=getXTrain(df)
    yTrain = getYTrain(df)

    #Create the learner
    learner = knn.KNNLearner(k=3)

    #Train the learner
    learner.addEvidence(xTrain.values, yTrain.values)

    #Query the learner ON THE IN SAMPLE DATA
    predicted = learner.query(xTrain.values)
    predictedDf = pd.DataFrame(data=predicted, index = prices.index, columns = ['PRED'])

    #Call the strategy. Args to pass it are:
    #The df with the prices data for the test year, for the plot
    #The df with the predictions for the test year, for the strategy
    #The symbol
    myStrategy(df, predictedDf, "IBM", "inSampleIbm.csv", "IN SAMPLE IBM")

#OUT OF SAMPLE SINE DATA, STRATEGY TEST
def outOfSampleSineTest():
    # Get data for 2008-2009 training
    dates = pd.date_range('2007-12-31', '2009-12-31')
    symbols = ['ML4T-399']
    prices = get_data(symbols, dates)
    df = getAllData(symbols, dates)

    #Get data for 2010 testing. Need the correct index, and the prices in order to plot it.
    testDates = pd.date_range('2009-12-31', '2010-12-31')
    df2010Dates = get_data(symbols, testDates)
    df2010 = getAllData(symbols, testDates)
    correctIndex = df2010Dates.index


    #Get the x train and the y train values from the 2008-2009 dataframe
    xTrain=getXTrain(df)
    yTrain = getYTrain(df)

    #Create the learner
    learner = knn.KNNLearner(k=3)

    #Train the learner on the 2008-2009 values
    learner.addEvidence(xTrain.values, yTrain.values)

    #Get query data for 2010
    xTest = getXTrain(df2010)

    #Query the learner
    predicted = learner.query(xTest.values)
    predictedDf = pd.DataFrame(data = predicted, index = correctIndex, columns = ['PRED'])

    #Run the strategy
    myStrategy(df2010, predictedDf, "ML4T-399", "outOfSampleSine.csv", "OUT OF SAMPLE 399")


#OUT OF SAMPLE IBM DATA, STRATEGY TEST
def outOfSampleIbmTest():
     # Get data for 2008-2009 training
    dates = pd.date_range('2007-12-31', '2009-12-31')
    symbols = ['IBM']
    prices = get_data(symbols, dates)
    df = getAllData(symbols, dates)

    #Get data for 2010 testing. Need the correct index, and the prices in order to plot it.
    testDates = pd.date_range('2009-12-31', '2010-12-31')
    df2010Dates = get_data(symbols, testDates)
    df2010 = getAllData(symbols, testDates)
    correctIndex = df2010Dates.index


    #Get the x train and the y train values from the 2008-2009 dataframe
    xTrain=getXTrain(df)
    yTrain = getYTrain(df)

    #Create the learner
    learner = knn.KNNLearner(k=3)

    #Train the learner on the 2008-2009 values
    learner.addEvidence(xTrain.values, yTrain.values)

    #Get query data for 2010
    xTest = getXTrain(df2010)

    #Query the learner
    predicted = learner.query(xTest.values)
    predictedDf = pd.DataFrame(data = predicted, index = correctIndex, columns = ['PRED'])

    #Run the strategy
    myStrategy(df2010, predictedDf, "IBM", "outOfSampleIBM.csv", "OUT OF SAMPLE IBM")

#PLOT THE ACTUAL PRICE, TRAINING Y, AND PREDICTED Y FOR 2008-2009, ML4T-399
def chartOne():
    # Get data
    dates = pd.date_range('2007-12-31', '2009-12-31')
    symbols = ['ML4T-399']
    prices = get_data(symbols, dates)
    df = getAllData(symbols, dates)

    #Get the x train and the y train values
    xTrain=getXTrain(df)
    yTrain = getYTrain(df)

    #Create the learner
    learner = knn.KNNLearner(k=3)

    #Train the learner
    learner.addEvidence(xTrain.values, yTrain.values)

    #Query the learner
    predicted = learner.query(xTrain.values)
    predictedDf = pd.DataFrame(data=predicted, index = prices.index, columns = ['PRED'])
    dfYVals = df['YVal']

    pricesToUse = prices['ML4T-399']
    trainingToUse =  pricesToUse * (1 + dfYVals)
    predictedToUse = pricesToUse * (1 + predictedDf)

    allToChart = pd.DataFrame(index = prices.index, columns = ['PRICES', 'TRAINING_Y', 'PREDICTED_Y'])
    allToChart['PRICES']=pricesToUse
    allToChart['TRAINING_Y']=trainingToUse
    allToChart['PREDICTED_Y']=predictedToUse
    plot_chart(allToChart, "PRICES, PREDICTED, AND TRAINING DATA FOR ML4T-399")



#main
def test_run():
    chartOne()
    inSampleSineTest()
    inSampleIbmTest()
    outOfSampleSineTest()
    outOfSampleIbmTest()

if __name__ == "__main__":
    test_run()