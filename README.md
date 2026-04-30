# Radiology Prior Study Relevance API

This is a simple FastAPI service that helps determine whether prior medical imaging studies are relevant to a current study. It compares things like scan type, body region, and how far apart the studies are in time.

It’s a lightweight, rule-based implementation meant for organizing radiology cases and prototyping ideas around clinical data matching.

---

## What it does

Given a current study and a list of prior studies, the API checks each prior and returns whether it seems relevant or not.

It uses a few simple rules:

* Matches imaging modality (MRI, CT, X-ray, Ultrasound)
* Looks for overlapping body regions (brain, head, chest, abdomen, spine)
* Filters based on time difference (roughly a 5-year cutoff)

---

## Endpoint

### POST `/predict`

---

## Input format

You send a list of cases. Each case includes a current study and one or more prior studies.

```json
{
  "cases": [
    {
      "case_id": "123",
      "current_study": {
        "study_description": "MRI brain without contrast",
        "study_date": "2021-05-10"
      },
      "prior_studies": [
        {
          "study_id": "a1",
          "study_description": "MRI brain with contrast",
          "study_date": "2019-03-01"
        }
      ]
    }
  ]
}
```

---

## Output format

The response returns one prediction per prior study.

```json
{
  "predictions": [
    {
      "case_id": "123",
      "study_id": "a1",
      "predicted_is_relevant": true
    }
  ]
}
```

---

## How it works

For each prior study, the API:

* Detects imaging modality from keywords in the study description
* Checks whether body regions overlap between current and prior studies
* Compares study dates using ISO 8601 format
* Filters out studies older than ~5 years
* Returns a boolean relevance result

---

## Running locally

### Install dependencies

```bash
pip install fastapi uvicorn
```

### Start the server

```bash
uvicorn main:app --reload
```

Then open:

```
http://127.0.0.1:8000/docs
```

---

## Notes

* This is a rule-based prototype, not a production medical system
* Matching is based on keyword logic rather than NLP or clinical models
* Date parsing expects ISO 8601 format strings

---

## Future improvements

* Replace keyword rules with an NLP or ML model
* Add confidence scores instead of boolean outputs
* Improve anatomical mapping using medical ontologies
* Add schema validation with Pydantic
* Expand modality and body region coverage

---

This project is meant as a starting point and can be extended in several directions depending on the use case.
