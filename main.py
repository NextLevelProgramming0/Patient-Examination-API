from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

# simple check to make sure the API is up
@app.get("/")
def home():
    return {"message": "Radiology API is running"}


# improved scan type detection with more real-world variants
def get_modality(desc):
    desc = desc.replace("-", " ").lower()

    if "mri" in desc:
        return "mri"
    elif "ct" in desc:
        return "ct"
    elif "xray" in desc or "x ray" in desc or "x-ray" in desc or "radiograph" in desc:
        return "xray"
    elif "ultrasound" in desc:
        return "ultrasound"
    return None


# broader body part matching (more flexible than strict AND logic)
BODY_PARTS = ["brain", "head", "chest", "abdomen", "spine"]


def is_relevant(current, prior):
    current_desc = current.get("study_description", "").replace("-", " ").lower()
    prior_desc = prior.get("study_description", "").replace("-", " ").lower()

    # check scan type match
    current_mod = get_modality(current_desc)
    prior_mod = get_modality(prior_desc)

    if current_mod != prior_mod:
        return False

    # looser body region match (improves recall)
    match = False
    for part in BODY_PARTS:
        if part in current_desc or part in prior_desc:
            match = True
            break

    if not match:
        return False

    # date filter (keep but make it safe)
    try:
        current_date = datetime.fromisoformat(current["study_date"])
        prior_date = datetime.fromisoformat(prior["study_date"])

        diff_days = abs((current_date - prior_date).days)

        # ignore anything older than 5 years
        if diff_days > 5 * 365:
            return False

    except Exception as e:
        # if dates are bad, don't block prediction
        print("date parsing issue:", e)

    return True


# smoke test sometimes hits GET instead of POST
@app.get("/predict")
def predict_get():
    return {"message": "Use POST /predict with JSON input"}


# main prediction endpoint
@app.post("/predict")
def predict(data: dict):
    predictions = []

    cases = data.get("cases", [])
    print("received cases:", len(cases))

    for case in cases:
        case_id = case.get("case_id")
        current = case.get("current_study", {})
        priors = case.get("prior_studies", [])

        print(f"case {case_id} -> priors:", len(priors))

        for prior in priors:
            result = is_relevant(current, prior)

            predictions.append({
                "case_id": case_id,
                "study_id": prior.get("study_id"),
                "predicted_is_relevant": result
            })

    print("total predictions:", len(predictions))

    return {"predictions": predictions}
