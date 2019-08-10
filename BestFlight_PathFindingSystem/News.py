import re
from newspaper import Article
from collections import Counter
import plotly.io as pio
import plotly.graph_objs as go
import pandas as pd
import StringMatching as strM


def readCities():
    df = pd.read_csv('cities.csv')
    cities = []

    for index, row in df.iterrows():
        if index is not 0:
            cities.append(row['City'])
    return cities

# 5 url to one article for each city
def urlToArticle():
    MoscowNews = ['https://www.themoscowtimes.com/2019/05/24/russia-warns-it-will-take-measures-in-response-to-new-near-border-spy-radar-in-arctic-norway-a65740',
                  'https://www.themoscowtimes.com/2019/05/22/us-sanctions-russian-arms-makers-over-alleged-iran-n-korea-and-syria-dealings-a65685',
                  'https://www.themoscowtimes.com/2019/05/23/another-censorship-scandal-rocks-the-media-and-russias-dirty-oil-crisis-a65719',
                  'https://www.theconversation.com/russia-responds-to-mueller-report-moscow-wins-putin-is-stronger-than-trump-and-us-is-a-pain-in-the-a-114244',
                  'https://www.bbc.com/news/world-europe-48398074']

    JakartaNews = ['https://www.thejakartapost.com/news/2019/05/22/post-election-unrest-grips-jakarta.html',
                   'https://www.thejakartapost.com/news/2019/05/22/jakarta-riot-protesters-throw-firecrackers-at-police-in-c-jakarta.html?src=mostviewed&pg=news/politics',
                   'https://www.thejakartapost.com/news/2019/05/22/police-detain-at-least-20-in-election-riot.html',
                   'https://www.thejakartapost.com/news/2019/05/22/its-provocateurs-prabowo-camp-rejects-blame-for-jakarta-riots.html',
                   'https://www.theguardian.com/world/2019/may/23/indonesia-pm-riot-deaths-jakarta-joko-widodo']

    CanberraNews = ['https://www.canberratimes.com.au/story/6182023/the-inside-story-of-how-the-liberals-beat-labor-at-its-own-game/?cs=14230',
                    'https://www.canberratimes.com.au/story/6181586/just-a-jump-to-the-left-and-then-a-step-to-the-right-the-challenges-facing-anthony-albanese/?cs=14230',
                    'https://www.canberratimes.com.au/story/6180684/andrew-leigh-blasts-greens-over-campaign-strategy/?cs=14230',
                    'https://www.canberratimes.com.au/story/6180456/bleeds-labor-why-albanese-has-left-nothing-on-the-table/?cs=14230',
                    'https://www.abc.net.au/news/2019-05-19/federal-election-canberra-candidates-safe-seat-labor-win/11124348']

    ShangHaiNews = ['https://www.straitstimes.com/asia/east-asia/potential-for-cooperation-between-singapore-and-shanghai-is-huge-dpm-heng',
                    'https://www.shine.cn/news/metro/1905255415/',
                    'https://www.shanghainews.net/news/261196413/trump-wields-more-powerful-weapon-than-tariffs-in-trade-war',
                    'https://www.scmp.com/news/china/politics/article/2172762/shanghais-jailed-top-prosecutor-implicates-100-other-officials',
                    'https://www.cnbc.com/2019/05/21/us-china-trade-war-will-get-worse-before-it-gets-better-says-expert.html']

    ParisNews = ['https://www.theguardian.com/books/2019/may/26/afropean-notes-from-black-europe-paris-johny-pitts-extract',
                 'https://www.independent.co.uk/news/people/najat-vallaud-belkacem-france-politics-burkini-a7214456.html',
                 'https://www.independent.co.uk/news/world/europe/marine-le-pen-win-france-presidential-election-pollsters-donald-trump-a7421061.html',
                 'https://www.theguardian.com/world/2018/nov/24/paris-fuel-tax-protest-macron-france-poverty',
                 'https://www.thelocal.fr/20190430/more-than-7000-police-to-be-on-duty-in-paris-for-may-1st-protests']

    TokyoNews = ['https://www.japantimes.co.jp/news/2019/05/25/national/politics-diplomacy/bill-banning-parents-physically-punishing-children-pass-diet/#.XOqMrYgzY2w',
                 'https://www.japantimes.co.jp/news/2019/05/23/national/politics-diplomacy/double-japanese-general-election-looks-realistic-unpopular-tax-hike-approaches/#.XOqNWIgzY2w',
                 'https://www.japantimes.co.jp/news/2019/05/24/national/politics-diplomacy/japan-turns-heat-fails-convince-south-korea-accept-arbitration-wartime-labor/#.XOqNVIgzY2w',
                 'https://japantoday.com/category/politics/Trump-arrives-in-Tokyo',
                 'https://japantoday.com/category/politics/focus-clock-is-ticking-if-abe-wants-to-force-double-election']

    SeoulNews = ['https://www.bloomberg.com/news/articles/2019-04-25/south-korea-s-surprisingly-bad-economy-deepens-moon-s-troubles',
                 'http://www.koreaherald.com/view.php?ud=20190524000128',
                 'http://english.chosun.com/site/data/html_dir/2019/05/23/2019052301317.html',
                 'http://english.hani.co.kr/arti/english_edition/e_international/894934.html',
                 'http://world.kbs.co.kr/service/news_view.htm?lang=e&Seq_Code=145387']

    news = [MoscowNews, JakartaNews, CanberraNews, ShangHaiNews, ParisNews, TokyoNews, SeoulNews]
    cities = readCities()

    articleList = []
    for i in range(7):
        fname = cities[i] + "News.txt"
        articleList.append(fname)
        f = open(fname, "w+")
        print('News of ', cities[i])
        for new in news[i]:

            print("news>> ", new)
            article = Article(new)
            article.download()
            # article.html
            article.parse()
            f.write(article.text.lower())

    return articleList

                     #rabin karb algo find string match
