# create telegram bot which works via telephoto that signs in to my account and do...

## Execution Summary
Governed runtime execution plan for `vibe` in mode interactive_governed.

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

## Task Modules
- `module_telegram_core`: Implement Telethon client session configuration, MTProto authentication, and URL/entity parser for Telegram posts, stories, usernames, and channel IDs.
- `module_downloader_engine`: Implement downloading engine for channel posts, user stories (all vs last 24 hours), and media extraction with captions and timestamps.
- `module_bot_interface`: Implement Telegram bot interaction handler allowing users to send links, channel IDs, and usernames via bot commands.
- `module_test_verification`: Develop and run comprehensive unit and mock integration test suite following TDD methodology.

## Candidate Skills By Module
- `module_telegram_core`: `python-pro`
- `module_downloader_engine`: `python-pro`
- `module_bot_interface`: `python-pro`
- `module_test_verification`: `test-driven-development`

## Uncovered Modules
- None. Every declared module is covered by an Agent-selected local Skill.

## L / XL Organization Difference
- L: Clarify modules, then organize a lightweight sequential workflow.
- XL: Clarify modules, then organize a comprehensive phased wave workflow with clear lane boundaries.
- Selected workflow level: `XL`

## Frozen Inputs
- Requirement doc: D:\projects\private bot\docs\requirements\2026-10-10-create-telegram-bot-which-works-via-telephoto-that-signs-in-to-m.md
- Source task: create telegram bot which works via telephoto that signs in to my account and download posts videos and photos with captions and uploaded date from links. i can send link to story or post in telegram channel. and i can send username/id of user to download  all of its public stories or just last 24 hours ones. and telegram channel name or id to download all posts from telegram channel Update: create telegram bot which works via telephoto that signs in to my account and download posts videos and photos with captions and uploaded date from links. i can send link to story or post in telegram channel. and i can send username/id of user to download  all of its public stories or just last 24 hours ones. and telegram channel name or id to download all posts from telegram channel Update: create telegram bot which works via telephoto that signs in to my account and download posts videos and photos with captions and uploaded date from links. i can send link to story or post in telegram channel. and i can send username/id of user to download  all of its public stories or just last 24 hours ones. and telegram channel name or id to download all posts from telegram channel

## Wave Plan
- Wave 1 (`sequential`): `module_telegram_core` via skill `python-pro` as `owner`
- Wave 2 (`sequential`): `module_downloader_engine` via skill `python-pro` as `owner`
- Wave 3 (`sequential`): `module_bot_interface` via skill `python-pro` as `owner`
- Wave 4 (`sequential`): `module_test_verification` via skill `test-driven-development` as `owner`

## Delivery Acceptance Plan
- Freeze downstream product acceptance inside the governed requirement doc and reuse it rather than inventing closeout claims later.
- Emit a per-run delivery-acceptance report during `phase_cleanup` so runtime/process success is kept separate from project-delivery success.
- Delivery-acceptance report: D:\projects\private bot\outputs\runtime\vibe-sessions\20261010T115516Z-fc1f6557\delivery-acceptance-report.json
- If manual spot checks are declared in the requirement doc, final completion wording stays blocked until they are cleared or explicitly downgraded to manual review.
- Release truth aggregation remains an outer-layer gate; this run emits the per-run delivery-truth report only.

## Code Task TDD Evidence Plan
- Reuse the frozen `Code Task TDD Evidence Requirements` section from the requirement doc rather than inventing late closeout claims.
- Reuse the frozen `Code Task TDD Exceptions` section when strict failing-first sequencing is intentionally exempted.
- Map each frozen requirement or exception to an implementation step, a targeted verification command, and a proof artifact.
- If strict failing-first sequencing is blocked, execution must record the bounded reason and fallback evidence explicitly.

## Module Work Plan
- `module_telegram_core`: Implement Telethon client session configuration, MTProto authentication, and URL/entity parser for Telegram posts, stories, usernames, and channel IDs.
  Required: `True`; dependencies: none; Execution mode: `skill_assigned`
  Work: skill `python-pro` as `owner` - Implement Telethon client session, authentication, and URL/entity parser.
  Acceptance: `core-auth-and-parsing` (automated) - Telethon client config loads credentials and entity/link parser accurately extracts post, story, channel, and user identifiers.
