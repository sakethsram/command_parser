# MX80 CLI Parsing Pipeline

This project implements an offline, class-based CLI parsing pipeline for
Juniper MX80 router outputs.

The goal is to transform raw CLI text into structured, in-memory Python
objects using a clean, layered design.

## Scope

- Platform: Juniper MX80 only
- Mode: Offline parsing (no device connections)
- Output: In-memory Python objects (JSON-like)
- Persistence: None (no files written)

## File Structure

mx80_cli_parser/
├── raw_cli_dump.txt
├── command_segmenter.py
├── mx80_models.py
├── mx80_parser_engine.py
└── README.md

## Architecture Overview

The pipeline consists of three strictly separated stages:

### 1. Segmentation Layer

File: `command_segmenter.py`

- Reads raw CLI text
- Identifies each command and its corresponding output
- Produces an in-memory mapping of:
  command → raw output

This layer performs NO parsing and NO field extraction.

---

### 2. Model Layer

File: `mx80_models.py`

- Defines Python classes that represent the expected structure of parsed data
- Acts as a schema or contract
- Contains no parsing logic

---

### 3. Parsing Layer

File: `mx80_parser_engine.py`

- Consumes segmented CLI output
- Uses pyATS / Genie as the primary parser
- Uses regex only as a fallback or normalization step
- Produces structured Python objects that conform to the models

---

## Design Principles

- Single responsibility per file
- No hardcoded assumptions outside models
- Genie is preferred but not blindly trusted
- Parsing logic is isolated from representation
- Easy to extend for additional commands later

## Future Extensions

- JSON serialization
- Excel export
- Database ingestion
- REST API exposure

These can be added without changing the core architecture.
