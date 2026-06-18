// ============================================================
// Baklee's Maths Practice — shared test engine
// Expects a global `TEST` object defined in each test page:
// TEST = { title, chapter, marks, time, questions: [...] }
// questions: [{ num, diff, marks, correct }]
// ============================================================

(function () {
  const selected = {};
  let submitted = false;
  let timerInterval = null;

  function init() {
    document.querySelectorAll('.opt').forEach(el => {
      el.addEventListener('click', function () {
        if (submitted) return;
        const q = this.dataset.q;
        document.querySelectorAll(`.opt[data-q="${q}"]`).forEach(o => {
          o.classList.remove('selected', 'correct', 'wrong');
        });
        this.classList.add('selected');
        selected[q] = this.dataset.opt;
        const hint = document.getElementById('hint-' + q);
        if (hint) hint.classList.remove('show');
      });
    });

    const submitBtn = document.getElementById('submitBtn');
    if (submitBtn) submitBtn.addEventListener('click', submitTest);

    const keyBtn = document.getElementById('keyBtn');
    if (keyBtn) {
      keyBtn.style.display = 'none';
      keyBtn.addEventListener('click', toggleHints);
    }

    const resetBtn = document.getElementById('resetBtn');
    if (resetBtn) resetBtn.addEventListener('click', resetTest);

    startTimer();
  }

  // ---- Countdown timer ----

  function startTimer() {
    const minutes = (window.TEST && window.TEST.time) ? window.TEST.time : 45;
    let remaining = minutes * 60;

    const timerEl = document.getElementById('timerDisplay');
    if (!timerEl) return;

    function render() {
      const m = Math.floor(remaining / 60);
      const s = remaining % 60;
      timerEl.textContent = String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0');
      if (remaining <= 300) timerEl.classList.add('timer-warn');
      if (remaining <= 60)  timerEl.classList.add('timer-critical');
    }

    render();
    timerInterval = setInterval(function () {
      if (remaining <= 0) {
        clearInterval(timerInterval);
        timerEl.textContent = '00:00';
        if (!submitted) submitTest(true);
        return;
      }
      remaining--;
      render();
    }, 1000);
  }

  // ---- Submit ----

  function submitTest(autoSubmit) {
    if (submitted) return;

    const unattempted = window.TEST.questions.filter(q => !selected[q.num]).length;
    if (!autoSubmit && unattempted > 0) {
      const ok = confirm(
        unattempted + ' question' + (unattempted > 1 ? 's' : '') +
        ' not answered. Submit anyway?'
      );
      if (!ok) return;
    }

    submitted = true;
    clearInterval(timerInterval);

    // Lock options visually
    document.querySelectorAll('.opt').forEach(o => o.classList.add('locked'));

    const byDiff = {};
    let score = 0, total = 0, attempted = 0;

    window.TEST.questions.forEach(q => {
      total += q.marks;
      const diff = q.diff;
      if (!byDiff[diff]) byDiff[diff] = { correct: 0, total: 0, marks: 0, totalMarks: 0 };
      byDiff[diff].total++;
      byDiff[diff].totalMarks += q.marks;

      const opts = document.querySelectorAll(`.opt[data-q="${q.num}"]`);
      if (selected[q.num]) {
        attempted++;
        if (selected[q.num] === q.correct) {
          score += q.marks;
          byDiff[diff].correct++;
          byDiff[diff].marks += q.marks;
          opts.forEach(o => { if (o.dataset.opt === q.correct) o.classList.add('correct'); });
        } else {
          opts.forEach(o => {
            if (o.dataset.opt === selected[q.num]) o.classList.add('wrong');
            if (o.dataset.opt === q.correct) o.classList.add('correct');
          });
          const hint = document.getElementById('hint-' + q.num);
          if (hint) hint.classList.add('show');
        }
      } else {
        opts.forEach(o => { if (o.dataset.opt === q.correct) o.classList.add('correct'); });
      }
    });

    const pct = total > 0 ? Math.round((score / total) * 100) : 0;
    let grade;
    if (pct >= 90) grade = 'Outstanding! 🏅';
    else if (pct >= 75) grade = 'Well done! ✅';
    else if (pct >= 50) grade = 'Good effort — review the hints below.';
    else grade = 'Keep practising — check the hints on missed questions.';

    const scoreBox = document.getElementById('scoreBox');
    document.getElementById('scoreNum').textContent = score + ' / ' + total;
    document.getElementById('scoreLabel').textContent =
      attempted + ' of ' + window.TEST.questions.length + ' attempted · ' + pct + '% · ' + grade;

    // Difficulty breakdown
    const breakdownEl = document.getElementById('scoreBreakdown');
    if (breakdownEl) {
      const ORDER = ['Easy', 'Medium', 'Hard'];
      const colors = { Easy: 'green', Medium: 'amber', Hard: 'red' };
      breakdownEl.innerHTML = ORDER
        .filter(d => byDiff[d])
        .map(d => {
          const b = byDiff[d];
          return `<span class="breakdown-pill ${colors[d]}">${d}: ${b.correct}/${b.total} (${b.marks}/${b.totalMarks} marks)</span>`;
        }).join('');
    }

    saveBestScore(score, total, pct);

    scoreBox.style.display = 'block';
    scoreBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    // Swap submit button label and reveal hints toggle
    const submitBtn = document.getElementById('submitBtn');
    if (submitBtn) submitBtn.textContent = 'Submitted';
    const keyBtn = document.getElementById('keyBtn');
    if (keyBtn) keyBtn.style.display = '';
  }

  function toggleHints() {
    document.querySelectorAll('.hint-box').forEach(h => h.classList.toggle('show'));
  }

  function resetTest() {
    submitted = false;
    clearInterval(timerInterval);
    document.querySelectorAll('.opt').forEach(o => o.className = 'opt');
    document.querySelectorAll('.hint-box').forEach(h => h.classList.remove('show'));
    Object.keys(selected).forEach(k => delete selected[k]);
    document.getElementById('scoreBox').style.display = 'none';
    const timerEl = document.getElementById('timerDisplay');
    if (timerEl) {
      timerEl.className = 'timer-display';
    }
    const submitBtn = document.getElementById('submitBtn');
    if (submitBtn) submitBtn.textContent = 'Submit & check score';
    const keyBtn = document.getElementById('keyBtn');
    if (keyBtn) keyBtn.style.display = 'none';
    window.scrollTo({ top: 0, behavior: 'smooth' });
    startTimer();
  }

  function saveBestScore(score, total, pct) {
    const key = 'history_' + location.pathname.split('/').pop().replace('.html', '');
    const history = JSON.parse(localStorage.getItem(key) || '[]');
    history.unshift({
      score, total, pct,
      date: new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
    });
    // Keep last 20 attempts
    if (history.length > 20) history.length = 20;
    localStorage.setItem(key, JSON.stringify(history));
  }

  document.addEventListener('DOMContentLoaded', init);
})();
