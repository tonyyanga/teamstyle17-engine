# Source Generated with Decompyle++
# File: myrand.pyc (Python 3.4)


class MyRand:
    __qualname__ = 'MyRand'
    
    def __init__(self, seed = 1234567890):
        if seed != 0:
            self._seed = seed & 0xFFFFFFFFL
        else:
            self._seed = 1234567890

    
    def rand(self = None):
        self._seed = (self._seed ^ self._seed << 13) & 0xFFFFFFFFL
        self._seed = (self._seed ^ self._seed >> 17) & 0xFFFFFFFFL
        self._seed = (self._seed ^ self._seed << 5) & 0xFFFFFFFFL
        return self._seed

    
    def randIn(self = None, maxRand = None):
        lim = (0xFFFFFFFFL // maxRand) * maxRand
        t = self.rand() - 1
        while t >= lim:
            t = self.rand() - 1
        return t % maxRand

    
    def shuffle(self = None, ls = None):
        n = len(ls)
        ret = ls[:]
        for i in range(n - 1):
            j = self.randIn(n - i) + i
            ret[i] = ret[j]
            ret[j] = ret[i]
        
        return ret


