import attr
import typing
import structures as S

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
  course_level   = attr.ib(type=int)
  required_level = attr.ib(type=int)

@attr.s
class SequenceConstraint (Constraint):
  sequence = attr.ib(type=typing.List[S.Course])

@attr.s
class OneOfConstraint (Constraint):
  course_set = attr.ib(type=typing.List[S.Course])

@attr.s
class AnyOfConstraint (Constraint):
  course_set = attr.ib(type=typing.List[S.Course])

@attr.s
class LimitOfConstraint (Constraint):
  count = attr.ib(type=int)
  course_set = attr.ib(type=typing.List[S.Course])

# Returns a boolean
def interp(constraint, course_set, desired_course):
  # NoCourseLevelConstraint
  if isinstance(constraint, NoCourseLevelConstraint):
    return (desired_course.level == constraint.course_level)
  # HasCourseLevelConstraint
  elif isinstance(constraint, HasCourseLevelConstraint):
    meets_constraint = False
    if desired_course.level == constraint.course_level:
      for c in course_set:
        if c.level == constraint.required_level:
          meets_constraint = True
    return meets_constraint
  # SequenceConstraint
  elif isinstance(constraint, SequenceConstraint):
    all_in = True
    for constc in constraint.sequence:
      constr_in_set = False
      for setc in course_set:
        if constc.get_id() == setc.get_id():
          constr_in_set = True
      all_in = all_in and constr_in_set
    return all_in
  elif isinstance(constraint, OneOfConstraint):
    member = False
    for c in course_set:
      for cc in constraint.course_set:
        if c.get_id() ==  cc.get_id():
          member = True
    return member

  else:
    # If I find no reason to limit enrollment, then
    # it's OK based on the constraints.
    return True