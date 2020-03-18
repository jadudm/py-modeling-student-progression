import attr
import typing
import course as CO

@attr.s
class Constraint (object):
  """A base class for course enrollment constraints."""
  def check(self, course_set, desired_course):
    """Self-check constraints given a set of courses and a desired course.
    
    :param course_set: A list of Course objects that the student has previously taken.
    :param desired_course: A Course object that represents the course a student wants to take.
    """
    pass

@attr.s
class NoCourseLevelConstraint (Constraint):
  """Courses at a given level have no constraints. 
  E.g. 100-level courses can always be taken.
  
  Returns false if the desired course is not of the same level."""
  course_level = attr.ib(type=int)
  def check(constraint, course_set, desired_course):
    return (desired_course.level == constraint.course_level)

@attr.s
class HasCourseLevelConstraint (Constraint):
  """Checks whether a student has taken a course in the past at the given level. For example,
  to take a 200-level course, a student may need to have taken (any) 100-level course."""
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
  """To take the desired course, students must have taken all of the courses
  in the sequence prior."""
  target   = attr.ib(type=CO.Course)
  sequence = attr.ib(type=typing.List[CO.Course])
  def check(constraint, course_set, desired_course):
    all_in = False
    if constraint.target.get_id() == desired_course.get_id():
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
  """To take a target course, a student must have taken 
  at least one of the courses in the constraint sequence."""
  target = attr.ib(type=CO.Course)
  course_set = attr.ib(type=typing.List[CO.Course])
  def check(constraint, course_set, desired_course):
    if constraint.target.get_id() == desired_course.get_id():   
      return member_counter(constraint, course_set) == 1
    else:
      return False

@attr.s
class AnyOfConstraint (Constraint):
  """To take the target course, students must have taken any 
  of the courses in the constraint sequence.""" 
  target = attr.ib(type=CO.Course)
  course_set = attr.ib(type=typing.List[CO.Course])
  def check(constraint, course_set, desired_course):
    if constraint.target.get_id() == desired_course.get_id():
      if not constraint.course_set:
        return True
      else:
        return member_counter(constraint, course_set) > 0
    else:
      return False

@attr.s
class AndConstraint (Constraint):
  """Both constraints must be true."""
  lhs = attr.ib(type=Constraint)
  rhs = attr.ib(type=Constraint)
  def check(constraint, cs, desired):
    return constraint.lhs.check(cs, desired) and constraint.rhs.check(cs, desired)

@attr.s
class OrMapConstraint (Constraint):
  """At least one of the constraints in the constraints array must be true."""
  constraints = attr.ib(type=typing.List[Constraint])
  def check (constraint, cs, desired):
    result = False
    for c in constraint.constraints:
      result = result or c.check(cs, desired)
    return result

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
