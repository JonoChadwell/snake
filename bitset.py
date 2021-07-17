import itertools

class Bitset:
    def __init__(self):
        self.data = []
        self.bits_each = 64

    def __eq__(self, obj):
        if not isinstance(obj, Bitset):
            return False
        if self.bits_each != obj.bits_each:
            return False
        for pair in itertools.zip_longest(self.data, obj.data, fillvalue=0):
            if pair[0] != pair[1]:
                return False
        return True

    def __hash__(self):
        return hash(' '.join([str(x) for x in self.data]))

    def get(self, idx):
        superidx = idx // self.bits_each
        subidx = idx % self.bits_each
        if len(self.data) < superidx:
            return False
        return self.data[superidx] & (1 << subidx) > 0

    def set(self, idx):
        superidx = idx // self.bits_each
        subidx = idx % self.bits_each
        while len(self.data) <= superidx:
            self.data.append(0)
        self.data[superidx] |= (1 << subidx)

    def clear(self, idx):
        if not self.get(idx):
            return
        superidx = idx // self.bits_each
        subidx = idx % self.bits_each
        self.data[superidx] -= (1 << subidx)