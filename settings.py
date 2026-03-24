"""
R_10 EVEN/ODD 5-TICK BOT — COMBINED EDITION
=============================================
Contract : DIGITEVEN / DIGITODD on R_10
Expiry   : 5 ticks
Symbol   : R_10 (Volatility 10 Index)

TRUE PROBABILITY:
  Even (digits 0,2,4,6,8) = 0.50 exactly
  Odd  (digits 1,3,5,7,9) = 0.50 exactly

BREAK-EVEN WIN RATE:
  At 87% payout: 1/(1+0.87) = 53.5%
  At 85% payout: 1/(1+0.85) = 54.1%
  Models must find edge above this threshold.

THREE-LAYER ARCHITECTURE:
  Layer 1 (A) — Distribution context (100-150 digit window):
    Statistical approach — frequency + significance.
    Layer 1 answers: IS there a distributional bias right now?

  Layer 2 (B) — Sequence prediction (short window):
    Transition patterns, run structure, positional lookahead.
    Layer 2 answers: WHAT does the sequence say comes next?

  Layer 3 (C) — Pattern heuristics (very short window):
    Streak reversals, recent parity imbalance, hot digit clustering.
    Layer 3 answers: WHAT is the current short-term pattern saying?

  All three layers must agree on direction before a trade fires.
  Confidence blend: 40% L1 + 35% L2 + 25% L3.
"""

import os

# ── Connection ────────────────────────────────────────────────────
DERIV_APP_ID    = "1089"
DERIV_API_TOKEN = os.environ.get("DERIV_API_TOKEN", "iCCn0vuMCzLcq1J")
DERIV_WS_URL    = "wss://ws.derivws.com/websockets/v3"

# ── Contract ──────────────────────────────────────────────────────
SYMBOL          = "R_10"
EXPIRY_TICKS    = 5
EXPIRY_UNIT     = "t"
EVEN_DIGITS     = {0, 2, 4, 6, 8}
ODD_DIGITS      = {1, 3, 5, 7, 9}
TRUE_PROB       = 0.50

# ── Tick / digit buffer ───────────────────────────────────────────
TICK_BUFFER     = 1000
DIGIT_BUFFER    = 500
WARMUP_TICKS    = 150      # minimum before any model votes

# ─────────────────────────────────────────────────────────────────
# LAYER 1 — DISTRIBUTION CONTEXT  (Option A)
# ─────────────────────────────────────────────────────────────────

ENTROPY_WINDOW      = 60
ENTROPY_MAX         = 0.985

FREQ_WINDOW         = 120
FREQ_HALFLIFE       = 20
FREQ_BIAS_MIN       = 0.030

ZSCORE_WINDOWS      = [30, 50, 80, 120]
ZSCORE_MIN          = 1.8
ZSCORE_STRONG       = 2.5

CHISQ_WINDOW        = 150
CHISQ_PVALUE_MAX    = 0.15

# ─────────────────────────────────────────────────────────────────
# LAYER 2 — SEQUENCE PREDICTION  (Option B)
# ─────────────────────────────────────────────────────────────────

TRANSITION_WINDOW   = 100
TRANSITION_MIN_DEV  = 0.055

RUN_WINDOW          = 60
RUN_Z_MIN           = 1.5

POSITIONAL_WINDOW   = 200
POSITIONAL_LOOKBACK = 3
POSITIONAL_MIN_PROB = 0.545
POSITIONAL_MIN_N    = 8

# ─────────────────────────────────────────────────────────────────
# LAYER 3 — PATTERN HEURISTICS  (Option C)
# Fast short-horizon models ported from the VIX25 heuristic engine.
# ─────────────────────────────────────────────────────────────────

# Model C1: Streak Reversal
# N+ consecutive same-parity digits → bet the opposite
STREAK_MIN          = 5

# Model C2: Recent Parity Imbalance
# Last C2_WINDOW digits skewed beyond C2_THRESHOLD → bet underdog
C2_WINDOW           = 10
C2_THRESHOLD        = 6        # e.g. 7/10 even → vote ODD

# Model C3: Hot Digit Parity
# Top C3_HOT_COUNT most frequent digits in last C3_WINDOW ticks
# Majority parity of hot digits → vote that direction
C3_WINDOW           = 20
C3_HOT_COUNT        = 3

LAYER3_WINDOW_MIN   = 30       # minimum digits before L3 models vote

# ─────────────────────────────────────────────────────────────────
# CONFLUENCE
# ─────────────────────────────────────────────────────────────────
LAYER1_REQUIRED     = 2        # of 3 models
LAYER2_REQUIRED     = 2        # of 3 models
LAYER3_REQUIRED     = 2        # of 3 models

# Confidence blend weights — must sum to 1.0
L1_WEIGHT           = 0.40
L2_WEIGHT           = 0.35
L3_WEIGHT           = 0.25

CONFIDENCE_MIN      = 0.53
TOP_CONF_MIN        = 0.55

# ─────────────────────────────────────────────────────────────────
# TRADE MANAGEMENT
# ─────────────────────────────────────────────────────────────────
FIRST_STAKE         = 0.35
MARTINGALE_FACTOR   = 1.75
MARTINGALE_AFTER    = 1
MARTINGALE_MAX_STEP = 4

TARGET_PROFIT       = 100.0
STOP_LOSS           = 20.0

COOLDOWN_MIN        = 20
COOLDOWN_MAX        = 40

RECONNECT_BASE      = 3
RECONNECT_MAX       = 60

TELEGRAM_TOKEN      = os.environ.get("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID    = os.environ.get("TELEGRAM_CHAT_ID", "")

LOG_FILE            = "/tmp/r10_eo_bot.log"
TRADES_FILE         = "/tmp/r10_eo_trades.csv"
STATS_FILE          = "/tmp/r10_eo_stats.json"
