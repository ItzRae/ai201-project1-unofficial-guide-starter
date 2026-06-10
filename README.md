# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

     A campus guide for students at Amherst College, designed for incoming, prospective, or current students who want to learn more about academics, social life, and campus culture, etc -- valuable because many student experiences and opinions are scattered across blogs, Reddit threads, and official college webpages, making it difficult to find a complete picture of campus life in one place.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Amherst Student: First-Year Survival Guide | Student newspaper article | documents/first-year-survival-guide.txt |
| 2 | Reddit: Amherst student life thread | Reddit discussion thread | documents/reddit-amherst-student-life.txt |
| 3 | Amherst College AC Dining Meal Plans | Official college webpage | documents/meal-plans.txt |
| 4 | College Kid Guide: Amherst guide | Student/blog guide | documents/college-kid-guide-amherst.txt |
| 5 | Amherst College Dining FAQ | Official college FAQ | documents/dining-faq.txt |
| 6 | Amherst College Academic Support | Official college webpage | documents/academic-resources.txt |
| 7 | Amherst College Campus Life | Official college webpage | documents/campus-life.txt |
| 8 | Niche Amherst Campus Life Polls | Student review/poll site | documents/niche-campus-life.txt |
| 9 | Amherst Student: The Anguish of Amherst College Students | Student newspaper article | documents/amherst-social-life.txt |
| 10 | BigFuture Amherst Campus Life | College information webpage | documents/bigfuture-campus-life.txt |
---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
I used chunks of around 750 characters, with most chunks falling between about 500 and 750 characters.

**Overlap:**
I used about 100 characters of overlap between chunks so that important context would not be lost if an idea crossed a chunk boundary.

**Why these choices fit your documents:**
My documents are mostly official AC webpages, student articles, FAQs, and Reddit content. A medium chunk size works well because it is large enough to keep a full idea together, such as one FAQ answer or one paragraph of student advice, but not so large that unrelated topics get mixed together. I also cleaned the text before chunking by removing extra whitespace and using `.txt` files with title, source, and URL metadata.

**Final chunk count:**
85

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** 
all-MiniLM-L6-v2 from the sentence-transformers library

**Production tradeoff reflection:**
I chose it because it runs locally, is easy to set up, and provides good semantic search performance for a  small project like this. It is fast (with embedding and retreival steps) without needing an API key.

If I were deploying this system for real users and cost was not a constraint, I would mainly consider retrieval accuracy and latency. A larger embedding model could better understand nuanced student opinions and informal language/slang, which might improve retrieval quality. But larger models are slower and require more computational resources, which could increase response times for users.

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
My generation step uses a system prompt that tells the model to answer only from the retrieved context. The instruction says that if the answer can't supported by the retrieved chunks, the model must say along the lines of: “I don’t have enough information to answer this.” The prompt also tells the model not to use outside knowledge or make assumptions beyond the retrieved text.

