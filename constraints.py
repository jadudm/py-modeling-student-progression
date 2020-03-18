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
  def check(self, course_set, desired_course):
    pass

@attr.s
class NoCourseLevelConstraint (Constraint):
  course_level = attr.ib(type=int)
  def check(constraint, course_set, desired_course):
    return (desired_course.level == constraint.course_level)

@attr.s
class HasCourseLevelConstraint (Constraint):
  course_level   = attr.ib(type=int)
  required_level = attr.ib(type=int)
  def check(constraint, course_set, desired_course):
    meets_constraint = False
    if desired_course.level == constraint.course_level:
      for c in course_set:
        if c.level == constraint.required_level:
          meets_constraint = True
    return meets_constraint

@attr.s
class SequenceConstraint (Constraint):
  sequence = attr.ib(type=typing.List[S.Course])
  def check(constraint, course_set, desired_course):
    all_in = True
    for constc in constraint.sequence:
      constr_in_set = False
      for setc in course_set:
        if constc.get_id() == setc.get_id():
          constr_in_set = True
      all_in = all_in and constr_in_set
    return all_in

def member_counter(constraint, course_set):
  member = 0
  for c in course_set:
    for cc in constraint.course_set:
      if c.get_id() ==  cc.get_id():
        member = member + 1
  return member
    
@attr.s
class OneOfConstraint (Constraint):
  course_set = attr.ib(type=typing.List[S.Course])
  def check(constraint, course_set, desired_course):
    return member_counter(constraint, course_set) == 1

@attr.s
class AnyOfConstraint (Constraint):
  course_set = attr.ib(type=typing.List[S.Course])
  def check(constraint, course_set, desired_course):
    return member_counter(constraint, course_set) > 0

@attr.s
class LimitOfConstraint (Constraint):
  count = attr.ib(type=int)
  course_set = attr.ib(type=typing.List[S.Course])
  def check(constraint, course_set, desired_course):
    members = member_counter(constraint, course_set)
    print("{} <= {}".format(members, constraint.count))
    return  members <= constraint.count

@attr.s
class AndConstraint (Constraint):
  lhs = attr.ib(type=Constraint)
  rhs = attr.ib(type=Constraint)
  def check(constraint, cs, desired):
    return constraint.lhs.check(cs, desired) and constraint.rhs.check(cs, desired)

# Returns a boolean
# Another way to do this would have been to allow
# each object to have a .check(cs, desired) method.
# Perhaps... hm. Perhaps that would have been better?
# Dunno. TMTWWTDI. This will work better, I think, if I 
# want to parse constraints in from a textual format.
#
# UPDATE: I changed it so that the objects do their own checking.
# I think this will be better for the overall app architecture.
def interp(constraint, course_set, desired_course):
  return constraint.check(course_set, desired_course)
