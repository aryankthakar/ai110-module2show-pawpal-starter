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

The scheduler considers priority level, time blocks (start/end time), and recurring frequency; priority ranked highest because it directly encodes owner preference, which the project spec called out as the core constraint.

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

The most effective Copilot features were inline autocomplete for boilerplate (like `__init__` methods and property setters) and the chat panel for talking through design decisions. Autocomplete saved a lot of time on repetitive class scaffolding — once I wrote one class, it basically knew what the next ones should look like. Chat was most useful when I asked narrow, specific questions like "how should a Scheduler's `get_tasks_by_date` handle recurring tasks?" rather than broad ones. That forced me to already have a mental model and use the AI to pressure-test it.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

When building conflict detection, Copilot suggested auto-resolving overlapping tasks by bumping the later one's start time forward. I rejected this because it silently mutates a user's data without their knowledge. I kept conflict detection as a warning only (which was already in the design) and verified this was the right call by checking that the tradeoff explanation I'd already written still held: owners need control, not automatic decisions made for them.

**c. Separate chat sessions by phase**

Using separate chat sessions for design, implementation, and testing kept context clean and focused. When I was in the design phase, the chat didn't have half-written code cluttering the context, so suggestions stayed at the right level of abstraction. During implementation, I wasn't re-explaining design rationale every time. It also made it easier to backtrack. if a session went sideways, I could just start a fresh one for that phase without losing everything else.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested adding/removing pets and tasks, sorting by priority and date, conflict detection, and recurring task logic — these covered the core scheduler behaviors that everything else depends on.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I'm confident in the happy-path flows, but I'd next test edge cases like tasks spanning midnight, recurring tasks with end dates, and owners with no pets or pets with no tasks.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I'm most satisfied with the conflict detection design — keeping it as a warning rather than auto-resolution was a deliberate call that kept user control intact and made the tradeoff easy to explain.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I'd redesign how recurring tasks are stored — right now frequency is a field on the task, but a proper recurrence rule (with end dates, exceptions, and skips) really deserves its own class.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

 AI tools are fast and confident, which makes it easy to let them drive. But when I did that, the design would drift: classes got extra responsibilities they didn't need, abstractions appeared before there was a reason for them, and naming stopped reflecting the domain. The code still ran, but it stopped being *my* system.

What actually worked was showing up to each AI session with a decision already half-made. I wanted the AI to stress-test it, but I had to have a position. "I'm thinking conflict detection should warn, not resolve. What breaks if I do it that way?" is a productive question. "How should I handle conflicts?" gives the AI the wheel.

The lead architect's job with AI is less about generating ideas and more about having clear enough intent that you can tell when a suggestion fits your design versus just fits the problem. Those are different things, and only you can draw that line.
