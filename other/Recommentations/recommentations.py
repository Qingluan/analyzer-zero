from math import sqrt 
from math import pow
import os



critics  = {
	'Lisa Rose':
		{
			'Lady in the water' :2.5,
			'Snakes on a plane' :3.5,
			'Just my Luck' : 3.0,
			'Superman' : 3.5,
			'You, Me and Dupree' :  2.5,
			'The night Listener' : 3.0, 
		},
	'Gene Seymour' : 
		{
			'Lady in the water' :3.0,
			'Snakes on a plane' :3.5,
			'Just my Luck' : 1.5,
			'Superman' : 5.0,
			'You, Me and Dupree' :  3.0,
			'The night Listener' : 1.5, 
		},
	'Michael Phillips':
		{
			'Lady in the water' :2.5,
			'Snakes on a plane' :3.0,

			'Superman' : 3.5,

			'The night Listener' : 4.0, 
		},
	'Claudia Puig':
		{

			'Snakes on a plane' :3.5,
			'Just my Luck' : 3.0,
			'Superman' : 4.0,
			'You, Me and Dupree' :  2.5,
			'The night Listener' : 4.5, 
		},
	'Mick LaSalle':
		{
			'Lady in the water' :3.0,
			'Snakes on a plane' :4.0,
			'Just my Luck' : 2.0,
			'Superman' : 3.0,
			'You, Me and Dupree' :  2.0,
			'The night Listener' : 3.0, 
		},
	'Jack Matthews':
		{
			'Lady in the water' :3.0,
			'Snakes on a plane' :4.0,

			'Superman' : 5.0,
			'You, Me and Dupree' :  3.5,
			'The night Listener' : 3.0, 
		},
	'Toby' :
		{

			'Snakes on a plane' :4.5,

			'Superman' : 4.0,
			'You, Me and Dupree' :  1.0,

		}
}

def sim_distance(prefs,person_1,person_2):
    si = {}
    for item in prefs[person_1]:
        if item in prefs[person_2]:
            si[item] = 1
    print si

    if len(si) == 0 :
        return 0
    sum_of_distance = sum([ pow(prefs[person_1][item]- prefs[person_2][item] ,2 ) for item in si])
    return 1/ (1 + sqrt (sum_of_distance))


def classify_per(prefs,per1,per2):
    xdim,ydim = [],[]sa
    for item in prefs[per1]:
        if item in prefs[per2]:
            print item
            xdim +=[ prefs[per1][item]]
            ydim +=[ prefs[per2][item]]

    if len(xdim)==0: return 0
    
    return (xdim,ydim)


def sim_correlation(perfs,person1,person2):
	si = {}
	for i in perfs[person1]:
		if i in perfs[person2]:
			si[i] = 1

	if len(si) == 0 :return 0

	n = len(si)

	sum1 = sum([perfs[person1][it] for it in si])
	sum2 = sum([perfs[person2][it] for it in si])

	# print "sum1 : {}\nsum2 : {}".format(sum1,sum2)

	sum1Sq = sum([pow(perfs[person1][item],2) for item in si])
	sum2Sq = sum([pow(perfs[person2][item],2) for item in si])

	# print "sum1Sq : {}\nsum2Sq : {}".format(sum1Sq,sum2Sq)

	pSum = sum([perfs[person1][item] * perfs[person2][item] for item in si])

	# print "pSum : {}".format(pSum)

	#calculate person score
	num = pSum - (sum1 * sum2)/n
	
	den = sqrt((sum1Sq - pow(sum1,2)/n)*(sum2Sq - pow(sum2,2)/n))

	# print "num : {}\nden : {}".format(num,den)
	
	if den == 0: return 0

	r = num/den

	print r
	return r

def getRecommentaion(prefs,person,similarity=sim_correlation):
	totals = {}
	simSum = {}

	def _compare(other):
		if other == person:
			return
		sim=similarity(prefs, person, other)
		if sim < 0 :return

		for item in prefs[other]:
			if item not in prefs[person] or prefs[person][item] == 0:
				totals.setdefault(item,0)

				totals[item]+= prefs[other][item]* sim

				simSum.setdefault(item,0)
				simSum[item] += sim

	map(_compare, prefs)
	print totals
	print simSum
	rankings = [(total/simSum[item],item) for item , total in totals.items()  ]

	rankings.sort()

	return rankings

def loadDataLen(path="./data"):
	files = [ path+x for x in  os.listdir(path) if "dat" in x ]
	print "load ," files
	prefs  = {}
	movies = {}
	with open(path+"/movies.dat") as fp:

	classifies = {}








