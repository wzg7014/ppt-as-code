# AGENTS.md

This repository is a template for building presentation decks with an AI coding agent.

The agent should treat the deck as a project, not as a one-shot document. The human makes content and visual decisions. The agent handles structure, prompts, scripts, records, and Git hygiene.

## Default Language

Use Chinese by default unless the user asks for English.

Keep standard technical terms in English when they are clearer: Prompt, Git, API, release, agent, ref image.

## Project Goal

Help the user turn an outline, script, or presentation brief into a high-quality visual PPT workflow:

1. Import content
2. Plan pages
3. Define visual style
4. Generate candidate images page by page
5. Let the human choose and give feedback
6. Record every page decision
7. Commit progress at page-level granularity

## Core Rules

- Do not generate a whole deck blindly.
- Do not decide the final image for the user.
- Generate multiple candidates for each page when possible.
- Ask for confirmation before marking a page complete.
- Keep prompts, generated images, and records under the page directory.
- Keep API keys in `.env`; never commit secrets.
- Preserve the chosen visual system across pages by reusing reference images.
- Prefer small, page-level commits over large mixed commits.

## Phase 1: Initialize

If `progress.md` does not exist, initialize the project.

Ask for or create:

- `.env` with image API config
- `content/` with the user's script or outline
- visual style rules
- page plan
- `progress.md`
- `ppt-pages/XX/` directories

After reading the content, propose a concise page plan. Do not over-structure the deck if a simpler plan works.

## Phase 2: First Version

For each page:

1. Read `progress.md`
2. Read the matching content section
3. Discuss the page concept briefly
4. Ask whether to use a reference image
5. Write `ppt-pages/XX/init/gen.py`
6. Generate 3 candidates if the configured API is available
7. Ask the user which image they prefer
8. Iterate if needed
9. When the user confirms, write the record and update progress

Use the helper in `tools/gen_ppt_image.py`:

```python
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from gen_ppt_image import gen

PROMPT = """
Describe the slide image here.
"""

gen(prompt=PROMPT, page_dir=str(Path(__file__).parent), count=3)
```

## Phase 3: Revisions

When the user has feedback:

1. Collect feedback
2. Write a revision plan
3. Modify only the affected pages
4. Put revision files in `ppt-pages/XX/revN/`
5. Record what changed and why

## Generated Files

These are local project outputs and should normally stay untracked:

- `.env`
- `content/`
- `progress.md`
- `ppt-pages/`
- `ppt-ref-images/`

Examples under `examples/` are intentionally tracked.

## Quality Bar

A page is complete only when:

- the visual goal is clear
- generated candidates are saved
- the user has selected or approved the result
- the prompt and reference image choices are recorded
- `progress.md` reflects the current state

Keep the workflow practical. If the user's goal can be solved with a simpler structure, say so and use the simpler structure.
