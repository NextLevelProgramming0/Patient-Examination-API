# Radiology Prior Study Relevance API

This is a simple FastAPI service that helps decide whether prior medical imaging studies are relevant to a current study. It looks at things like the type of scan, the body part involved, and how far apart the studies were in time.

It was built as a lightweight rule-based approach to organizing radiology cases.

---

## What it does

Given a current study and a list of prior studies, the API checks each prior study and returns whether it is likely relevant or not.

It uses a few basic rules:

* Match imaging type (MRI, CT, X-ray, Ultrasound)
* Match body region (brain, head, chest, abdomen, spine)
* Check how old the prior study is (about a 5-year cutoff)

---

## Endpoint

### POST `/predict`

---

## Input format

You send a list of cases. Each case has a current study and prior studies.

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

The response returns a list of predictions for each prior study.

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

1. Checks the scan type based on keywords in the description
2. Looks for matching body parts in the description
3. Compares the study dates
4. Filters out studies older than about 5 years
5. Returns true or false for relevance

---

## Running it locally

### Install dependencies

```bash
```
