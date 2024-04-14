# get data from chinese dictionary from word

import os
import re

# MARK: test
def get_chinese_match(word: str):
    bruks_path = os.path.realpath(os.path.join(os.getcwd(), "dabruks_240408"))
    with open(bruks_path) as bruks:
        # records
        records = list(bruks)
        # find a word (filter), that is matches with records
        exact_matched_dict = {records[i][:len(records[i])-1]: _map_suggestions(records[i+1]) for i in range(len(records) - 1) if word == records[i]}
        #matched_dict = dict(sorted(matched_dict.items()))
        
        return {
            "status": "ok",
            "matches": exact_matched_dict
        }


def _map_suggestions(value: str):
    # mN - headingN
    # refs into which you can get down
    # relevant tags: [mN] - layer, [ref] - go down
    # irrelivant: [i], [b], [c] - possibly color, [*]
    irrelivant = ["[i]", "[b]", "[c]", "[*]", "[ex]", "[i]", "[/b]", "[/c]", "[/*]", "[/ex]"]
    for ir in irrelivant:
        value = re.sub(re.escape(ir), "", value)

 
    # define groups
    whole_suggestions = define_suggestion_groups(value=value)

    # structure groups
    
    mapped_suggestions = []
    for suggestion in whole_suggestions:
        mapped_suggestion = {}
        # attach each level
        while True:
            found_level = re.search(pattern=r"\[m.*?\[\/m\]", string=suggestion)
            if found_level == None:
                break
            # where group(0), is actually a match, and group(1) is actually a group
            mapped_suggestion[found_level.group(0)[:4]] = re.search(pattern=r"\[m.\](.*?)\[\/m\]", string=found_level.group(0)).group(1)
            suggestion = re.sub(pattern=r"\[m.*?\[\/m\]", repl="", string=suggestion, count=1)
        mapped_suggestions.append(mapped_suggestion)

    return mapped_suggestions


def define_suggestion_groups(value: str) -> list[str]:
    """define dictionary suggestions into groups"""

    whole_suggestions = re.findall("(\[m1\].*?(?=\[m1\]))", value)
    for suggestion in whole_suggestions:
        value = re.sub(re.escape(suggestion), "", value)
    last_suggestion = re.findall("\[m1\].*", value)[0]
    whole_suggestions.append(last_suggestion)
    
    # possible recursion here
    return whole_suggestions