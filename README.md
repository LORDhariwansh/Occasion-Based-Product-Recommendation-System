# Occasion-Based Product Recommendation System

A local product recommendation application that turns a natural-language occasion into ranked catalog products. It uses the supplied catalog only and needs no paid services or API keys.

## Problem statement

Choosing a suitable gift from a large product catalog is time-consuming when the shopper begins with an occasion rather than a product name. This project accepts an occasion such as `Wedding celebration`, `Diwali gift`, or `Something under ₹1000`, then returns relevant, available catalog products.

## Features

- Natural-language occasion search with optional budget filtering.
- Hybrid ranking that combines semantic similarity, TF-IDF relevance, and title-token overlap.
- Eligibility filtering for approved, active, in-stock, non-deleted catalog products.
- Cached `all-MiniLM-L6-v2` embeddings to avoid regenerating product vectors on each request.
- FastAPI API with OpenAPI documentation and CORS configuration.
- Responsive React interface with loading, error, initial, and no-results states.
- Catalog images when available and locally stored, product-type-specific fallback images when they are not.
- Automated API and preprocessing tests.

## How recommendation works

The preprocessing pipeline normalizes the provided catalog and creates searchable text from the actual product name, brand, descriptions, and category ID. No category names or product details are fabricated.

For each request, the system embeds the occasion with Sentence Transformers, calculates cosine similarity against cached product embeddings, and blends that result with lexical relevance:

```text
0.65 × semantic cosine similarity
+ 0.22 × TF-IDF similarity
+ 0.13 × title token overlap
```

Scores are used internally for ranking. Results below `MIN_RELEVANCE_SCORE` are excluded. Budget-only searches return eligible products at or below the extracted price ceiling without asserting an occasion match. The supplied catalog analysis is available in [DATASET_ANALYSIS.md](DATASET_ANALYSIS.md).

## Technology stack

- Backend: Python 3.11+, FastAPI, Uvicorn, Pydantic
- Machine learning: Sentence Transformers, scikit-learn, NumPy
- Frontend: React, Vite, Tailwind CSS, Lucide React
- Testing: pytest and FastAPI TestClient

## Architecture

```text
products.json → loader → preprocessing and eligibility filter → searchable catalog text
                                                            ↘ cached MiniLM embeddings
occasion query → context and budget parsing → hybrid ranking → FastAPI → React interface
```

## Prerequisites

- Python 3.11 or newer
- Node.js 18 or newer
- npm

## Installation and local development

Clone the repository and open its root directory:

```powershell
git clone https://github.com/LORDhariwansh/Occasion-Based-Product-Recommendation-System.git
cd Occasion-Based-Product-Recommendation-System
```

### Backend

Create an environment, install the backend dependencies, and start the API:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r backend\requirements.txt
$env:PYTHONPATH = "$PWD\backend"
uvicorn app.main:app --app-dir backend --reload --port 8000
```

The first startup downloads `all-MiniLM-L6-v2` and creates an embedding cache in `backend/.cache/`. API documentation is available at `http://localhost:8000/docs`.

### Frontend

In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in a browser.

## Configuration

Copy the example configuration files only when defaults need to change:

```powershell
Copy-Item .env.example .env
Copy-Item frontend\.env.example frontend\.env.local
```

| Variable | Default | Purpose |
| --- | --- | --- |
| `PRODUCTS_PATH` | `backend/products.json` | Catalog JSON location |
| `CACHE_DIR` | `backend/.cache` | Embedding cache directory |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Sentence Transformer model |
| `MIN_RELEVANCE_SCORE` | `0.20` | Minimum hybrid relevance score |
| `CORS_ORIGINS` | local Vite URLs | Comma-separated permitted frontend origins |
| `VITE_API_URL` | `http://localhost:8000` | Frontend API base URL |

`.env` files are ignored by Git. The included example files contain placeholders and no credentials.

## API usage

`GET /` returns API health, the eligible-product count, and the active embedding backend.

`GET /products` returns normalized eligible products.

`POST /recommend` accepts an occasion and optional result count:

```json
{
  "occasion": "Diwali celebration",
  "top_k": 5
}
```

The response contains the original product ID, catalog details, internal similarity score, selected image URL, and a catalog-grounded recommendation reason. Blank occasions receive HTTP 422; no-match queries return HTTP 200 with an empty recommendation list.

## Testing and verification

Run backend tests from the repository root:

```powershell
$env:PYTHONPATH = "$PWD\backend"
python -m pytest backend\tests -q
```

Build the frontend:

```powershell
cd frontend
npm run build
```

## Project structure

```text
backend/
  app/
    routes/             API endpoints
    schemas/            Request and response models
    services/           Loading, preprocessing, embedding, and ranking
  tests/                API and preprocessing tests
  products.json         Supplied product catalog
frontend/
  public/fallback-images/  Local, product-type fallback images
  src/components/       User-interface components
  src/services/         API client
DATASET_ANALYSIS.md     Catalog inspection report
```

## Limitations and future improvements

- The supplied catalog uses opaque category IDs; category labels need a separate lookup dataset.
- The catalog has no labelled relevance dataset, so the project does not claim a retrieval-accuracy metric.
- Recommendation quality depends on the completeness of supplied product text.
- Remote catalog image availability depends on the source host; local fallbacks preserve card layout when an image cannot load.
- Potential next steps include a labelled evaluation set, product/category metadata enrichment, and a production deployment configuration.

## Author

Built by [LORDhariwansh](https://github.com/LORDhariwansh).

## AI assistance disclosure

AI coding assistance was used during development for implementation support, code review, and documentation. The system behavior, catalog-grounded recommendations, and final verification should be reviewed by the repository owner before production use.
