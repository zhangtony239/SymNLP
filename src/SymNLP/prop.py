from typing import Literal

class MockObj:
    def __init__(self, name:str):
        self.name = name
    
    def __str__(self):
        return self.name

class Proposition:
    def __init__(self, s:object, v:object, o:object, value:bool|Literal[1,0]):
        self.s = s
        self.v = v
        self.o = o
        self.value = bool(value)
    
    @property
    def key(self):
        return f"{self.s}{self.v}{self.o}"

@staticmethod
def SVO(s1:MockObj, v1:MockObj, o1:MockObj, s2:MockObj, v2:MockObj, o2:MockObj): #后期换成对应的oop
    if s1.name == s2.name:
        s = s1
    else:
        s = f'{s1.name}{s2.name}'
    if v1.name == v2.name:
        v = v1
    else:
        raise ValueError("不同类动作不可运算！")
    if o1.name == o2.name:
        o = o1
    else:
        o = f'{o1.name}{o2.name}'
    return s,v,o

@staticmethod
def Imply(From:Proposition,To:Proposition):
    s,v,o = SVO(From.s,From.v,From.o,To.s,To.v,To.o)
    if From.value and not To.value:
        value = 0
    else:
        value = 1
    return Proposition(s,v,o,value)

@staticmethod
def And(p:Proposition,q:Proposition):
    s,v,o = SVO(p.s,p.v,p.o,q.s,q.v,q.o)
    return Proposition(s,v,o,p.value and q.value)

if __name__ == "__main__":
    from SymNLP.prop import Proposition as Prop
    p = Prop(MockObj('4'),MockObj('是'),MockObj('素数'),0)
    #q = Prop(MockObj('小红'),MockObj('唱'),MockObj('歌'),1)
    q = Prop(MockObj('3'),MockObj('是'),MockObj('素数'),1)
    for i in p,q:
        print(i.key)
    print(Imply(p,q).value)