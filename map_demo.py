
li1 = [1, 2, 3, 4]
li2 = [2, 3]


def add(num1, num2):
    return num1 + num2


class mymap(map):

    def __str__(self):
        _str = "[%s]" % ",".join([str(x) for x in self])

        return _str


ret = mymap(add, li1, li2)
print(ret)
# for r in ret:
#     print(r)

