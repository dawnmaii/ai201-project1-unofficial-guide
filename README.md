# The Unofficial Guide

Dawn Mai, advice_threads

---

## Unit 1

## What This Does

This is a question-answering system built on the `advice_threads` corpus — a set of forum-style threads where students post questions about campus life and other students reply with upvoted advice. Ask it something the corpus covers, like "what's the pass/fail limit per year?" or "which study spots are usually empty?", and it retrieves the relevant thread and answers using only what's in it, naming the source file. Ask it something the corpus doesn't cover — a question from an entirely different topic, like car maintenance or sports trivia — and it says so instead of guessing.

## Chunking Strategy

**Chunk size:** Not fixed
**Overlap:** 0

The starter's fixed 800-character window was a bad fit for `advice_threads`: every thread is well under 800 characters, so it rarely split anything on its own, but when a thread happened to run just past that limit, it produced a real chunk plus a near-useless tail fragment — `thread_meal_plan_tier.txt` split into a 682-character chunk and a 2-character leftover ("t."), and `thread_bike_commute.txt` split into 739 and 59 characters, cutting a sentence in half rather than at a natural boundary. Reading through the corpus in Milestone 1, I noticed each thread is already structured as a title followed by several `--- reply N (votes) ---` blocks, and each reply is a self-contained point from a different commenter. One thread, `thread_first_year_regret.txt`, even bundles five unrelated tips (deadlines, pass/fail, the writing centre, and more) into a single document — splitting on character count would either merge those unrelated tips into one chunk or cut a single reply in half depending on where the 800-character line fell. Splitting on the reply marker instead follows a boundary the corpus already marks for me, so every chunk is exactly one commenter's point, no more and no less.

Chunk size varied due to the length of each individual reply per thread in the corpus. On average, replies were anywhere from 105 to 254 characters in length, which roughly translates to a 175 character average. Overlap is 0 because we divided chunks based on reply, and each reply is unique. No content is cut off or shared between replies.

## Sample Chunks

```text
======================================================================
Chunk 1  |  source: thread_bike_commute.txt#0  |  produced by: chunker.py::split_documents
======================================================================

THREAD: Is a bike worth it for a 20 minute walk commute?

Yeah. Cuts an 18 minute walk to about 6. The thing nobody mentions is storage — covered bike parking exists at three buildings and is full by 9am at all three.

======================================================================
Chunk 2  |  source: thread_first_gen.txt#1  |  produced by: chunker.py::split_documents
======================================================================

THREAD: Anything specific for first-generation students?

The thing I'd say: the unwritten rules are the hard part, not the coursework. Ask about the unwritten rules explicitly. People are happy to explain them and nobody volunteers them.

======================================================================
Chunk 3  |  source: thread_laptop_specs.txt#2  |  produced by: chunker.py::split_documents
======================================================================

THREAD: How much laptop do I actually need for CS courses?

I did two years on an 8GB machine and it was fine until the last project, at which point it very much wasn't. 16 is the answer.

======================================================================
Chunk 4  |  source: thread_parking.txt#1  |  produced by: chunker.py::split_documents
======================================================================

THREAD: Worth getting a parking permit?

Street parking on Verrill is legal and free and unmarked, which is why half the upper years do it.

======================================================================
Chunk 5  |  source: thread_sleep_schedule.txt#1  |  produced by: chunker.py::split_documents
======================================================================

THREAD: Everyone says fix your sleep. Does it actually matter?

The library being open until 2am is a trap. It's a resource, not a schedule.
```

## Sample Answer

```text
**Question:** What is the limit to use the pass/fail option on classes per year?

**Answer:** Based on the provided documents, the limit is two per year (and eight across the degree) (thread_pass_fail.txt).

**Sources retrieved:** thread_first_year_regret.txt, thread_pass_fail.txt
```

**My relevance cutoff:**

| Question | In corpus? | Best distance |
| --- | --- | --- |
| Which study spots are usually empty? | yes | 0.382 |
| When can I change rooms if I don't like my roommate? | yes | 0.367 |
| What is the limit to use the pass/fail option on classes per year? | yes | 0.210 |
| Which RAM option do CS students usually use on their laptops? | yes | 0.287 |
| What is the printing quota for black and white pages? | yes | 0.256 |
| What is the capital of Mongolia? | no | 0.899 |
| How do I change the oil in a diesel engine? | no | 0.905 |
| Who won the 1994 World Cup? | no | 0.898 |
| What is the recommended dosage of ibuprofen for a headache? | no | 0.819 |
| How do I write a for loop in Rust? | no | 0.861 |

In-scope questions had a lower distance overall (0.210 - 0.382) than the out-of-scope questions (0.819 - 0.905), showing a clean separation between what my corpus covers and what it doesn't. I decided to keep 0.6 as the cutoff because it's almost exactly the midpoint of the gap between the two groups' distances ((0.382 + 0.819)/2 = 0.6005), giving equal margin on both sides. I also kept `top_k` at 5 because the answer-bearing chunk already appeared somewhere in the top 5 results for all five of my test questions, so raising it wouldn't have added anything.

## How I Used AI

**1.** I asked Claude to walk me through writing `split_documents` in `chunker.py` line by line instead of pasting in a finished version, so I typed the reply-boundary splitting logic myself. When I ran it, my editor flagged the `continue` statement as making the rest of the function unreachable — I'd left it at the same indentation as the `if not replies:` line above it instead of inside that block, so it ran on every document instead of only the ones with no replies. I fixed the indentation myself once Claude pointed out what the warning meant.

**2.** While drafting `criteria.md`, I asked Claude to check criterion 5 for ambiguity — specifically, whether someone could check it without asking me what I meant. It came back that "in at least 4 of 5 tries" didn't say which 5 questions those were, unlike criterion 3, which points at a named list (`OUT_OF_SCOPE`). I fixed it by adding a `THREAD_CONFUSION_QUESTIONS` list to `questions.py` with five specific question pairs, and reworded criterion 5 to point at that list the same way criterion 3 does.

---

## Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
