from collections import defaultdict
import matplotlib.pyplot as plt

def getItemSetAndTransList(fname):
    transactionList = list()
    itemSet = set()
    with open(fname) as rows:
        for row in rows:
            row = row.strip()
            transaction = frozenset(row.split(" "))
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
    """Join a set with itself and returns the n-element itemsets"""
    return set(
        [i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length]
    )


def apriori(minSupport, itemSet, transactionList):

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

    return resultItems


def printResults(items):
    for item, support in sorted(items, key=lambda x: x[1]):
        print("item: %s, %.2f%s" % (str(item).replace(",)", ")"), support*100, "%"))
    return len(items)


if __name__ == "__main__":

    supports = [0.01, 0.03, 0.05, 0.1, 0.15, 0.2]
    itemSet, transactionList = getItemSetAndTransList("retail.dat")

    items = apriori(min(supports), itemSet, transactionList)
    itemsCount = list()

    for support in supports:
        print("=================================")
        print(f"\t Support = {support*100}%")
        itemsFilter = filter(lambda x: x[1]>=support, items)
        itemsCount.append(printResults(list(itemsFilter)))
        print("=================================\n")

    fig, ax = plt.subplots()
    ax.plot(supports, itemsCount, color = 'r', linewidth = 3)
    ax.grid(which='major',
            color = 'k')
    ax.minorticks_on()
    ax.grid(which='minor',
            color = 'gray',
            linestyle = ':')
    plt.show()