#############################################################################################
d = 2560                                                                                     #
                                                                                            #
def search(index,pat, txt, q):                                                              #
    M = len(pat)                                                                            #
    N = len(txt)                                                                            #
    i = 0                                                                                   #
    j = 0                                                                                   #
    p = 0                                                                                   #
    t = 0                                                                                   #
    h = 1                                                                                   #
                                                                                            #
                                                                                            #
    if(N<M):                                                                                #
        return -1                                                                           #
                                                                                            #
    for i in range(M - 1):                                                                  #
        h = (h * d) % q                                                                     #
                                                                                            #
    for i in range(M):                                                                      #
        p = (d * p + ord(pat[i])) % q                                                       #
        t = (d * t + ord(txt[i])) % q                                                       #
                                                                                            #
    for i in range(N - M + 1):                                                              #
                                                                                            #
        if p == t:                                                                          #
                                                                                            #
            for j in range(M):                                                              #
                if txt[i + j] != pat[j]:                                                    #
                    break                                                                   #
                                                                                            #
            j += 1                                                                          #
                                                                                            #
            if j == M:                                                                      #
                return index                                                                #
                                                                                            #
        if i < N - M:                                                                       #
            t = (d * (t - ord(txt[i]) * h) + ord(txt[i + M])) % q                           #
                                                                                            #
            if t < 0:                                                                       #
                t = t + q                                                                   #
                                                                                            #
    return -1                                                                               #
                                                                                            #
#############################################################################################


array = []
array2 =[]

arrays1=[]
arrayn1=[]
arrays2=[]
arrayn2=[]


