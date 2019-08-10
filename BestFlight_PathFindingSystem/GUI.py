import csv
import math
import pandas as pd
import googlemaps
from geopy.geocoders import Nominatim
import urllib.request
from tkinter.ttk import Frame, Style
import tkinter.ttk as ttk

import News as nw
import AllRoute
from tkinter import *
from PIL import ImageTk, Image

global brand_preview

# read cities from csv file into data frame names 'df'
df = pd.read_csv('cities.csv')
print(df)


# get city location, write to new file
# Uses the Geocoding API and the Directions API with an API key:
gmaps = googlemaps.Client(key='AIzaSyDzn3O2uaTWx0Nt5w2izAoVH-3BxKDQGNA')
# To geolocate a query to an address and coordinates:
geolocator = Nominatim(user_agent="specify_your_app_name_here")

# empty list - will be used to store calculated latitude & longitude
lati = []
longi = []
city = []
to = []
distance_list = []
path_list = []
path = []
sort_list = []
destination = []

# Loop through each row in the data frame
for index, row in df.iterrows():
    pin = row['City']
    # print("==>", pin)
    location = geolocator.geocode(pin)
    lati.append(location.latitude)
    longi.append(location.longitude)
    # print(location.address)
    # print((location.latitude, location.longitude))

# Add column 'Distance' to data frame and assign to list values
df['Latitude'] = lati
df['Longitude'] = longi

df.to_csv('cities_location.csv', index=None, header=['City', 'Latitude', 'Longitude'])

nw.newsMain()

def distance_to_all():
    # calculate all the distance between 2 city and save in distance_list
    distance_list.clear()
    df = pd.read_csv("cities_location.csv")
    for i in range(len(df.index)):
        city = []
        for j in range(len(df.index)):
            to = []
            to.append(df.iat[i, 0])
            to.append(df.iat[j, 0])
            to.append(getDistance(df.iat[i, 1], df.iat[i, 2], df.iat[j, 1], df.iat[j, 2]))
            city.append(to)
        distance_list.append(city)


def getShortestPath(option):
    # calculate the shortest path from Kuala Lumpur to option city
    path_list.clear()
    for i in range(len(distance_list)):
        for j in range(len(distance_list)):
            path = []
            for k in range(len(distance_list)):
                length = 0
                city = []
                if j is 0 or k is 0 or i is 0 or i is k or i is j or j is k or i is option or j is option:
                    continue
                elif k is option:
                    length += distance_list[0][i][2] + distance_list[i][j][2] + distance_list[j][k][2]
                    city.append(distance_list[0][i][0])
                    city.append(distance_list[i][j][0])
                    city.append(distance_list[j][k][0])
                    city.append(distance_list[j][k][1])
                    city.append(' ')
                    city.append(length)
                    path.append(city)
                elif k is not option:
                    length += distance_list[0][i][2] + distance_list[i][j][2] + distance_list[j][k][2] + \
                                distance_list[k][option][2]
                    city.append(distance_list[0][i][0])
                    city.append(distance_list[i][j][0])
                    city.append(distance_list[j][k][0])
                    city.append(distance_list[k][option][0])
                    city.append(distance_list[k][option][1])
                    city.append(length)
                    path.append(city)
            if path is not None:
                path_list.append(path)


