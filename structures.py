import attr

@attr.s
class Course (object):
  level  = attr.ib(type=int, default=100)
  rubric = attr.ib(type=str, default="CS")
  id     = attr.ib(type=str, default="_")

  def get_id(self):
    return "{}{}".format(self.rubric, self.level)
  def get_name(self):
    return "{}{}{}".format(self.rubric, self.level, self.id)
