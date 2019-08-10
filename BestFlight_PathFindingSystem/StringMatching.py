from collections import Counter
import plotly.io as pio
import plotly.graph_objs as go
import csv

#=====  PrepareWords  ==================================================
# to change all the words to lower case and eliminate punctuation
def preparePNWords():
    with open('PositiveWords.txt', 'r') as f:
        lines = f.readlines()
    # eliminate punctuation
    lines = [line.replace("-", ' ') for line in lines]
    lines = [line.replace(' ', '') for line in lines]
    lines = [line.replace(",", ' ') for line in lines]
    lines = [line.replace("–", ' ') for line in lines]
    lines = [line.replace("’", '') for line in lines]
    lines = [line.lower() for line in lines]

    # finally, write lines in the file
    with open('positivePattern.txt', 'w') as f:
        f.writelines(lines)

    with open('NegativeWords.txt', 'r') as f:
        lines = f.readlines()
    # eliminate punctuation
    lines = [line.replace("-", ' ') for line in lines]
    lines = [line.replace(' ', '') for line in lines]
    lines = [line.replace(",", ' ') for line in lines]

    # finally, write lines in the file
    with open('negativePattern.txt', 'w') as f:
        f.writelines(lines)


preparePNWords()
#===================================================================================

positiveString = []
negativeString = []


def brute_force_match(word, text, type):
    m = len(word)
    n = len(text)
    counter = 0

    for i in range(0, n-m+1):
        found = True
        for j in range(0, m):
            if word[j] != text[i+j]:
                found = False
                break
        if found:
            counter += 1

    if counter != 0:
        if type == "positive":
            positiveString.append(word)
        if type == "negative":
            negativeString.append(word)


def preparedataArray(string):
    new = str(string)
    x = new.replace("Counter({'", " ")
    x = x.replace("': ", " ")
    x = x.replace(", '", " ")
    x = x.replace(' })"', " ")
    x = x.split()
    list = x

    array = [x for x in list if (x.isalpha())]
    return array


def preparedataArraynum(string):
    new = str(string)
    x = new.replace("Counter({'", " ")
    x = x.replace("': ", " ")
    x = x.replace(", '", " ")
    x = x.replace(' })"', " ")
    x = x.split()
    list = x
    arraynum = []

    for x in list:
        if x.isdigit() and isnumber != 'true' and isfirstindex != 'true':
            arraynum.append(x)
            isnumber = 'true'
            isfirstindex = 'false'
        else:
            isnumber = "false"
            isfirstindex = 'false'
    return arraynum


def percentageWords(arr, totalwords):
    total = 0
    for i in range(len(arr)):
        arr[i] = int(arr[i])
        total += arr[i]
    percentage = total/totalwords * 100
    output = round(percentage, 2)
    return output


# compare with positive words
def positivePercent(fname):
    with open('positivepattern.txt', 'r') as f:
        lines1 = f.read().split(" ")

    # the article/news
    with open(fname, 'r') as f:
        lines = f.readlines()
    lines = [line.replace(",", '') for line in lines]
    lines = [line.replace('.', '') for line in lines]
    lines = [line.lower() for line in lines]
    with open('newtext.txt', 'w') as f:
        f.writelines(lines)
    with open('newtext.txt', 'r') as f:
        lines2 = f.read().split(" ")

    # run string matching
    for y in range(len(lines1)):
        for z in range(len(lines2)):
            brute_force_match(lines1[y], lines2[z], "positive")
    # count the frequency of matching words
    counts1 = Counter(positiveString)

    # print("Positive Words")
    percent = float(percentageWords(preparedataArraynum(counts1), len(lines2))) % 100 % 50
    print("The percentage of Positive Words :", round(percent, 2), '%')
    return percent

# compare with negative words
def negativePercent(fname):
    with open('negativepattern.txt', 'r') as f:
        lines1 = f.read().split(" ")

    # the article/news
    with open(fname, 'r') as f:
        lines = f.readlines()
    lines = [line.replace(",", '') for line in lines]
    lines = [line.replace('.', '') for line in lines]
    lines = [line.lower() for line in lines]
    with open('newtext.txt', 'w') as f:
        f.writelines(lines)
    with open('newtext.txt', 'r') as f:
        lines2 = f.read().split(" ")

    # run string matching
    for y in range(len(lines1)):
        for z in range(len(lines2)):
            brute_force_match(lines1[y], lines2[z], "negative")
    # count the frequency of matching words
    counts2 = Counter(negativeString)

    # print("Negative Words")
    percent = float(percentageWords(preparedataArraynum(counts2), len(lines2))) % 100 % 50
    print("The percentage of Negative Words :", round(percent, 2), "%")
    return percent



# TO CONCLUDE
def conclude(positive, negative, neutral):
    # avg = (positive + negative + neutral) / 100
    con = (positive - negative)
    if (positive > negative) and (positive > neutral):
        print( "The article is giving positive sentiment.")
    elif (negative > positive) and (negative > neutral):
        print( "The article is giving negative sentiment.")
    # else:
    #     print( "The article is neutral.")
    return con


def showGraph(a, b, fname):
    counts1 = Counter(positiveString)
    counts2 = Counter(negativeString)

    data = [
        go.Histogram(
            histfunc="sum",
            x=preparedataArray(counts1),
            y=preparedataArraynum(counts1),
            name="Positive"
        ),
        go.Histogram(
            histfunc="sum",
            x=preparedataArray(counts2),
            y=preparedataArraynum(counts2),
            name="Negative"
        )
    ]

    # Edit the layout
    layout = dict(title='Frequency of Words',
                  xaxis=dict(title='Words'),
                  yaxis=dict(title='Number of Words'),
                  )

    fig = dict(data=data, layout=layout)
    # plotly.offline.plot(fig, filename="graph1.html")
    imgName = fname[:-4] + '+ve-ve.jpeg'
    pio.write_image(fig, imgName, width=1000, height=500, scale=0)

    x = ["Article Country"]
    y1 = [a]
    y2 = [b]
    y3 = [100 - (a + b)]
    data = [
        go.Histogram(
            histfunc="sum",
            x=x,
            y=y1,
            name="Positive"
        ),
        go.Histogram(
            histfunc="sum",
            x=x,
            y=y2,
            name="Negative"
        ),
        go.Histogram(
            histfunc="sum",
            x=x,
            y=y3,
            name="Neutral"
        ),
    ]

    # Edit the layout
    layout = dict(title='Percentage of Words',
                  xaxis=dict(title='Type'),
                  yaxis=dict(title='Percentage'),
                  )

    fig = dict(data=data, layout=layout)
    # plotly.offline.plot(fig, filename="graph2.html")
    imgName = fname[:-4] + 'percent.jpeg'
    pio.write_image(fig, imgName, width=1000, height=500, scale=0)


# def pointCal()

def strMatchMain(cities):
    resList = [["City", "Political"]]
    for city in cities:
        fname = city + "News.txt"
        print(">> ", fname)
        a = positivePercent(fname)
        b = negativePercent(fname)
        c = float(100-(a+b))
        showGraph(a, b, fname)
        # print("Conclusion:")
        res = conclude(a, b, c)
        resList.append([city, res])
    with open("PoliticalSentiment.csv", "w", newline='') as writeFile:
        writeFile.truncate()
        writer = csv.writer(writeFile)
        # writer.writerows(["City", "Political"])
        writer.writerows(resList)
    writeFile.close()




