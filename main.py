Experiments
Baseline

I started with a simple rule-based approach using the study descriptions from the current and prior exams. The goal was to decide whether a prior exam would be useful to a radiologist when reading the current study.

My initial approach focused on direct keyword matching in the study descriptions, mainly looking for overlaps in imaging modality (MRI, CT, X-ray, ultrasound) and basic anatomical regions.

What worked

The strongest signal by far was still imaging modality. When the current and prior studies were the same type (for example, both CT or both MRI), they were much more likely to be clinically relevant.

After that, improving text normalization helped a lot. Lowercasing and handling formatting variations (like “x-ray” vs “x ray” or “radiograph”) made the matching more consistent and reduced missed cases.

The body region logic also improved after loosening it slightly. Instead of requiring strict matches, treating overlap in anatomy keywords (brain, head, chest, abdomen, spine) as sufficient increased recall without introducing too much noise.

Finally, the date-based filtering helped reduce older priors from being incorrectly marked as relevant, especially when studies were several years apart. Using a more tolerant comparison also made the system more stable when dealing with imperfect or inconsistent timestamps.

Overall, the rule-based approach remained effective, but these small adjustments significantly improved performance without adding complexity.

What didn’t work

Early on, strict keyword matching caused issues because radiology reports often describe the same anatomy using different terms (for example, “head CT” vs “brain MRI”). This led to unnecessary false negatives.

I also tried making body region matching too strict (requiring exact overlap), which reduced recall and missed valid prior studies that were still clinically relevant.

In addition, relying too heavily on raw text without normalization caused inconsistent results due to formatting differences like hyphens, spacing, and synonyms.

More complex approaches like external model calls or per-comparison scoring were considered but quickly ruled out due to latency and evaluation constraints.

Improvements / Next Steps

If I had more time, I would:

Replace keyword matching with embedding-based similarity (e.g., sentence transformers) to better capture semantic relationships between studies
Introduce a lightweight scoring system instead of binary rules to better balance precision and recall
Map anatomy terms to a medical ontology (such as RadLex) to improve consistency across synonyms
Add caching for repeated comparisons to reduce redundant computation during large batch evaluations
Explore learning-based ranking instead of fixed thresholds for modality and anatomy matching
Final Approach

The final solution is a rule-based system with improved normalization and more flexible matching logic.

It checks:

Whether the imaging modality matches (MRI, CT, X-ray/radiograph, ultrasound), with support for common variations in terminology
Whether there is overlap in anatomical regions using a relaxed keyword-based approach
Whether the prior study falls within a reasonable time window (approximately 5 years), with safeguards for inconsistent date formatting

This approach was chosen because it is fast, interpretable, and performs reliably under evaluation constraints. The improvements over the baseline mainly focus on reducing overly strict matching rules and increasing recall without significantly increasing noise.
