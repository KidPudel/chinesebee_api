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
        exact_matched_dict = {records[i][:len(records[i])-1]: _map_suggestions(records[i+1]) for i in range(len(records) - 1) if word == records[i].lower()}
        #matched_dict = dict(sorted(matched_dict.items()))
        
        return {
            "status": "ok",
            "match": exact_matched_dict
        }


def _map_suggestions(value: str):
    # mN - headingN
    # refs into which you can get down
    # relevant tags: [mN] - layer, [ref] - go down
    # irrelivant: [i], [b], [c] - possibly color, [*]
    irrelivant = ["[i]", "[b]", "[c]", "[*]", "[ex]", "[/i]", "[/b]", "[/c]", "[/*]", "[/ex]"]
    for ir in irrelivant:
        value = re.sub(re.escape(ir), "", value)

 
    # define groups
    whole_suggestions = define_suggestion_groups(value=value)

    # structure groups
    
    mapped_suggestions = []
    for suggestion in whole_suggestions:
        mapped_suggestion = {}
        print(suggestion)
        level_to_remove = 0
        # attach each level
        while True:
            found_level = re.search(pattern=r"\[m.*?\[\/m\]", string=suggestion)
            
            if found_level == None:
                break
            
            
            
            if found_level != None and any([chap in re.search(r"\[m.\](.*?)\[\/m\]", found_level.group(0)).group(1) for chap in ["I", "II", "III"]]):
                print("GOT CHAPTER shit")
                level_to_remove = 1
                suggestion = re.sub(pattern=r"\[m.*?\[\/m\]", repl="", string=suggestion, count=1)
                continue
            
            level_number = int(found_level.group(0)[2:3]) - level_to_remove
            
            # if no level, or level is m1 that is for reference, which is not needed for me
            if (found_level.group(0)[4] == "-" or found_level.group(0)[4] == "•" or len(re.search(r"\[m.\](.*?)\[\/m\]", found_level.group(0)).group(1)) == 2):
                suggestion = re.sub(pattern=r"\[m.*?\[\/m\]", repl="", string=suggestion, count=1)
                continue
            
            # where group(0), is actually a match, and group(1) is actually a group (key is level tag)
            if level_number > 1 and level_number in mapped_suggestion.keys():
                mapped_suggestion[level_number].append(re.search(pattern=r"\[m.\](.*?)\[\/m\]", string=found_level.group(0)).group(1))
            elif level_number == 2 or level_number == 3:
                mapped_suggestion[level_number] = [re.search(pattern=r"\[m.\](.*?)\[\/m\]", string=found_level.group(0)).group(1)]
            else:
                mapped_suggestion[level_number] = re.search(pattern=r"\[m.\](.*?)\[\/m\]", string=found_level.group(0)).group(1)
            suggestion = re.sub(pattern=r"\[m.*?\[\/m\]", repl="", string=suggestion, count=1)
        if mapped_suggestion:
            mapped_suggestions.append(mapped_suggestion)

    return mapped_suggestions


def define_suggestion_groups(value: str) -> list[str]:
    """define dictionary suggestions into groups"""

    whole_suggestions = re.findall(r"(\[m1\].*?(?=\[m1\]))", value)
    for suggestion in whole_suggestions:
        value = re.sub(re.escape(suggestion), "", value)
    last_suggestion = re.findall(r"\[m1\].*", value)[0]
    
    whole_suggestions.append(last_suggestion)
    
    # possible recursion here
    return whole_suggestions