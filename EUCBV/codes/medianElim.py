'''
Created on Jul 28, 2015

@author: Subhojyoti
'''

import math
import random
import numpy
#import statistics

class medianElim(object):
    '''
    classdocs
    '''
    
    min1=-9999999
    
    def __init__(self):
        '''
        Constructor
        '''
        #print self.numRounds
        #print self.means
        
    
    def rewards(self,choice,t):
        #return sum(numpy.random.binomial(1,self.means[choice],1))/1.0
        return random.gauss(self.means[choice],self.variance[choice])
    
    
    def remArms(self):
        count=0
        arm=-1
        for i in range(self.numActions):
            if self.B[i]!=-1:
                count=count+1
                arm=i
        return count
        
    def medianElimimation(self,arms,epsilon,delta,wrong,turn):
        
        self.numActions = arms
        self.horizon=300000
        
        self.bestAction=self.numActions-2

        self.means =[0.1 for i in range(self.numActions)]
        self.variance =[0.7 for i in range(self.numActions)]


        i=(1*self.numActions)/3
        while i<self.numActions:
            self.means[i]=0.8
            self.variance[i]=0.1
            i=i+1

        '''
        i=(2*self.numActions)/3
        while i<self.numActions:
            self.means[i]=0.03
            i=i+1
        '''
        self.means[self.bestAction]=0.9
        self.variance[self.bestAction]=0.7
        

        print "Means: "+str(self.means)

        self.arm_reward = [0]*self.numActions
        
        self.timestep=0
        self.B=[0 for i in range(self.numActions)]
        
        self.payoffSums = [0] * self.numActions
        self.numPlays = [0] * self.numActions
        self.avgPayOffSums = [0] * self.numActions
        
        self.cumulativeReward = 0
        self.bestActionCumulativeReward = 0
        self.regret = 0
        
        self.arm_reward = [0]*self.numActions

        self.actionRegret=[]

        l=1
        epsilon_l=epsilon*0.25
        delta_l=delta*0.5
        
        while True:
            
            print "\n\nRound: "+str(l)
            self.numRounds = int(math.ceil((1/(epsilon_l*0.5))*math.log(3/delta_l)))
            print "nm: "+str(self.numRounds)
            
            for i in range(self.numActions):
                for j in range(self.numRounds):
                    
                    if self.B[i]!=-1:
                        theReward = self.rewards(i, self.timestep)
                            
                        self.arm_reward[i]=self.arm_reward[i]+theReward
                        self.numPlays[i] += 1
                        self.payoffSums[i] += theReward
                        self.avgPayOffSums[i] = self.payoffSums[i] / self.numPlays[i]
                            
                        self.cumulativeReward += theReward
                        self.bestActionCumulativeReward += theReward if i == self.bestAction else self.rewards(self.bestAction, self.timestep)
                        self.regret = self.bestActionCumulativeReward - self.cumulativeReward

                        self.actionRegret.append(self.regret)

                        self.timestep=self.timestep+1

            self.avgPayOffSums1=[]
            for i in range(self.numActions):
                if self.B[i]!=-1:
                    self.avgPayOffSums1.append(self.avgPayOffSums[i])
            median_val=numpy.median(sorted(self.avgPayOffSums1))
            
            
            print "AvgPayoff: "+str(self.avgPayOffSums)
            print "Median: "+str(median_val)
            
            for i in range(self.numActions):
                if self.B[i]!=-1:
                    if self.avgPayOffSums[i]<median_val:
                        self.B[i]=-1
            
            print "B: "+str(self.B)
            print "Rem arms: "+str(self.remArms())
            
            
            epsilon_l=0.75*epsilon_l
            delta_l=0.5*delta_l
            l=l+1
                 
            count=self.remArms()
            if count<=1 or self.timestep>=self.horizon:
                break
            
        for i in range(self.numActions):
            if self.B[i]!=-1:
                bestArm=i

        arm=bestArm

        print "last arm:"+str(arm) + " turn:"+str(turn) + " wrong:"+str(wrong)
        while self.timestep<self.horizon:

            theReward = self.rewards(arm,self.timestep)
            self.arm_reward[arm]=self.arm_reward[arm]+theReward
            self.numPlays[arm] += 1
            self.payoffSums[arm] += theReward

            self.avgPayOffSums[arm] = self.payoffSums[arm] / self.numPlays[arm]

            self.cumulativeReward += theReward
            self.bestActionCumulativeReward += theReward if arm == self.bestAction else self.rewards(self.bestAction, self.timestep)
            self.regret = self.bestActionCumulativeReward - self.cumulativeReward
            self.actionRegret.append(self.regret)

            self.timestep=self.timestep+1



        f = open('NewExpt1/expt21/testRegretMedElim.txt', 'a')
        for r in range(len(self.actionRegret)):
            f.write(str(self.actionRegret[r])+"\n")
        f.close()

        return self.cumulativeReward,self.bestActionCumulativeReward,self.regret,bestArm,self.timestep
        
        
if __name__ == "__main__":
    

    
    wrong=0
    i=100
    while i<=100:
        
        for j in range(0,100):

            numpy.random.seed(i+j)
            me= medianElim()
            f = open('NewExpt1/expt21/testMedElim.txt', 'a')
            cumulativeReward,bestActionCumulativeReward,regret,bestArm,timestep=me.medianElimimation(i,0.1,0.1,wrong,j)
            if bestArm!=i-2:
                wrong=wrong+1
            f.writelines("arms: %d\tbArms: %d\ttimestep: %d\tregret: %d\tcumulativeReward: %.2f\tbestCumulativeReward: %.2f\n" % (i, bestArm, timestep, regret, cumulativeReward, bestActionCumulativeReward))
            f.close()
        i=i+1
    
    
    #ucb= UCBRevisted2()
    
