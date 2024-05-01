import gensim.models.doc2vec as doc
import os
import graphUtils_n
import random


def arr2str(arr):
    result = ""
    for i in arr:
        result += " "+str(i)
    return result
    

def generateWalkFile(dirName, walkLength):
    walkFile = open(dirName+'.walk', 'w')
    indexToName = {}
    
    for  root, dirs, files in os.walk(dirName):
        index = 0
        for name in files:
            if index %100 == 0:
                print(name)
            subgraph = graphUtils_n.getGraph(os.path.join(root, name))
            # print(subgraph)
            # print(random.choice(list(subgraph.nodes())))
            walk = graphUtils_n.randomWalk(subgraph, walkLength)
            walkFile.write(arr2str(walk) +"\n")
            indexToName[index] = name
            index += 1
    walkFile.close()
    
    return indexToName
    
def saveVectors(vectors, outputfile, IdToName):
    output = open(outputfile, 'w')
    
    output.write(str(len(vectors)) +"\n")
    for i in range(len(vectors)):
        output.write(str(IdToName[i]))
        for j in vectors[i]:
            output.write('\t'+ str(j))
        output.write('\n')
    output.close()
    
    
def neighborhood_embedding(args):
    inputDir = args.input
    outputFile = args.output
    iterations = args.iter
    dimensions = args.d
    window = args.windowSize
    dm = 1 if args.model == 'dm' else 0
    if not os.path.isfile(inputDir+'.walk'):
        indexToName = generateWalkFile(inputDir, args.walkLength, args.p)
    else:
        print(".walk file already exist")
        indexToName = {}
        for root, dirs, files in os.walk(inputDir):
            index = 0
            for name in files:
                indexToName[index] = name
                index += 1
    sentences = doc.TaggedLineDocument(inputDir+'.walk')
    print("finish generate sentences")
    model = doc.Doc2Vec(sentences, vector_size = dimensions, epochs = iterations, dm = dm, window = window )
    
    saveVectors(list(model.dv.vectors), outputFile, indexToName)
    
    
    
    
    

    