def wordCount(fname):
            #article to array,and eliminate "," , "\n" , "'" , "." , "(" , ")",":"
    ###########################################################################################
    array = []
    arrayn1 = []
    arrayn2 = []
            #
    f = open(fname,"r")                                                                      #

    elminate = {"," , "\n" , "'" , "." , "(" , ")",":"}                                         #

    for line in f:                                                                              #
        fields = line.split(" ",)                                                               #
        for column in fields:                                                                   #
            array.append(column.translate({ord(i): None for i in elminate}))
            #
    array=str(array)

    array = re.sub("[^\w]", " ",  array).split()
                                                                                          #
    counts1 = Counter(array)

    string1 = str(counts1)                                                                                     #
    #############################################################################################

                            #delete stopwords using Rabin Karp
    #############################################################################################
    stopwords = ['a', 'about', 'above', 'across', 'after', 'afterwards']                        #
    stopwords += ['again', 'against', 'all', 'almost', 'alone', 'along']                        #
    stopwords += ['already', 'also', 'although', 'always', 'am', 'among']                       #
    stopwords += ['amongst', 'amoungst', 'amount', 'an', 'and', 'another']                      #
    stopwords += ['any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere']                  #
    stopwords += ['are', 'around', 'as', 'at', 'back', 'be', 'became']                          #
    stopwords += ['because', 'become', 'becomes', 'becoming', 'been']                           #
    stopwords += ['before', 'beforehand', 'behind', 'being', 'below']                           #
    stopwords += ['beside', 'besides', 'between', 'beyond', 'bill', 'both']                     #
    stopwords += ['bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant']                       #
    stopwords += ['co', 'computer', 'con', 'could', 'couldnt', 'cry', 'de']                     #
    stopwords += ['describe', 'detail', 'did', 'do', 'done', 'down', 'due']                     #
    stopwords += ['during', 'each', 'eg', 'eight', 'either', 'eleven', 'else']                  #
    stopwords += ['elsewhere', 'empty', 'enough', 'etc', 'even', 'ever']                        #
    stopwords += ['every', 'everyone', 'everything', 'everywhere', 'except']                    #
    stopwords += ['few', 'fifteen', 'fifty', 'fill', 'find', 'fire', 'first']                   #
    stopwords += ['five', 'for', 'former', 'formerly', 'forty', 'found']                        #
    stopwords += ['four', 'from', 'front', 'full', 'further', 'get', 'give']                    #
    stopwords += ['go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her']                    #
    stopwords += ['here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers']                  #
    stopwords += ['herself', 'him', 'himself', 'his', 'how', 'however']                         #
    stopwords += ['hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed']                            #
    stopwords += ['interest', 'into', 'is', 'it', 'its', 'itself', 'keep']                      #
    stopwords += ['last', 'latter', 'latterly', 'least', 'less', 'ltd', 'made']                 #
    stopwords += ['many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine']                    #
    stopwords += ['more', 'moreover', 'most', 'mostly', 'move', 'much']                         #
    stopwords += ['must', 'my', 'myself', 'name', 'namely', 'neither', 'never']                 #
    stopwords += ['nevertheless', 'next', 'nine', 'no', 'nobody', 'none']                       #
    stopwords += ['noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of']                     #
    stopwords += ['off', 'often', 'on','once', 'one', 'only', 'onto', 'or']                     #
    stopwords += ['other', 'others', 'otherwise', 'our', 'ours', 'ourselves']                   #
    stopwords += ['out', 'over', 'own', 'part', 'per', 'perhaps', 'please']                     #
    stopwords += ['put', 'rather', 're', 's', 'same', 'see', 'seem', 'seemed']                  #
    stopwords += ['seeming', 'seems', 'serious', 'several', 'she', 'should']                    #
    stopwords += ['show', 'side', 'since', 'sincere', 'six', 'sixty', 'so']                     #
    stopwords += ['some', 'somehow', 'someone', 'something', 'sometime']                        #
    stopwords += ['sometimes', 'somewhere', 'still', 'such', 'system', 'take']                  #
    stopwords += ['ten', 'than', 'that', 'the', 'their', 'them', 'themselves']                  #
    stopwords += ['then', 'thence', 'there', 'thereafter', 'thereby']                           #
    stopwords += ['therefore', 'therein', 'thereupon', 'these', 'they']                         #
    stopwords += ['thick', 'thin', 'third', 'this', 'those', 'though', 'three']                 #
    stopwords += ['three', 'through', 'throughout', 'thru', 'thus', 'to']                       #
    stopwords += ['together', 'too', 'top', 'toward', 'towards', 'twelve']                      #
    stopwords += ['twenty', 'two', 'un', 'under', 'until', 'up', 'upon']                        #
    stopwords += ['us', 'very', 'via', 'was', 'we', 'well', 'were', 'what']                     #
    stopwords += ['whatever', 'when', 'whence', 'whenever', 'where']                            #
    stopwords += ['whereafter', 'whereas', 'whereby', 'wherein', 'whereupon']                   #
    stopwords += ['wherever', 'whether', 'which', 'while', 'whither', 'who']                    #
    stopwords += ['whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with']                   #
    stopwords += ['within', 'without', 'would', 'yet', 'you', 'your']                           #
    stopwords += ['yours', 'yourself', 'yourselves']                                            #
    ########sc#####################################################################################

    ############sc version fix bug###############################################################################                                                                            #
    for index, item in enumerate(array):                                                        #
        for j in stopwords:                                                                     #
            if(search(index,item, j, 101))!=-1:                                                 #

                array[index] = " "                                                      #
                break
    #############################################################################################

    #################get array in form of string and number for graph (before stopwors)#########
    counts2 = Counter(array)
    string2=str(counts2)


    x = string1.replace("Counter({'", " ")
    x = x.replace("': "," ")
    x = x.replace(", '"," ")
    x = x.replace(' })"'," ")
    x = x.split()
    list1 = x

    arrays1 = [x for x in list1
                         if  (x.isalpha()  )]

    isnumber='false'
    isfirstindex='true'
    for x in list1:
            if (x.isdigit() and isnumber!='true' and isfirstindex!='true' ):
               arrayn1.append(x)
               isnumber='true'
               isfirstindex = 'false'
            else:
             isnumber="false"
             isfirstindex = 'false'


    x = string2.replace("Counter({'", " ")
    x=x.replace("': "," ")
    x=x.replace(", '"," ")
    x=x.replace(' })"'," ")
    x=x.split()
    list2=x

    arrays2 = [x for x in list2
                         if  (x.isalpha() and x!="Counter" )]

    isnumber='false'
    isfirstindex='true'
    for x in list2:
            if (x.isdigit() and isnumber!='true' and isfirstindex!='true' ):
               arrayn2.append(x)
               isnumber='true'
               isfirstindex='false'
            else:
             isnumber="false"
             isfirstindex='false'


    ##############################reduce array to 20 element#############################################
    numofword=40      ###############number of word to show
    for i in range(len(arrays1)-numofword ):
               arrays1.pop()

    for i in range(len(arrayn1)-numofword ):
               arrayn1.pop()

    for i in range(len(arrays2)-numofword ):
               arrays2.pop()

    for i in range(len(arrayn2)-numofword):
               arrayn2.pop()

    counttt=0
    for x in arrays1:
        for y in arrays2:
            if(x == y):
               counttt=counttt+1


    for i in range(len(arrays2)-counttt):
               arrays2.pop()

    for i in range(len(arrayn2)-counttt):
               arrayn2.pop()

    ##############create line graph with plotty#######################################################

    data = [
      go.Histogram(
        histfunc = "sum",
        x=arrays1,
        y=arrayn1,
        name = "Before [All words]"
      ),
      go.Histogram(
        histfunc = "sum",
          x=arrays2,
          y=arrayn2,
         name = "After [No stopwords]"
      )
    ]

    # Edit the layout
    layout = dict(title = 'Words count',
                  xaxis = dict(title = 'Words'),
                  yaxis = dict(title = 'Number of words'),
                  )

    fig = dict(data=data, layout=layout)
    # plotly.offline.plot(fig)

    # plot(fig)
    imgName = fname[:-4] + '_wordCtn.jpeg'
    pio.write_image(fig, imgName, width=1000, height=500, scale=0)


def newsMain():
    cities = readCities()
    strM.strMatchMain(cities)




















