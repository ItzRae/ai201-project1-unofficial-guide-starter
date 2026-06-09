# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

The domain for this project is an unofficial Amherst College student survival guide that combines information about academics, dining, campus life, student experiences, and social culture. While Amherst provides extensive official resources, many practical questions students have—such as what campus life is really like, how students feel about dining options, or how to navigate social and academic challenges—are answered through scattered blogs, student discussions, and community forums. This brings together those perspectives into a searchable knowledge base that reflects both institutional information and authentic student experiences.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Amherst Student Blog | Survival Guide for First Years | https://amherststudent.com/article/the-first-years-survival-guide/ | 
| 2 | Reddit | Reddit thread of student life | https://www.reddit.com/r/amherstcollege/comments/1r2pfbm/amherst_student_life/ |
| 3 | Official Amherst College website | Information about AC Dining | https://www.amherst.edu/campuslife/housing-dining/dining/about-ac-dining/meal_plans_2025-2026 |
| 4 | Blog | Blog article of an AC guide | https://www.collegekidguide.com/home-1/blog-post-title-three-9c5lk |
| 5 | Official AC Website | FAQ of Dining Plans/Info | https://www.amherst.edu/campuslife/housing-dining/dining/about-ac-dining/faq |
| 6 | Official AC Website | Academic information | https://www.amherst.edu/academiclife/support |
| 7 | Official AC Website | Campus Life information | https://www.amherst.edu/campuslife |
| 8 | Niche polls site | Student Polls about campus life | https://www.niche.com/colleges/amherst-college/campus-life/ |
| 9 | Amherst Student blog | About community/social life in AC | https://amherststudent.com/article/the-anguish-of-amherst-college-students/ |
| 10 | Bigfuture College Site | Student and campus details about AC | https://bigfuture.collegeboard.org/colleges/amherst-college/campus-life |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
