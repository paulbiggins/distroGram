import sys
import csv
import math
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'AkkuratPro'
plt.rcParams['xtick.major.pad']='9'
plt.rcParams['ytick.major.pad']='9'
colorMap = ['#0066cc', '#ff0000', '#f2b111', '#78aa42', '#833083', '#ff6600', '#fc27c1', '#b0ff01', '#7c757f']
             #blue      #red       #yellow    #green     #purple    #orange    #pink      #neon      #grey

def mean(data):
#return the sample arithmetic mean of data.
    n = len(data)
    if n < 1:
        raise ValueError('mean requires at least one data point')
    return sum(data)/n # in Python 2 use sum(data)/float(n)


def _ss(data):
#return sum of square deviations of sequence data.
    c = mean(data)
    ss = sum((x-c)**2 for x in data)
    return ss


def pstdev(data):
#calculates the population standard deviation.
    n = len(data)
    if n < 2:
        raise ValueError('variance requires at least two data points')
    ss = _ss(data)
    pvar = ss/n # the population variance
    return pvar**0.5


def IQR(data):
#calculates the IQR
    data.sort()
    n = len(data)
    q1pos = (n + 1) / 4
    q1posfloor = int(math.floor(q1pos))
    q3pos = 3 * (n + 1) / 4
    q3posfloor = int(math.floor(q3pos))

    q1 = data[q1posfloor] + (q1pos - q1posfloor) * (data[q1posfloor+1] - data[q1posfloor])
    q3 = data[q3posfloor] + (q3pos - q3posfloor) * (data[q3posfloor+1] - data[q3posfloor])

    IQR = q3 - q1
    return IQR

def statigram (data, plotType):
#does statistics on the data
    mu = sigma = bins = r = 0

    if plotType == 'Distribution':
        mu = mean(data)
        sigma = pstdev(data)
        n = len(data)
        #bins = math.ceil(math.sqrt(n)) #square root choice
        #bins = math.ceil(math.log(n,2)+1) #sturges' formula
        #bins = math.ceil(2*n**(1/3.0)) #rice rule
        #binwidth = 3.5 * sigma / (n**(1/3.0)) #scott's nominal reference rule
        binwidth = 2 * IQR(data) / (n**(1/3.0)) #freedman-diaconis' choice
        bins = math.ceil((max(data) - min(data)) / binwidth)

    elif plotType == 'Correlation':
        muA = mean(data[0][0])
        a = [(val - muA) for val in data[0][0]]
        muB = mean(data[1][0])
        b = [(val - muB) for val in data[1][0]]

        aTimesb = [a[i] * b[i] for i in range(len(a))]
        aSquared = [aDex**2.0 for aDex in a]
        bSquared = [bDex**2.0 for bDex in b]
        r = sum(aTimesb) / math.sqrt(sum(aSquared) * sum(bSquared))

    return (mu, sigma, bins, r)

def parsigram (f, plotType):
#parses out a mess of CSV's
    parsedData = []

    try:
        reader = csv.reader(f)

        header = next(reader)
        #make an options dialog
        print ('\nChoose data for ' + plotType + 'plot:\n')
        for option in range(0,len(header)):
            print ("(%i) %s" % (option, header[option]))
        choice = int(raw_input('\nType a Number: '))
        axTitle = header[choice]

        #grab data and put into list form
        for row in reader:
            if row[choice]:
                parsedData.append(float(row[choice]))

    finally:
        f.close()

    return (parsedData, axTitle)


def histoplot (data, xTitle, mu, sigma, bins):
#plots a histogram of the data

    plt.style.use('fivethirtyeight')
    plt.figure(num = None, figsize = (12, 9), dpi = 80, facecolor = 'w', edgecolor = 'k')
    plt.title(name + ', Mean = %.2f, Sigma = %.2f' %(mu, sigma))

    colorNum = 0
    plt.hist(data, bins, normed = 0, facecolor = colorMap[colorNum]) #normed is for frequency (probability)
    plt.ylabel('Counts')
    colorNum += 1
    plt.axvline(mu, color = colorMap[colorNum], linewidth = 3, linestyle = '-')
    colorNum += 1

    for n in range(1,4):
        plt.axvline(mu - (n*sigma), color = colorMap[colorNum], linewidth = 4, linestyle = '--', alpha = 0.1 * n + 0.2)
        plt.axvline(mu + (n*sigma), color = colorMap[colorNum], linewidth = 4, linestyle = '--', alpha = 0.1 * n + 0.2)
    plt.text(mu-(3*sigma), -2.5, '%.2f' %(mu-(3*sigma)), fontsize = 10, color = colorMap[colorNum], horizontalalignment = 'center')
    plt.text(mu+(3*sigma), -2.5, '%.2f' %(mu+(3*sigma)), fontsize = 10, color = colorMap[colorNum], horizontalalignment = 'center')
    plt.xlabel(xTitle)

    plt.grid(True)
    plt.show()
    return


def correlaplot (data, xTitle, yTitle, r):
#plots a scatter plot of correlation data

    plt.style.use('fivethirtyeight')
    plt.figure(num = None, figsize = (12, 9), dpi = 80, facecolor = 'w', edgecolor = 'k')
    plt.title(name + ', Correlation Coefficient = %.2f' %r)

    plt.scatter(data[0][0], data[1][0], s = 50, color = colorMap[0], alpha = 0.35)
    plt.ylabel(yTitle)
    plt.xlabel(xTitle)

    plt.show()
    return


#void main() {
data = []
typeNum = int(sys.argv[2])
plotType = ['Distribution', 'Correlation'] #argv[2]
name = sys.argv[1] + ' ' + plotType[typeNum]

if typeNum == 0:
    f = open(sys.argv[3], 'rt')
    data.append(parsigram(f, plotType[typeNum]))
    mu, sigma, bins, r = statigram(data[0][0], plotType[typeNum])
    histoplot(data[0][0], data[0][1], mu, sigma, bins)
elif typeNum == 1:
    if len(sys.argv) > 4:
        for i in range(3, len(sys.argv)):
            f = open(sys.argv[i], 'rt')
            data.append(parsigram(f, plotType[typeNum]))
    else:
        for i in range(2):
            f = open(sys.argv[3], 'rt')
            data.append(parsigram(f, plotType[typeNum]))

    mu, sigma, bins, r = statigram(data, plotType[typeNum])
    correlaplot(data, data[0][1], data[1][1], r)
