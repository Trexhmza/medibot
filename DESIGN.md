---
name: Clinical Noir
colors:
  surface: '#131313'
  surface-dim: '#131313'
  surface-bright: '#3a3939'
  surface-container-lowest: '#0e0e0e'
  surface-container-low: '#1c1b1b'
  surface-container: '#201f1f'
  surface-container-high: '#2a2a2a'
  surface-container-highest: '#353534'
  on-surface: '#e5e2e1'
  on-surface-variant: '#e4bebc'
  inverse-surface: '#e5e2e1'
  inverse-on-surface: '#313030'
  outline: '#ab8987'
  outline-variant: '#5b403f'
  surface-tint: '#ffb3b1'
  primary: '#ffb3b1'
  on-primary: '#680011'
  primary-container: '#ff535b'
  on-primary-container: '#5b000e'
  inverse-primary: '#bb152c'
  secondary: '#ffb4a8'
  on-secondary: '#690000'
  secondary-container: '#920703'
  on-secondary-container: '#ff9a8a'
  tertiary: '#c8c6c5'
  on-tertiary: '#313030'
  tertiary-container: '#929090'
  on-tertiary-container: '#2a2a2a'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffdad8'
  primary-fixed-dim: '#ffb3b1'
  on-primary-fixed: '#410007'
  on-primary-fixed-variant: '#92001c'
  secondary-fixed: '#ffdad4'
  secondary-fixed-dim: '#ffb4a8'
  on-secondary-fixed: '#410000'
  on-secondary-fixed-variant: '#920703'
  tertiary-fixed: '#e5e2e1'
  tertiary-fixed-dim: '#c8c6c5'
  on-tertiary-fixed: '#1c1b1b'
  on-tertiary-fixed-variant: '#474746'
  background: '#131313'
  on-background: '#e5e2e1'
  surface-variant: '#353534'
typography:
  display-lg:
    fontFamily: Hanken Grotesk
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Hanken Grotesk
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
  headline-lg-mobile:
    fontFamily: Hanken Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  title-md:
    fontFamily: Hanken Grotesk
    fontSize: 18px
    fontWeight: '500'
    lineHeight: 24px
  body-lg:
    fontFamily: Hanken Grotesk
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 26px
  body-sm:
    fontFamily: Hanken Grotesk
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 4px
  gutter: 16px
  margin-mobile: 16px
  margin-desktop: 48px
  container-max-width: 1200px
---

## Brand & Style
The design system is engineered for high-stakes healthcare environments where clarity, speed, and focus are paramount. It adopts a **Corporate Modern** style with a dark-mode-first philosophy to reduce eye strain for medical professionals and patients in low-light settings. 

The aesthetic is characterized by deep atmospheric blacks and rich medicinal reds, creating a "Mission Control" for health. It communicates serious reliability through a structured, low-contrast interface that prioritizes data legibility and trust. The emotional response is one of calm authority, professionalism, and modern precision.

## Colors
The palette is rooted in a "Deep Blood" red spectrum. The **Primary Color** (#E63946) is a vibrant, clinical red used sparingly for key actions and branding. The **Secondary Color** (#8B0000) provides a somber, grounded accent for borders and container backgrounds.

The **Neutral** tones follow a charcoal-to-black scale. Backgrounds are nearly pure black to ensure maximum contrast for text and medical data. Borders use a subtle red-tinted dark gray to maintain the brand's warmth within a cold, dark interface.

## Typography
This design system utilizes **Hanken Grotesk** for all primary communication. It is a clean, sharp, and highly legible grotesque that feels contemporary yet clinical. For technical data, timestamps, and healthcare-specific identifiers, **JetBrains Mono** is used to provide a "lab-result" precision and distinguish metadata from conversational text.

Headlines should be kept concise. Body text utilizes a generous line height (1.6x) to ensure that dense medical information remains digestible.

## Layout & Spacing
The layout follows a **Fixed Grid** model for desktop, centered within the viewport to maintain focus. A 12-column system is used with 16px gutters. For the AI Chat interface, a specialized 3-column layout is recommended:
- **Left/Main (8 columns):** The primary chat stream and input.
- **Right Sidebar (4 columns):** Quick suggestions, medical profile, and lab result previews.

On mobile, the layout collapses into a single-column fluid stack, where the sidebar becomes a bottom-sheet or a secondary tab. All spacing is derived from a 4px base unit to ensure surgical precision in alignment.

## Elevation & Depth
Depth is achieved through **Tonal Layers** rather than heavy shadows. In a dark environment, depth is conveyed by making "higher" elements slightly lighter or more saturated.
- **Level 0 (Base):** Pure black #050505.
- **Level 1 (Containers):** Deep charcoal #121212 with a 1px border of #2A1212.
- **Level 2 (Chat Bubbles/Modals):** Dark gray #1A1A1A with a subtle inner glow on the top edge.
- **Overlays:** Semi-transparent backdrops using #000000 at 80% opacity with a 10px background blur.

## Shapes
The shape language is **Soft (Level 1)**. It uses a 0.25rem (4px) base radius. This creates a disciplined, professional look that avoids the "playfulness" of highly rounded corners while remaining more approachable than sharp 90-degree angles. Chat bubbles and primary buttons use `rounded-lg` (8px) to provide a distinct touch target and visual comfort.

## Components
### Chat Bubbles
- **Assistant:** Background #1A1A1A, border left 4px solid #E63946. Text is white.
- **User:** Background #2A1212, no border. Text is #E0E0E0.
- **Avatar:** 32px circular frames with high-resolution clinical portraits or medical icons.

### Quick Suggestions
- **Style:** Ghost buttons with a #2A1212 border and #E63946 icon.
- **Interaction:** On hover, the background fills with a faint red tint (5% opacity) and the border brightens.

### Input Fields
- **Style:** Underlined or fully enclosed with #2A1212 border. 
- **Focus:** The border transitions to #E63946 with a soft red outer glow.
- **Typography:** Uses `body-sm`.

### Healthcare Icons
- **Style:** 24px stroke-based icons with 1.5px weight. 
- **Coloring:** Icons should use the Primary Red when active or indicating health-critical data, and Mid-Gray for neutral actions.

### Progress & Status
- **Critical Status:** Pulse animation using Primary Red.
- **Stable Status:** Solid Deep Gray.