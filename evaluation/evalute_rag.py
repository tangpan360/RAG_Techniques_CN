from __future__ import annotations

import json
import re
from typing import Any, Dict, List

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate


def _extract_json_obj(s: str) -> Dict[str, Any] | None:
    s = s.strip()
    m = re.search(r"\{[\s\S]*\}", s)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except Exception:
        return None


def calculate_average_scores(results: List[str | Dict[str, Any]]) -> Dict[str, float | None]:
    scores: Dict[str, List[float]] = {"Relevance": [], "Completeness": [], "Conciseness": []}

    for r in results:
        if r is None:
            continue
        obj: Dict[str, Any] | None
        if isinstance(r, dict):
            obj = r
        elif isinstance(r, str):
            obj = _extract_json_obj(r)
        else:
            obj = None
        if not obj:
            continue

        for k in scores.keys():
            v = obj.get(k)
            if isinstance(v, (int, float)):
                scores[k].append(float(v))

    return {k: (sum(v) / len(v) if v else None) for k, v in scores.items()}


def evaluate_rag(retriever, num_questions: int = 5) -> Dict[str, Any]:
    """
    Quick evaluation aligned with the original repository style.

    This function:
    - generates `num_questions` questions
    - retrieves context with `retriever.invoke(question)`
    - asks the LLM to rate the retrieval quality with 3 scores (1-5)
    """
    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

    eval_prompt = PromptTemplate.from_template(
        """
Evaluate the following retrieval results for the question.

Question: {question}
Retrieved Context: {context}

Rate on a scale of 1-5 (5 being best) for:
1. Relevance
2. Completeness
3. Conciseness

Return JSON with keys: Relevance, Completeness, Conciseness.
"""
    )
    eval_chain = eval_prompt | llm | StrOutputParser()

    question_gen_prompt = PromptTemplate.from_template(
        "Generate {num_questions} diverse test questions about climate change (one per line):"
    )
    question_chain = question_gen_prompt | llm | StrOutputParser()
    questions = [q.strip() for q in question_chain.invoke({"num_questions": num_questions}).splitlines() if q.strip()]

    results: List[str] = []
    for q in questions:
        docs = retriever.invoke(q)
        context_text = "\n".join([d.page_content for d in docs])
        results.append(eval_chain.invoke({"question": q, "context": context_text}))

    return {
        "questions": questions,
        "results": results,
        "average_scores": calculate_average_scores(results),
    }

