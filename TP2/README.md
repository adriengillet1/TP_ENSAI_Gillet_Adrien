# Product Indexing System

## Overview

This project implements a product indexing system, creating multiple inverted indexes to support search functionality. The system processes 150 product documents in JSONL format and generates various indexes for efficient retrieval.

## Index Structure

### 1. Title Index (`my_inversed_index_title.json`)
Inversed index mapping tokens to documents with position information:
```json
{
  "token": {
    "product_url": [0, 5, 12]
  }
}
```
- Tokens are lowercased, stripped of punctuation, and filtered for stopwords
- Position values indicate token occurrence order in the title

### 2. Description Index (`my_inversed_index_description.json`)
Same structure as title index, applied to product descriptions.

### 3. Review Index (`my_review_index.json`)
Aggregated review metrics per product:
```json
{
  "product_url": {
    "total_reviews": 15,
    "mean_mark": 4.2,
    "last_rating": 5
  }
}
```

### 4. Feature Indexes
Four separate inverted indexes for product features:

- **Brand Index** (`my_inversed_index_brand.json`): Maps brand names to product URLs
- **Origin Index** (`my_inversed_index_origin.json`): Maps manufacturing origins to product URLs
- **Design Index** (`my_inversed_index_design.json`): Maps design-related tokens to product URLs
- **Color Index** (`my_inversed_index_color.json`): Maps color tokens to product URLs

Structure for feature indexes:
```json
{
  "feature_value": ["url1", "url2"]
}
```

## Technical Choices

### Text Processing
- **Tokenization**: Using spaCy's English tokenizer with space-based splitting
- **Normalization**: Lowercasing all tokens
- **Punctuation removal**: Using Python's `string.punctuation` translation table
- **Stopword filtering**: Leveraging spaCy's default English stopword list

### URL Parsing
Product IDs and variants are extracted from URLs using `urllib.parse`:
- Product ID: Third path segment after domain
- Variant: Query parameter value

### Data Structures
- `defaultdict` for automatic key initialization
- Nested `defaultdict` for position tracking in title/description indexes

## Additional Features

Beyond the required brand and origin indexes, the system implements:
- **Design Index**: Tokenized search on design descriptions
- **Color Index**: Tokenized search on product colors

## Usage

### Requirements
```bash
pip install spacy
```

### Running the Code
```bash
python main.py
```

The script expects:
- Input file: `input/products.jsonl`
- Output: Seven JSON index files in the current directory

## Project Structure
```
.
├── main.py                  # Main execution script
├── processing_functions.py  # Index creation functions
├── utils.py                 # Helper functions (I/O, NLP setup)
└── README.md
```