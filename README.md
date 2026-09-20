# Yevoo Justice Selasi — Portfolio

Single-page portfolio site, live at [yevsel.com](https://yevsel.com).

## Stack

Plain HTML + CSS in one file (`index.html`) — no build step, no JavaScript, no dependencies. Flat, monochrome, Swiss-minimal design with smooth in-page anchor scrolling and minimal hover transitions only.

## Structure

- `index.html` — the entire site (markup + styles)
- `avatar.jpg` — optimized profile photo used in the hero and as the social share image
- `profile_picture.png` — original, full-resolution source photo (not deployed)
- `robots.txt`, `sitemap.xml` — search engine crawling/indexing config
- `CNAME` — custom domain config for GitHub Pages (`yevsel.com`)
- `.github/workflows/static.yml` — GitHub Actions workflow that deploys `main` to GitHub Pages on every push

## Content

Sections: Summary, Core Competencies, Technical Stack, Professional Experience, Education, Contact. Content is sourced from the résumé (kept locally, gitignored) — update `index.html` directly to reflect résumé changes.

## Deployment

Push to `main` — GitHub Pages builds and deploys automatically via the Actions workflow. No manual build step required.

## SEO

The page includes meta description/keywords, canonical URL, Open Graph + Twitter Card tags, and JSON-LD `Person` structured data. `sitemap.xml` and `robots.txt` are served from the repo root.
