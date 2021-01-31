from pyshpe.shpe import replace_with_array, PrimitiveTask
from dataclasses import dataclass


def test_replace_with_array():
    assert replace_with_array([1, 2, 3, 4], 2, [8, 9]) == [1, 2, 8, 9, 4]


def test_binding_parameters():
    @dataclass
    class Task1(PrimitiveTask):
        a: int
        b: int
        c: str

        def test(self):
            return str(self.a + self.b) + self.c

    @dataclass
    class Task2(PrimitiveTask):
        loc: str

        def test(self):
            return self.loc + str(4)

    t11 = Task1(5, 3, 'cat')
    t12 = Task1(1, 2, 'orange')
    t2 = Task2('yavin')

    assert (5, 3, 'cat') == (t11.a, t11.b, t11.c)
    assert (1, 2, 'orange') == (t12.a, t12.b, t12.c)
    assert 'yavin' == t2.loc

    assert '8cat' == t11.test()
    assert '3orange' == t12.test()
    assert 'yavin4' == t2.test()
