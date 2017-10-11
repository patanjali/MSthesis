'''
Created on Oct 6, 2015

@author: Subhojyoti
'''

import math
import random
import numpy

class klucbTest(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''



    def upperBound(self, step, numPlays):
        #return math.sqrt(2 * math.log(step + 1) / numPlays)
        return math.sqrt(max(math.log((step + 1.0)/(self.numActions*numPlays)),0.0) / numPlays)


    def rewards(self,choice):

        #return sum(numpy.random.binomial(1,self.means[choice],1))/1.0
        return random.gauss(self.means[choice],self.variance[choice])


    def klucbGauss(self, x, d, sig2=1., precision=0.):
        """klUCB index computation for Gaussian distributions.

        Note that it does not require any search.
        """
        return x + math.sqrt(2*sig2*d)

    def klucbBern(self, x, d, precision=1e-6):
        """klUCB index computation for Bernoulli distributions."""
        upperbound = min(1., self.klucbGauss(x, d))
        #upperbound = min(1.,klucbPoisson(x,d)) # also safe, and better ?
        return self.klucb(x, d, self.klBern, upperbound, precision)


    def klBern(self, x, y):
        """Kullback-Leibler divergence for Bernoulli distributions."""

        eps = 1e-15
        x = min(max(x, eps), 1-eps)
        y = min(max(y, eps), 1-eps)
        return x*math.log(x/y) + (1-x)*math.log((1-x)/(1-y))

    def klucb(self, x, d, div, upperbound, lowerbound=-float('inf'), precision=1e-6):
        """
        The generic klUCB index computation.

        Input args.: x, d, div, upperbound, lowerbound=-float('inf'), precision=1e-6,
        where div is the KL divergence to be used.
        """
        l = max(x, lowerbound)
        #upperbound = self.klucbGauss(x, d, precision)
        u = upperbound
        while u-l>precision:
            m = (l+u)/2

            if div(x, m)>d:
                u = m
            else:
                l = m
        return (l+u)/2

#     def klucbGauss(self, x, d, sig2=1., precision=0.):
#         """klUCB index computation for Gaussian distributions.
#
#         Note that it does not require any search.
#         """
#         return x + math.sqrt(2*sig2*d)
#
#     def klucbBern(self, x, d, precision=1e-6):
#         """klUCB index computation for Bernoulli distributions."""
#         upperbound = min(1., self.klucbGauss(x, d))
#         #upperbound = min(1.,klucbPoisson(x,d)) # also safe, and better ?
#         return self.klucb(x, d, self.klBern, upperbound, precision)



    '''
    def maxEV(self, p, V, klMax):

        Uq = numpy.zeros(len(p))
        Kb = p>0.
        K = ~Kb
        if any(K):
            # Do we need to put some mass on a point where p is zero?
            # If yes, this has to be on one which maximizes V.
            eta = max(V[K])
            J = K & (V == eta)
            if (eta > max(V[Kb])):
                y = numpy.dot(p[Kb], numpy.log(eta-V[Kb])) + math.log(numpy.dot(p[Kb],  (1./(eta-V[Kb]))))
                #print "eta = " + str(eta) + ", y="+str(y);
                if y < klMax:
                    rb = math.exp(y-klMax)
                    Uqtemp = p[Kb]/(eta - V[Kb])
                    Uq[Kb] = rb*Uqtemp/sum(Uqtemp)
                    Uq[J] = (1.-rb) / sum(J) # or j=min([j for j in range(k) if J[j]]); Uq[j] = r
                    return(Uq)
        # Here, only points where p is strictly positive (in Kb) will receive non-zero mass.
        if any(abs(V[Kb] - V[Kb][0])>1e-8):
            eta = self.reseqp(p[Kb], V[Kb], klMax) # (eta = nu in the article)
            Uq = p/(eta-V)
            Uq = Uq/sum(Uq)
        else:
            Uq[Kb] = 1/len(Kb); # Case where all values in V(Kb) are almost identical.
        return(Uq)

    def reseqp(self, p, V, klMax):

        mV = max(V)
        l = mV+0.1
        tol = 1e-4
        if mV<min(V)+tol:
            return(float('inf'))
        u = numpy.dot(p, (1/(l-V)))
        y = numpy.dot(p, numpy.log(l-V)) + math.log(u) - klMax; #print "l="+str(l)+", y="+str(y);
        while abs(y)>tol:
            yp = u -  numpy.dot(p, (1/(l-V)**2)) / u # derivative
            l = l - y / yp ; #print "l = "+str(l)# newton iteration
            if l<mV:
                l = (l+y/yp +mV)/2 # unlikely, but not impossible
            u = numpy.dot(p,  (1/(l-V)))
            y = numpy.dot(p, numpy.log(l-V)) + math.log(u) - klMax ; #print "l="+str(l)+", y="+str(y); # function
        return(l)
    '''

    def computeIndex(self, arm, t):

        self.c=0.0
        #d = 2.51
        if self.numPlays[arm] == 0:
            return float('+infinity')
        else:
            #self.cumReward[arm] / self.nbDraws[arm], self.c * log(self.t) / self.nbDraws[arm], 1e-4
            #return self.klucbBern((self.payoffSums[arm] / self.numPlays[arm]), (self.c * math.log(t)) / self.numPlays[arm], 1e-4)
            #for Bernoulli
            #return self.klucbBern((self.payoffSums[arm] / self.numPlays[arm]), (math.log(t)+self.c * math.log(math.log(t))) / self.numPlays[arm], 1e-4)
            #for Gaussian
            return self.klucbGauss((self.payoffSums[arm] / self.numPlays[arm]), (math.log(t)+self.c * math.log(math.log(t))) / self.numPlays[arm], 1e-4)

    def klucbTest(self,numActions):

        #Set the environment
        self.numActions=numActions

        self.payoffSums = [0] * self.numActions
        self.numPlays = [0] * self.numActions
        self.ucbs = [0] * self.numActions
        self.upbs = [0] * self.numActions
        self.numRounds = 300000
        #self.numRounds = 400000
        #numRounds = 250000

        self.arm_reward = [0]*numActions

        #bestAction=arms/2
        self.bestAction=self.numActions-2

        #biases = [1.0 / k for k in range(5,5+numActions)]
        #means = [0.5 + b for b in biases]
        self.means =[0.1 for i in range(self.numActions)]
        self.variance=[0.7 for i in range(self.numActions)]



        self.means =[0.6 for i in range(self.numActions)]
        self.variance = [0.1 for i in range(self.numActions)]


        for i in range(0,1*self.numActions/3):
            self.means[i]=0.4
            self.variance[i]=0.2



        '''
        for i in range(0,1*self.numActions/3):
            self.means[i]=0.5
        '''
        '''
        for i in range(self.numActions/3):
            self.means[i]=0.47

        '''
        '''
        i=(2*self.numActions)/3
        while i<self.numActions:
            self.means[i]=0.46
            i=i+1
        '''
        '''
        for i in range(self.numActions/3):
            self.means[i]=0.01
        '''
        '''
        i=(2*self.numActions)/3
        while i<self.numActions:
            self.means[i]=0.05
            i=i+1
        '''

        self.means[self.bestAction]=0.9
        self.variance[self.bestAction]=0.7

        cumulativeReward = 0
        bestActionCumulativeReward = 0
        self.actionRegret=[]
        # initialize empirical sums

        t=1
        for i in range(self.numActions):

            action=i
            theReward = self.rewards(action)
            #print theReward,action
            self.arm_reward[action]=self.arm_reward[action]+theReward
            self.numPlays[action] += 1
            self.payoffSums[action] += theReward

            #f1.writelines("ucbs: (%s)" % (', '.join(["%.8f" % ucb for ucb in ucbs])))
            #f1.writelines("\tupbs: (%s)\n" %( ', '.join(["%.8f" % upb for upb in upbs])))

            #yield action, theReward, ucbs



            cumulativeReward += theReward
            bestActionCumulativeReward += theReward if action == self.bestAction else self.rewards(self.bestAction)
            regret = bestActionCumulativeReward - cumulativeReward

            self.actionRegret.append(regret)

            t = t + 1

        #t = numActions




        #t=self.numActions
        while True:
            ucbs = [(self.computeIndex(i,t)) for i in range(self.numActions)]
            #upbs = [self.upperBound(t, self.numPlays[i]) for i in range(self.numActions)]
            #print "upbs"
            #print upbs
            #print ucbs
            #getting the maximum of the ucbs
            #action = max(range(self.numActions), key=lambda i: ucbs)

            max1=-99999.0
            for p in range(self.numActions):
                if ucbs[p]>max1:
                    max1=ucbs[p]
                    action=p

            #print action
            #action = random.sample(len(self.numActions),ucbs)

            theReward = self.rewards(action)
            #print theReward,action
            self.arm_reward[action]=self.arm_reward[action]+theReward
            self.numPlays[action] += 1
            self.payoffSums[action] += theReward

            #f1.writelines("ucbs: (%s)" % (', '.join(["%.8f" % ucb for ucb in ucbs])))
            #f1.writelines("\tupbs: (%s)\n" %( ', '.join(["%.8f" % upb for upb in upbs])))

            #yield action, theReward, ucbs



            cumulativeReward += theReward
            bestActionCumulativeReward += theReward if action == self.bestAction else self.rewards(self.bestAction)
            regret = bestActionCumulativeReward - cumulativeReward

            self.actionRegret.append(regret)

            if t>=self.numRounds:
                break

            t = t + 1

            #print t

            if t%10000==0:
                print t,regret



        action=max(range(self.numActions), key=lambda i: self.arm_reward[i])
        #print self.arm_reward


        f = open('NewExpt1/expt42/testRegretKLUCB01.txt', 'a')
        for r in range(len(self.actionRegret)):
            f.write(str(self.actionRegret[r])+"\n")
        f.close()

        return cumulativeReward,bestActionCumulativeReward,regret,action,t


if __name__ == "__main__":

    wrong=0
    i=100
    while i<=100:
        turn=0
        for j in range(0,100):
            random.seed(i+j)
            obj=klucbTest()
            cumulativeReward,bestActionCumulativeReward,regret,arm,timestep=obj.klucbTest(i)
            if arm!=i-2:
            #if arm!=i/2:
                wrong=wrong+1
            print "turn: "+str(turn)+"\twrong"+str(wrong)+"\tarms: "+str(i)+"\tbarm: "+str(arm)+"\tReward: "+str(cumulativeReward)+"\tbestCumReward: "+str(bestActionCumulativeReward)+"\tregret: "+str(regret)
            f = open('NewExpt1/expt42/testKLUCB01.txt', 'a')
            f.writelines("arms: %d\tbArms: %d\ttimestep: %d\tregret: %d\tcumulativeReward: %.2f\tbestCumulativeReward: %.2f\n" % (i, arm, timestep, regret, cumulativeReward, bestActionCumulativeReward))
            f.close()

            turn=turn+1
        i=i+1
