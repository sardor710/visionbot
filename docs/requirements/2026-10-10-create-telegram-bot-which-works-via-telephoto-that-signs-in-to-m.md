# create telegram bot which works via telephoto that signs in to my account and do...

## Goal
create telegram bot which works via telephoto that signs in to my account and download posts videos and photos with captions and uploaded date from links. i can send link to story or post in telegram channel. and i can send username/id of user to download  all of its public stories or just last 24 hours ones. and telegram channel name or id to download all posts from telegram channel Update: create telegram bot which works via telephoto that signs in to my account and download posts videos and photos with captions and uploaded date from links. i can send link to story or post in telegram channel. and i can send username/id of user to download  all of its public stories or just last 24 hours ones. and telegram channel name or id to download all posts from telegram channel Update: create telegram bot which works via telephoto that signs in to my account and download posts videos and photos with captions and uploaded date from links. i can send link to story or post in telegram channel. and i can send username/id of user to download  all of its public stories or just last 24 hours ones. and telegram channel name or id to download all posts from telegram channel

## Deliverable
The user-requested outcome described in the full goal, with supporting evidence appropriate to that outcome

## Constraints
- Do not bypass the fixed six-stage governed runtime.
- Do not widen scope silently beyond the frozen requirement document.

## Acceptance Criteria
- Requirement document is frozen before execution.
- Execution plan exists before task execution.
- Verification evidence exists before completion claims.
- Phase cleanup receipt is produced.

## Product Acceptance Criteria
- Requirement document is frozen before execution.
- Execution plan exists before task execution.
- Verification evidence exists before completion claims.
- Phase cleanup receipt is produced.
- The delivered output must satisfy observable behavior implied by the frozen goal and deliverable, not only internal runtime progress.
- Full completion wording is allowed only after downstream delivery truth is passing.

## Manual Spot Checks
- None required beyond automated verification for this task unless the execution scope expands to a user-visible or interactive flow.

## Completion Language Policy
- Full completion wording is allowed only when governance truth, engineering verification truth, workflow completion truth, and product acceptance truth are all passing.
- `completed_with_failures`, degraded execution, or pending manual actions must be reported as non-complete states.
- If manual spot checks remain pending, the run must be described as requiring manual review rather than fully ready.

## Delivery Truth Contract
- Governance truth: requirement, plan, execution, and cleanup artifacts remain traceable and authoritative.
- Engineering verification truth: targeted verification passes or fails explicitly; silence does not count as success.
- Workflow completion truth: planned units, delegated lanes, and specialist outputs reconcile back into the governed plan.
- Product acceptance truth: observable deliverable behavior satisfies frozen acceptance criteria before full completion language is allowed.

## Code Task TDD Mode
TDD mode: required
Decision source: host_decision
Reason: The task includes implementation or defect-correction intent that requires code-task TDD evidence.

## Code Task TDD Evidence Requirements
- Record failing-first evidence for the changed behavior before implementation or defect correction.
- Record the green rerun that proves the targeted behavior passed after implementation.
- Map the changed behavior to targeted verification evidence; generic suite success alone is insufficient.
- If automated failing-first evidence is not appropriate, freeze and honor an explicit code-task TDD exception instead of silently skipping the requirement.

Non-goals:
- Do not create separate M/L/XL entry commands.
- Do not introduce a second router or control plane.

## Skill Search Guide
- Decompose task into modules first
- Search local skills per module
- Search local skills independently per module
- Review candidate skill name and summary first, then read candidate `SKILL.md`
- Keep at most 3 candidates per module to prevent context dilution
- Determine fit based on actual `SKILL.md` purpose, not keyword collisions
- Provide both `L` and `XL` skill organization plans with explicit responsibilities
- Prefer direct module owners over loose helper skills
- A single skill may cover multiple modules
- explicit_only skills are selected only when specifically named by the user
- Respect boundary constraints and negative application limits of candidates
- Disclose coverage gaps honestly when no owner exists
- Clearly flag modules lacking direct skill owners
- Disclose search methodology at requirement stage; present L/XL candidate workflows before user selection without claiming pre-selection
- Disclose modules, candidates, final selections, and gaps at xl_plan stage
- Disclose actively enabled skills during execution stage

## Workflow Level Confirmation
- User-visible: True
- Recommended level: L
- Recommendation reason: 当前任务更像单主线交付：先冻结需求和计划，再让 Agent 按模块组织一个较轻量的 skills 方案，通常比一开始就上分波次协作更省沟通成本。
- Why this decision matters: L 和 XL 会直接改变后续的协作深度、是否进入分波次执行，以及证据和回归边界的强度。
- Before asking the user to choose L or XL, explain each task-specific workflow and list its task-specific candidate skill names. Label those names as candidates that are not yet selected or used.
- L: Level L is ideal for multi-step sequential tasks: freezes requirements/plans with full evidence verification under a unified main process.
- L workflow: Freeze requirements and plan, then execute sequentially through a single main process.
- L skills: 会先按模块搜索本地 skills、阅读候选 `SKILL.md`，再给出较轻量的 L 级组织方案；涉及代码改动或缺陷修复时，会补充 `tdd` 这类 failure-first 验证 skill，但不默认拆成多代理。
- L rationale: 适合仍然是一个主交付物、依赖链较短、并行收益不高的任务，可以把沟通成本压低，同时保留完整的冻结与验证边界。
- L confirm reply: 如果你认可这个较轻量但证据完整的流程，请回复：`走 L 级`。
- XL: XL 级适合研究交付、多产物、多技能协作或风险更高的任务：会有更严格的需求冻结、计划冻结、分阶段执行、证据清单和收尾检查。
- XL workflow: 先冻结需求和计划，再把 Agent 组织出的方案拆成分波次执行；只有在依赖安全时才允许小步并行，最后统一回到验证和收尾。
- XL skills: 会先按模块组织更完整的本地 Skills；确需多代理时，由当前 Agent 依据已冻结计划分波次协调，不额外假定一个协调 Skill。
- XL rationale: 适合多产物、多技能协作、研究交付或高风险改动，因为它能先讲清分工、阶段边界和证据清单，再进入执行。
- XL confirm reply: 如果你希望先把分工和波次讲清楚，再进入更重的执行流程，请回复：`走 XL 级`。
- Question: Confirm workflow level: Proceed with Level L (sequential) or Level XL (multi-agent waves)?
- Selection prompt: Please review the options above and confirm your preferred workflow level.

## Assumptions
- Interactive clarification is allowed if unresolved ambiguity materially changes the requested outcome.
