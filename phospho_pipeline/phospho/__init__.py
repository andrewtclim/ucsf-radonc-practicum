"""PhosphoAtlas package exports."""

from phospho.uniprot import (
    fetch_entry,
    get_gene_symbol,
    get_primary_accession,
    get_protein_name,
    get_ptm_texts,
    search_uniprot,
    uniprot_request_data,
)
from phospho.phosphosite import (
    load_psp_dataset,
    fetch_sites,
    get_reference_summary,
    get_underresearched_sites,
    get_relative_research_score,
)

__all__ = [
    "search_uniprot",
    "fetch_entry",
    "uniprot_request_data",
    "get_primary_accession",
    "get_gene_symbol",
    "get_protein_name",
    "get_ptm_texts",
    "load_psp_dataset",
    "fetch_sites",
    "get_reference_summary",
    "get_underresearched_sites",
    "get_relative_research_score",
]
