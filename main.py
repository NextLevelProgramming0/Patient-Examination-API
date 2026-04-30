from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

# simple health check route so you know the API is running
@app.get("/")
def home():
    return {"message": "Radiology API is running"}


# tries to figure out the scan type from the description text
def get_modality(desc):
    desc = desc.lower()
    if "mri" in desc:
        return "mri"
    elif "ct" in desc:
        return "ct"
    elif "xray" in desc or "x-ray" in desc:
        return "xray"
    elif "ultrasound" in desc:
        return "ultrasound"
    return None


# basic list of body parts we care about for now
BODY_PARTS = ["brain", "head", "chest", "abdomen", "spine"]


def is_relevant(current, prior):
    current_desc = current.get("study_description", "").lower()
    prior_desc = prior.get("study_description", "").lower()

    # first check if both studies are the same type of scan
    current_mod = get_modality(current_desc)
    prior_mod = get_modality(prior_desc)

    if current_mod != prior_mod:
        return False

    # then check if they mention the same body region
    match = False
    for part in BODY_PARTS:
        if part in current_desc and part in prior_desc:
            match = True
            break

    if not match:
        return False

    # finally compare dates to make sure it's not too old
    try:
        current_date = datetime.fromisoformat(current["study_date"])
        prior_date = datetime.fromisoformat(prior["study_date"])

        diff_days = (current_date - prior_date).days

        # ignore anything older than ~5 years
        if diff_days > 5 * 365:
            return False
    except Exception as e:
        # if date parsing breaks, just skip the filter and continue
        print("date parsing issue:", e)

    return True


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
