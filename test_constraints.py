import constraints as C
import structures as S

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