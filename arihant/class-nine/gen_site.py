import json, os

SITE = "/home/claude/site"
TESTS_DIR = os.path.join(SITE, "tests")
os.makedirs(TESTS_DIR, exist_ok=True)

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Baklee's Maths Practice</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Lora:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/style.css">
</head>
<body>

<div class="margin-rule"></div>
<div class="wrap">

  <a class="back-link" href="../index.html">&larr; All tests</a>

  <header class="site-header" style="padding-top:0;">
    <p class="eyebrow">{chapter} &middot; {set_label}</p>
    <h1>{title}</h1>
    <div class="test-meta-bar">
      <span>📝 {num_q} Questions</span>
      <span>🎯 {total_marks} Marks</span>
      <span>⏱ {time} Minutes</span>
    </div>
  </header>

  <main id="questions">
{questions_html}
  </main>

  <div class="action-bar">
    <button class="btn primary" id="submitBtn">Submit &amp; check score</button>
    <button class="btn" id="keyBtn">Show / hide hints</button>
    <button class="btn" id="resetBtn">Reset</button>
  </div>

  <div class="score-box" id="scoreBox">
    <div class="score-num" id="scoreNum">—</div>
    <div class="score-label" id="scoreLabel"></div>
  </div>

  <footer class="site-footer">
    {chapter} &middot; CBSE / NCERT Class IX
  </footer>

</div>

<script>
window.TEST = {test_json};
</script>
<script src="../assets/test-engine.js"></script>
</body>
</html>
"""

SECTION_DIVIDER = """    <div class="section-divider {diff_class}">
      <span class="label">{label}</span>
      <span class="rule"></span>
      <span class="marks">{marks_each} mark{plural} each</span>
    </div>
"""

QUESTION_TEMPLATE = """    <div class="question">
      <div class="q-num-row">
        <span class="q-num">Q{num}</span>
        <span class="diff-pill {diff_class}">{diff}</span>
      </div>
      <div class="q-text">{text}</div>
      <div class="options">
{options_html}
      </div>
      <div class="hint-box" id="hint-{num}"><strong>Hint:</strong> {hint}</div>
    </div>
