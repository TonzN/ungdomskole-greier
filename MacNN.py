import math
import random
import numpy as np

#Genetic Algorithm
class Dummy:
    def __init__(self, FitnessFunction, Arch, MR):
        self.Gene = NeuralNetwork("GA")
        self.Gene.Create(Arch)
        self.Arch = Arch 
        self.Fitness, self.Output = FitnessFunction(self.Gene)
        self.FF = FitnessFunction
        self.MR = MR
    
    def Crossover(self, Partner):
        Cross = math.floor((len(self.Gene.Weights)-1)/2)
        child = Dummy(self.FF, self.Arch, self.MR)
        for i in range(len(self.Gene.Weights)-1):
            if i < Cross:
                child.Gene.Weights["rIndex"+str(i)] = self.Gene.Weights["rIndex"+str(i)]
            else:
                child.Gene.Weights["rIndex"+str(i)] = Partner.Gene.Weights["rIndex"+str(i)]
        return child

    def Mutate(self, Type = "Single"):
        for l in range(len(self.Gene.Weights)): #Layer
            for r in range(len(self.Gene.Weights["rIndex"+str(l)])) : #Row             
                for i in range(len(self.Gene.Weights["rIndex"+str(l)][r])): #Weight
                    if random.randint(1, 10**5)/100000 <= self.MR:
                        self.Gene.Weights["rIndex"+str(l)][r][i] = random.randint(1,10**6)/1000000
        
class Population:
    def __init__(self, PopSize, MR, FitnessFunction, Arch):
        self.MutationRate = MR
        self.Size = PopSize
        self.Population = [] 
        self.MatingPool = []
        self.Gen = 0
        self.Arch = Arch
        self.WorstScore = 0
        self.Record = 0
        
        for i in range(self.Size):
            New = Dummy(FitnessFunction, Arch, self.MutationRate)
            self.Population.append(New)

    def NaturalSelection(self):
        self.MatingPool = []
        MaxFitness = 0
        TotallScore = 0
        for i in self.Population:
            if i.Fitness > MaxFitness:
                MaxFitness = i.Fitness
            TotallScore += i.Fitness
        avarage = TotallScore/len(self.Population)

        for i in self.Population:
            normalized = (i.Fitness-0.1)/(MaxFitness-0.1)
            x = math.floor(normalized * 100)
            if i.Fitness >= avarage:
                for n in range(0, x):
                    self.MatingPool.append(i)
                    
    def NextGen(self):
        for i in range(0, len(self.Population)-1):
            x = self.MatingPool[random.randint(0, len(self.MatingPool)-1)]
            y = self.MatingPool[random.randint(0, len(self.MatingPool)-1)]
            child = x.Crossover(y)
            child.Mutate(self.MutationRate)
            self.Population[i] = child
        
        self.Gen += 1

    def BestIndevidual(self):
        Best = 0
        TotallScore = 0
        BestOutput = None
        for i in self.Population:
            TotallScore += i.Fitness
            if self.WorstScore == 0:
                self.WorstScore = i.Fitness
            elif self.WorstScore > i.Fitness:
                self.WorstScore = i.Fitness

            if i.Fitness > Best:
                Best = i.Fitness
                BestOutput = i.Output

        self.Avarage = TotallScore/len(self.Population)
        if Best > self.Record:
            self.Record = Best

        return Best, BestOutput

#Activation Function
def Sigmoid(x):
    return 1/(1+np.exp(-x))

def dSigmoid(x):
    return Sigmoid(x)*(1-Sigmoid(x))

def Relu(x):
    return np.maximum(0, x)

def dReLu(x):
    x[x<=0] = 0
    x[x>0] = 1
    return x

#Training
def Cost(prediction, y): 
    mse = np.mean(np.square(y-prediction)) * 0.5
    return np.squeeze(mse)

def dCost(prediction, y): 
    return 2 * 0.5*np.subtract(y, prediction)

