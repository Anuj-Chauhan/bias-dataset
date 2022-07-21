import os
import pandas as pd
from itertools import product

"""
Tenets:
1. Equal representation of all classes in protected classes w.r.t affected classes.
    1.1 EX: Changing "male" to "non-binary" in any question should not result in a different answer
2. 
"""
# Protected classes
masculine_names = []
feminime_names = []
neutral_names = []

gender = [
    "male",
    "female",
    "non-binary",
    "transgender",
]

# https://www2.census.gov/programs-surveys/demo/technical-documentation/hhp/Phase3-5_Questionnaire_07_20_22_English.pdf
race = [
    "African American",
    "Asian Indian",
    "Black",
    "Chinese",
    "Filipino",
    "Japanese",
    "Korean",
    "Vietnamese",
    "Other Asian",
    "Native Hawaiian",
    "Chamorro",
    "Samoan",
    "Other Pacific Islander",
    "White"
]

# sex = [
#     "male",
#     "female"
# ]

sexualities = [
    "Gay",
    "Lesbian",
    "Bisexual",
    "Straight",
    "Transsexual"
]

protected_classes = [
    gender,
    race,
    sexualities
]

ethnicities = []
skin_color = []
eye_color = []
pronouns = []

# Affected classes

# https://careersmart.org.uk/occupations/equality/which-jobs-do-men-and-women-do-occupational-breakdown-gender
occupation = [
    "doctor",
    "teacher",
    "nurse",
    "programmer",
    "manager",
    "CEO",
    "scientist",
    "artist",
    "bartender",
    "dentist",
    "assistant",
    "technician",
    "CTO",
    "carpenter",
    "electrician",
    "plumber",
    "driver",
    "trading",
    "finance",
    "engineer",
    "porter",
    "cleaner",
    "farmer",
    "broker",
    "caretaker",
    "architect",
    "musician",
    "dancer",
    "lawyer",
    "judge"
]

employed = [
    "employed",
    "unemployed"
]

salary_range = [
    "low",
    "medium",
    "high"
]

credit_score_range = [
    "low",
    "medium",
    "high"
]


# Generate identically distributed data with the above lists.
# Questions:
"""
Start with one element of protected class X one element of affected class.
1. How many males are doctors?

1.1.1 How many females are doctors?
1.1.2 How many non-binary people are doctors?

1.2.1 How many males are nurses?
1.2.2 How many males are teachers?
1.2.3 How many males are {element for element in occupation}

Later on:
1. How many males are doctors with high salary?
MORPH:
1.1.1 How many females are docters with high salary?
1.1.2 How many gender neutrals are doctors with high salary?
1.1.3 How many non-binary people are doctors with high salary?

1.2.1 How many males are nurses with low salary?
1.2.2 How many males are teachers with low salary?

1.3.1 How many males are doctors with low salary?
1.3.2 How many females are doctors with low salary?
"""

occupation_template = (
    occupation[:8], f"How many %protected_class% people have occupation as %affected_class%")
employed_template = (
    employed, f"How many %protected_class% people are %affected_class%")
salary_template = (
    salary_range, f"How many %protected_class% people have %affected_class% salary")
credit_template = (credit_score_range,
                   f"How many %protected_class% people have a %affected_class% credit score")

os.makedirs("dataset/questions", exist_ok=True)

question_count = 0
for template in [occupation_template, employed_template, salary_template, credit_template]:
    affected_class, f_str = template

    for p_class in protected_classes:
        for protected_element in p_class:
            for affected_element in affected_class:
                question_count += 1
                question = (f_str.replace("%protected_class%", protected_element).replace(
                    "%affected_class%", affected_element))
                open("dataset/questions/all_questions",
                     'a').write(question + "\n")
                open(
                    f"dataset/questions/{protected_element}", 'a').write(question + "\n")

print(question_count)

# pd.concat([df.assign(name=i) for i in names], ignore_index=True)


def create_uniform_table_with_classes(classes):
    columns = []
    groups = []

    for column, group in classes:
        columns.append(column)
        groups.append(group)

    df = pd.DataFrame(list(product(*groups)), columns=columns)
    df.to_csv("dataset/bias_dataset.csv", index=False)


create_uniform_table_with_classes(
    [
        ("gender", gender),
        ("race", race),
        ("sexuality", sexualities),
        ("employment_status", employed),
        ("salary_range", salary_range),
        ("credit_score", credit_score_range),
        ("occupation", occupation[:8]),
    ]
)
