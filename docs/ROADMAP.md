# Roadmap

## v0.1: MVP (current)
- [x] Tag lookup with validation
- [x] Player snapshot
- [x] Deck doctor: roles, average cost, upgrade order
- [x] Battle review with level comparison and disconnect labels
- [x] Nemesis cards
- [x] Rule-based "Fix these first" tips
- [x] Upcoming chests
- [x] Store every battle in SQLite

## v0.2: Better coaching
- [ ] Test with low-level / beginner accounts and tune thresholds
- [ ] Matchup stats by opponent archetype (bait, beatdown, cycle, siege...)
- [ ] Analyze every deck the player used, not only the current one
- [ ] Glossary page for game terms
- [ ] Short "Learn" tips matched to the player's weaknesses
- [ ] Check card-level conversion against the game for every rarity

## v0.3: Progress over time
- [ ] "Since your last visit" (trophies, win rate, new tips fixed)
- [ ] Charts for win rate and trophies over time
- [ ] Background refresh for returning players

## v0.4: Deploy
- [x] Vercel config and RoyaleAPI proxy support (see DEPLOY.md)
- [ ] Hosted Postgres instead of SQLite, so history survives on Vercel
- [ ] Rate limiting and better caching

## Later: Video analysis
Card placement and timing aren't in the API. The plan is to analyze screen
recordings of matches with computer vision (detect troops and where they're
placed, read the elixir bar and timer) to show placement heatmaps and when
elixir was actually wasted.
