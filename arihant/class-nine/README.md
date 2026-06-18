# Baklee's Maths Practice

A small, growing site of interactive CBSE Class IX Maths chapter tests — built page by page as a study companion. Click into a test, answer the MCQs, and get instant scoring with hints on anything missed.

## Publishing to GitHub Pages

1. Create a new GitHub repository (e.g. `amans-maths-practice`).
2. Copy everything in this folder (`index.html`, `assets/`, `tests/`) into the repo root.
3. Commit and push:
   ```bash
   git init
   git add .
   git commit -m "Initial site: Polynomials Set 1 & 2"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<repo-name>.git
   git push -u origin main
   ```
4. On GitHub: **Settings → Pages → Source → Deploy from branch → `main` / `(root)`** → Save.
5. Your site will be live at:
   `https://<your-username>.github.io/<repo-name>/`

## Folder structure

```
.
├── index.html              ← homepage, organized by chapter
├── assets/
│   ├── style.css           ← shared "notebook" styling
│   └── test-engine.js      ← shared scoring/hint logic
└── tests/
    ├── polynomials-set1.html
    └── polynomials-set2.html
```

## Adding a new test later

1. Open `gen_site.py` (kept alongside this project, not deployed) — copy the pattern used for `set2_questions` and define a new list of question dicts for your new chapter/set.
2. Call `render_test(...)` with a new `slug`, `title`, `chapter`, and your sections/questions.
3. Re-run the script — it writes a new file into `tests/`.
4. Add a new `<a class="test-card">` block to `index.html` under the right chapter section (or create a new `<section class="chapter-section">` for a brand-new chapter).
5. Commit and push — GitHub Pages updates automatically within a minute or two.

Each question needs: `num`, `diff` (Easy/Medium/Hard), `marks`, `text`, `options` (list of `(key, text)` tuples), `correct` (the right option key), and `hint` (shown if the student gets it wrong, or on demand via "Show / hide hints").
