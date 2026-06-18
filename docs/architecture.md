The app should prefer "unknown" over a weak guess.

A food spawn is only logged once while the object remains visible.

A capture is confirmed by:

- object disappearance
- OCR score increase
- inferred score change
- or a combination of those signals

Capture Region Config
↓
MSS Capture Loop
↓
Frame Processor
↓
State Detector
↓
Object Detector
↓
Score Reader
↓
Session Manager
↓
Event Logger
↓
CSV / JSONL / Dashboard
