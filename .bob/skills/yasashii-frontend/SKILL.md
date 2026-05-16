---
name: yasashii-frontend
description: Generate frontend files for Yasashii Sensei Japanese learning web app using vanilla HTML CSS and JS with Flask Jinja2 templates
---

Generate the frontend for やさしい先生 (Yasashii Sensei).

<Steps>
<Step>
Create templates/index.html with:
- Two tabs: NHK Web Easy articles + Paste text
- Article list fetched from GET /api/articles
- Difficulty badges per article (N5-N2)
- Textarea for pasting Japanese text
- Loading spinner
</Step>

<Step>
Create templates/results.html with:
- Original text with ruby/furigana tags
- JLPT level badge (color coded)
- Vocabulary cards grid
- Grammar patterns section
- Translation section
- Cultural notes section
- Comprehension questions
- "Analyze Another" button
</Step>

<Step>
Create static/css/style.css with:
- Noto Sans JP font from Google Fonts
- Navy/blue color scheme (#1F4E79, #BDD7EE)
- JLPT badges: N5=green N4=blue N3=yellow N2=orange N1=red
- Responsive mobile layout
- Loading spinner animation
</Step>

<Step>
Create static/js/app.js with:
- fetchArticles() → GET /api/articles
- analyzeText() → POST /api/analyze
- displayResults(data) → render lesson
- showLoading() / hideLoading()
- Tab switching logic
- API base URL: http://localhost:5001
</Step>
</Steps>