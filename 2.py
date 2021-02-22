from itertools import chain, combinations
from collections import defaultdict
import matplotlib.pyplot as plt


def getItemSetAndTransList(fname):
    transactionList = list()
    itemSet = set()
    with open(fname) as file_iter:
        for line in file_iter:
            line = line.strip()
            transaction = frozenset(line.split(" "))
            transactionList.append(transaction)
            for item in transaction:
                itemSet.add(frozenset([item])) 
    return itemSet, transactionList


def returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet):
    _itemSet = set()
    localSet = defaultdict(int)

    for item in itemSet:
        for transaction in transactionList:
            if item.issubset(transaction):
                freqSet[item] += 1
                localSet[item] += 1

    for item, count in localSet.items():
        support = float(count) / len(transactionList)

        if support >= minSupport:
            _itemSet.add(item)

    return _itemSet


def joinSet(itemSet, length):
    return set(
        [i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length]
    )


def getCombinations(set):
    """ все комбинации которые можем составить в наборе"""
    return chain(*[combinations(set, index + 1) for index, element in enumerate(set)])


def apriori(minSupport, minConfidence, itemSet, transactionList):

    freqSet = defaultdict(int)
    largeSet = dict()

    minSupItemsSet = returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet)

    n = 2
    currentNSet = minSupItemsSet
    while currentNSet != set([]):
        largeSet[n-1] = currentNSet
        currentNSet = joinSet(currentNSet, n)
        curMinSupItemsSet = returnItemsWithMinSupport(
            currentNSet, transactionList, minSupport, freqSet
        )
        currentNSet = curMinSupItemsSet
        n = n + 1

    def getSupport(item):
        return float(freqSet[item]) / len(transactionList)

    resultItems = []
    for key, value in largeSet.items():
        resultItems.extend([(tuple(item), getSupport(item)) for item in value])

    resultRules = []
    for key, value in largeSet.items():
        if(key > 1):
            for item in value:
                combinationSets = map(frozenset, [allCombInSet for allCombInSet in getCombinations(item)])
                for oneCombination in combinationSets:
                    remain = item.difference(oneCombination)
                    if len(remain) > 0:
                        confidence = float(freqSet[item])/float(freqSet[oneCombination])
                        if confidence >= minConfidence:
                            resultRules.append(((tuple(oneCombination), tuple(remain)), confidence))
    return resultItems, resultRules


def printResults(rules):
    """prints the generated itemsets sorted by support and the confidence rules sorted by confidence"""

    for rule, confidence in sorted(rules, key=lambda x: x[1]):
        pre, post = rule
        print("Rule: %s ==> %s , %.3f" % (str(pre), str(post), confidence))
    print(f"Rules count: {len(rules)}")
    return len(rules)




if __name__ == "__main__":

    support = 0.7
    itemSet, transactionList = getItemSetAndTransList("accidents.dat")
    confidences = [0.70, 0.75, 0.8, 0.85, 0.9, 0.95]
    items, rules = apriori(support, min(confidences), itemSet, transactionList)

    rulesCount = list()


    for confidence in confidences:
        print("=================================")
        print(f"\t Confidence = {confidence*100}%")
        rulesSortFilter = filter(lambda x: x[1]>=confidence, sorted(rules, key=lambda x: x[1]))
        rulesCount.append(printResults(list(rulesSortFilter)))
        print("=================================\n")


    print(rulesCount)
    fig, ax = plt.subplots()
    ax.plot(confidences, rulesCount, color = 'r', linewidth = 3)
    ax.grid(which='major',
            color = 'k')
    ax.minorticks_on()
    ax.grid(which='minor',
            color = 'gray',
            linestyle = ':')
    plt.show()

