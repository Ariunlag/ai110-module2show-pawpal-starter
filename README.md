# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Testing PawPal+

Run the test suite with:

```bash
python -m pytest
```

Current tests cover:

- **Sorting**: verifies tasks are ordered correctly by `HH:MM` time.
- **Filtering**: verifies completed vs pending task subsets are accurate.
- **Recurring tasks**: verifies daily completion creates the next-day task while preserving history.
- **Conflict detection**: verifies same-time tasks produce conflict warnings.

These tests matter because they validate core scheduler behavior, reduce regression risk, and ensure task planning output stays predictable as features evolve.

**Confidence Level:** ★★★★☆ (4/5)

The core scheduling paths are well-covered, but confidence is not 5/5 yet because advanced overlap logic and invalid-time validation are still limited.

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
