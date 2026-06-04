---
name: Ethereal Health Intelligence
colors:
  surface: '#f8fafb'
  surface-dim: '#d8dadb'
  surface-bright: '#f8fafb'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f4f5'
  surface-container: '#eceeef'
  surface-container-high: '#e6e8e9'
  surface-container-highest: '#e1e3e4'
  on-surface: '#191c1d'
  on-surface-variant: '#414849'
  inverse-surface: '#2e3132'
  inverse-on-surface: '#eff1f2'
  outline: '#717879'
  outline-variant: '#c0c8c9'
  surface-tint: '#3c656a'
  primary: '#002428'
  on-primary: '#ffffff'
  primary-container: '#0d3b40'
  on-primary-container: '#7ba5ab'
  inverse-primary: '#a3ced4'
  secondary: '#006689'
  on-secondary: '#ffffff'
  secondary-container: '#8dd5fd'
  on-secondary-container: '#005d7d'
  tertiary: '#042421'
  on-tertiary: '#ffffff'
  tertiary-container: '#1c3a36'
  on-tertiary-container: '#85a49e'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#bfeaf0'
  primary-fixed-dim: '#a3ced4'
  on-primary-fixed: '#001f23'
  on-primary-fixed-variant: '#234d52'
  secondary-fixed: '#c2e8ff'
  secondary-fixed-dim: '#87cff7'
  on-secondary-fixed: '#001e2c'
  on-secondary-fixed-variant: '#004d68'
  tertiary-fixed: '#c8e9e2'
  tertiary-fixed-dim: '#adcdc7'
  on-tertiary-fixed: '#01201c'
  on-tertiary-fixed-variant: '#2f4c47'
  background: '#f8fafb'
  on-background: '#191c1d'
  surface-variant: '#e1e3e4'
  deep-teal: '#0D3B40'
  medical-blue: '#2D7DA1'
  soft-mint: '#D1F2EB'
  glass-white: rgba(255, 255, 255, 0.7)
  error-alert: '#FF4B4B'
typography:
  display-lg:
    fontFamily: Montserrat
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Montserrat
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: 0.01em
  headline-lg-mobile:
    fontFamily: Montserrat
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Montserrat
    fontSize: 24px
    fontWeight: '500'
    lineHeight: '1.3'
    letterSpacing: 0.02em
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
    letterSpacing: 0.01em
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '700'
    lineHeight: '1.0'
    letterSpacing: 0.1em
  chat-bubble:
    fontFamily: Inter
    fontSize: 15px
    fontWeight: '400'
    lineHeight: '1.5'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  container-max: 1200px
  gutter: 24px
  margin-mobile: 20px
  margin-desktop: 64px
---

## Brand & Style

The design system is engineered to evoke the "million-dollar tech startup" aesthetic—a fusion of clinical precision and high-vibe wellness. It targets a health-conscious, tech-savvy demographic that demands both expertise and an elevated user experience.

The visual style is **Glassmorphism**, characterized by translucent surfaces, multi-layered depth, and a sense of weightlessness. The design narrative centers on "Calm Authority," utilizing vast negative space and refined transparency to make complex medical data feel approachable and futuristic. The interface should feel less like a database and more like a premium concierge service.

## Colors

The palette balances the grounded reliability of **Deep Teal** and **Medical Blue** with the refreshing, airy qualities of **Soft Mint**. 

- **Primary & Secondary:** Use Deep Teal for core structural elements and high-hierarchy typography. Medical Blue serves as the primary action color for buttons and interactive states.
- **Surface Strategy:** The background is a clean, near-white neutral. Use Soft Mint as a subtle wash for secondary containers or success states.
- **High-Vibe Accents:** Implement linear gradients transitioning from Medical Blue to Soft Mint (45-degree angle) for primary progress bars, active chat bubbles, and "high-vibe" feature highlights.

## Typography

Typography focuses on "Generous Legibility." **Montserrat** provides a geometric, modern confidence for headings, while **Inter** ensures data-heavy medical information remains readable and neutral.

Increased letter spacing (tracking) is applied to uppercase labels and headlines to enhance the premium feel. Avoid heavy weights for body text; rely on Medium (500) for emphasis to maintain a light, sophisticated aesthetic. Line heights are intentionally tall to create a relaxed reading rhythm.

## Layout & Spacing

The layout follows a **Fluid Grid** model with significant breathing room. 
- **Desktop:** 12-column grid with wide 64px external margins to center the focus.
- **Mobile:** 4-column grid with 20px margins.
- **Rhythm:** Use an 8px base unit. Component internal padding should be generous (e.g., 24px or 32px for cards) to prevent the "cramped" feel often found in traditional medical software. 
- **Chat Interface:** Center-aligned conversational flow with max-width constrained to 800px to ensure optimal line length for readability.

## Elevation & Depth

Depth is achieved through **Glassmorphism** rather than traditional opaque stacking.

- **The Glass Layer:** Foreground containers use `rgba(255, 255, 255, 0.7)` with a `backdrop-filter: blur(20px)`. 
- **Shadows:** Use "Ambient Shadows"—ultra-diffused (40px-60px blur), low opacity (5-8%), tinted with a touch of Medical Blue (`#2D7DA1`) to prevent gray, muddy looks.
- **Glows:** High-importance elements (like the active Bot Avatar or "Ask" button) feature a soft outer glow in Soft Mint to simulate a "high-vibe" energy source.

## Shapes

The shape language is "Approachable Geometric." 

Standard components use a **0.5rem (8px)** base radius. However, interactive elements like Chat Bubbles and Primary Action Buttons utilize a **Pill-shape (max-roundedness)** to soften the user's emotional response and lean into the futuristic startup aesthetic. Subtle 1px inner borders (semi-transparent white) should be applied to glass elements to define edges against vibrant backgrounds.

## Components

- **Chat Bubbles:** User bubbles are solid Deep Teal with white text. Bot bubbles use the Glassmorphism style (blurred white background) with Medical Blue text.
- **Buttons:** Primary buttons use a gradient (Medical Blue to Soft Mint) with a subtle floating animation on hover. No hard borders; use soft shadows for definition.
- **Input Fields:** Floating labels with a background-blur effect. The focus state should illuminate the border with a Soft Mint glow.
- **Cards:** Used for medical insights or "Health Scores." These should feature a 1px "shine" border (linear gradient: white to transparent) to emphasize the glass effect.
- **The "Pulse" Indicator:** A small, animated Soft Mint circle that pulses slowly when the AI is "thinking," creating a sense of life within the interface.
- **Chips:** Highly rounded, using low-opacity versions of the brand colors for categorization (e.g., "Symptom," "History").