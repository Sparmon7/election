from enum import Enum
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter


#asking user for inputs
print("Welcome to Spencer's election simulation")
print()

#format
print("1: Partisan primary with plurality voting")
print("2: Final four primary with plurality voting")
print("3: Final four primary with ranked choice voting")
class Format(Enum):
    Partisan = 1
    Mixed = 2
    RCV = 3
formatRaw = 0
while(formatRaw < 1 or formatRaw > 3 ):  
    try: 
        formatRaw = int(input("Type the number of the type of election you would like: "))
    except:
        formatRaw=0
format = Format(formatRaw)

#percent republican
print()
percentRepublican = -1.0
while(percentRepublican <0 or percentRepublican > 100): 
    try:
        percentRepublican = float(input("What percent of the district would you like to be Republican? "))
    except:
        percentRepublican = -1.0

#number of voters
print()
numVoters = -1
while(numVoters <0): 
    try:
        numVoters = int(input("How many voters? "))
    except:
        numVoters = -1

#number of politicians from each party
print()
numPoliticians = 0
while(numPoliticians <1 + int(format is not Format.Partisan)): 
    try:
        numPoliticians = int(input("How many politicians do you want running from each party? "))
    except:
        numPoliticians = 0

#number of simulations
print()
simulations = 0
while(simulations <1 ): 
    try:
        simulations = int(input("How many times would you like to run the simulation? "))
    except:
        simulations = 0
print()

#voter chooses closest candidate        
def findClosest( array, value):
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or abs(value - array[idx-1]) < abs(value - array[idx])):
        return idx-1
    else:
        return idx
        
#simulation       
results = []
differences = []
absResults = []
absDifferences=[]
for number in range(0, simulations):
    

    #creating voters
    #https://www.pewresearch.org/politics/2014/06/12/political-polarization-in-the-american-public/
    #94% of dems are to the left of the median rep, so standard deviation = 1.286
    #92% of reps are to the left of the median dem, so standard deviation = 1.423
    #instead i average it out to get 1.36 for 93%
    numRep = int(0.01*numVoters*percentRepublican)
    demVoters = np.sort(np.random.normal(loc = -1,  scale = 1.36, size = numVoters-numRep))
    repVoters = np.sort(np.random.normal(loc = 1,  scale = 1.36, size = numRep))
    voters = np.sort(np.concatenate([demVoters, repVoters]))
   
    ##graphing voters
    """
    bins = np.linspace(-3, 3, 24)
    plt.hist(demVoters, bins, color = "blue", alpha = 0.25, label="Democrats", weights =  np.ones(len(demVoters)) / len(voters))
    plt.hist(repVoters, bins, color = "red", alpha = 0.25, label="Republicans", weights =  np.ones(len(repVoters)) / len(voters))
    plt.xlabel("Ideological score")
    plt.ylabel("Frequency")
    plt.axvline(np.median(demVoters), label = "Median Democrat Voter", color = "Blue", linestyle = "dashed")
    plt.axvline(np.median(repVoters), label = "Median Republican Voter", color = "Red", linestyle = "dashed")
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1, decimals = 1))
    plt.legend()
    plt.xlim([-3,3])
    plt.show()
    """
   
    #creating politicians
    demPoliticians = np.sort(np.random.normal(loc = -1, scale = 1.36, size = numPoliticians))
    repPoliticians = np.sort(np.random.normal(loc =  1, scale = 1.36, size = numPoliticians))


    #primary           
    generalPoliticians = None
    if(format is Format.Partisan):
        winners = [0]*2
        #partisan primary
        #democratic side
        demVotes = [0]*demPoliticians
        for i in demVoters:
            demVotes[findClosest(demPoliticians, i)] +=1
        winners[0] = demPoliticians[np.argmax(demVotes)]
        
        #republican side
        repVotes = [0]*repPoliticians
        for i in repVoters:
            repVotes[findClosest(repPoliticians, i)] +=1
        winners[1] = repPoliticians[np.argmax(repVotes)]
        winners.sort()

        generalPoliticians = np.array(winners)
        
        
    else:
        #final four primary
        winners = [0]*4
        tempPoliticians = np.sort(np.concatenate([demPoliticians, repPoliticians]))
        tempVotes = [0]*len(tempPoliticians)
        for i in voters:
            tempVotes[findClosest(tempPoliticians, i)]+=1
        sortedVertices = np.argsort(tempVotes)
        for j in range(0,4):
            winners[j] = tempPoliticians[sortedVertices[len(sortedVertices)-1-j]]
        winners.sort()
        generalPoliticians = np.copy(np.array(winners))

    #General election
    winner = None
    if(format is not Format.RCV):
        #plurality
        votes = [0]*4
        for i in voters:
            votes[findClosest(generalPoliticians, i)] +=1
        votes = np.array(votes)
        winner = generalPoliticians[np.argmax(votes)]
            
    else:
        #RCV
        votes = [None]*numVoters
        #creating preferences
        for k in range(0,numVoters):
            i = voters[k]
            voterPoliticians = generalPoliticians.copy()
            tempArray = []
            j=0
            while j < 3:
                fav = findClosest(voterPoliticians, i)
                tempArray.append(voterPoliticians[fav])
                voterPoliticians = np.delete(voterPoliticians,fav)
                j+=1
                
            tempArray.append(voterPoliticians[0])
            votes[k]= tempArray
        
        #finding the winner   
        while(winner is None):
            totals = [0]*len(generalPoliticians)
            for i in votes:
                totals[np.where(generalPoliticians==i[0])[0][0]] +=1
            winner = generalPoliticians[totals.index(max(totals))]
            if max(totals) < numVoters/2:
                winner = None
                loser = generalPoliticians[totals.index(min(totals))]
                generalPoliticians = np.delete(generalPoliticians, totals.index(min(totals)))
                for i in range(0, numVoters): 
                    tempArray = votes[i]
                    tempArray.remove(loser)
                    votes[i]=tempArray
                    
        
    #end result
    results.append(winner)
    absResults.append(abs(winner))
    differences.append(winner - np.median(voters))
    absDifferences.append(abs(winner-np.median(voters)))

#results
print("Note that a value of 1 symbolizes the average republican and a value of -1 symbolizes an average democrat, with 0 being a centrist.")
print(f"The mean election result was {np.mean(results)}")
print(f"The mean absolute election result was {np.mean(absResults)}")
print(f"The average distance from median was {np.mean(differences)}")
print(f"The average absolute distance from median was {np.mean(absDifferences)}")
