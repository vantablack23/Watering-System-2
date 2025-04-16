import json

f=open("plans/plan1.json")
plans=json.load(f)

print(plans["plans"])