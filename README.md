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

## Smarter Scheduling

This implementation includes advanced scheduling features that go beyond basic task management:

### 🔄 **Automatic Recurring Tasks**
- Daily and weekly recurring tasks automatically create next occurrences when completed
- No manual rescheduling required for routine pet care

### ⚡ **Intelligent Conflict Detection**
- Detects overlapping time windows between tasks
- Provides clear warnings without preventing scheduling
- Optimized O(n log n) algorithm for performance

### 🔍 **Flexible Task Filtering**
- Filter tasks by completion status (completed/incomplete)
- Filter by specific pet names
- Combine filters for precise task queries

### ⏰ **Multiple Sorting Options**
- Priority-based sorting (high → medium → low, then by time)
- Time-based sorting for chronological views
- Customizable display options

### 📊 **Comprehensive Testing**
- 17 unit tests covering all major functionality
- Edge case handling and algorithmic validation

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
