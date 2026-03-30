# PawPal+ Project Reflection

## 1. System Design

**Core user actions**

- Add and manage pet profile information (for example pet name, type, and care notes).
- Create, edit, and prioritize care tasks (like feeding, walks, medication, and grooming) with duration.
- Generate and view today’s schedule so tasks are ordered based on available time and priority.

**a. Initial design**

- Briefly describe your initial UML design.
My initial UML design defined four main components—Owner, Pet, Task, and Scheduler—and illustrated how they interact.
The Owner provides scheduling constraints, the Pet provides care context, Tasks represent daily activities, and the Scheduler coordinates them to generate a daily plan.
The UML diagram focused on showing relationships (Owner → Pet → Task) and the Scheduler’s role in orchestrating the workflow

- What classes did you include, and what responsibilities did you assign to each?
- Owner – stores user preferences such as available minutes, preferred time blocks, and priority rules.
- Pet – holds pet‑specific information and special‑care requirements.
- Task – represents an individual care activity with duration, priority, and scheduling rules.
- Scheduler – filters due tasks, sorts them, applies time constraints, and produces the final daily plan with explanations


**b. Design changes**

- Did your design change during implementation?
yes. when i review my code with help of ai it suggested some shanges.
- If yes, describe at least one change and why you made it.
    - Add validation in Scheduler: every task.pet_id must match pet.pet_id.
    - Add task timing state: due_date and last_completed_at (or completion log relation).
    - Add a ScheduleItem model (task, time_block/start, reason) and make generate_daily_plan return those.
    - Add a reset step in generate_daily_plan to clear selected/unscheduled lists before recomputing.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- My scheduler primarily considers scheduled time, completion status, and pet grouping from the Owner as the single source of truth.
- I prioritized time ordering first because it directly affects day-to-day usability, then status filtering and grouping for clarity in the UI.
- I reviewed `display_schedule` and used a more Pythonic approach by relying on Scheduler helpers (for sorting/filtering) instead of repeating list-processing logic in the UI layer.

**b. Tradeoffs**

- My conflict detection currently flags conflicts only when two tasks have the exact same `scheduled_time` string.
- I chose this simpler rule instead of full time-overlap detection (start/end windows and duration math) to keep the logic easy to understand, test, and maintain for this project scope.
- The tradeoff is lower accuracy for edge cases, but better simplicity and reliability for a beginner-friendly scheduler.

---

## 3. AI Collaboration

**a. How you used AI**

- I used AI for design brainstorming, method planning, test generation, and UI refactoring across phases of the project.
- The most helpful prompts were specific implementation requests, such as adding scheduler features, writing isolated pytest cases, and improving Streamlit formatting.

**b. Judgment and verification**

- I did not accept the first conflict-display suggestion as-is because it showed generic warnings without enough user context.
- I revised it to include affected pets, then verified behavior with test cases and direct UI checks to confirm it improved clarity without breaking architecture.

---

## 4. Testing and Verification

**a. What you tested**

- I tested sorting by `HH:MM`, filtering by completion state, recurring-task creation, conflict detection, and empty-pet edge cases.
- These tests were important because they validate core scheduler correctness and reduce regressions when refactoring backend or UI logic.

**b. Confidence**

- My confidence level is high (about 4/5) for current scope because core flows are covered with automated tests and manual schedule checks.
- With more time, I would test invalid time strings, same-time conflicts across larger task sets, and richer overlap logic beyond exact time matching.

---

## 5. Reflection

**a. What went well**

- I am most satisfied with keeping a clean architecture where `Owner` is the source of truth, `Scheduler` handles logic, and the UI stays focused on presentation.

**b. What you would improve**

- In another iteration, I would add stronger time validation, interval-based conflict detection, and task editing/completion controls directly in the UI.

**c. Key takeaway**

- My key takeaway is that AI is most effective when I provide precise constraints and still make the final design decisions like a lead architect.
