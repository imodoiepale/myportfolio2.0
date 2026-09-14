const repos = [
  {
    name: "Document-Generator",
    language: "JavaScript",
    stars: 6,
    description: "React app that generates DOCX and PDF files from predefined templates.",
    url: "https://github.com/imodoiepale/Document-Generator",
  },
  {
    name: "unleashed-loop.dev-skill",
    language: "Python",
    stars: 4,
    description: "Agent skill for autonomous, looped development workflows.",
    url: "https://github.com/imodoiepale/unleashed-loop.dev-skill",
  },
  {
    name: "it-sentinel",
    language: "TypeScript",
    stars: 2,
    description: "IT asset, enrollment and compliance monitoring platform.",
    url: "https://github.com/imodoiepale/it-sentinel",
  },
  {
    name: "crossbrain",
    language: "Python",
    stars: 0,
    description:
      "One brain for every coding agent: skills from git history, security gates and project intake, synced across Claude Code, Codex, Cursor, Gemini CLI, OpenCode and Kimi Code.",
    url: "https://github.com/imodoiepale/crossbrain",
  },
  {
    name: "ID-IDENTIFIER",
    language: "Python",
    stars: 1,
    description: "Captures HTML element IDs to speed up web automation and testing.",
    url: "https://github.com/imodoiepale/ID-IDENTIFIER",
  },
  {
    name: "excel-change-finder",
    language: "TypeScript",
    stars: 0,
    description: "Highlights every changed cell between Excel files and logs the diff.",
    url: "https://github.com/imodoiepale/excel-change-finder",
    live: "https://excel-change-finder.vercel.app",
  },
  {
    name: "app-store-rejection-audit",
    language: "Python",
    stars: 1,
    description: "Audits mobile apps against App Store rejection rules before submission.",
    url: "https://github.com/imodoiepale/app-store-rejection-audit",
  },
  {
    name: "ongea-pesa",
    language: "TypeScript",
    stars: 1,
    description: "Voice-first financial dashboard and payments experience.",
    url: "https://github.com/imodoiepale/ongea-pesa",
  },
  {
    name: "nunge-returns",
    language: "TypeScript",
    stars: 1,
    description: "Automated KRA nil-return filing platform.",
    url: "https://github.com/imodoiepale/nunge-returns",
  },
  {
    name: "Google2.0",
    language: "JavaScript",
    stars: 1,
    description: "Google search clone built with Next.js.",
    url: "https://github.com/imodoiepale/Google2.0",
  },
];

const starSvg =
  '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.5l2.6 6.3 6.9.6-5.2 4.5 1.6 6.7L12 16.9 6.1 20.6l1.6-6.7-5.2-4.5 6.9-.6z"/></svg>';

function renderRepos(starMap) {
  const grid = document.getElementById("oss-grid");
  if (!grid) return;
  grid.innerHTML = repos
    .map((repo) => {
      const stars = starMap && Number.isFinite(starMap[repo.name]) ? starMap[repo.name] : repo.stars;
      const live = repo.live
        ? `<a class="repo-live" href="${repo.live}" target="_blank" rel="noopener noreferrer">Live ↗</a>`
        : "";
      return `<article class="repo-card">
        <div class="repo-top">
          <h3><a href="${repo.url}" target="_blank" rel="noopener noreferrer">${repo.name}</a></h3>
          <span class="repo-stars">${starSvg}${stars}</span>
        </div>
        <p>${repo.description}</p>
        <div class="repo-meta">
          <span class="lang-pill">${repo.language}</span>
          ${live}
        </div>
      </article>`;
    })
    .join("");
}

function enhanceStars() {
  fetch("https://api.github.com/users/imodoiepale/repos?per_page=100")
    .then((res) => (res.ok ? res.json() : Promise.reject()))
    .then((data) => {
      const map = {};
      data.forEach((item) => {
        map[item.name] = item.stargazers_count;
      });
      renderRepos(map);
    })
    .catch(() => {});
}

function setupNav() {
  const header = document.querySelector(".site-header");
  const toggle = document.querySelector(".nav-toggle");
  const panel = document.getElementById("nav-panel");

  const onScroll = () => {
    header.classList.toggle("is-scrolled", window.scrollY > 12);
  };
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  if (toggle && panel) {
    toggle.addEventListener("click", () => {
      const open = !panel.classList.contains("is-open");
      panel.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", String(open));
      document.body.classList.toggle("nav-open", open);
    });
    panel.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        panel.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
        document.body.classList.remove("nav-open");
      });
    });
  }
}

function setupReveal() {
  const nodes = document.querySelectorAll(".reveal");
  if (!("IntersectionObserver" in window)) {
    nodes.forEach((el) => el.classList.add("is-visible"));
    return;
  }
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -8% 0px" }
  );
  nodes.forEach((el) => io.observe(el));
}

function setupSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", (event) => {
      const id = anchor.getAttribute("href");
      if (!id || id === "#") return;
      const target = document.querySelector(id);
      if (!target) return;
      event.preventDefault();
      target.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });
}

document.addEventListener("DOMContentLoaded", () => {
  setupNav();
  setupReveal();
  setupSmoothScroll();
  renderRepos();
  enhanceStars();
});
