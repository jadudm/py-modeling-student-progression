import attr
import typing 
import constraints as C
import requirements as R
import course as CO

@attr.s
class Student (object):
  name = attr.ib(type=str)

@attr.s
class Offering (object):
  level = attr.ib(type=int)
  rubric = attr.ib(type=str, default="CS")
  seats = attr.ib(type=int, default=24)
  students = attr.ib(default=dict())
  def has_space(self):
    return self.seats > 0
  def enroll (self, s):
    self.students[self.seats] = s
    self.seats = self.seats - 1


@attr.s
class Term (object):
  offerings = attr.ib(type=typing.List[Offering])

@attr.s
class World (object):
  students = attr.ib(type=typing.List[Student])
  terms    = attr.ib(type=typing.List[Term])
  constraints = attr.ib(type=typing.List[C.Constraint])
  requirements = attr.ib(type=typing.List[R.Requirement])
