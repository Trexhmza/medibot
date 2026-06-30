# HealBuddy — AI-Powered Healthcare Chatbot

## Big Picture

HealBuddy is an intelligent healthcare companion that brings AI-driven medical guidance to anyone with a browser. Users describe symptoms, ask health questions, or upload images (rashes, injuries, prescriptions), and get conversational advice from one of two AI doctor personas — **Dr. Elena** (warm and empathetic) or **Dr. James** (direct and clinical).

The entire application runs client-side: no servers, no databases, no backend. It calls the Groq API directly for LLM inference, uses LLaMA 4 Scout for vision analysis, and persists chat histories in the browser's local storage. This makes it lightweight, fast, and deployable anywhere static files can be served — currently hosted on GitHub Pages.

Beyond the chat interface, HealBuddy has a full marketing landing page with 3D hero visuals (powered by Spline), doctor profiles, testimonials, and an embeddable widget so any website can offer AI health triage.

## Tech Stack

- **Frontend:** Pure HTML, CSS, and Vanilla JavaScript (no frameworks)
- **AI Backend:** Groq API (LLaMA 3.3-70B for text, LLaMA 4 Scout for vision)
- **3D Graphics:** Spline Viewer
- **Deployment:** GitHub Pages via GitHub Actions
- **Storage:** Browser localStorage

## Key Features

- Conversational symptom checker with two doctor personas
- AI image analysis for visual symptoms
- Full chat history with load/delete
- Marketing landing page with 3D hero section
- Embeddable chat widget for third-party sites
- Responsive dark-themed UI

## Team

| Name | Roll No |
|---|---|
| M Hamza Shahzad | F2023266996 |
| Zaina Nadeem | F20232661084 |
