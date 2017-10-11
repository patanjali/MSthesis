'''
Created on Apr 1, 2017

@author: Subhojyoti
'''

import math
import random
import numpy
from sets import Set
import fileinput

class EUCBV(object):
    '''
    classdocs
    '''

    min1=-9999999

    def __init__(self):
        '''
        Constructor
        '''



    #Calculate rewards
    def rewards(self,choice, timesteps):
        #Gaussain Reward
        return random.gauss(self.means[choice],self.variance[choice])
        #Bernoulli Reward(1 sample from Binomial Distribution)
        #return sum(numpy.random.binomial(1,self.means[choice],1))/1.0

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

    #Count the number of remaining arms
    def remArms(self):
        count=0
        for i in range(self.numActions):
            if self.B[i]!=-1:
                count=count+1
        return count

    def exp_func(self):
        
        #self.func=1.0
        #self.func=math.log(self.horizon)
        #self.func=self.numActions*self.numActions*self.horizon
        #self.func=self.horizon / math.log(self.horizon*self.numActions)
        self.func=self.horizon / (self.numActions*self.numActions)
        return self.func

    def upperBoundVar(self, numPlays, arm):
        vj=((self.sqPayOffSums[arm]/self.numPlays[arm]) - (self.avgPayOffSums[arm]*self.avgPayOffSums[arm]))
        #return math.sqrt(self.rho * vj * max(math.log(( self.exp_func()*self.numRounds*self.delta_tilda)),0) / (4*numPlays) + (self.rho * max(0,math.log((self.exp_func()*self.numRounds*self.delta_tilda))) / (4*numPlays)))
        return math.sqrt((self.rho * (vj+2.0) * max(math.log(( self.exp_func()*self.numRounds*self.delta_tilda)),0)) / (4.0 *numPlays) )


    #Arm Elimination
    def ArmElimination(self):

        take=self.min1
        for i in range(0,self.numActions):
            if self.B[i]!=-1:
                if take < self.avgPayOffSums[i]:
                    take = i

        for i in range(0,self.numActions):

            if self.B[i]!=-1:
                #c=math.sqrt((self.rho * math.log(self.exp_func() *self.horizon*self.rangetake))/(2*self.nm))

                #c=self.upperBoundVar(self.numPlays[i],i)
                #c1=self.upperBoundVar(self.numPlays[take],take)

                c=self.upperBoundVar(self.numPlays[i],i)
                c1=self.upperBoundVar(self.numPlays[take],take)

                if (self.avgPayOffSums[i] + c < self.avgPayOffSums[take] - c1) and i!=take:
                #if self.avgPayOffSums[b] + c*math.sqrt(self.weight*1.0/self.rangetake) < self.avgPayOffSums[take1] - c*math.sqrt(self.weight*1.0/self.rangetake):
                        
                    self.B[i]=-1


                    print "Remove Arm:"+ str(i)


    #Calculate number of pulls each round
    def calculate_pulls(self):

        self.nm= int(math.ceil((math.log(self.exp_func() *self.horizon*self.delta_tilda*self.delta_tilda))/(2.0*self.delta_tilda)))
        self.T = self.timestep + (self.remArms() * self.nm )
                
        print "nm: "+str(self.nm), "T: "+str(self.T), "Regret: "  + str(self.regret)
        #return self.nm


    '''
    Running the Clustered UCB
    '''

    def eUCBV(self,arms,turn,wrong):

        '''
        Set Environment
        '''
        self.numActions = arms

        #self.horizon=60000
        self.horizon=400000
        #self.horizon=100000 + self.numActions*self.numActions*1000
        #self.horizon = 100000 + self.numActions*self.numActions*self.numActions



        self.delta_tilda=1.0
        self.bestAction=self.numActions-2



        self.numRounds = math.floor(0.5*math.log10(self.horizon/math.e)/math.log10(2))
        #self.numRounds = math.floor(0.5*math.log10((7.0*self.horizon)/self.numActions)/math.log10(2))
        #self.numRounds = math.floor(0.5*math.log10(self.horizon)/math.log10(2))

        print "\n\nnumrounds:"+str(self.numRounds)

        self.means=[]
        self.variance=[]
        self.readenv()

        print self.means

        self.B=[0 for i in range(self.numActions)]
        self.timestep=0

        self.nm=1.0
        self.m=0.0
        self.rho=0.5

        self.ucbs=[0.0 for i in range(self.numActions)]

        self.payoffSums = [0] * self.numActions
        self.sqPayOffSums = [0] * self.numActions
        self.numPlays = [0] * self.numActions
        self.avgPayOffSums = [0] * self.numActions
        self.variance = [0] * self.numActions

        self.cumulativeReward = 0
        self.bestActionCumulativeReward = 0
        self.regret = 0
        self.regretBounds = 0

        self.arm_reward = [0]*self.numActions

        #self.func=math.log(self.horizon)
        #self.func=1.0
        #self.func=self.numRounds / math.log(self.horizon*self.numActions)

        self.actionRegret=[]
        
        #Pull each arm once
        for i in range(self.numActions):
            theReward = self.rewards(i, self.timestep)

            self.arm_reward[i]=self.arm_reward[i]+theReward
            self.numPlays[i] += 1
            self.payoffSums[i] += theReward
            self.sqPayOffSums[i] += theReward*theReward
            self.avgPayOffSums[i] = self.payoffSums[i] / self.numPlays[i]

            self.cumulativeReward += theReward
            self.bestActionCumulativeReward += theReward if i == self.bestAction else self.rewards(self.bestAction, self.timestep)
            self.regret = self.bestActionCumulativeReward - self.cumulativeReward
                                
            self.actionRegret.append(self.regret)

            self.timestep=self.timestep+1
        
        self.calculate_pulls()
        
        while True:

            for i in range(self.numActions):
                if self.B[i]!=-1:
                    #c=math.sqrt((self.rho_s * math.log(self.exp_func() *self.horizon*self.delta_tilda*self.delta_tilda))/(2*(self.numPlays[i])))
                    #self.alpha=self.numRounds/self.numPlays[i]
                    #c=math.sqrt(self.rho*(math.log(self.exp_func() *self.horizon*self.delta_tilda))/(2*(self.numPlays[i])))
                    self.ucbs[i]=self.avgPayOffSums[i] + self.upperBoundVar(self.numPlays[i],i)
                
            #arm = max(range(self.numActions), key=lambda j: self.ucbs[j])
            take=self.min1
            arm=-1
            for i in range(self.numActions):
                if take < self.ucbs[i] and self.B[i]!=-1:
                    take = self.ucbs[i]
                    arm=i
            
            
            theReward = self.rewards(arm, self.timestep)

            self.arm_reward[arm]=self.arm_reward[arm]+theReward
            self.numPlays[arm] += 1
            self.payoffSums[arm] += theReward
            self.sqPayOffSums[arm] += theReward*theReward
            self.avgPayOffSums[arm] = self.payoffSums[arm] / self.numPlays[arm]
    
            self.cumulativeReward += theReward
            self.bestActionCumulativeReward += theReward if arm == self.bestAction else self.rewards(self.bestAction, self.timestep)
            self.regret = self.bestActionCumulativeReward - self.cumulativeReward
                                    
            self.actionRegret.append(self.regret)
    
            self.timestep=self.timestep+1
            
            self.ArmElimination()

            if self.timestep>=self.horizon:
                break   
             
            if self.timestep >= self.T and self.m <= self.numRounds:
                   
                print "\n\nRound: "+str(self.m)
                print "AvgPayOffsums: " + str(self.avgPayOffSums)
                
                print "B: "+str(self.B)
                print "numPlays: " +str(self.numPlays)
                
                #self.ArmElimination()
                #self.SetElimination()
                
                #update parameters
                
                self.delta_tilda=self.delta_tilda/2
                self.m = self.m + 1

                self.calculate_pulls()
                

        #Print output file for regret for each timestep
        f = open('NewExpt/expt5/testRegretEUCBV01.txt', 'a')
        for r in range(len(self.actionRegret)):
            f.write(str(self.actionRegret[r])+"\n")
        f.close()

                
        print "\n\nEnd Horizon: "+str(self.timestep)
        print "AvgPayOffsums: " + str(self.avgPayOffSums)

        print "B: "+str(self.B)
        print "numPlays: " +str(self.numPlays)        
        
        return self.cumulativeReward,self.bestActionCumulativeReward,self.regret,arm,self.timestep


if __name__ == "__main__":


    wrong=0

    arms=100
    while arms<=100:

        for turn in range(0,100):

            #set the random seed, same for all environment
            random.seed(arms+turn)

            ucb= EUCBV()
            cumulativeReward,bestActionCumulativeReward,regret,bestArm,timestep=ucb.eUCBV(arms,turn,wrong)
            if bestArm!=arms-2:
                wrong=wrong+1

            print "turn: "+str(turn+1)+"\twrong: "+str(wrong)+"\tarms: "+str(arms)+"\tbarm: "+str(bestArm)+"\tReward: "+str(cumulativeReward)+"\tbestCumReward: "+str(bestActionCumulativeReward)+"\tregret: "+str(regret)


            #Print final output file for cumulative regret
            f = open('NewExpt/expt5/EUCBV01.txt', 'a')
            f.writelines("arms: %d\tbArms: %d\ttimestep: %d\tregret: %d\tcumulativeReward: %.2f\tbestCumulativeReward: %.2f\n" % (arms, bestArm, timestep, regret, cumulativeReward, bestActionCumulativeReward))
            f.close()

        arms=arms+10

        print "total wrong: "+str(wrong)

