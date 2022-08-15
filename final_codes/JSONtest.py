import json

with open('final_codes/JSON files/svt.JSON','r') as f:
    data = json.load(f)

print((data["paths"]["svt_dec"]))
