"""
Your test questions.

Milestone 2 asks you to write five questions your system should be able to
answer from your corpus, specific enough to have a right answer.

  ✗ "What are good dining halls?"          — no right answer
  ✓ "What do students say about wait times at Commons during lunch?"

Fill in `QUESTIONS` below. `expects` is a word or short phrase you'd expect a
correct answer to contain — you'll use it in unit 2 when you build a scorer,
and having written it now means you decided what "correct" meant before you saw
any results.

`OUT_OF_SCOPE` holds five questions your documents clearly don't cover. You
need these in Milestone 4 to find where your relevance cutoff belongs, and
again in unit 2, where `run_eval.py` runs them through the gate and writes what
happened into your run log — that's the evidence for criterion 3.

Swap them for your own if you like. Keep five of them either way: criterion 3
names a target of "4 of 5", and four of three is not a thing.
"""

QUESTIONS = [
    # {"question": "...", "expects": "..."},
    {"question": "Which study spots are usually empty?", "expects": "science building"},
    {"question": "When can I change rooms if I don't like my roommate?", "expects": "end of the semester"},
    {"question": "What is the limit to use the pass/fail option on classes per year?", "expects": "two"},
    {"question": "Which RAM option do CS students usually use on their laptops?", "expects": "16GB"},
    {"question": "What is the printing quota for black and white pages?", "expects": "about 600 pages, $30"},
]

# Five questions for criterion 5: each one has a correct answer in
# `correct_source`, but is topically close enough to `confusable_with` that a
# retriever with weak discrimination could easily pull the wrong thread.
# There are five of these for the same reason `OUT_OF_SCOPE` has five: criterion
# 5 names a target of "4 of 5", which needs five things to try it against.
THREAD_CONFUSION_QUESTIONS = [
    {
        "question": "What did it cost in total to keep a cheap bike just for the fall?",
        "expects": "$120",
        "correct_source": "thread_bike_commute.txt",
        "confusable_with": "thread_commuting.txt",
    },
    {
        "question": "Who should I actually talk to if I want to change my major?",
        "expects": "adviser for the major you want",
        "correct_source": "thread_changing_major.txt",
        "confusable_with": "thread_transfer_credits.txt",
    },
    {
        "question": "Is it normal to show up to office hours with no specific question?",
        "expects": "yes",
        "correct_source": "thread_office_hours_etiquette.txt",
        "confusable_with": "thread_professor_email.txt",
    },
    {
        "question": "How many courses can I take pass/fail per year?",
        "expects": "two",
        "correct_source": "thread_pass_fail.txt",
        "confusable_with": "thread_first_year_regret.txt",
    },
    {
        "question": "When's the right time to ask an instructor for a deadline extension?",
        "expects": "before the deadline",
        "correct_source": "thread_late_work.txt",
        "confusable_with": "thread_first_year_regret.txt",
    },
]

# Questions from a different world entirely. Your gate should refuse all five.
#
# There are five of these because criterion 3 in criteria.md names a target of
# "at least 4 of 5" — you need five things to try before you can report 4 of 5.
# `run_eval.py` runs these through retrieval and the gate on every eval and
# records what happened, so criterion 3 has evidence in the run log alongside
# the others. They cost no model calls: a refusal never reaches the model.
OUT_OF_SCOPE = [
    "What is the capital of Mongolia?",
    "How do I change the oil in a diesel engine?",
    "Who won the 1994 World Cup?",
    "What is the recommended dosage of ibuprofen for a headache?",
    "How do I write a for loop in Rust?",
]


def answered() -> list[dict]:
    """The questions you've actually filled in."""
    return [q for q in QUESTIONS if q.get("question", "").strip()]
