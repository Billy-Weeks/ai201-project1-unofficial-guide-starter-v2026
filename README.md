# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->
Billy Weeks; Corpus: city_guides

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

## Chunking Strategy

**Chunk size: 400 characters maximum**
**Overlap: 0**

I split the city-guide documents at paragraph boundaries and keep headings with the content they introduce. I chose this because the corpus is organized into labeled sections with short, meaningful paragraphs. Splitting at these boundaries should preserve complete ideas better than fixed character windows.

After testing, I found that 400 characters provides enough context for these guides while still keeping chunks focused. A smaller limit might work for this corpus, but 400 is a reasonable balance between perserving context and avoiding unrelated information.

The splitter produced 106 chunks, averaging 271 characters. The shortest was 54 characters and the longest was 399 characters

## Sample Chunks

**Chunk 1** — source: `guide_accessibility.md#0` — produced by: `chunker.py::split_documents`

```
======================================================================
Chunk 1  |  source: guide_accessibility.md#0  |  produced by: chunker.py::split_documents
======================================================================
# Getting around the region with limited mobility

An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.

```

**Chunk 2** — source: `guide_corry_vale.md#5` — produced by: `chunker.py::split_documents`

```
======================================================================
Chunk 2  |  source: guide_corry_vale.md#5  |  produced by: chunker.py::split_documents
======================================================================
## Where to stay

Perhaps thirty beds in the entire valley, spread across two pubs and a handful of farmhouse rooms. In summer these are booked months ahead. Camping is permitted on two marked fields and nowhere else.

```

**Chunk 3** — source: `guide_givens_mill.md#2` — produced by: `chunker.py::split_documents`

```
======================================================================
Chunk 3  |  source: guide_givens_mill.md#2  |  produced by: chunker.py::split_documents
======================================================================
## Getting around

Everything is on one street along the river. The mill is at one end and the church at the other, eight minutes apart. The riverside path continues in both directions for as far as you want to walk.

```

**Chunk 4** — source: `guide_marchwood.md#0` — produced by: `chunker.py::split_documents`

```
======================================================================
Chunk 4  |  source: guide_marchwood.md#0  |  produced by: chunker.py::split_documents
======================================================================
# Marchwood

Marchwood is the regional hub — 180,000 people, the junction everyone changes trains at, and a city most visitors pass through rather than stop in. That is a mistake, though an understandable one, since almost nothing of interest is near the station.

```

**Chunk 5** — source: `guide_regional_transport.md#5` — produced by: `chunker.py::split_documents`

```
======================================================================
Chunk 5  |  source: guide_regional_transport.md#5  |  produced by: chunker.py::split_documents
======================================================================
Parking is the constraint rather than driving. Both Halden Bay lots fill by
10am on summer weekends. Kestrelford's lower car park is free and involves a
steep walk up.

```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question: Which town has a step-free mill museum?**

```
(.venv) meznu@BillyLaptop:/mnt/c/CodePath_AI-2/ai201-project1-unofficial-guide-starter-v2026$ python app.py --corpus city_guides ask "Which town has a step-free mill museum?"
  (best distance 0.384, cutoff 0.6)

```

**Answer:**

```

Brightwater has a step-free mill museum, according to guide_accessibility.md.

Sources retrieved: guide_accessibility.md, guide_brightwater.md, guide_givens_mill.md, guide_marchwood.md


```

**Retrieval setting:**

I kept the default top-k value of 5 after inspecting the returned chunks. The
relevant chunks appeared in the results without too much unrelated material.

**My relevance cutoff:**

0.6

**Explanation:**
I kept the starter cutoff of 0.6 because it correctly separated all five in-corpus questions from all five out of scope questions. Although a slightly higher cutoff might also work, say 0.75 or 0.8, there was no evidence that changing it would improve results, and raising it could allow weaker matches through.


| Question | In corpus? | Best distance |
|-------------------------------------------------------------------------|---|---|
| "Which town has a step-free mill museum?"                               | yes | 0.3835 |
| "Which town is a regional hub?" | yes | 0.5521 |
| "Which town is difficult to reach by car, but easy to explore on foot?" | yes | 0.4154 |
| "In Kestrelford, what is the reason most people come back?" | yes | 0.5313 |
| "When is arguably the best week of the year in Brightwater?" | yes | 0.3575 |
| "What is the capital of Mongolia?" | no | 0.8026 |
| "How do I change the oil in a diesel engine?" | no | 0.8917 |
| "Who won the 1994 World Cup?" | no | 0.9360 |
| "What is the recommended dosage of ibuprofen for a headache?" | no | 0.8486 |
| "How do I write a for loop in Rust?" | no | 0.8130 |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.**

**2.**

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

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
