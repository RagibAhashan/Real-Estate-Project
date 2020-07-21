def isLastPage(currentPage):
    x = currentPage
    current = x[:(x.find('/')-1)]
    last = x[(x.find('/'))+2 : len(x)]
    return current == last