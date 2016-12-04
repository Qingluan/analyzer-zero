#!/usr/loacal/bin/python


from math import sqrt
from PIL import Image
from PIL import ImageDraw
import random


def readfile(name):
    """
    @parmeters : filename
    @return : blognames , words ,data
    
    """
    lines = [line for line in file(name)]

    #First is column titles
    colnames = lines[0].strip().split("\t")[1:]

    row_name = []
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')

        #add row name 
        row_name.append(p[0])

        #The data for this row is the remainder of the row
        data.append([float(x) for x in p[1:]])

    return row_name,colnames,data



def pearson(v1,v2):
    sum1 = sum(v1)
    sum2 = sum(v2)

    # define a meth method :  to sum( [x**2 for x in v1 or v2])
    SqrSum = lambda v : sum([x**2 for x in  v])
    Sqsum1 = SqrSum(v1)
    Sqsum2 = SqrSum(v2)

    # ele's count 
    count = len(v1)

    pSum = sum([ v1[i]*v2[i] for i in range(len(v1)) ])

    num = pSum - sum1 * sum2 /count
    den = sqrt((Sqsum1 - sum1**2/ count ) *( Sqsum2 - sum2**2 / count )) 

    if den== 0: return 0

    return 1.0 - num/den


#to define a bicluster has some property
class bicluster(object):
    def __init__(self,vec,left=None,right=None,distance=0.0,id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance



def hcluster(rows,distance=pearson):
    distances = {}
    currentClusterId = -1

    #Cluster are init just rows

    cluster = [bicluster(rows[i],id=i) for i in range(len(rows)) ]


    while len(cluster) >1:
        lowestPair = (0,1)
        closest = distance(cluster[0].vec,cluster[1].vec)


        for i in range(len(cluster)):
            for j in range(i+1,len(cluster)):

                
                if not (cluster[i].id,cluster[j].id)  in distances:
                    distances[(cluster[i].id,cluster[j].id)] = distance(cluster[i].vec, cluster[j].vec)
                d = distances[(cluster[i].id,cluster[j].id)]

                if d < closest:
                    print "new lower : {} < {}".format(d,closest)
                    closest = d
                    lowestPair = (i,j)

        #calculate average of the two clusters

        mergevec = [
            (cluster[lowestPair[0]].vec[i] + cluster[lowestPair[1]].vec[i])/2.0
            for i in range(len(cluster[0].vec))
        ]


        # create id s that weren't in the original set are negative
        newcluster = bicluster(
            mergevec,
            left=cluster[lowestPair[0]],
            right=cluster[lowestPair[1]],
            distance=closest,
            id=currentClusterId
        )

        currentClusterId -= 1
        del cluster[lowestPair[1]]
        del cluster[lowestPair[0]]
        cluster.append(newcluster)

    return cluster[0]



def printclust(clust,labels=None,n=0):
    # indent tp make a hierachy layout

    for i in range(n): print " ",

    if clust.id < 0:
        print "-"
    else :
        if labels == None : print clust.id
        else: print labels[clust.id]

    if clust.left != None : printclust(clust.left,labels=labels,n = n+1 )
    if clust.left != None : printclust(clust.right,labels=labels,n = n+1 )


def getheight(cluster):
    """
        cluster is a object for clust , it is a bin-tree
        this will recursivily get how node this cluster is 
    """
    if cluster.left == None and cluster.right == None: return 1

    return getheight(cluster.left) + getheight(cluster.right)
    

def getdepth(clusters):
    
    if clusters.left == None and clusters.right == None : return 0

    return max(getdepth(clusters.left), getdepth(clusters.right) + clusters.distance )


def drawdendrogram(cluster,labels,fill=(255,0,0),jpg="cluster.jpg") :
    """this is will draw a cluster's jpg by some fixed width  """

    h = getheight(cluster) * 20
    w = 1200 
    depth = getdepth(cluster)

    # this is a scalling coefficient
    scalling = float( w -350 ) / depth

    img = Image.new("RGB",(w,h),(255,255,255))
    draw = ImageDraw.Draw(img)

    draw.line((0,h/2,10,h/2),fill=(255,0,0))

    print h
    print scalling
    drawnode(draw,cluster,10,h/2,scalling,labels)

    img.save(jpg)
    return img

def drawnode(draw,cluster,x,y,scalling,labels) :
    if cluster.id <0 :
        h1 = getheight(cluster.left) * 20
        h2 = getheight(cluster.right) * 20

        top = y - (h1 + h2)/2 
        bottom  = y + (h1 + h2 )/2

        ll = cluster.distance * scalling

        draw.line((x,top + h1/2,x,bottom-h2/2),fill=(255,0,0))

        draw.line((x,top + h1/2,x+ll,top+h1/2),fill=(255,0,0))        

        draw.line((x,bottom - h2/2,x+ll, bottom - h2/2 ),fill=(255,0,0))        

        # draw left and right node recurisivly
        drawnode(draw, cluster.left, x+ll, top + h1/2, scalling, labels)
        drawnode(draw, cluster.right, x+ll, bottom - h2/2, scalling, labels)

    else:
        draw.text((x+5, y-7),labels[cluster.id],fill=(0,0,0))


def rotamatrx(data) :
    newdata = []
    for i in range(len(data[0])) :
        newrow = [ data[j][i] for j in range(len(data)) ]
        newdata.append(newrow)

    return newdata


def kcluster(rows,distance=pearson,k=4):

    # determin the minimum and maximum values for each point
    ranges = [ ( min([row[i] for row in rows]) , max([row[i] for row in rows ]) ) for i in range(len(rows[0])) ]

    #create k randomly placed centroids
    # for each column create a k ,witch is range in min to max in values of columns
    clusters = [[random.random() * (ranges[i][1] - ranges[i][0]) + ranges[i][0] for i in range(len(rows[0]))] for j in range(k)]

    lastmatches = None
    for t in range(100) : 
        print 'Iteration %d '%t
        bestmatches = [[] for i in range(k)]

        #Find witch centroid is  closest for each row
        for j in range(len(rows)) :
            row = rows[j]
            bestmatch = 0
            for i in range(k): 
                d = distance(clusters[i], row)
                if d < distance(clusters[bestmatch], row) : bestmatch = i
            bestmatches[bestmatch].append(i)

        #if the result are the same as last time ,this is complete
        if bestmatches == lastmatches : break 
        lastmatches = bestmatches

def scaledown(data,distances=pearson , rate=0.01):
    n = len(data)

    display_compare = []
    #real distance between  every pair of items
    realdist = [[distances(data[i] , data[j]) for j in range(n)] for i in range(n)]

    outersum = 0.0

    #Randomly  initialize the starting points of the loacations in 2D
    loc = [[random.random(),random.random()] for i in range(n)]
    fakedist = [[0.0 for  j in range(n)] for i in range(n)]
    loc_column = 2

    lasteerror =  None
    for m in range(0,1000):
        #Find projected distances
        for i in range(n):
            for j in range(n):
                fakedist[i][j] = sqrt (sum([pow (loc[i][x] -loc[j][x],2 )
                                        for x in range(loc_column)]))
        #MMoved points
        grad = [[0.0, 0.0 ] for i in range(n) ]

        totalerror = 0
        for k in range(n):
            if  j ==k :
                continue 

            # Thee error is percent difference  between the distances 
            if realdist[j][k] == 0:
                continue
            errorterm = (fakedist[j][k] -realdist[j][k] )/realdist[j][k]
            print "real:{} || fake:{} [{}] loc:{} | error : {}".format(realdist[j][k],fakedist[j][k],m,loc[k],errorterm)

            #Each point nedds to be moved away from or toards the other 
            # point in propety to how much error  it has 
            grad[k][0] += ((loc [k][0] - loc [j][0] )/ fakedist[j][k])* errorterm
            grad[k][1] += ((loc [k][1] - loc[j][1] ) / fakedist[j][k] ) * errorterm

            #Keep track of the total error 
            totalerror = abs(errorterm)
        print totalerror
        
        #if the answer got worse by moving the points , we are done 
        if lasteerror and lasteerror <  totalerror : break
        lasteerror = totalerror

        #move each of  the points by the learning  rate times the gradient 
        for k in range(n):
            loc[k][0] -= rate  * grad[k][0]
            loc[k][1] -= rate * grad[k][1]
    return loc


def draw2d(data,labels ,jpg="mds2d.jpg"):
    img = Image.new("RGB",(2000,2000),(255,255,255))
    draw = ImageDraw.Draw(img)
    n = len(data)
    print (n)
    for i in range(n):
        x = (data[i][0] + 0.5) * 1000
        y = (data[i][1] + 0.5) * 1000
        draw.text((x,y), labels[i],(0,0,0))
    img.save(jpg,"JPEG")
    return img



