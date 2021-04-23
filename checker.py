import json

def checker(my_output, sample_output):
    with open(my_output) as f:
        my_results = json.load(f)
    with open(sample_output) as f:
        correct_results = json.load(f)
    result = set(my_results.keys()) == set(correct_results.keys())
    result = result and set(my_results['postingsList'].keys()) == set(correct_results['postingsList'].keys())
    #result = result and set(my_results['daatAnd'].keys()) == set(correct_results['daatAnd'].keys())
    if not result:
        return False
    for key in my_results:
        for word in my_results[key]:
            result = result and (my_results[key][word] == correct_results[key][word])
    return result

print(checker("final_out.json", "sample_output.json"))