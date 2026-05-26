"""PhosphoSitePlus flat-file loader and phosphosite reference helpers.

PhosphoSitePlus does not offer a public REST API. Data must be manually
downloaded from https://www.phosphosite.org/staticDownloads after accepting
their academic license agreement.

Required file: Phosphorylation_site_dataset.gz
Place it at: data/phosphosite_data/Phosphorylation_site_dataset.gz

This module mirrors the pattern of phospho/uniprot.py:
  - One loader function (reads + caches the flat file)
  - Fetch functions (filter by accession)
  - Parsing/extraction functions (compute reference counts, flag underresearched sites)
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

# Default expected location for the downloaded PSP flat file
DEFAULT_PSP_PATH = Path("data/phosphosite_data/Phosphorylation_site_dataset.gz")

# Module-level cache so the file is only read once per Python session
_PSP_CACHE: pd.DataFrame | None = None


# ── LOADER ────────────────────────────────────────────────────────────────────

def load_psp_dataset(path: str | Path = DEFAULT_PSP_PATH) -> pd.DataFrame:
    """Load the PhosphoSitePlus phosphorylation site flat file into a DataFrame.

    PSP flat files have 2 comment rows before the header, so we skip them.
    Results are filtered to human proteins and cached in memory for the session.

    Parameters
    ----------
    path : path to the downloaded Phosphorylation_site_dataset.gz file

    Returns
    -------
    DataFrame with all human phosphorylation sites and their reference counts.
    """
    global _PSP_CACHE

    # Return cached copy if already loaded
    if _PSP_CACHE is not None:
        return _PSP_CACHE

    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"PhosphoSitePlus dataset not found at: {path}\n"
            "Download 'Phosphorylation_site_dataset.gz' from:\n"
            "  https://www.phosphosite.org/staticDownloads\n"
            "and place it at the expected path above."
        )

    # PSP files have 2 comment/header rows before the actual column header
    df = pd.read_csv(path, sep="\t", skiprows=2, low_memory=False)

    # Filter to human only — PSP contains mouse, rat, and other organisms
    df = df[df["ORGANISM"] == "human"].copy()

    # Normalize accession field: strip whitespace, uppercase
    df["ACC_ID"] = df["ACC_ID"].astype(str).str.strip().str.upper()

    # Fill missing reference count columns with 0 so arithmetic is always safe
    for col in ["LT_LIT", "MS_LIT", "MS_CST"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    _PSP_CACHE = df
    print(f"Loaded PSP dataset: {len(df):,} human phosphorylation sites across {df['ACC_ID'].nunique():,} proteins")
    return df


# ── FETCH FUNCTIONS ────────────────────────────────────────────────────────────

def fetch_sites(accession: str, path: str | Path = DEFAULT_PSP_PATH) -> pd.DataFrame:
    """Return all phosphorylation sites for one UniProt accession.

    Each row is one site (e.g. S473-p) with its reference counts.

    Parameters
    ----------
    accession : UniProt accession ID (e.g. 'P31749' for AKT1)
    path      : path to PSP flat file (uses default if not specified)

    Returns
    -------
    DataFrame with columns: ACC_ID, GENE, MOD_RSD, SITE_GRP_ID,
    SITE_7_AA, DOMAIN, LT_LIT, MS_LIT, MS_CST, total_refs
    """
    df = load_psp_dataset(path)
    accession = accession.strip().upper()

    sites = df[df["ACC_ID"] == accession].copy()

    if sites.empty:
        return pd.DataFrame()

    # total_refs = all three reference sources combined
    sites["total_refs"] = sites["LT_LIT"] + sites["MS_LIT"] + sites["MS_CST"]

    keep_cols = [c for c in ["ACC_ID", "GENE", "MOD_RSD", "SITE_GRP_ID",
                              "SITE_7_AA", "DOMAIN", "LT_LIT", "MS_LIT",
                              "MS_CST", "total_refs"] if c in sites.columns]

    return sites[keep_cols].sort_values("total_refs", ascending=False).reset_index(drop=True)


# ── PARSING / EXTRACTION FUNCTIONS ────────────────────────────────────────────

def get_reference_summary(accession: str, path: str | Path = DEFAULT_PSP_PATH) -> dict:
    """Return a high-level reference count summary for one protein.

    This is the top-level number your pipeline needs: how many total
    literature references exist for all phosphosites on this protein.

    Parameters
    ----------
    accession : UniProt accession ID

    Returns
    -------
    dict with keys:
        accession       : the input accession
        gene            : gene symbol (if available)
        n_sites         : number of known phosphosites
        total_lt_lit    : sum of all low-throughput literature references
        total_ms_lit    : sum of all mass spec literature references
        total_ms_cst    : sum of all CST internal references
        total_refs      : sum of all three sources
        max_site_refs   : highest reference count on a single site
    """
    sites = fetch_sites(accession, path)

    if sites.empty:
        return {
            "accession": accession,
            "gene": None,
            "n_sites": 0,
            "total_lt_lit": 0,
            "total_ms_lit": 0,
            "total_ms_cst": 0,
            "total_refs": 0,
            "max_site_refs": 0,
        }

    gene = sites["GENE"].iloc[0] if "GENE" in sites.columns else None

    return {
        "accession": accession,
        "gene": gene,
        "n_sites": len(sites),
        "total_lt_lit": int(sites["LT_LIT"].sum()),
        "total_ms_lit": int(sites["MS_LIT"].sum()),
        "total_ms_cst": int(sites["MS_CST"].sum()),
        "total_refs": int(sites["total_refs"].sum()),
        "max_site_refs": int(sites["total_refs"].max()),
    }


def get_underresearched_sites(
    accession: str,
    lt_lit_min: int = 1,
    lt_lit_max: int = 5,
    path: str | Path = DEFAULT_PSP_PATH,
) -> pd.DataFrame:
    """Return phosphosites in the 'underresearched but confirmed' zone.

    Filters to sites with LT_LIT between lt_lit_min and lt_lit_max.
    These sites have at least one targeted experiment confirming them
    (so they're real), but haven't received sustained research attention.

    Default window: 1–5 low-throughput literature references.

    Parameters
    ----------
    accession  : UniProt accession ID
    lt_lit_min : minimum LT_LIT count (inclusive) — must be >= 1 to exclude
                 sites that have only been seen in mass spec screens
    lt_lit_max : maximum LT_LIT count (inclusive) — keeps out the well-studied

    Returns
    -------
    DataFrame of underresearched sites, sorted by LT_LIT descending.
    """
    sites = fetch_sites(accession, path)

    if sites.empty:
        return pd.DataFrame()

    mask = (sites["LT_LIT"] >= lt_lit_min) & (sites["LT_LIT"] <= lt_lit_max)
    return sites[mask].sort_values("LT_LIT", ascending=False).reset_index(drop=True)


def get_relative_research_score(
    accession: str, path: str | Path = DEFAULT_PSP_PATH
) -> pd.DataFrame:
    """Score each phosphosite by its relative research attention within this protein.

    Raw reference counts are biased — a protein with 50 sites will naturally
    have more total references than one with 5 sites. This function normalizes
    each site's LT_LIT by the protein's own maximum, giving a 0–1 score.

    A score near 0 = almost unstudied relative to the protein's best-known site.
    A score near 1 = as well-studied as the most-referenced site on this protein.

    Parameters
    ----------
    accession : UniProt accession ID

    Returns
    -------
    DataFrame with an added 'relative_lt_score' column (0.0 – 1.0).
    """
    sites = fetch_sites(accession, path)

    if sites.empty:
        return pd.DataFrame()

    max_lt = sites["LT_LIT"].max()

    # Avoid division by zero for proteins where all LT_LIT = 0
    if max_lt == 0:
        sites["relative_lt_score"] = 0.0
    else:
        sites["relative_lt_score"] = (sites["LT_LIT"] / max_lt).round(3)

    return sites.sort_values("relative_lt_score", ascending=False).reset_index(drop=True)
