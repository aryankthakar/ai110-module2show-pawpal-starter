# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

Core actions to perform:
- Add and schedule a task
- Set how frequent this task will be recurring
- See tasks for a specific date

- What classes did you include, and what responsibilities did you assign to each?

Task:
- Info
  - description
  - date to complete the task
  - how often task repeats (daily, weekly, monthly, custom)
  - Priority level (likert scale, 1 being highest and 3-4 being lowest)
  - Specific time (defaults to empty)
- Actions
  - Edit description
  - Edit priority level (defaults to priority 3 or 4)
  - Edit date to complete task (defaults to today or no date)
  - Edit recurring frequency of task (defaults to None)
  - Edit time block to complete the task

Pets:
- Info
  - List of Tasks
- Action
  - Add/Remove task

Owner:
- Info
  - List of Pets
- Actions
  - Add/remove pet



**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
