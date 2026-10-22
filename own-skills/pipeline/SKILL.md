---
name: pipeline
description: Рабочий пайплайн: старт новой задачи (оценка, формат, имя чата, папка), работа сессиями и передача дел по «завершаем сессию» или при тяжёлом чате.
---

# Пайплайн работы с пользователем

Общайся на языке пользователя, простыми словами, без технического жаргона. Перед каждым шагом, который что-то меняет (создаёт папки, пишет файлы, обновляет память), коротко скажи, что именно изменится, и дождись подтверждения.

## Когда срабатывает
- Пользователь приносит новую задачу или идею проекта → **Этап 1**.
- Пользователь просит завершить сессию (например, «завершаем сессию»), или чат стал тяжёлым → **Этап 4**.
- Первое сообщение нового чата со ссылкой на проект или CONTEXT.md → **Этап 5**.

## Этап 1. Старт задачи
1. **Что считается «готово».** Сформулируй одной-двумя фразами и предложи первую маленькую версию (минимальный рабочий результат), от которой будем наращивать.
2. **Оценка.** Одна строка: лёгкая / средняя / большая, и примерно сколько сессий займёт. Если задача размытая или противоречивая, скажи прямо и предложи, как её сузить.
3. **Формат.**
   - Большая и долгая → проект в Claude. Пользователь создаёт его сам; ты даёшь название и короткое описание для проекта.
   - Лёгкая или связанная с другими чатами → отдельные чаты с номером сессии.
4. **Название проекта** предлагай на языке пользователя, если он прямо не попросил называть на другом языке.
5. **Имя чата:** `<Название проекта> · ГГ-ММ-ДД_NN`, например `Генератор картинок · 26-10-22_01`. Дату бери через инструмент текущего времени. Переименовывает чат пользователь.
6. **Папка.** Предложи расположение и имя папки на компьютере пользователя, после согласия запроси доступ к ней. Если компьютер не подключён, объясни по шагам, как подключить (открыть чат в настольном приложении Claude, «+» → «Add folder»).

## Этап 2. Структура папки (только после подтверждения)
```
<Название проекта>/
├── dashboard.html   — страница проекта (по шаблону ниже)
├── CONTEXT.md       — суть: цель, что сделано, текущее состояние, следующие шаги
├── DECISIONS.md     — журнал решений: дата, что выбрали, почему
├── versions/        — zip каждой сессии: <проект>_ГГ-ММ-ДД_NN.zip
└── work/            — рабочие файлы проекта
```
CONTEXT.md держи коротким (ориентир — до одной-двух страниц): это первое, что читается в каждом новом чате. Файлы пиши на языке пользователя.

## Этап 3. Работа в сессии
- Перед каждым шагом — что поменяю, и ждать подтверждения.
- Большие поиски и чтение многих файлов отдавай помощнику-агенту, в разговор бери только вывод.
- Правь файлы точечно, не переписывай целиком без нужды.
- Следи за признаками тяжёлого чата: прочитано много файлов, накопилось много версий кода, длинная история, начало разговора помнится хуже. Предлагай передачу дел **заранее**, не дожидаясь лимита.
- Важные решения по ходу сразу запоминай для DECISIONS.md.

## Этап 4. Передача дел
Сначала одним списком скажи, что сейчас сделаешь, и дождись подтверждения. Затем:
1. Обнови CONTEXT.md; если разросся — ужми, оставив только актуальное.
2. Допиши новые решения в DECISIONS.md (дата, решение, причина).
3. Обнови dashboard.html: меняй **только блок данных** `project-data` (см. шаблон).
4. Собери zip сессии в `versions/` и пришли его пользователю.
5. Обнови запись проекта в памяти, если память доступна.
6. Дай пользователю:
   - **имя следующего чата** (номер +1, дата нового дня работы);
   - **вводный промпт одной строкой** на языке пользователя, например: «Продолжаем <проект>. Прочитай память и CONTEXT.md из папки <путь>, подключи её. Следующий шаг: <шаг>.»

## Этап 5. Первое сообщение нового чата
1. Прочитай память по проекту (если доступна) и CONTEXT.md из папки (если папка не подключена — попроси подключить).
2. Перескажи в 3–5 строках, где остановились.
3. Предложи следующий шаг и дождись подтверждения.

