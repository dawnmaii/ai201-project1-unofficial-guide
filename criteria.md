# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
<!-- e.g. "One of my questions is about a topic only two documents mention, so
     I expect that one to be hard." -->

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
<!-- Why all five and not four? What about your setup makes that achievable —
     or what would have to go wrong for it not to be? -->

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
<!-- What did your distances look like when you set the cutoff in Milestone 4?
     Was there a clean gap, or did the two groups overlap? -->

---

## 4. No chunk is a fragment

Every chunk in the index is at least 100 characters long.

**Why this target:**
With the old fixed-window chunker, advice_threads produced fragments as short as 2 characters (`thread_meal_plan_tier.txt`'s leftover "t."), because the window cut mid-sentence with no regard for content boundaries. Switching to reply-boundary splitting fixes that directly — the shortest chunk is now 105 characters, comfortably above 100 — but the target is worth keeping on its own rather than dropping it, since it's a concrete check that would catch a regression (e.g., a thread with an unusually short reply, or a future corpus where reply-splitting produces something tiny) rather than assuming the fix holds forever.

---

## 5. Retrieval doesn't confuse similarly-themed threads

For at least 4 of the 5 test questions (specifically in `THREAD_CONFUSION_QUESTIONS` in questions.py), the top retrieved chunk's source file exactly matches that question's `correct_source`.

**Why this target:**
`advice_threads` has several thread pairs that share vocabulary and topic area without sharing an answer — `bike_commute`/`commuting` (both about getting to campus), `changing_major`/`transfer_credits` (both about credits mapping to a major), `office_hours_etiquette`/`professor_email` (both literally say office hours are "usually empty"), and `pass_fail`/`late_work` each overlapping with `first_year_regret`, which restates facts from both. Criterion 1 only checks that *an* answer-bearing chunk shows up; it doesn't catch the case where the retriever pulls a confident-looking chunk from the wrong thread because the topics are semantically close. `THREAD_CONFUSION_QUESTIONS` names the five specific pairs so this is checkable the same way twice, not a judgment call about which threads "count" as similar.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
