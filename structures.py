import attr

@attr.s
class Course (object):
  level = attr.ib(type=int)
  
