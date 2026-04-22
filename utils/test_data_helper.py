import os
import random

folder_path = "/Users/kunalsikka/Downloads/Test_Images/"

def get_random_subject():
    subjects = ["Bug", "Feedback", "Query"]
    return random.choice(subjects)

def get_random_message():
    messages = ["This is a test message",
        "Automation testing message",
        "Please check this issue",
        "Random QA message"]
    return random.choice(messages)

def get_random_file(folder_path = "/Users/kunalsikka/Downloads/Test_Images/"):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    random_file = random.choice(files)
    return os.path.join(folder_path, random_file)

def search_for_a_product():
    search_suggestions = ["t-shirt", "tshirt", "blue-pant", "sleevel", "random", "noPRODuct"]
    return random.choice(search_suggestions)

def get_test_emails():
    return [
        "",                     # empty case
        "invalidemail",         # no @
        "test@com",             # invalid format
        "user123@gmail.com"     # valid
    ]
def get_random_quantity(min_val=1, max_val=5):
    return random.randint(min_val, max_val)

def get_random_test_case(data_list):
    return random.choice(data_list)