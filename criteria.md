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
Four of my five real test questions retrieved the answer-bearing chunk at rank 1 with a low distance (0.210-0.382). The fifth — "When can I change rooms if I don't like my roommate?" — had its answer at rank 2 (distance 0.380) instead of rank 1, behind another reply from the same thread. Retrieval isn't guaranteed to rank the single most relevant reply first when a thread has several replies about closely related sub-topics, so I set the target at 4 of 5 rather than 5 of 5 to leave room for that kind of near-miss without treating it as a failure, since the answer still shows up somewhere in the top-k either way.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
Unlike criterion 1, this isn't about retrieval quality — it's enforced directly in the prompt. `generate.py`'s `GROUNDING_INSTRUCTION` and `build_prompt` both explicitly tell the model to name the filename it used, on every question that reaches generation. A question only reaches generation after passing the relevance gate, so as long as the model follows an instruction repeated in every prompt, there's no reason one answered question would name a source while another wouldn't. I set this one at 5 of 5, not 4 of 5, because it's a prompt-following check, not a variable retrieval outcome.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

**Why this target:**
When I ran the five `OUT_OF_SCOPE` questions against the five real ones in Milestone 4, the two groups didn't overlap at all: real questions scored 0.210-0.382, out-of-scope questions scored 0.819-0.905, a gap of over 0.4. With separation that clean on the corpus I actually tested, I'd expect close to 5 of 5 in practice — but I still set the target at 4 of 5 rather than 5 of 5, since these five out-of-scope questions are the only ones I've measured, and an out-of-scope question worded closer to my corpus's vocabulary than these five happen to be could plausibly land nearer the gate.

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
