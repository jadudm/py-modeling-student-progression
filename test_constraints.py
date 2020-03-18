import constraints as C
import structures as S
import pytest

# 100 level courses have no constraints.
# A desired 100-level course should pass.
def test_nclc1():
  nclc = C.NoCourseLevelConstraint(100)
  cs = []
  desired = S.Course(level=100)
  result = C.interp(nclc, cs, desired)
  assert(result)

# A 200-level course will not pass a NCL Constraint
def test_nclc2():
  nclc = C.NoCourseLevelConstraint(100)
  cs = []
  desired = S.Course(level=200)
  result = C.interp(nclc, cs, desired)
  assert(not result)

# A 200-level course has a 100-level constraint.
# With no prior classes, this fails.
def test_hclc1():
  hclc = C.HasCourseLevelConstraint(200, 100)
  cs = []
  desired = S.Course(level=200)
  result = C.interp(hclc, cs, desired)
  assert(not result)

# A 200-level will pass if a student
# has a 100-level course. 
def test_hclc2():
  hclc = C.HasCourseLevelConstraint(200, 100)
  cs = [S.Course(level=100)]
  desired = S.Course(level=200)
  result = C.interp(hclc, cs, desired)
  assert(result)

# A 200-level will pass if a student
# has a 100-level course. 
def test_hclc3():
  hclc = C.HasCourseLevelConstraint(200, 100)
  cs = [S.Course(level=200), S.Course(level=100)]
  desired = S.Course(level=200)
  result = C.interp(hclc, cs, desired)
  assert(result)

# Do I have a sequence of required courses?
def test_seq1():
  seqc = C.SequenceConstraint([S.Course(level=100)])
  cs = []
  desired = S.Course(level=200)
  result = C.interp(seqc, cs, desired)
  assert(not result)

# If I do have a one-course sequence requirement
def test_seq2():
  seqc = C.SequenceConstraint([S.Course(level=100)])
  cs = [S.Course(level=100)]
  desired = S.Course(level=200)
  result = C.interp(seqc, cs, desired)
  assert(result)

# But I don't have two...
def test_seq3():
  seqc = C.SequenceConstraint([S.Course(level=100), S.Course(level=200)])
  cs = [S.Course(level=100)]
  desired = S.Course(level=200)
  result = C.interp(seqc, cs, desired)
  assert(not result)

# But I do have both courses!
def test_seq4():
  seqc = C.SequenceConstraint([S.Course(level=100), S.Course(level=200)])
  cs = [S.Course(level=100), S.Course(level=200)]
  desired = S.Course(level=200)
  result = C.interp(seqc, cs, desired)
  assert(result)

# Testing subtlety of rubric...
# I need a CS and LIT course, but I have two CS courses...
# The previous tests used the default rubric. However,
# The check uses .get_id(), so it builds an ID from the 
# rubric and the level.
def test_seq5():
  seqc = C.SequenceConstraint([S.Course(level=100, rubric="CS"), 
                               S.Course(level=200, rubric="LIT")])
  cs = [S.Course(level=100, rubric="CS"), 
        S.Course(level=200, rubric="CS")]
  desired = S.Course(level=200)
  result = C.interp(seqc, cs, desired)
  assert(not result)

# I like table testing. I should do that here.

# OneOfConstraint
# Make sure that the course set contains at least
# one of the courses listed in the constraint.
a_100 = S.Course(level=100)
a_200 = S.Course(level=200)
a_300 = S.Course(level=300)
oocdata = [
  # The desired course doesn't matter for these.
  ([a_100], [], None, False),
  ([a_100], [a_100], None, True),
  ([a_100, a_200], [a_100], None, True),
  ([a_100, a_200], [a_300], None, False)
]

@pytest.mark.parametrize("const,cs,desired,expected", oocdata)
def test_ooc(const, cs, desired, expected):
  ooc = C.OneOfConstraint(const)
  result = C.interp(ooc, cs, desired)
  assert(result == expected)

