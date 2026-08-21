def build_checklist(matched_schemes):
    checklist ={}
    for scheme in matched_schemes:
        for doc in scheme["documents"]:
            if doc not in checklist:
                checklist[doc] = []
            checklist[doc].append(scheme["name"])
    return checklist

if __name__ == "__main__":
    from matching_agent import match_schemes

    sample_profile = {"occupation": "farmer", "income": 200000, "age":25, "state": "Uttar Pradesh", "gender": "male"}
    results = match_schemes(sample_profile)

    checklist = build_checklist(results)
    for doc, schemes in checklist.items():
        print(f"{doc}: needed for {len(schemes)} schemes(s) -> {schemes}")