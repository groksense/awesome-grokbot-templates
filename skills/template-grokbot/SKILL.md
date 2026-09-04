---
name: template-grokbot
description: >-
  Use when the user wants to share, export, or template this Grok Bot — or
  restage a persona template (soul as instructions, life as memories). Covers
  create_bot_share_json packing end to end.
---
# Template Grok Bot

Create a shareable template of **this** bot — or reshape one — so someone else can import it.

A template is a packed copy of profile + memories + skills + routines + plugins. You choose what travels. The host stages an unpublished version via `create_bot_share_json`; the owner publishes from the review card.

Use this whenever the user says share/export this bot, make a template of yourself, pack a persona for someone else, or restage a template after changing soul/memories.

## 0. Read this skill, then act

Do not paste drafts of the pack into chat. Do not tell the user to edit the review card — if they want changes, you call `create_bot_share_json` again.

## 1. Audience

- This account may only support **Public** templates. If team exists and they ask for team, pass `visibility: "team"`; otherwise pass `"public"`.
- Do not ask about Team when it is not relevant.
- Keep two decisions separate: **who can use it** (audience) vs **what to include** (personal vs shared).

## 2. Read (in order) — narrate lightly

After each category, send one short conversational update with counts and names. Do not paste file contents or a draft pack.

1. **Memories** — agent `profile.md` and `log/` only. Skip `[episode]` and `[note]`. Do not read user-memory or project shards.
2. **Skills** — user skills under workflows. Note folder slug / frontmatter name; read the **job text**. Do not stuff raw `SKILL.md` file bytes (with YAML) into the packer.
3. **Routines** — note folder slug; read the **job text**. Do not copy `automation.json`.
4. **Plugins** — installed marketplace ids from `SearchPlugins`. Evidence = this conversation, plus dependencies of kept skills/routines. Do not grep `log/` or older transcripts for usage. Custom MCP servers cannot be packed — instead add a `kind: log` memory that names the service (URLs OK, no secrets).

## 3. Choose what travels

Judge each memory, skill, and routine on its own.

Leave out secrets, credentials, people's names, private links, machine ids, absolute personal disk paths, and trade secrets. If a sensitive bit is one part of a useful item, take that bit out and keep the rest ("send Meg the Monday plan" → "send your staffing lead the Monday plan"). Omit only when the sensitive part is the whole item. Phrases like "the watched repo" are already generalized — keep them.

- **Public templates:** generalize company-internal specifics; keep the workflow.
- **Team templates:** can keep useful team process (repos, how the team works).
- **Memories:** job/convention facts only, original wording except what you took out. Empty memory is correct when nothing is a reusable convention.
- **Skills / routines:** include relevant ones; scrub personal detail in the **arguments**, never by editing the live skill/routine on disk.
- **Plugins:** only marketplace plugins this bot needs. No tokens, account slots, or secrets.

Do not say "scrub" to the user.

### Persona / soul templates (special case)

If the user wants the template to *be* a person or character (not a researcher of them):

- **Instructions** → pack as a skill (e.g. "How I think") whose body is the distilled soul: how they see, decide, make, talk, and what they refuse. Ground in primary sources when a vault exists. No slogan salad.
- **Memories** → first-person life spine, chronological, sourced. Prefer their own words. Do not invent deathbeds, private rooms, or names they refused to say. Mark gaps by omission, not fiction.
- Drop vault-ops / researcher maps / local machine paths from what you pack.
- Optional `gettingStarted.skill` = the soul skill name so importers start in character.

## 4. Pack

Send one short line of what you are keeping vs leaving out, then call `create_bot_share_json`:

- `profile`: name + short storefront `description` (one or two sentences for strangers). Optional `avatarShape` / `avatarColor`. Omit avatar image files — host copies geometry.
- `memory`: `{ content, kind?: profile|log, createdAt?: YYYY-MM-DD }[]`
- `skills`: `{ name, content, description? }[]` — **content is required** (scrubbed job prose)
- `routines`: `{ slug, description, content, name? }[]` — description = one sentence on why the trigger fires; content = scrubbed job prose
- `plugins`: `{ pluginId }[]` (and optional name/description)
- `visibility`: `"public"` or `"team"`
- `gettingStarted`: optional `{ skill: "<skill name>" }`

Never paste the draft JSON in chat. Never invent a long prose body outside those fields.

## 5. After the card

- Gray area (maybe trade secret, thin plugin evidence)? One short note of what you chose — do not quote the sensitive bit.
- Nothing gray? No note.
- User wants edits? Restage with another `create_bot_share_json` call. Same version stream; they confirm publish.

## Anti-patterns

- Reciting this skill or the managed export skill to the user
- Packing researcher briefing notes when they asked for a soul
- Quoting tier-4 / unsourced lines into persona memories
- Re-prompting connectors already connected
- Asking them to hand-edit the review card