def ReinforcementLearning():
    pass

AF = {
    "Relu": Relu,
    "Sigmoid": Sigmoid
}

dAF = {
    "Relu": dReLu,
    "Sigmoid": dSigmoid
}

class Agent:
    pass

class NeuralNetwork: #Object class
    def __init__(self, TrainingAlgorithm = "BackPropogation"):
        self.Generation = 0
        self.TrainingAlgorithm = TrainingAlgorithm

    def Create(self, Architecture):
        self.Weights = {}
        self.TotallCost = 0
        self.Biases = {}
        self.firstCost = False
        self.Arch = Architecture
        self.Layers = [Architecture[i][1] for i in range(1,len(Architecture))]
        
        for l in range(len(Architecture)-1):
            self.Weights["rIndex"+str(l)] = np.random.rand(Architecture[l][0], Architecture[l+1][0]) 
            self.Biases["rIndex"+str(l)] = np.random.rand(Architecture[l][0]) 

    def Activate(self, Layer, aI):
        Bias = self.Biases["rIndex"+str(Layer)]
        Sum = np.dot(self.Weights["rIndex"+str(Layer)], aI)
        Layer = str(self.Layers[Layer])
      
        return AF[Layer](np.add(Sum, Bias)), np.add(Sum, Bias)

    def Forward_prop(self, inp):
        ActivatedInput = inp #aI
        self.Log = {}
        
        for i in range(len(self.Layers)):
            prevAI = ActivatedInput
            ActivatedInput, z = self.Activate(i, prevAI)
            self.Log["pAI"+str(i)] = prevAI # Previous Activated Input
            self.Log["AI"+str(i)] = ActivatedInput
            self.Log["z"+str(i)] = z
        
        return ActivatedInput

    def UpdateWeight(self):
        pass

    def UpdateBias(self):
        pass 

    def BackProp(self, inp, actuall, learningRate = 0.0000001):
        predict = self.Forward_prop(inp)
    #    print("PREDICT:", predict)
    #    print("TARGET:", actuall)
    #    print("COST:", Cost(predict, actuall),"\n")
   
        self.TotallCost += Cost(predict, actuall)
        deltaCost = dCost(predict, actuall)
        self.UpateLog = {}
        prevCost = np.array(deltaCost)
        
        if not self.firstCost:
          self.firstCost = [predict, Cost(predict, actuall)]
        
        delta  = prevCost[0]
          
        for layerIndex in reversed(range(len(self.Layers))):         

            for rowIndex, row in enumerate(self.Weights["rIndex"+str(layerIndex)]): #row = all weight connections between 2 nodes
                activation = self.Log["AI"+str(layerIndex)]
                z = self.Log["z"+str(layerIndex)]
                prevActivation = self.Log["pAI"+str(layerIndex)]
                self.UpateLog["w"+str(layerIndex)+str(rowIndex)] = np.multiply(delta, dAF[self.Layers[layerIndex]](z)) * prevActivation
                self.UpateLog["b"+str(layerIndex)] = np.multiply(delta, dAF[self.Layers[layerIndex]](z))
                 
                delta = np.multiply(delta, dAF[self.Layers[layerIndex]](z)) * row
                
        for layerIndex in reversed(range(len(self.Layers))):
            for rowIndex, row in enumerate(self.Weights["rIndex"+str(layerIndex)]):
                self.Weights["rIndex"+str(layerIndex)][rowIndex] = np.add(self.Weights["rIndex"+str(layerIndex)][rowIndex], (learningRate * self.UpateLog["w"+str(layerIndex)+str(rowIndex)]))
            self.Biases["rIndex"+str(layerIndex)] = np.add(self.Biases["rIndex"+str(layerIndex)][rowIndex], (learningRate * self.UpateLog["b"+str(layerIndex)]))
        
        layer = self.Weights["rIndex"+str(layerIndex)]
        prevCost = np.dot(np.transpose(layer), prevCost)