- `module_downloader_engine`: Implement downloading engine for channel posts, user stories (all vs last 24 hours), and media extraction with captions and timestamps.
  Required: `True`; dependencies: `module_telegram_core`; Execution mode: `skill_assigned`
  Work: skill `python-pro` as `owner` - Implement media downloading, metadata extraction (captions, date), and story filtering (24h/all).
  Acceptance: `downloader-engine-features` (automated) - Engine successfully fetches posts, photos, videos, stories with 24h filter and captures caption/date metadata.
- `module_bot_interface`: Implement Telegram bot interaction handler allowing users to send links, channel IDs, and usernames via bot commands.
  Required: `True`; dependencies: `module_downloader_engine`; Execution mode: `skill_assigned`
  Work: skill `python-pro` as `owner` - Implement Telegram bot interaction handlers and main application entrypoint.
  Acceptance: `bot-command-handling` (automated) - Bot commands and incoming messages dispatch to the download engine and return download progress to user.
- `module_test_verification`: Develop and run comprehensive unit and mock integration test suite following TDD methodology.
  Required: `True`; dependencies: `module_bot_interface`; Execution mode: `skill_assigned`
  Work: skill `test-driven-development` as `owner` - Design and execute TDD test harness covering parser, story 24h filtering, and download orchestrator.
  Acceptance: `full-test-verification` (automated) - All unit tests pass verifying parsing, story time filtering, metadata extraction, and bot commands.
- Dispatch python-pro as owner.
  Binding profile: module_work_unit; dispatch phase: in_execution; lane policy: module_dependency_contract; parallel in XL: True
  Write scope: src/telebot_downloader/core/**; review mode: module_acceptance; execution priority: 50
  Reason: approved_module_work_plan
  Required inputs: 
  Expected outputs: src/telebot_downloader/core/client.py, src/telebot_downloader/core/parser.py
  Verification: py -3 -m pytest tests/test_parser.py
- Dispatch python-pro as owner.
  Binding profile: module_work_unit; dispatch phase: in_execution; lane policy: module_dependency_contract; parallel in XL: True
  Write scope: src/telebot_downloader/downloader/**; review mode: module_acceptance; execution priority: 50
  Reason: approved_module_work_plan
  Required inputs: 
  Expected outputs: src/telebot_downloader/downloader/engine.py, src/telebot_downloader/downloader/stories.py
  Verification: py -3 -m pytest tests/test_downloader.py
- Dispatch python-pro as owner.
  Binding profile: module_work_unit; dispatch phase: in_execution; lane policy: module_dependency_contract; parallel in XL: True
  Write scope: src/telebot_downloader/bot/**; review mode: module_acceptance; execution priority: 50
  Reason: approved_module_work_plan
  Required inputs: 
  Expected outputs: src/telebot_downloader/bot/handlers.py, src/telebot_downloader/main.py
  Verification: py -3 -m pytest tests/test_bot.py
- Dispatch test-driven-development as owner.
  Binding profile: module_work_unit; dispatch phase: in_execution; lane policy: module_dependency_contract; parallel in XL: True
  Write scope: tests/**; review mode: module_acceptance; execution priority: 50
  Reason: approved_module_work_plan
  Required inputs: 
  Expected outputs: tests/test_parser.py, tests/test_downloader.py, tests/test_bot.py
  Verification: py -3 -m pytest tests/

## Verification Commands
- Run every verification command frozen for the module work units and retain its real result.
- Reconcile every module acceptance criterion against the returned execution evidence.
- Review the delivery-acceptance report emitted during `phase_cleanup` before using full completion language.

## Rollback Plan
- If verification fails, revert only changes inside the approved module write scopes.
- Do not roll back unrelated user changes.

## Phase Cleanup Contract
- Remove temporary artifacts created by the approved module work only.
- Write cleanup receipt before completion.
