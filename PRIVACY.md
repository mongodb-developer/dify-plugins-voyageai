# Privacy Policy — Voyage AI Plugin

## Overview

This plugin generates vector embeddings and reranks documents using Voyage AI models hosted on MongoDB Atlas.

## Data Collected

| Data | Purpose | Stored By |
|---|---|---|
| Voyage AI API key | Authenticate to the Atlas Voyage AI API | Dify platform (encrypted) |

No other personal data is collected by this plugin.

## Data Processing

- **Text inputs** (documents and queries) are transmitted to the Voyage AI API (`https://api.voyageai.com`) hosted on MongoDB Atlas infrastructure for embedding and reranking.
- Embeddings and relevance scores are returned to your Dify workflow and are subject to the privacy policies of any downstream nodes.
- No text inputs or embeddings are logged, stored, or retained by this plugin beyond the lifetime of a single API call.

## Data Retention

This plugin does not persist any data. All processing is stateless — no inputs, embeddings, or scores are written to disk.

## Third-Party Services

This plugin communicates exclusively with:

1. **Voyage AI API on MongoDB Atlas** (`https://api.voyageai.com`)

Usage is subject to the [MongoDB Atlas Terms of Service](https://www.mongodb.com/legal/terms-of-service).

## Support & Contact

- **GitHub Issues:** https://github.com/Pash10g/dify-plugins/issues
- **MongoDB Developer Community:** https://www.mongodb.com/community/forums/

## Related Policies

- [MongoDB Privacy Policy](https://www.mongodb.com/legal/privacy-policy)
- [MongoDB Atlas Terms of Service](https://www.mongodb.com/legal/terms-of-service)
