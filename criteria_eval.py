"""
For evaluating all five criteria and providing evidence for them as per Milestone 1,
since run_eval.py only accounts for criterion #3.

"""

import config
import questions as qs
from store import search
from chunker import split_documents
from ingest import load_documents
import scorer

# 1. Retrieved chunks contain the answer
def check_retrieval_contains_answer():
    items = qs.answered()
    rows = []
    for item in items:
        question = item["question"]
        expects = item["expects"]
        chunks = search(question, top_k=config.TOP_K, corpus=config.CORPUS)
        hit = scorer.retrieval_hits(expects, chunks)
        rows.append((question, hit))
        print(f"{'HIT ' if hit else 'MISS'}  {question}")
    passed = sum(hit for _, hit in rows)
    print(f"\ncriterion 1: {passed} of {len(rows)}")
    return rows

# 2. Every answer names a source
def check_answers_name_sources(runs=3):
    from run_eval import run_once
    items = qs.answered()
    rows = []
    for item in items:
        question = item["question"]
        marks = []
        for _ in range(runs):
            answer, results, decision = run_once(
                question, config.TOP_K, config.THRESHOLD, config.CORPUS, "default"
            )
            if not decision.passed:
                marks.append(None)
                continue
            sources = {r.source for r in results}
            named = any(source in answer for source in sources)
            marks.append(named)
        rows.append((question, marks))
        readable = " ".join({True: "yes", False: "NO", None: "-"}[m] for m in marks)
        print(f"{readable}  {question}")
    return rows

# 4. No chunk is a fragment
def check_chunk_lengths():
    documents = load_documents(config.CORPUS)
    chunks = split_documents(documents)
    lengths = [(c.label, len(c.text)) for c in chunks]
    shortest = min(lengths, key=lambda pair: pair[1])
    fragments = [pair for pair in lengths if pair[1] < 100]
    print(f"shortest chunk: {shortest[0]} at {shortest[1]} chars")
    print(f"chunks under 100 chars: {len(fragments)} of {len(lengths)}")
    return lengths

# 5. Retrieval doesn't confuse similarly-themed threads
def check_thread_confusion():
    items = qs.THREAD_CONFUSION_QUESTIONS
    rows = []
    for item in items:
        question = item["question"]
        correct_source = item["correct_source"]
        chunks = search(question, top_k=config.TOP_K, corpus=config.CORPUS)
        top_source = chunks[0].source if chunks else None
        matched = top_source == correct_source
        rows.append((question, top_source, correct_source, matched))
        print(f"{'MATCH' if matched else 'WRONG'}  top={top_source}  expected={correct_source}")
    passed = sum(row[3] for row in rows)
    print(f"\ncriterion 5: {passed} of {len(rows)}")
    return rows

if __name__ == "__main__":
    print("=== Criterion 1 ===")
    check_retrieval_contains_answer()
    print("\n=== Criterion 2 ===")
    check_answers_name_sources()
    print("\n=== Criterion 4 ===")
    check_chunk_lengths()
    print("\n=== Criterion 5 ===")
    check_thread_confusion()

