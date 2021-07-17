from bitset import Bitset

def test_simple():
    a = Bitset()
    a.set(100)
    assert not a.get(0)
    assert not a.get(99)
    assert not a.get(101)
    assert a.get(100)
    a.clear(100)
    assert not a.get(100)

def test_equality():
    a = Bitset()
    a.set(17)
    a.set(63)
    a.set(100)
    a.set(1000)

    b = Bitset()
    b.set(17)
    b.set(63)
    b.set(100)
    b.set(1000)

    assert a == b

    a.set(23)
    assert a != b

    a.clear(23)
    assert a == b

    a.set(2000)
    assert a != b

    b.set(2000)
    assert a == b

def test_use_in_sets():
    thing = set()

    a = Bitset()
    a.set(16)
    thing.add(a)

    b = Bitset()
    assert not b in thing

    b.set(16)
    assert b in thing