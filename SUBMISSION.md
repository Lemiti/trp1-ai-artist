# [TRP1] Lemi - AI Content Exploration

## 1. Environment Setup
- **APIs Configured:** Google Gemini (Lyria/Veo), AIMLAPI (MiniMax).
- **Setup Success:** Successfully established "Heartbeat" connection via Tenx MCP Server.
- **Issues:** Encountered significant upstream API instability (Lyria) and account verification blocks (AIMLAPI).

## 2. Codebase Understanding
- **Architecture:** The system uses a **Plugin Registry** pattern (`src/ai_content/core/registry.py`). This allows providers to be swapped at runtime without changing the CLI logic.
- **Pipeline Orchestration:** Found that `src/ai_content/pipelines/full.py` manages the end-to-end flow from Archive.org searching to final media merging via FFmpeg.
- **Insight:** The use of **SQLite** for job tracking (`job_tracker.py`) is a critical design choice for handling long-running AI tasks like MiniMax which take 5-15 minutes.

## 3. Challenges & Persistence
> #### **Critical Blockers & Troubleshooting Log**
> 
> *   **Issue 1: Google Lyria (Music) - 1011 Internal Error**
>     *   *Diagnosis:* Persistent handshake timeouts and keepalive pings suggest the experimental Google WebSocket endpoint is currently unstable or regionally restricted in Ethiopia. 
>     *   *Workaround:* Attempted reducing duration to 10s and using different presets to bypass server-side complexity. 
> 
> *   **Issue 2: Google Veo (Video) - Module Attribute Error**
>     *   *Diagnosis:* `module 'google.genai.types' has no attribute 'GenerateVideoConfig'`. This indicates a version mismatch between the code's implementation and the installed `google-genai` library (likely a breaking change in the Alpha SDK). 
> 
> *   **Issue 3: AIMLAPI (MiniMax) - 403 Forbidden**
>     *   *Diagnosis:* Encountered `err_unverified_card`. Despite being in a free assessment tier, the MiniMax 2.0 provider requires active account verification which was a hard blocker for real-time generation.
>     *   *Workaround:* Switched to testing the `lyria` provider to verify local configuration was correct.

## 4. Insights & Learnings
- **Surprise:** The depth of the preset system—specifically the inclusion of `ethiopian-jazz`—shows a thoughtful localization of the tool.
- **Improvement:** I would implement a more robust dependency check for the `google-genai` SDK to prevent the `AttributeError` found during video generation.