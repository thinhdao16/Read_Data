import os
import json

def load_result_json():
    base_path = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_path, '..', 'data', 'result.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data