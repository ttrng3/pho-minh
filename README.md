# Phố Mình

A pitch and walkthrough page for **Phố Mình**, Omni Service's proposed resident and staff app for Eco Central Park (Vinh) and Eco Retreat (Long An).

Live at **https://ttrng3.github.io/pho-minh/**

The page has two parts:
1. **A 90-second pitch intro** with narration (Vietnamese or English) and soft background music.
2. **An animated walkthrough** of one repair request moving between a resident's phone, the Phố Mình core and a staff member's phone.

It is an illustration. Names, screens and the walkthrough figures are examples, not a built product.

## Public on purpose
Ty asked for this to be public (02/10/2026). `robots.txt` and a `noindex` meta tag keep it out of search engines. It contains no resident personal data. It does show some internal operating figures:
- the 477 staff count;
- the handover progress from the ECP and ELA weekly reports.

Remove those from `src/page.html` if the page should carry public figures only.

## How it is built
- `src/page.html` is the single source, written as a fragment with a `/*__DATA__*/` marker.
- `src/script.json` holds the narration text (VI and EN).
- `voice/*.mp3` holds the narration clips: Microsoft neural voices via `edge-tts`, `vi-VN-HoaiMyNeural` and `en-US-AvaNeural`, mono 40 kbps.
- `python3 tools/build.py` embeds the clips and writes two outputs:
  - `index.html`, the full document served by GitHub Pages;
  - `build/artifact.html`, the fragment for the Cowork preview.

Never edit `index.html` by hand. Edit `src/` and rebuild.

To change a line of narration:
1. Edit `src/script.json`.
2. Regenerate that clip with `edge-tts`, using the same voice and the rates `-4%` (VI) and `-6%` (EN).
3. Convert it with `ffmpeg -ac 1 -ar 24000 -b:a 40k`.
4. Rebuild.

The music is synthesised in the browser (Web Audio), so there is no audio file and no licence to track.

## Visual standard
Apple design, one light theme, system font, hairlines. Status colours: blue = running, green = done, red = urgent. Pink is used only for thanks.
