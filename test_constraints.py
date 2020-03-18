import constraints as C
from collections import namedtuple as NT
import structures as S
import pytest

a_100 = S.Course(level=100)
a_200 = S.Course(level=200)
a_300 = S.Course(level=300)
a_400 = S.Course(level=400)

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
ST = NT('ST', ['target', 'sequence', 'cs', 'desired', 'expected'])
seqdata = [
  ST(a_100, [], [], a_100, True),
  ST(a_200, [a_100], [], a_200, False),
  ST(a_200, [a_100], [a_100], a_200, True),
  ST(a_300, [a_100, a_200], [a_100], a_300, False),
  ST(a_300, [a_100, a_200], [a_100, a_200], a_300, True),
  ST(a_200, [S.Course(level=100, rubric="CS"), S.Course(level=200, rubric="LIT")], [a_100, a_200], a_200, False),
]

@pytest.mark.parametrize("st", seqdata)
def test_seq(st):  
  seqc = C.SequenceConstraint(st.target, st.sequence)
  result = C.interp(seqc, st.cs, st.desired)
  assert(result == st.expected)

# OneOfConstraint
# Make sure that the course set contains at least
# one of the courses listed in the constraint.

SC = NT('OC', ['target', 'sequence', 'cs', 'desired', 'expected'])
oocdata = [
  SC(a_100, [], [], a_100, False),
  SC(a_200, [a_100], [], a_200, False),
  SC(a_200, [a_100], [a_100], a_200, True),
  SC(a_300, [a_100, a_200], [a_100], a_300, True),
  SC(a_300, [a_100, a_200], [a_200], a_300, True),
  SC(a_300, [a_100, a_200], [a_400], a_300, False),
  SC(a_300, [a_100, a_200], [a_300], a_300, False),
  # Can only have one of the courses in the constraint set.
  SC(a_300, [a_100, a_200], [a_100, a_200], a_300, False) 
]

@pytest.mark.parametrize("st", oocdata)
def test_ooc(st):
  c = C.OneOfConstraint(st.target, st.sequence)
  result = C.interp(c, st.cs, st.desired)
  assert(result == st.expected)

aocdata = [
  SC(a_100, [], [], a_100, True),
  SC(a_200, [a_100], [], a_200, False),
  SC(a_200, [a_100, a_200], [a_100], a_200, True),
  SC(a_300, [a_100, a_200], [a_100], a_300, True),
  SC(a_400, [a_200, a_300], [a_100], a_400, False),
  SC(a_400, [a_200, a_300], [a_200], a_400, True),
  SC(a_300, [a_100, a_200], [a_100, a_200], a_300, True)
]

@pytest.mark.parametrize("st", aocdata)
def test_aoc(st):
  c = C.AnyOfConstraint(st.target, st.sequence)
  result = C.interp(c, st.cs, st.desired)
  assert(result == st.expected)
