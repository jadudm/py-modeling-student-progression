import attr
import typing

# Constraints are essentially a language.
# However, Python does not have a way to implement
# languages *per se*, so I'll use structures
# as a way to express an AST. Ultimately, I can add
# a parser on the front-end to generate these structures.

@attr.s
class Constraint (object):
  pass

@attr.s
class NoCourseLevelConstraint (Constraint):
  course_level = attr.ib(type=int)

@attr.s
class HasCourseLevelConstraint (Constraint):
  course_level = attr.ib(type=int)
  requires     = attr.ib(type=int)

@attr.s
class SequenceConstraint (Constraint):
  sequence = attr.ib(type=typing.List[str])

@attr.s
class OneOfConstraint (Constraint):
  course = attr.ib(type=str)
  course_set = attr.ib(type=typing.List[str])

@attr.s
class AnyOfConstraint (Constraint):
  course = attr.ib(type=str)
  course_set = attr.ib(type=typing.List[str])

@attr.s
class LimitOfConstraint (Constraint):
  count = attr.ib(type=int)
  course_set = attr.ib(type=typing.List[str])
  