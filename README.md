[README.md](https://github.com/user-attachments/files/24496574/README.md)

## NLDB Engine


An LLM-Driven Natural Language Database Engine with Cryptographic HITL Concurrency Control
## Overview
The **NLDB Engine is a lightweight, LLM-core–driven Natural Language Database system** designed to translate natural language queries into safe, verifiable database operations.

The system is intentionally lightweight:

  * It avoids heavyweight locking mechanisms

  * It does not modify underlying database internals

  * It operates as an **external orchestration layer**

At its core, a **Large Language Model (LLM)** performs natural language understanding and SQL generation, while **FastAPI connects and orchestrates all pipeline components**. This modular design allows the system to remain fast, stateless, and easy to integrate with existing databases.

To address correctness in **Human-in-the-Loop (HITL)** workflows, the engine integrates **cryptographic SHA** hashing to enforce data integrity and concurrency safety. Instead of locks or version counters, the system validates execution by **cryptographically verifying that the approved data state has not changed**.

By combining:

  * **LLM reasoning** for flexibility,

  *  **FastAPI orchestration** for deterministic control,

  * **Cryptographic verification** for integrity,

the NLDB Engine provides a scalable and lightweight solution for deploying LLM-powered database interfaces in concurrent, real-world environments.
## System Philosophy

The NLDB Engine is designed around the recognition that modern AI systems are **inherently probabilistic**, while **databases demand deterministic correctness**. This mismatch becomes especially critical in **Human-in-the-Loop (HITL)** pipelines, where human approvals can become invalid due to concurrent data changes.

To resolve this tension, the system follows a **layered and lightweight philosophy**, where each component is responsible for a distinct form of correctness, and no component is trusted beyond its strengths.

**1. LLMs Are Reasoners, Not Authorities**

Large Language Models excel at:

* Understanding ambiguous natural language

* Inferring user intent

* Generating candidate SQL queries

However, LLM outputs are **non-deterministic** and **not correctness-guaranteed**.

Therefore, in this system:

* The **LLM core proposes**, but does not decide.

* Every LLM-generated query is treated as a **hypothesis**, not a final action.

* This ensures that reasoning power is utilized without granting unchecked authority or execution privileges.



**2. Humans Provide Semantic Validation**

Humans are introduced into the pipeline to:

* Validate query intent

* Catch semantic or contextual errors

* Enforce domain-specific judgment

However, human validation alone is insufficient in concurrent systems:

* Humans reason over snapshots, not live data

* Time gaps introduce the risk of stale approvals

Thus, human decisions must be state-bound, not trust-based.
Approval without state verification is treated as unsafe by design.


**3. FastAPI as a Deterministic and Lightweight Orchestrator**

FastAPI acts as the deterministic backbone of the system:

* Enforces strict execution order

* Separates reasoning, validation, and execution

* Ensures no step bypasses cryptographic checks

FastAPI does **not interpret meaning**—it enforces protocol correctness.

By remaining stateless and external to the database engine, FastAPI enables:

* Lightweight orchestration

* Asynchronous, low-latency pipelines

* Easy integration without intrusive database changes

This clean separation prevents logic leakage between components and keeps execution fast.



**4. Cryptography as the Source of Truth**

Cryptographic hashing is elevated from a security mechanism to a correctness primitive.

Instead of asking:

    “Do we trust this query?”

The system asks:

    “Can this query be cryptographically proven to be valid for the current state?”

By binding:

* Database state

* Schema

* Query intent

to a *SHA hash*, the system guarantees:

* Immutability of approvals

* Automatic staleness detection

* Stateless concurrency control

No execution occurs without cryptographic proof.

**5. Lightweight and Fast-by-Design Validation**

The system is intentionally designed to remain lightweight and responsive:

* No locks

* No long-lived transactions

* No database engine modifications

Query validation is reduced to:

* A deterministic hash computation

* A constant-time hash comparison

This enables:

* Quick validation

* Immediate rejection of stale queries

* Fast execution once validation succeeds

LLM latency is isolated to query generation and regeneration, ensuring that validation and execution remain deterministic and fast.

**6. Correctness Over Convenience**

* The system intentionally favors:

* Rejection over unsafe execution

* Regeneration over stale execution

* Proof over assumption




## Core Components

**1. LLM Core:**
 Translates natural language queries into SQL and extracts query intent.
Acts as a reasoning engine, not an execution authority.

**2. FastAPI Pipeline Layer:**
Orchestrates the end-to-end workflow between the LLM, HITL interface, cryptographic validation, and database execution.
Ensures deterministic, lightweight, and stateless request handling.

**3. Cryptographic Validation Module (SHA):**
Generates and verifies cryptographic hashes over query-relevant data, schema, and intent.
Enforces data integrity, staleness detection, and concurrency safety.

**4. Human-in-the-Loop (HITL) Interface:**
Enables semantic validation of LLM-generated queries.
Approvals are cryptographically bound to a specific database state.

**5. Database Execution Engine:**
Executes queries only after successful hash validation, guaranteeing correctness under concurrency.


## Problem Addressed

**HITL + LLM Concurrency Gap**

In Human-in-the-Loop AI systems:

* Humans approve LLM-generated queries.

* Databases may change **between approval** and **execution.**

* This creates stale approvals, race conditions, and integrity violations.

Traditional OCC does not align well with LLM pipelines.         


## HITL Workflow

* User submits a natural language query.

* LLM core generates SQL and intent metadata.

* FastAPI triggers SHA **hash computation**.

* Human reviews and approves the query.

* Before execution, FastAPI re-validates the hash.

* Execution proceeds only **if hashes match**.


## Custom AST & Regular Expression Validators

**AST-Based Validation**

* LLM-generated SQL is parsed into a custom AST(Abstract Syntax Tree)

* The AST is analyzed to:

  *  Enforce allowed query structures

  * Detect forbidden operations (e.g., destructive commands)

  * Restrict query scope and complexity

* Ensures **semantic structure correctness**, not just string-level safety

AST validation is **deterministic, fast, and independent** of the database engine.

**Regular Expression Validation**

* Regex-based rules provide rapid pattern-level checks for:

  * Disallowed keywords or clauses

  * Unsafe query patterns

  * Policy violations

Acts as a **lightweight guardrail** before deeper validation stages

Regex validation is intentionally simple to maintain **low latency and predictability**.



## Project Status & Ongoing Development

**Current Status**

*  Functional Prototype Completed

* LLM core integrated for NL → SQL translation

* FastAPI-based pipeline orchestration in place

* Custom AST and regex validators implemented

* Cryptographic (SHA) HITL concurrency validation working end-to-end

* Human approval bound to database state

* Safe query execution under concurrent update

The system currently supports **lightweight, fast validation and execution** with strong data integrity guarantees in HITL workflows.


**Ongoing Development**


**Retrieval-Augmented Validation Pipeline**

To further reduce **LLM hallucinations and semantic drift**, the project is actively integrating a retrieval pipeline that:

Retrieves previously validated queries and execution patterns

Grounds LLM generation in **historically correct SQL templates**

Reduces reliance on free-form generation

This shifts the system toward **evidence-backed query generation** rather than pure probabilistic reasoning.



**RedisStack-Based Semantic Caching (Dockerized)**

The project is integrating RedisStack (via Docker) to:

* Store embeddings of natural language queries

* Cache validated SQL queries and intent hashes

* Skip redundant LLM calls for semantically similar queries

This enables:

* Lower latency

* Reduced API costs

* More deterministic behavior

* Improved scalability under repeated query patterns