**How source attribution is surfaced in the response:**
Instead of asking the model to generate citations on its own, I attach source information from the retrieved chunks directly to the final response. Each chunk includes metadata such as the title, source, URL, and file name, which are displayed in a Sources section below the answer. This can make sure that users can see exactly where the information came from.

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What academic support resources does Amherst list for students? | Should cite Amherst’s academic support page and mention the writing center, the strategic learning center, Frost Library resources, etc | Amherst provides support in areas such as writing, research, and quantitative realms, as well as resources for students with documented disabilities. Additionally, the First-Year Survival Guide (Amherst Student) mentions specific resources including the Writing Center, the Q Center for quantitative classes, and the library for research assistance (source: First-Year Survival Guide). The College also offers access to faculty advisors, experts in particular skill areas, and entire offices that provide academic-support services .| Relevant | Accurate |
| 2 | What do students say about Amherst social life or campus community? | Students report that Amherst's social life is heavily clique-based, with limited interaction between groups, occasional feelings of isolation, and a strong work-hard/play-hard culture centered around parties and campus traditions. | Students express feelings of anguish and suffocation due to the social division caused by cliques, which prevent cross-group interaction. Additionally, students mention the pressure to enjoy their youth while they can, as it is a transitory stage between childhood and adulthood. They also describe the repetitive nature of the average week, characterized by a "work hard, play hard" mentality (source: The Anguish of Amherst College Students). However, Campus Life at Amherst (Amherst College) presents a more positive view, suggesting that Amherst has a "true college-town feel" with many opportunities for social life and community engagement | Relevant | Accurate|
| 3 |  What advice do students give incoming, first-year students at Amherst? | They recommend that first-years embrace new experiences, take advantage of campus resources, make diverse social connections, communicate with professors, and get involved in the campus community.| The system summarized advice from the First-Year Survival Guide, including being open to change, embracing uncertainty, staying connected to sources of comfort, managing time and commitments intentionally, and avoiding pressure to have everything figured out immediately.| Relevant | Partially Accurate |
| 4 | How do meal plans work at the Amherst College dining hall? | First-year students receive the Unlimited meal plan, which allows unlimited Dining Hall access using an Amherst ID card or mobile app. Meal swipes can also be used at Keefe Grab and Go, and students can manage balances through the Mammoth Mobile App. | Correctly explained that first-year students are automatically enrolled in the Unlimited meal plan, described Dining Hall access, meal plan options, Keefe Grab & Go access, guest passes, and rules for changing meal plans between semesters. | Relevant | Accurate |
| 5 | What do students say about things to do in Amherst town? | Students say Amherst offers lots of restaurants, cafes, bars, shopping areas, outdoor activities, and campus events. Popular places to hang/visit include downtown Amherst, Route 9, Northampton, local hiking trails, Puffer's Pond, and the Norwottuck Rail Trail. | Explained that Amherst has shops, restaurants, a library, nearby Northampton, opportunities through the Five Colleges, and local destinations such as the Inn on Boltwood, AJ Hastings, and Amherst Books. | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** Can I get a meal plan at Amherst?

**What the system returned:** The system answered "Yes" and explained Amherst meal plan options.

**Root cause (tied to a specific pipeline stage):**
This was a limitation at the generation stage. The retrieval system  found meal plan documents, but the generation model assumed the user was an Amherst student, so the model failed to recognize that the question required additional context about the user's situation/eligibility.

**What you would change to fix it:**
I would add a clarification step before generation for ambiguous questions involving eligibility, personal status, or user-specific circumstances. The system could perhaps ask follow-up questions when the retrieved documents don't contain enough information to answer for a particular user
---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
The planning spec helped me stay organized because I already knew what documents I was working with, what chunk size I wanted, and what retrieval setup I was aiming for before writing code. It also made it easier to prompt Claude because I could give it my chunking strategy, embedding model, top-k value, and pipeline diagram instead of asking it to make those decisions from scratch.


**One way your implementation diverged from the spec, and why:**
One thing that changed was the chunking approach. I originally planned around 600–800 character chunks with 100 characters of overlap, but my first version produced too many tiny fragments and chunks that started in the middle of words. So I changed the chunking function to be more paragraph-aware and added filtering for very small chunks so the final chunks were more readable for retrieval!

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

-  *What I gave the AI:* I gave Claude my Documents section, Chunking Strategy section, and the Milestone 3 requirements for ingestion and chunking.
- *What it produced:* it helped generate the ingestion script that loaded my `.txt` files, parsed title/source/URL metadata, cleaned the text, and split the documents into chunks.
- *What I changed or overrode:* I adjusted the chunking logic after inspecting the sample chunks because the first version created some awkward fragments. I changed it to make the chunks more readable, filtered out very small chunks, and checked the output manually before moving on


**Instance 2**

- *What I gave the AI:* I gave Claude my Retrieval Approach section and pipeline diagram, including the requirement to use the all-Mini model, ChromaDB, and top-k retrieval.
- *What it produced:* It helped draft the embedding and retrieval code, including loading chunks from `chunks.json`, embedding them with the SentenceTransformer model and writing a retrieval function.
- *What I changed or overrode:* I made sure the code preserved source metadata like title, URL, source file, and chunk index because I needed that later for citations. I also chose to use cosine distance instead of the default L2 distance after checking which metric made more sense for sentence-transformer embeddings. I reviewed and ran the model set up, chunk embedding, and metadata store code myself.
