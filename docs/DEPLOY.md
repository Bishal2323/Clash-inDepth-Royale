# Deploying to Vercel

Vercel runs the FastAPI app as a serverless function. It finds `app` in
`index.py` at the project root (which imports the app from `app/web.py`) automatically, installs `requirements.txt`, and redeploys on every
push to `main`.

## 1. Get an API key that works on Vercel

Clash Royale keys only work from the IP addresses registered on them, and Vercel
doesn't have a fixed IP. So we send requests through the
[RoyaleAPI proxy](https://docs.royaleapi.com/proxy.html), which does.

1. Open the proxy docs page above and note the IP address to whitelist.
2. On https://developer.clashroyale.com, create a **new** key (e.g. "vercel") and
   enter that IP as the allowed address.
3. Keep your existing key for local development.

## 2. Create the Vercel project

1. Sign in at https://vercel.com with GitHub.
2. **Add New → Project**, import `Clash-inDepth-Royale`.
3. Framework preset: **FastAPI** (detected automatically). Leave build settings as they are.
4. Under **Environment Variables**, add:

   | Name | Value |
   |---|---|
   | `CR_API_KEY` | the new key from step 1 |
   | `CR_API_BASE_URL` | `https://proxy.royaleapi.dev/v1` |

5. Click **Deploy**. You'll get a URL like `clash-indepth-royale.vercel.app`.

## 3. Check it

- `https://<your-url>/health` should return `{"ok": true}`.
- Open a player report. If it says the key was rejected (403), the key's IP
  doesn't match the proxy's IP.

## How it behaves on Vercel

- **Battle history is temporary.** Only `/tmp` is writable, so the SQLite file
  lives there and disappears when the server instance stops. Reports still work
  because they always fetch fresh battles; long-term history needs a hosted
  database (see roadmap).
- **The 2-minute cache is per server instance**, so it helps less under traffic
  spread over many instances. That's fine at portfolio scale.
- After changing environment variables, redeploy for them to take effect.