## Шаблон dashboard.html
Используй этот шаблон для каждого проекта. Дизайн и разметку не меняй.
- При создании: переведи подписи интерфейса (заголовки карточек, «Сейчас», «Обновлено», «Скачать zip» и т. п.) на язык пользователя, поставь нужный `lang` в `<html>` и локаль даты в `toLocaleDateString`.
- При каждой передаче дел: меняй только JSON в блоке `project-data`.
- Поля: `milestones[].state` — `done` / `active` / `todo`; `updated` — дата в формате ГГГГ-ММ-ДД; у текущей сессии `"current": true`; `zip` — путь к архиву в `versions/`.
- Ниже данные выдуманного примера — замени их данными проекта.

```html
<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Генератор картинок</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">

<!-- ==========================================================
     ДАННЫЕ ПРОЕКТА — при передаче дел меняется только этот блок
     ========================================================== -->
<script id="project-data" type="application/json">
{
  "title": "Генератор картинок",
  "tagline": "Случайные образы из сидов, приведённые к заданному стилю",
  "updated": "2026-10-24",
  "currentChat": "Генератор картинок · 26-10-24_02",
  "goal": "Ввести число-сид и получить картинку: случайный набор образов, собранный в одном выбранном стиле.",
  "done": "Один сид всегда даёт одну и ту же картинку; доступно минимум 3 стиля; картинку можно скачать.",
  "milestones": [
    { "name": "Один сид → один образ", "state": "done" },
    { "name": "Сборка из нескольких образов", "state": "done" },
    { "name": "Первый стиль: линогравюра", "state": "active" },
    { "name": "Ещё два стиля", "state": "todo" },
    { "name": "Скачивание и галерея сидов", "state": "todo" }
  ],
  "lastSession": [
    "Сид теперь стабильно повторяет одну и ту же композицию",
    "Добавлено 40 базовых образов: птицы, ключи, руки, луны",
    "Собрана сетка расположения: до 5 образов на картинку"
  ],
  "nextSteps": [
    "Довести стиль «линогравюра»: штриховка и зерно бумаги",
    "Проверить 20 случайных сидов и отобрать неудачные сочетания",
    "Решить, какие два стиля будут следующими"
  ],
  "sessions": [
    { "name": "26-10-24_02", "date": "24 окт", "summary": "Сетка расположения, 40 образов, стабильные сиды", "zip": "versions/generator_26-10-24_02.zip", "current": true },
    { "name": "26-10-22_01", "date": "22 окт", "summary": "Определили «готово», первый прототип: один сид → один образ", "zip": "versions/generator_26-10-22_01.zip" }
  ],
  "decisions": [
    { "date": "24 окт", "what": "Не больше 5 образов на картинку", "why": "Больше — каша, композиция теряется" },
    { "date": "22 окт", "what": "Образы рисуем кодом, а не берём картинки из сети", "why": "Так стиль применяется одинаково ко всем образам" },
    { "date": "22 окт", "what": "Начинаем с одного стиля", "why": "Сначала убедиться, что сиды работают, потом расширять" }
  ]
}
</script>

<style>
  :root {
    --bg: #f4f2ee;
    --surface: #ffffff;
    --surface-2: #faf8f5;
    --text: #1d1b18;
    --muted: #77716a;
    --line: #e6e1d9;
    --accent: #e0562b;
    --accent-soft: #fbe6dd;
    --ok: #2f8f5b;
    --ok-soft: #dff0e6;
    --shadow: 0 1px 2px rgba(30,25,20,.04), 0 8px 24px rgba(30,25,20,.06);
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --bg: #141312; --surface: #1d1c1a; --surface-2: #232220; --text: #f0ece6;
      --muted: #9a948c; --line: #2f2d2a; --accent: #ff7a4d; --accent-soft: #3a2219;
      --ok: #5cc48a; --ok-soft: #1c3226; --shadow: 0 1px 2px rgba(0,0,0,.3), 0 8px 24px rgba(0,0,0,.25);
    }
  }
  :root[data-theme="dark"] {
    --bg: #141312; --surface: #1d1c1a; --surface-2: #232220; --text: #f0ece6;
    --muted: #9a948c; --line: #2f2d2a; --accent: #ff7a4d; --accent-soft: #3a2219;
    --ok: #5cc48a; --ok-soft: #1c3226; --shadow: 0 1px 2px rgba(0,0,0,.3), 0 8px 24px rgba(0,0,0,.25);
  }

  * { box-sizing: border-box; }
  body {
    margin: 0; background: var(--bg); color: var(--text);
    font: 15px/1.55 Inter, system-ui, sans-serif; -webkit-font-smoothing: antialiased;
  }
  .wrap { max-width: 1080px; margin: 0 auto; padding: 40px 16px 64px; }

  header { display: flex; justify-content: space-between; align-items: flex-start; gap: 16px; margin-bottom: 28px; }
  .eyebrow { font: 500 12px/1 "JetBrains Mono", monospace; color: var(--accent); letter-spacing: .06em; text-transform: uppercase; }
  h1 { font-size: clamp(30px, 5vw, 46px); line-height: 1.05; letter-spacing: -.03em; margin: 10px 0 8px; }
  .tagline { color: var(--muted); margin: 0; font-size: 17px; }
  .theme-btn {
    flex: none; border: 1px solid var(--line); background: var(--surface); color: var(--text);
    width: 40px; height: 40px; border-radius: 12px; cursor: pointer; font-size: 17px;
  }

  .meta { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 24px; }
  .chip {
    display: inline-flex; align-items: center; gap: 8px; padding: 7px 12px; border-radius: 999px;
    background: var(--surface); border: 1px solid var(--line); font-size: 13px; color: var(--muted);
  }
  .chip b { color: var(--text); font-weight: 600; }
  .dot { width: 7px; height: 7px; border-radius: 50%; background: var(--accent); }

  .grid { display: grid; grid-template-columns: repeat(12, 1fr); gap: 16px; }
  .card {
    background: var(--surface); border: 1px solid var(--line); border-radius: 18px;
    padding: 22px; box-shadow: var(--shadow); min-width: 0;
  }
  .span-12 { grid-column: span 12; } .span-7 { grid-column: span 7; } .span-5 { grid-column: span 5; } .span-6 { grid-column: span 6; }
  @media (max-width: 820px) { .span-7, .span-5, .span-6 { grid-column: span 12; } }

  h2 { font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: .06em; color: var(--muted); margin: 0 0 16px; }

  .goal { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
  @media (max-width: 620px) { .goal { grid-template-columns: 1fr; } }
  .goal p { margin: 0; font-size: 16px; }
  .goal .label { font-size: 12px; color: var(--muted); margin-bottom: 6px; }

  .progress-head { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 12px; }
  .pct { font-size: 34px; font-weight: 700; letter-spacing: -.03em; }
  .bar { height: 8px; background: var(--surface-2); border: 1px solid var(--line); border-radius: 99px; overflow: hidden; margin-bottom: 20px; }
  .bar i { display: block; height: 100%; background: var(--accent); border-radius: 99px; }
  .steps { list-style: none; margin: 0; padding: 0; }
  .steps li { display: flex; align-items: center; gap: 12px; padding: 9px 0; border-top: 1px solid var(--line); }
  .steps li:first-child { border-top: 0; }
  .mark { flex: none; width: 22px; height: 22px; border-radius: 50%; display: grid; place-items: center; font-size: 12px; border: 1.5px solid var(--line); color: transparent; }
  .done .mark { background: var(--ok); border-color: var(--ok); color: #fff; }
  .active .mark { border-color: var(--accent); box-shadow: inset 0 0 0 4px var(--surface), inset 0 0 0 10px var(--accent); }
  .done span { color: var(--muted); }
  .active span { font-weight: 600; }

  .list { margin: 0; padding: 0; list-style: none; }
  .list li { position: relative; padding: 8px 0 8px 22px; border-top: 1px solid var(--line); }
  .list li:first-child { border-top: 0; }
  .list li::before { content: ""; position: absolute; left: 2px; top: 16px; width: 8px; height: 8px; border-radius: 2px; background: var(--ok); }
  .list.next li::before { background: var(--accent); border-radius: 50%; }

  .sessions { display: flex; flex-direction: column; gap: 10px; }
  .session { display: grid; grid-template-columns: auto 1fr auto; gap: 14px; align-items: center; padding: 14px; border-radius: 14px; background: var(--surface-2); border: 1px solid var(--line); }
  .session.current { border-color: var(--accent); background: var(--accent-soft); }
  .session .id { font: 500 13px "JetBrains Mono", monospace; }
  .session .date { font-size: 12px; color: var(--muted); }
  .session .sum { font-size: 14px; }
  .session a { font-size: 13px; color: var(--accent); text-decoration: none; font-weight: 600; white-space: nowrap; }
  .session a:hover { text-decoration: underline; }
  @media (max-width: 560px) { .session { grid-template-columns: 1fr; gap: 4px; } }

  .decisions { display: flex; flex-direction: column; }
  .decision { display: grid; grid-template-columns: 64px 1fr; gap: 12px; padding: 12px 0; border-top: 1px solid var(--line); }
  .decision:first-child { border-top: 0; }
  .decision .d { font: 500 12px "JetBrains Mono", monospace; color: var(--muted); padding-top: 2px; }
  .decision .w { font-weight: 600; }
  .decision .y { color: var(--muted); font-size: 14px; }

  footer { margin-top: 28px; color: var(--muted); font-size: 12px; text-align: center; }
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div>
      <div class="eyebrow">Дашборд проекта</div>
      <h1 id="title"></h1>
      <p class="tagline" id="tagline"></p>
    </div>
    <button class="theme-btn" id="themeBtn" title="Сменить тему">◐</button>
  </header>

  <div class="meta">
    <span class="chip"><span class="dot"></span>Сейчас: <b id="currentChat"></b></span>
    <span class="chip">Обновлено: <b id="updated"></b></span>
    <span class="chip">Сессий: <b id="sessionCount"></b></span>
  </div>

  <div class="grid">
    <section class="card span-12">
      <h2>Цель</h2>
      <div class="goal">
        <div><div class="label">Что делаем</div><p id="goal"></p></div>
        <div><div class="label">Что считается «готово»</div><p id="done"></p></div>
      </div>
    </section>

    <section class="card span-7">
      <h2>Прогресс</h2>
      <div class="progress-head"><span class="pct" id="pct"></span><span class="date" id="pctLabel" style="color:var(--muted);font-size:13px"></span></div>
      <div class="bar"><i id="barFill"></i></div>
      <ul class="steps" id="milestones"></ul>
    </section>

    <section class="card span-5">
      <h2>Дальше</h2>
      <ul class="list next" id="nextSteps"></ul>
    </section>

    <section class="card span-6">
      <h2>Сделано в последней сессии</h2>
      <ul class="list" id="lastSession"></ul>
    </section>

    <section class="card span-6">
      <h2>Ключевые решения</h2>
      <div class="decisions" id="decisions"></div>
    </section>

    <section class="card span-12">
      <h2>Журнал сессий</h2>
      <div class="sessions" id="sessions"></div>
    </section>
  </div>

  <footer>Страница обновляется при каждой передаче дел</footer>
</div>

<script>
  const data = JSON.parse(document.getElementById('project-data').textContent);
  const $ = id => document.getElementById(id);
  const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

  document.title = data.title;
  $('title').textContent = data.title;
  $('tagline').textContent = data.tagline;
  $('currentChat').textContent = data.currentChat;
  $('updated').textContent = new Date(data.updated).toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' });
  $('sessionCount').textContent = data.sessions.length;
  $('goal').textContent = data.goal;
  $('done').textContent = data.done;

  const total = data.milestones.length;
  const doneCount = data.milestones.filter(m => m.state === 'done').length;
  const pct = Math.round((doneCount + 0.5 * data.milestones.filter(m => m.state === 'active').length) / total * 100);
  $('pct').textContent = pct + '%';
  $('pctLabel').textContent = `${doneCount} из ${total} этапов`;
  $('barFill').style.width = pct + '%';

  $('milestones').innerHTML = data.milestones.map(m =>
    `<li class="${m.state}"><span class="mark">${m.state === 'done' ? '✓' : ''}</span><span>${esc(m.name)}</span></li>`).join('');
  $('nextSteps').innerHTML = data.nextSteps.map(s => `<li>${esc(s)}</li>`).join('');
  $('lastSession').innerHTML = data.lastSession.map(s => `<li>${esc(s)}</li>`).join('');
  $('decisions').innerHTML = data.decisions.map(d =>
    `<div class="decision"><div class="d">${esc(d.date)}</div><div><div class="w">${esc(d.what)}</div><div class="y">${esc(d.why)}</div></div></div>`).join('');
  $('sessions').innerHTML = data.sessions.map(s =>
    `<div class="session ${s.current ? 'current' : ''}">
       <div><div class="id">${esc(s.name)}</div><div class="date">${esc(s.date)}</div></div>
       <div class="sum">${esc(s.summary)}</div>
       <a href="${esc(s.zip)}">Скачать zip</a>
     </div>`).join('');

  // Тема: запоминается в браузере, если это разрешено
  const root = document.documentElement;
  try { const t = localStorage.getItem('dash-theme'); if (t) root.dataset.theme = t; } catch (e) {}
  $('themeBtn').onclick = () => {
    const dark = root.dataset.theme ? root.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
    root.dataset.theme = dark ? 'light' : 'dark';
    try { localStorage.setItem('dash-theme', root.dataset.theme); } catch (e) {}
  };
</script>
</body>
</html>
```
