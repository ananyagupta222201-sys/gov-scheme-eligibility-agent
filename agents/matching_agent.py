import json

def load_schemes():
    with open("data/schemes.json", "r") as f:
        return json.load(f)

def match_schemes(profile):
    schemes = load_schemes()
    matched = []
    for scheme in schemes:
        occupation_ok = profile["occupation"] in scheme["eligibility"]["occupation"]

        income_max = scheme["eligibility"]["income_max"]
        income_ok = income_max is None or profile["income"] <= income_max

        age_min = scheme["eligibility"]["age_min"]
        age_max = scheme["eligibility"]["age_max"]
        age_ok = (age_min is None or profile["age"] >= age_min) and \
                 (age_max is None or profile["age"] <= age_max)

        state_ok = scheme["level"] == "central" or scheme["state"] == profile["state"]

        required_gender = scheme["eligibility"]["gender"]
        gender_ok = required_gender is None or required_gender == profile["gender"]

        required_category = scheme["eligibility"]["category_required"]
        user_category = profile.get("category")
        category_ok = required_category is None or user_category is None or user_category in required_category

        needs_disability = scheme["eligibility"]["disability_required"]
        has_disability = profile.get("has_disability", False)
        disability_ok = not needs_disability or has_disability

        if occupation_ok and income_ok and age_ok and state_ok and gender_ok and category_ok and disability_ok:
            matched.append(scheme)
    return matched

if __name__ == "__main__":
    schemes = load_schemes()
    print(f"Total schemes loaded: {len(schemes)}")
    print(schemes[0]["name"])

    sample_profile = {
        "occupation": "student",
        "income": 200000,
        "age": 20,
        "state": "Uttar Pradesh",
        "gender": "male",
        "category": "OBC",
        "has_disability": False
    }
    results = match_schemes(sample_profile)
    print(f"\nMatched schemes: {len(results)}")
    for r in results:
        print("-", r["name"])