"""

OPTION_TEMPLATE = '        <div class="opt" data-q="{num}" data-opt="{key}">{text}</div>'


def render_test(slug, title, chapter, set_label, time_min, sections, questions):
    """
    sections: list of (key, label, diff_class, from_q, to_q, marks_each)
    questions: list of dicts: num, diff (Easy/Medium/Hard), marks, text, options (list of (key,text)), correct, hint
    """
    diff_class_map = {"Easy": "easy", "Medium": "medium", "Hard": "hard"}

    html_parts = []
    section_starts = {s[3]: s for s in sections}  # from_q -> section tuple

    for q in questions:
        if q["num"] in section_starts:
            _, label, diff_class, f, t, marks_each = section_starts[q["num"]]
            plural = "" if marks_each == 1 else "s"
            html_parts.append(SECTION_DIVIDER.format(
                diff_class=diff_class, label=label, marks_each=marks_each, plural=plural
            ))

        opts_html = "\n".join(
            OPTION_TEMPLATE.format(num=q["num"], key=k, text=t) for k, t in q["options"]
        )
        html_parts.append(QUESTION_TEMPLATE.format(
            num=q["num"],
            diff_class=diff_class_map[q["diff"]],
            diff=q["diff"],
            text=q["text"],
            options_html=opts_html,
            hint=q["hint"],
        ))

    total_marks = sum(q["marks"] for q in questions)

    test_json_obj = {
        "title": title,
        "chapter": chapter,
        "marks": total_marks,
        "time": time_min,
        "questions": [
            {
                "num": q["num"],
                "diff": q["diff"],
                "marks": q["marks"],
                "correct": q["correct"],
            }
            for q in questions
        ],
    }

    page = PAGE_TEMPLATE.format(
        title=title,
        chapter=chapter,
        set_label=set_label,
        num_q=len(questions),
        total_marks=total_marks,
        time=time_min,
        questions_html="\n".join(html_parts),
        test_json=json.dumps(test_json_obj),
    )

    out_path = os.path.join(TESTS_DIR, f"{slug}.html")
    with open(out_path, "w") as f:
        f.write(page)
    print("Wrote", out_path)


# ============================================================
# SET 1 — Factorisation of Polynomials
# ============================================================

def sup(t, e):
    return f"{t}<sup>{e}</sup>"

sections_default = [
    ("A", "Easy", "easy", 1, 8, 1),
    ("B", "Medium", "medium", 9, 14, 2),
    ("C", "Hard", "hard", 15, 20, 3),
]

set1_questions = [
    dict(num=1, diff="Easy", marks=1,
         text=f"Which of the following is a factor of the polynomial {sup('x','2')} − 5x + 6?",
         options=[("A","x − 1"),("B","x − 2"),("C","x + 3"),("D","x + 6")],
         correct="B", hint="p(2) = 4 − 10 + 6 = 0, so (x − 2) is a factor."),
    dict(num=2, diff="Easy", marks=1,
         text="The zero of the polynomial p(x) = 2x + 5 is:",
         options=[("A","x = 5/2"),("B","x = −5/2"),("C","x = 2/5"),("D","x = −2/5")],
         correct="B", hint="2x + 5 = 0 ⟹ x = −5/2."),
    dict(num=3, diff="Easy", marks=1,
         text=f"Factorise: {sup('x','2')} − 9",
         options=[("A","(x − 3)(x − 3)"),("B","(x + 3)(x + 3)"),("C","(x − 3)(x + 3)"),("D","(x − 9)(x + 1)")],
         correct="C", hint="Difference of squares: a² − b² = (a−b)(a+b), here a=x, b=3."),
    dict(num=4, diff="Easy", marks=1,
         text="By the Factor Theorem, (x − a) is a factor of p(x) if and only if:",
         options=[("A","p(0) = 0"),("B","p(a) = 0"),("C","p(1) = a"),("D","p(−a) = 0")],
         correct="B", hint="Factor Theorem: (x − a) is a factor iff p(a) = 0."),
    dict(num=5, diff="Easy", marks=1,
         text=f"Is (x + 1) a factor of {sup('x','3')} + {sup('x','2')} + x + 1?",
         options=[("A","Yes"),("B","No"),("C","Cannot be determined"),("D","Only if x > 0")],
         correct="A", hint="Check p(−1): (−1)³+(−1)²+(−1)+1 = −1+1−1+1 = 0."),
    dict(num=6, diff="Easy", marks=1,
         text=f"Which identity is used to expand (x + 3){sup('','2')}?",
         options=[
            ("A", f"(a+b){sup('','2')} = {sup('a','2')} − 2ab + {sup('b','2')}"),
            ("B", f"(a+b){sup('','2')} = {sup('a','2')} + 2ab + {sup('b','2')}"),
            ("C", f"(a+b)(a−b) = {sup('a','2')} − {sup('b','2')}"),
            ("D", f"(a+b){sup('','3')} = {sup('a','3')} + {sup('b','3')}"),
         ],
         correct="B", hint="(a+b)² = a² + 2ab + b²."),
    dict(num=7, diff="Easy", marks=1,
         text=f"Factorise: 6{sup('x','2')} + 12x",
         options=[("A","6(x + 2)"),("B","6x(x + 2)"),("C","x(6x + 12)"),("D","Both B and C")],
         correct="D", hint="GCF is 6x: 6x²+12x = 6x(x+2). x(6x+12) is the same factorisation written differently."),
    dict(num=8, diff="Easy", marks=1,
         text=f"The value of p(x) = {sup('x','3')} − 2{sup('x','2')} + x − 1 at x = 1 is:",
         options=[("A","−1"),("B","0"),("C","1"),("D","2")],
         correct="A", hint="p(1) = 1 − 2 + 1 − 1 = −1."),

    dict(num=9, diff="Medium", marks=2,
         text=f"Factorise: {sup('x','2')} + 7x + 12",
         options=[("A","(x + 3)(x + 4)"),("B","(x + 2)(x + 6)"),("C","(x + 1)(x + 12)"),("D","(x − 3)(x − 4)")],
         correct="A", hint="Find two numbers with product 12 and sum 7: 3 and 4."),
    dict(num=10, diff="Medium", marks=2,
         text=f"Find the value of k if (x − 2) is a factor of {sup('x','3')} − 2{sup('x','2')} + kx − 4.",
         options=[("A","k = 2"),("B","k = 4"),("C","k = −2"),("D","k = 0")],
         correct="A", hint="Set p(2) = 0: 8 − 8 + 2k − 4 = 0 ⟹ k = 2."),
    dict(num=11, diff="Medium", marks=2,
         text=f"Factorise: 2{sup('x','2')} + 7x + 3",
         options=[("A","(2x + 1)(x + 3)"),("B","(2x + 3)(x + 1)"),("C","(x + 7)(2x + 3)"),("D","(2x − 1)(x − 3)")],
         correct="A", hint="Split 7x as 6x + x: 2x(x+3) + 1(x+3) = (2x+1)(x+3)."),
    dict(num=12, diff="Medium", marks=2,
         text=f"Using an identity, factorise: 4{sup('x','2')} − 12xy + 9{sup('y','2')}",
         options=[
            ("A", f"(4x − 9y){sup('','2')}"),
            ("B", f"(2x − 3y){sup('','2')}"),
            ("C", "(2x + 3y)(2x − 3y)"),
            ("D", "(4x − 3y)(x + 3y)"),
         ],
         correct="B", hint="(2x)² − 2(2x)(3y) + (3y)² = (2x − 3y)²."),
    dict(num=13, diff="Medium", marks=2,
         text=f"Factorise: {sup('x','3')} − 8 (using the identity {sup('a','3')} − {sup('b','3')})",
         options=[
            ("A", f"(x − 2)({sup('x','2')} + 2x + 4)"),
            ("B", f"(x − 2)({sup('x','2')} − 2x + 4)"),
            ("C", f"(x − 2){sup('','3')}"),
            ("D", f"(x + 2)({sup('x','2')} − 4)"),
         ],
         correct="A", hint="a³−b³ = (a−b)(a²+ab+b²), with a=x, b=2."),
    dict(num=14, diff="Medium", marks=2,
         text=f"If p(x) = {sup('x','3')} + 3{sup('x','2')} + 3x + 1, then p(−1) equals:",
         options=[("A","1"),("B","0"),("C","−1"),("D","8")],
         correct="B", hint="Notice p(x) = (x+1)³, so p(−1) = 0."),

    dict(num=15, diff="Hard", marks=3,
         text=f"Factorise completely: {sup('x','3')} − 2{sup('x','2')} − x + 2",
         options=[
            ("A","(x − 1)(x + 1)(x − 2)"),
            ("B","(x − 1)(x − 1)(x + 2)"),
            ("C","(x + 1)(x + 1)(x − 2)"),
            ("D", f"(x − 2)({sup('x','2')} + x − 1)"),
         ],
         correct="A", hint="Check p(1), p(−1), p(2) — all give zero, so all three are factors."),
    dict(num=16, diff="Hard", marks=3,
         text=f"Show that (2x − 1) is a factor of 2{sup('x','3')} − {sup('x','2')} − 4x + 2. Then find all factors.",
         options=[
            ("A", "(2x − 1)(x − √2)(x + √2)"),
            ("B", f"(2x − 1)({sup('x','2')} − 2)"),
            ("C", "Both A and B are correct"),
            ("D", f"(2x + 1)({sup('x','2')} − 2)"),
         ],
         correct="C", hint="p(½) = 0 confirms the factor. The quotient x²−2 factors further into (x−√2)(x+√2)."),
    dict(num=17, diff="Hard", marks=3,
         text=f"If a + b + c = 0, use the identity {sup('a','3')}+{sup('b','3')}+{sup('c','3')} = 3abc to evaluate: 1{sup('','3')} + (−3){sup('','3')} + 2{sup('','3')}",
         options=[("A","6"),("B","18"),("C","−18"),("D","0")],
         correct="C", hint="a+b+c = 1+(−3)+2 = 0, so the sum = 3abc = 3×1×(−3)×2 = −18."),
    dict(num=18, diff="Hard", marks=3,
         text=f"Factorise: {sup('x','3')} + 13{sup('x','2')} + 32x + 20 (use Factor Theorem to find one root first)",
         options=[
            ("A","(x + 1)(x + 2)(x + 10)"),
            ("B", f"(x + 1)({sup('x','2')} + 12x + 20)"),
            ("C","(x + 2)(x + 2)(x + 5)"),
            ("D","(x + 4)(x + 5)(x + 1)"),
         ],
         correct="A", hint="p(−1) = 0. Dividing gives x²+12x+20, which factors into (x+2)(x+10)."),
    dict(num=19, diff="Hard", marks=3,
         text=f"Expand using identity: (2x + y + z){sup('','2')} and verify the result for x = y = z = 1.",
         options=[
            ("A", f"4{sup('x','2')} + {sup('y','2')} + {sup('z','2')} + 4xy + 2yz + 4xz (value = 16)"),
            ("B", f"4{sup('x','2')} + {sup('y','2')} + {sup('z','2')} + 2xy + 2yz + 2xz (value = 12)"),
            ("C", f"4{sup('x','2')} + {sup('y','2')} + {sup('z','2')} + xy + yz + xz (value = 9)"),
            ("D", f"2{sup('x','2')} + {sup('y','2')} + {sup('z','2')} + 4xy + 2yz + 4xz (value = 14)"),
         ],
         correct="A", hint="(a+b+c)² = a²+b²+c²+2ab+2bc+2ca, with a=2x, b=y, c=z. At x=y=z=1: 4+1+1+4+2+4=16."),
    dict(num=20, diff="Hard", marks=3,
         text=f"Without actual division, prove that {sup('x','4')} + {sup('x','3')} − 7{sup('x','2')} − x + 6 is exactly divisible by (x−1)(x−2)(x+2)(x+3). What are all the zeros?",
         options=[
            ("A","x = 1, 2, −2, −3"),
            ("B","x = 1, −1, 2, −3"),
            ("C","x = 1, 2, 3, −2"),
            ("D","x = −1, −2, 2, 3"),
         ],
         correct="A", hint="Verify p(1)=p(2)=p(−2)=p(−3)=0 by direct substitution."),
]

render_test(
    slug="polynomials-set1",
    title="Factorisation of Polynomials",
    chapter="Polynomials (Ch. 2)",
    set_label="Set 1",
    time_min=45,
    sections=sections_default,
    questions=set1_questions,
)

# ============================================================
# SET 2 — Polynomials Mixed Review  (CORRECTED: Q9, Q13, Q17)
# ============================================================

set2_questions = [
    dict(num=1, diff="Easy", marks=1,
         text=f"The degree of the polynomial 5{sup('x','4')} − 3{sup('x','2')} + 7x − 1 is:",
         options=[("A","1"),("B","2"),("C","3"),("D","4")],
         correct="D", hint="Degree = highest power of x present, which is 4."),
    dict(num=2, diff="Easy", marks=1,
         text="Which of the following is a polynomial?",
         options=[("A","x + 1/x"),("B","√x + 3"),("C", f"{sup('x','2')} + 5x + 6"),("D","x^(1/2) − 2")],
         correct="C", hint="A polynomial needs non-negative integer powers of x — only option C qualifies."),
    dict(num=3, diff="Easy", marks=1,
         text="The number of zeros of the polynomial p(x) = (x − 1)(x + 2)(x − 3) is:",
         options=[("A","1"),("B","2"),("C","3"),("D","0")],
         correct="C", hint="Three distinct linear factors give three distinct zeros: 1, −2, 3."),
    dict(num=4, diff="Easy", marks=1,
         text=f"If p(x) = {sup('x','2')} + x + 1, then p(0) is:",
         options=[("A","0"),("B","1"),("C","2"),("D","3")],
         correct="B", hint="p(0) = 0 + 0 + 1 = 1."),
    dict(num=5, diff="Easy", marks=1,
         text=f"Which of the following is a zero of p(x) = {sup('x','2')} − 4?",
         options=[("A","x = 1"),("B","x = −1"),("C","x = 2"),("D","x = 4")],
         correct="C", hint="x² − 4 = 0 ⟹ x = ±2, so x = 2 is a zero."),
    dict(num=6, diff="Easy", marks=1,
         text=f"Using the identity, the value of (103){sup('','2')} is:",
         options=[("A","10600"),("B","10609"),("C","10690"),("D","10906")],
         correct="B", hint="(100+3)² = 100² + 2(100)(3) + 3² = 10000+600+9 = 10609."),
    dict(num=7, diff="Easy", marks=1,
         text="A polynomial of degree 2 is called a:",
         options=[("A","Linear polynomial"),("B","Cubic polynomial"),("C","Quadratic polynomial"),("D","Constant polynomial")],
         correct="C", hint="Degree 2 = quadratic; degree 1 = linear; degree 3 = cubic."),
    dict(num=8, diff="Easy", marks=1,
         text=f"The remainder when {sup('x','3')} + 1 is divided by (x + 1) is:",
         options=[("A","2"),("B","1"),("C","0"),("D","−1")],
         correct="C", hint="By Remainder Theorem, remainder = p(−1) = −1 + 1 = 0."),

    dict(num=9, diff="Medium", marks=2,
         text=f"If (x + 2) is a factor of {sup('x','3')} + a{sup('x','2')} − x − 2, find the value of a.",
         options=[("A","a = 1"),("B","a = 2"),("C","a = −1"),("D","a = 0")],
         correct="B", hint="Set p(−2)=0: −8 + 4a + 2 − 2 = 0 ⟹ 4a = 8 ⟹ a = 2."),
    dict(num=10, diff="Medium", marks=2,
         text=f"Factorise: {sup('x','2')} − x − 12",
         options=[("A","(x − 4)(x + 3)"),("B","(x + 4)(x − 3)"),("C","(x − 6)(x + 2)"),("D","(x + 6)(x − 2)")],
         correct="A", hint="Find two numbers with product −12 and sum −1: −4 and 3."),
    dict(num=11, diff="Medium", marks=2,
         text=f"Using the identity, expand: (2a − 3b){sup('','2')}",
         options=[
            ("A", f"4{sup('a','2')} + 9{sup('b','2')} − 12ab"),
            ("B", f"4{sup('a','2')} − 9{sup('b','2')} + 12ab"),
            ("C", f"4{sup('a','2')} + 9{sup('b','2')} + 12ab"),
            ("D", f"2{sup('a','2')} − 3{sup('b','2')} − 12ab"),
         ],
         correct="A", hint="(2a−3b)² = (2a)² − 2(2a)(3b) + (3b)² = 4a² − 12ab + 9b²."),
    dict(num=12, diff="Medium", marks=2,
         text=f"Factorise: {sup('x','3')} + 27",
         options=[
            ("A", f"(x + 3)({sup('x','2')} − 3x + 9)"),
            ("B", f"(x + 3)({sup('x','2')} + 3x + 9)"),
            ("C", f"(x − 3)({sup('x','2')} + 3x + 9)"),
            ("D", f"(x + 3){sup('','3')}"),
         ],
         correct="A", hint="a³+b³ = (a+b)(a²−ab+b²), with a=x, b=3."),
    dict(num=13, diff="Medium", marks=2,
         text=f"What is the remainder when 2{sup('x','3')} − 3{sup('x','2')} + x − 5 is divided by (x − 2)?",
         options=[("A","−3"),("B","3"),("C","−1"),("D","1")],
         correct="D", hint="By Remainder Theorem, remainder = p(2) = 2(8) − 3(4) + 2 − 5 = 16−12+2−5 = 1."),
    dict(num=14, diff="Medium", marks=2,
         text="Evaluate using identity: 99 × 101",
         options=[("A","9999"),("B","9801"),("C","10001"),("D","9900")],
         correct="A", hint="(100−1)(100+1) = 100² − 1² = 10000 − 1 = 9999."),

    dict(num=15, diff="Hard", marks=3,
         text=f"Factorise completely: 2{sup('x','3')} + 3{sup('x','2')} − 11x − 6",
         options=[
            ("A","(x + 3)(x − 2)(2x + 1)"),
            ("B","(x − 3)(x + 2)(2x − 1)"),
            ("C","(x + 3)(2x − 1)(x + 2)"),
            ("D","(x − 1)(2x + 3)(x + 2)"),
         ],
         correct="A", hint="p(−3) = 0 gives the first factor; dividing leaves 2x²−3x−2 = (2x+1)(x−2)."),
    dict(num=16, diff="Hard", marks=3,
         text=f"If x + y + z = 9 and xy + yz + zx = 26, find {sup('x','2')} + {sup('y','2')} + {sup('z','2')}.",
         options=[("A","29"),("B","81"),("C","55"),("D","27")],
         correct="A", hint="(x+y+z)² = x²+y²+z² + 2(xy+yz+zx) ⟹ 81 = (x²+y²+z²) + 52 ⟹ x²+y²+z² = 29."),
    dict(num=17, diff="Hard", marks=3,
         text=f"Factorise: {sup('x','3')} − 3{sup('x','2')} − 9x − 5",
         options=[
            ("A", f"(x + 1){sup('','2')}(x − 5)"),
            ("B","(x − 1)(x + 1)(x − 5)"),
            ("C","(x + 1)(x + 1)(x + 5)"),
            ("D","(x − 1)(x − 1)(x − 5)"),
         ],
         correct="A", hint="p(−1) = 0 (a repeated root) and p(5) = 0. So the factorisation is (x+1)²(x−5)."),
    dict(num=18, diff="Hard", marks=3,
         text=f"Using the identity for (a + b + c){sup('','2')}, expand: (x + 2y − 3z){sup('','2')}",
         options=[
            ("A", f"{sup('x','2')} + 4{sup('y','2')} + 9{sup('z','2')} + 4xy − 12yz − 6xz"),
            ("B", f"{sup('x','2')} + 4{sup('y','2')} + 9{sup('z','2')} + 4xy + 12yz − 6xz"),
            ("C", f"{sup('x','2')} + 2{sup('y','2')} + 3{sup('z','2')} + 4xy − 6yz − 6xz"),
            ("D", f"{sup('x','2')} + 4{sup('y','2')} + 9{sup('z','2')} − 4xy − 12yz + 6xz"),
         ],
         correct="A", hint="Use a=x, b=2y, c=−3z in a²+b²+c²+2ab+2bc+2ca."),
    dict(num=19, diff="Hard", marks=3,
         text=f"If p = 2 − a, show that {sup('a','3')} + 6ap + {sup('p','3')} − 8 = 0. Which identity explains this?",
         options=[
            ("A", f"(a+b+c){sup('','3')} identity; value = 0"),
            ("B", f"{sup('a','3')} + {sup('b','3')} + {sup('c','3')} − 3abc = (a+b+c)(...); value = 0"),
            ("C", f"(a−b){sup('','3')} identity; value = 0"),
            ("D", "Remainder Theorem; value = 8"),
         ],
         correct="B", hint="Since a + p + (−2) = 0, the identity a³+p³+(−2)³−3ap(−2)=0 applies directly."),
    dict(num=20, diff="Hard", marks=3,
         text=f"Factorise: {sup('x','4')} − {sup('y','4')} and hence evaluate (3.5){sup('','4')} − (2.5){sup('','4')}.",
         options=[
            ("A", f"({sup('x','2')}+{sup('y','2')})(x+y)(x−y); value = 96"),
            ("B", "(x+y)(x−y)(x+iy)(x−iy); value = 96"),
            ("C", f"({sup('x','2')}+{sup('y','2')})(x+y)(x−y); value = 111"),
            ("D", "(x−y)⁴; value = 1"),
         ],
         correct="C", hint="x⁴−y⁴ = (x²+y²)(x+y)(x−y). At x=3.5, y=2.5: (12.25+6.25)(6)(1) = 18.5×6 = 111."),
]

render_test(
    slug="polynomials-set2",
    title="Polynomials — Mixed Review",
    chapter="Polynomials (Ch. 2)",
    set_label="Set 2",
    time_min=45,
    sections=sections_default,
    questions=set2_questions,
)

print("\nAll test pages generated.")
