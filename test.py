import json
from redis import StrictRedis

r = StrictRedis()


class Student(object):
    def __init__(self, name):
        self.name = name
        self.courses = {}

    def add_course(self, name, score):
        self.courses[name] = score


bob = Student('Bob')
bob.add_course('Mathematics', 80)
bob.add_course('Chemistry', 95)
jeff = Student('Jeff')
jeff.add_course('Mathematics', 75)
jeff.add_course('Chemistry', 99)

r.mset(
    'user:1', json.dumps(bob),
    'user:2', json.dumps(jeff),
)

lua = '''
    local sum = 0
    local users = redis.call('mget', unpack(KEYS))
    for _, user in ipairs(users) do
        local courses = cjson.decode(user).courses
        for _, score in pairs(courses) do
            sum = sum + score
        end
    end
    return sum
'''

scores_sum = r.register_script(lua)
print(scores_sum(keys=[bob, jeff]))