# show map of each cities
def get_static_google_map(filename_wo_extension, center=None, zoom=1, origin='0,0', option=0, imgsize="500x500",
                          imgformat="jpeg",
                          maptype="roadmap", markers=None, key="AIzaSyDzn3O2uaTWx0Nt5w2izAoVH-3BxKDQGNA"):
    """retrieve a map (image) from the static google maps server

     See: https://maps.googleapis.com/maps/api/staticmap?

        Creates a request string with a URL like this:

        https://maps.googleapis.com/maps/api/staticmap?center=Brooklyn+Bridge,New+York,NY&zoom=13&size=600x300&maptype=roadmap
        &markers=color:blue%7Clabel:S%7C40.702147,-74.015794
        &markers=color:green%7Clabel:G%7C40.711614,-74.012318
        &markers=color:red%7Clabel:C%7C40.718217,-73.998284
        &key=AIzaSyDzn3O2uaTWx0Nt5w2izAoVH-3BxKDQGNA'

        """

    # assemble the URL
    request = "https://maps.googleapis.com/maps/api/staticmap?"  # base URL, append query params, separated by &

    # if center and zoom  are not given, the map will show all marker locations
    if center != None:
        request += "center=%s&" % "Brooklyn+Bridge,New+York,NY"  # or a search term
    request += "zoom=%i&" % zoom  # zoom 0 (all of the world scale ) to 22 (single buildings scale)
    request += "path=color:blue|weight:5"

    if option is len(df.index):
        request += addAllPath(origin)
    else:
        request += addShortestPath(option)
    # else:
    #     request += addOnePath(origin, option)

    request += "&size=%ix%i&" % (imgsize)  # tuple of ints, up to 640 by 640
    request += "maptype=%s&" % maptype  # roadmap, satellite, hybrid, terrain

    # add markers (location and style)
    if markers != None:
        for marker in markers:
            request += "%s&" % marker

    request += "key=%s&" % key
    # print ("==", request)

    print(">>", request)

    urllib.request.urlretrieve(request,
                               filename_wo_extension + "." + imgformat)  # Option 1: save image directly to disk


def getDistance(lat1, lng1, lat2, lng2):
    # formula to calculate distance using latitude and longitude
    distance = math.acos(math.cos(math.radians(90 - lat1)) * math.cos(
        math.radians(90 - lat2)) + math.sin(
        math.radians(90 - lat1)) * math.sin(
        math.radians(90 - lat2)) * math.cos(
        math.radians(lng1 - lng2))) * 6371
    return distance


def addPath(origin, destination):
    request = "|%s|%s" % (origin, destination)
    return request


def addOnePath(origin, destiCode):
    request = ''
    df = pd.read_csv('cities_location.csv')
    request += addPath(origin, str(df.loc[destiCode, "Latitude"]) + "," + str(df.loc[destiCode, "Longitude"]))
    return request


def addAllPath(origin):
    request = ''
    df = pd.read_csv('cities_location.csv')
    for index, row in df.iterrows():
        location = (str(row['Latitude']) + "," + str(row['Longitude']))
        request += "|%s" % (location)
    return request


def addShortestPath(option):
    #read the latitude and longitude from cities_location.csv and construct the shortest path route
    request = ''
    coordinate = pd.read_csv('cities_location.csv')
    location = coordinate.iat[option, 0]
    shortPath = pd.read_csv(location+'_final.csv')
    for i in range(5):
        for index, row in coordinate.iterrows():
            if str(shortPath.iat[0, i]) == str(row['City']):
                location = (str(row['Latitude']) + "," + str(row['Longitude']))
                request += "|%s" % (location)
                break
    return request


def markerList(option):
    df = pd.read_csv('cities_location.csv')
    marker_list_flight = []
    marker_list_flight.append("markers=size:mid|label:A|color:red|%s|" % (
            str(df.loc[0, "Latitude"]) + "," + str(df.loc[0, "Longitude"])))  # KL

    for index, row in df.iterrows():
        if index > 0:
            if index is not option:
                marker_list_flight.append(
                    "markers=size:mid|label:B|color:yellow|%s|" % (str(row['Latitude']) + "," + str(row['Longitude'])))
            elif index is destination:
                marker_list_flight.append("markers=size:mid|label:B|color:green|%s|" % destination)
            else:
                marker_list_flight.append("markers=size:mid|label:B|color:green|%s|" % (
                        str(df.loc[option, "Latitude"]) + "," + str(df.loc[option, "Longitude"])))
    return marker_list_flight


