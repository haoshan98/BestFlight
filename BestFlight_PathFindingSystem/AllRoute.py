import pandas as pd
import csv
import math
import News as nw

def politicPercent():
    res = []
    df = pd.read_csv("PoliticalSentiment.csv")
    for index, row in df.iterrows():
        res.append(df.iloc[index, 1])
    return res

def quicksort(A, p, r):
    if p < r:
        pi = partition(A, p, r)
        quicksort(A, p, pi - 1)
        quicksort(A, pi + 1, r)


def partition(A, p, r):
    i = (p - 1)
    pivot = A[r][7]
    for j in range(p, r):
        if A[j][7] - pivot > 0:
            i = i + 1
            A[i], A[j] = A[j], A[i]
    A[i + 1], A[r] = A[r], A[i + 1]
    return (i + 1)

def getDistance(lat1, lng1, lat2, lng2):
    # formula to calculate distance using latitude and longitude
    distance = math.acos(math.cos(math.radians(90 - lat1)) * math.cos(
        math.radians(90 - lat2)) + math.sin(
        math.radians(90 - lat1)) * math.sin(
        math.radians(90 - lat2)) * math.cos(
        math.radians(lng1 - lng2))) * 6371
    return distance

# list out all possible route and put them in diff csv file
def allRouteValue():
    cities = nw.readCities()
    politicRes = politicPercent()
    df2 = pd.read_csv('cities_location.csv')
    for city in cities:  #each city file
        fname = city + '_sortedpath.csv'
        df = pd.read_csv(fname)
        totalRow = 0
        for index, row in df.iterrows():
            if index < 8:
                ctn = 0
                percent = 0
                if df.iloc[index, 5] is None:
                    for col in range[1:4]:
                        cityName = df.iloc[index, col]
                        percent += politicRes[cities.index(cityName)]
                        if cityName is not None:
                            ctn += 1
                else:
                    for col in range(1, 3):
                        cityName = df.iloc[index, col]
                        percent += politicRes[cities.index(cityName)]
                        if cityName is not None:
                            ctn += 1
            totalRow += 1
            politicValue = percent / ctn
            df.loc[int(index), 'political'] = politicValue

        points = []
        values = []

        cityLoc = cities.index(city)
        for index, row in df.iterrows():
            if index < 8:
                # for index in range(9):
                longestRoute = df.iloc[149, 5]  #distance
                klLoc_x = df2.loc[cityLoc, 'Latitude']
                klLoc_y = df2.loc[cityLoc, 'Longitude']
                cityLoc_x = df2.loc[cityLoc, 'Latitude']
                cityLoc_y = df2.loc[cityLoc, 'Longitude']

                directDistance = getDistance(klLoc_x, klLoc_y, cityLoc_x, cityLoc_y)

                thisCityDistance = df.loc[index, 'distance']

                distanceValue = (longestRoute - thisCityDistance) / (longestRoute - directDistance)
                politicValue = df.loc[index, 'political']

                point = round(distanceValue * 70 + (politicValue + 50)/100 * 30, 2)

                df.loc[int(index), 'points'] = point

                points.append(point)
        highestPoint = max(points)
        for index, row in df.iterrows():
            df.loc[int(index), 'probabilityDistribution'] = round(df.loc[int(index), 'points'] / highestPoint, 4)*0.1
        for index, row in df.iterrows():
            if index < 8:
                values.append(list(row))

        quicksort(values, 0, len(values)-1)
        header = ["origin", "first city", "second city", "third city", "fourth city", "distance", "political", "points", "probabilityDistribution"]
        fname = city + '_final.csv'
        with open(fname, "w", newline='') as writeFile:
            writeFile.truncate()
            writer = csv.writer(writeFile)
            writer.writerow(header)
            writer.writerows(values)
        writeFile.close()




