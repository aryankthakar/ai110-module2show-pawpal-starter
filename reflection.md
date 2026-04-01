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

Tasks was chosen for keeping track of what needs to be done and any underlying context (i.e. timing, importance, etc.). Pets was chosen to keep track of which Pets a certain task is for. Owner was chosen for having the organization of the one-to-many relationship between Owner to Pets and the one between Pets to Tasks. Scheduler was added later in order to organize and group tasks by attributes other than which Pet they belong to. 


**b. Design changes**

- Did your design change during implementation?

Yes

- If yes, describe at least one change and why you made it.

The intentions in the README.md described "owner preference" and "time constraints" to be important when organizing the order of the tasks. I adapted my design to have prioritizing changed to "owner preference" for consistency/intuitiveness and the time constraint be implied by the Tuple field of Task object containing the start time and end time. This can make it such that the information is described to the user and developer using similar terminology.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff is that the scheduler detects time conflicts between tasks but does not automatically resolve them or prevent scheduling conflicting tasks. Instead, it simply warns the user about overlaps and continues with the schedule as planned.

This tradeoff is reasonable because pet owners may have valid reasons for scheduling overlapping tasks (e.g., one task might be flexible, or they might need to choose between alternatives). Automatic resolution could be overly prescriptive and remove user control. The warning approach provides awareness without restricting flexibility, allowing owners to make informed decisions about their pet care routines.

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
