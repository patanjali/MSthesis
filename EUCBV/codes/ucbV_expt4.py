'''
Created on May 10, 2016

@author: Subhojyoti
'''

import math
import random
import numpy
import fileinput

class ucbV(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        
    
    def upperBound(self, step, numPlays,payoffSums,sqpayoffSums):
        #return math.sqrt(2 * math.log(step + 1) / numPlays)
        #x=payoffSums / numPlays
        #print sqpayoffSums,numPlays,step
        
        vj=abs(((sqpayoffSums/numPlays) - (payoffSums/numPlays)*(payoffSums/numPlays)))
        #vj=1.0/numPlays*((payoffSums - (payoffSums/numPlays))*(payoffSums - (payoffSums/numPlays)))
        #print vj
        return (math.sqrt((2*vj*math.log(step+1))/numPlays)+math.log(step+1)/numPlays)
    
    def readenv(self):
        data=[]
        filename="env/env3.txt"
        for line in fileinput.input([filename]):

            try:
                line1 = [line.split(", ") or line.split("\n") ]
                #print numpy.shape(line1)
                #print line1
                take=[]
                for i in range(len(line1[0])):
                    take.append(float(line1[0][i]))
                #print take
                data.append(take)
            except ValueError,e:
                print e
        #print data
        self.means=(data[0])
        self.variance=(data[1])

    def rewards(self,choice):
        return random.gauss(self.means[choice],self.variance[choice])
        #return sum(numpy.random.binomial(1,self.means[choice],1))/1.0
        
    def ucb1(self,numActions):
    
        #Set the environment
        self.numActions=numActions
        
        self.payoffSums = [0] * self.numActions
        self.sqpayoffSums = [0] * self.numActions
        self.numPlays = [0] * self.numActions
        self.ucbs = [0] * self.numActions
        self.upbs = [0] * self.numActions
        #self.numRounds = 3000000
        self.numRounds = 400000
        #numRounds = 250000
        
        self.arm_reward = [0]*numActions
        
        #bestAction=arms/2
        self.bestAction=self.numActions-2

        self.means=[]
        self.variance=[]
        self.readenv()
        
        cumulativeReward = 0
        bestActionCumulativeReward = 0
        self.actionRegret=[]
        # initialize empirical sums
        
        t=1
       
        for i in range(self.numActions):
            theReward = self.rewards(i)
            self.payoffSums[i] += theReward
            self.sqpayoffSums[i] += abs( theReward*theReward)
            self.numPlays[i]=self.numPlays[i]+1
                
            cumulativeReward += theReward
            bestActionCumulativeReward += theReward if i == self.bestAction else self.rewards(self.bestAction)
            regret = bestActionCumulativeReward - cumulativeReward
            
            self.actionRegret.append(regret)
            
            t=t+1
                #t=t+1
                
        #ucbs = [(self.payoffSums[i] / self.numPlays[i]) + self.upperBound(t, self.numPlays[i],self.payoffSums[i],self.sqpayoffSums[i]) for i in range(self.numActions)]
        #upbs = [self.upperBound(t, self.numPlays[i],self.payoffSums[i],self.sqpayoffSums[i]) for i in range(self.numActions)]
                
        #t = numActions
        
        
            
        #print self.sqpayoffSums
        
        #t=d
        while True:
            #print self.sqpayoffSums
            
            #ucbs = [(self.payoffSums[i] / self.numPlays[i]) + self.upperBound(t, self.numPlays[i],self.payoffSums[i],self.sqpayoffSums[i]) for i in range(self.numActions)]
            ucbs = [ (self.payoffSums[i] / self.numPlays[i]) +self.upperBound(t, self.numPlays[i],self.payoffSums[i],self.sqpayoffSums[i]) for i in range(self.numActions)]
            #upbs = [self.upperBound(t, self.numPlays[i],self.payoffSums[i],self.sqpayoffSums[i]) for i in range(self.numActions)]
            #print "upbs"
            #print upbs
            #print ucbs
            #getting the maximum of the ucbs
            #action = max(range(self.numActions), key=lambda p: ucbs[p])
            
            max1=-99999.0
            for p in range(self.numActions):
                if ucbs[p]>max1:
                    max1=ucbs[p]
                    action=p
            
            theReward = self.rewards(action)
            #print theReward,action
            self.arm_reward[action]=self.arm_reward[action]+theReward
            self.numPlays[action] += 1
            self.payoffSums[action] += theReward
            self.sqpayoffSums[i] += (theReward*theReward)
            #f1.writelines("ucbs: (%s)" % (', '.join(["%.8f" % ucb for ucb in ucbs])))
            #f1.writelines("\tupbs: (%s)\n" %( ', '.join(["%.8f" % upb for upb in upbs])))
            
            #yield action, theReward, ucbs
            
            cumulativeReward += theReward
            bestActionCumulativeReward += theReward if action == self.bestAction else self.rewards(self.bestAction)
            regret = bestActionCumulativeReward - cumulativeReward
            
            self.actionRegret.append(regret)
            
            if t%10000==0:
                print t,regret
            
            if t>=self.numRounds:
                break
            
            
            
            t = t + 1
            
    
        action=max(range(self.numActions), key=lambda i: self.arm_reward[i])
        print self.arm_reward
        

        f = open('NewExpt/expt5/testRegretUCBV01.txt', 'a')
        for r in range(len(self.actionRegret)):
            f.write(str(self.actionRegret[r])+"\n")
        f.close()

        return cumulativeReward,bestActionCumulativeReward,regret,action,t
        

if __name__ == "__main__":
    
    wrong=0
    i=100
    while i<=100:
        turn=0
        for j in range(100):
            random.seed(i+j)
            obj=ucbV()
            cumulativeReward,bestActionCumulativeReward,regret,arm,timestep=obj.ucb1(i)
            if arm!=i-2:
            #if arm!=i/2:
                wrong=wrong+1
            print "turn: "+str(turn)+"\twrong: "+str(wrong)+"\tarms: "+str(i)+"\tbarm: "+str(arm)+"\tReward: "+str(cumulativeReward)+"\tbestCumReward: "+str(bestActionCumulativeReward)+"\tregret: "+str(regret)
            f = open('NewExpt/expt5/testUCBV01.txt', 'a')
            f.writelines("arms: %d\tbArms: %d\ttimestep: %d\tregret: %d\tcumulativeReward: %.2f\tbestCumulativeReward: %.2f\n" % (i, arm, timestep, regret, cumulativeReward, bestActionCumulativeReward))
            f.close()
            
            turn=turn+1
        i=i+1
        