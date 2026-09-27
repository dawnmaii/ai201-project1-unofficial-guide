def judge(question, expects, answer, results) -> bool:
    """
    q: 'give', expect: 'give'
    the expect is in the answer

    """
    return expects.lower().strip() in answer.lower()

def retrieval_hits(expected, results) -> bool:
    """
    any chunk in the results contains my expected phrase
    
    """
    return any(expected.lower().strip() in chunk.text.lower() for chunk in results)