def markerListAll():
    df = pd.read_csv('cities_location.csv')
    marker_list_flight = []
    marker_list_flight.append("markers=size:mid|label:A|color:red|%s|" % (
            str(df.loc[0, "Latitude"]) + "," + str(df.loc[0, "Longitude"])))  # KL
    for index, row in df.iterrows():
        if index > 0:
            marker_list_flight.append(
                "markers=size:mid|label:B|color:yellow|%s|" % (str(row['Latitude']) + "," + str(row['Longitude'])))
    return marker_list_flight


def quicksort(A, p, r):
    if p < r:
        pi = partition(A, p, r)
        quicksort(A, p, pi - 1)
        quicksort(A, pi + 1, r)


def partition(A, p, r):
    i = (p - 1)
    pivot = A[r][5]
    for j in range(p, r):
        if A[j][5] <= pivot:
            i = i + 1
            A[i], A[j] = A[j], A[i]
    A[i + 1], A[r] = A[r], A[i + 1]
    return (i + 1)


def main(option):
    df = pd.read_csv('cities_location.csv')
    origin = (str(df.loc[0, "Latitude"]) + "," + str(df.loc[0, "Longitude"]))
    destination = (str(df.loc[option, "Latitude"]) + "," + str(df.loc[option, "Longitude"]))
    print(option)
    if option is 0:
        # point out all location
        marker_list_flight = markerList(option)
        get_static_google_map("google_map_" + str(option), zoom=2, origin=origin,
                              option=option, imgsize=(640, 640), imgformat="png",
                              markers=marker_list_flight)
    elif option is len(df.index):
        # make map that shows all the markers
        marker_list_flight = markerListAll()
        get_static_google_map("google_map_" + str(option), zoom=2, origin=origin,
                              option=option, imgsize=(640, 640), imgformat="png",
                              markers=marker_list_flight)
    else:
        # marker_list_flight = markerList(option)
        # get_static_google_map("google_map_" + str(option), zoom=2, origin=origin,
        #                       option=option, imgsize=(640, 640), imgformat="png",
        #                       markers=marker_list_flight)
        getShortestPath(option)
        cities = nw.readCities()

        fname = cities[option-1]+ 'path.csv'
        with open(fname, "w", newline='') as writeFile:
            writeFile.truncate()
            writer = csv.writer(writeFile)
            for i in range(len(path_list)):
                for j in range(len(path_list[i])):
                    writer.writerow(path_list[i][j])
        writeFile.close()
        # print("path list >>\n", path_list)
        sort_list = []
        for i in range(len(path_list)):
            for j in range(len(path_list[i])):
                sort_list.append(path_list[i][j])
        quicksort(sort_list, 0, len(sort_list)-1)
        #sort_list is contain the shortest path to destination
        fname = cities[option-1] + '_sortedpath.csv'
        with open(fname, "w", newline='') as writeFile:
            writeFile.truncate()
            writer = csv.writer(writeFile)
            writer.writerow(["origin", "first city", "second city", "third city", "fourth city", "distance", "political", "points", "probabilityDistribution"])
            writer.writerows(sort_list)
        writeFile.close()



        marker_list_flight = markerList(option)
        get_static_google_map("google_map_" + str(9), zoom=2, origin=origin,
                              option=option, imgsize=(640, 640), imgformat="png",
                              markers=marker_list_flight)
        return Image.open("google_map_9.png")
    return Image.open("google_map_" + str(option) + ".png")


if __name__ == '__main__':
    distance_to_all()
    for i in range(8):
        main(i)
    AllRoute.allRouteValue()



# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)
class Window(Frame):

    # Define settings upon initialization. Here you can specify
    def __init__(self, master, im):

        # parameters that you want to send through the Frame class.
        Frame.__init__(self, master)

        # reference to the master widget, which is the tk window
        self.master = master

        # with that, we want to then run init_window, which doesn't yet exist
        self.init_window(im)

    # Creation of init_window
    def init_window(self, im):
        # changing the title of our master widget
        self.master.title("Best Flight Management System")
        self.style = Style()
        self.style.theme_use("default")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=True)

        self.showBtn()

        # creating a menu instance=====================================
        menu = Menu(self.master)
        self.master.config(menu=menu)
        # create the file object)
        file = Menu(menu)
        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        file.add_command(label="Exit", command=self.client_exit)
        # added "file" to our menu
        menu.add_cascade(label="File", menu=file)
        # create the file object)
        edit = Menu(menu)
        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        # edit.add_command(label="Show Text", command=self.showText)
        # added "file" to our menu
        menu.add_cascade(label="Edit", menu=edit)

    def showImg(self, im):

        info = ''

        self.image = ImageTk.PhotoImage(im)
        info += "All Routes Available"

        image_label = Label(self, image=self.image, bd=0)  # <--- will not work if 'image = ImageTk.PhotoImage(im)'
        image_label.grid(row=1, column=0, columnspan=2, rowspan=len(df.index) + 2,
                         padx=1, sticky=E + W + N)
        self.showText(info)

    def updateImg(self, im, i):
        img = main(i)
        print("updating Map")

        info = ''
        df = pd.read_csv('cities.csv')

        if i is len(df.index) or i is 9:
            self.image = ImageTk.PhotoImage(main(0))
            info += "Starting city >> " + df.loc[0, "City"]
        else:
            self.image = ImageTk.PhotoImage(img)
            if i is not 0:
                info += "Route from " + df.loc[0, "City"] + " to " + df.loc[i, "City"]
            else:
                info += "Starting city >> " + df.loc[0, "City"]
        image_label = Label(self, image=self.image, bd=0)  # <--- will not work if 'image = ImageTk.PhotoImage(im)'
        image_label.grid(row=1, column=0, columnspan=2, rowspan=len(df.index) + 2,
                         padx=1, sticky=E + W + N)

        self.showText(info)
        self.showAnalysis(i)


    def showAnalysis(self, i):
        df = pd.read_csv('cities.csv')
        cities = []

        for index, row in df.iterrows():
            if index is not 0:
                cities.append(row['City'])
        destination = cities[i-1]
        traversedCity = []
        fname = destination + "_final.csv"
        df2 = pd.read_csv(fname)
        if df2.iloc[0, 5] is None:
            for col in range[1:4]:
                cityName = df2.iloc[0, col]
                traversedCity.append(cityName)
        else:
            for col in range(1, 3):
                cityName = df2.iloc[0, col]
                traversedCity.append(cityName)
            traversedCity.append(None)

    def showText(self, info='Flight System'):
        ttk.Style().configure("TLabel", foreground='black', background='pink', padding=(2, 6, 2, 6),
                              font='serif 10', borderwidth=5)
        entry = ttk.Label(self, text=info, style="TLabel")
        entry.configure(anchor="center")
        entry.grid(row=0, column=0, columnspan=4, rowspan=1, pady=3, sticky=E + W + S + N)

    def showBtn(self):
        # creating buttons fot cities
        Style().configure("TButton", padding=(2, 8, 2, 8),
                          font='serif 10')
        # create column
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=3)

        df = pd.read_csv('cities.csv')

        # create row
        for i in range(len(df.index) + 3):
            self.rowconfigure(i, pad=3)

        self.showImg(im)
        print("---")
        ttk.Style().configure("TButton", foreground='black', background='yellow')
        fileToShow = ''
        for index, row in df.iterrows():
            if index is 0:
                abtn = ttk.Button(self, text=row['City'], style="TButton")#, command=lambda i=index: self.updateImg(im, i))
            else:
                abtn = ttk.Button(self, text=row['City'], style="TButton", command=lambda i=index: self.updateImg(im, i))

            fileToShow = 'newsSingapore.txt'
            abtn.grid(row=index + 1, column=3, sticky=W + E)

        btn = ttk.Button(self, text="Analysis", style="TButton")#, command=lambda: self.showAnalysis(fileToShow))
        btn.grid(row=len(df.index) + 1, column=3, sticky=W + E)

    def client_exit(self):
        exit()


im = Image.open("google_map_" + str(len(df.index)) + ".png")  # read map from disk


mainw = Tk()
mainw.frame = Window(mainw, im)
mainw.geometry("760x640")
mainw.mainloop()

