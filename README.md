# zbst-schemas

**Public JSON Schema Registry for CTV/OTT Ad Exchange**

🔗 Reusable schemas for OpenDirect, OpenRTB, VAST, CATS protocols  
📦 Generate Pydantic models with `datamodel-code-generator`  
✅ Production-ready, IAB-compliant specifications  
🌍 Community-driven, MIT Licensed

---

## Quick Start

### 1. Browse Schemas

All schemas are in `schemas/` directory:
```
zbst-schemas/
├── schemas/
│   ├── opendirect/          # OpenDirect v2.1
│   ├── openrtb/             # OpenRTB 2.6
│   ├── vast/                # VAST 4.2
│   ├── cats/                # CATS 1.0
│   ├── adcom/               # AdCOM 1.3
│   └── zbst/                # zbst-tech extensions
└── generators/              # Model generation scripts
```

### 2. Generate Pydantic Models

```bash
pip install datamodel-code-generator

# Generate from OpenDirect schema
datamodel-codegen \
  --input schemas/opendirect/account.schema.json \
  --input-file-type jsonschema \
  --output models/opendirect_account.py
```

### 3. Use in Your Project

```python
from models.opendirect_account import Account

account = Account(
    id="acc_123",
    advertiserid="adv_456",
    buyerid="buyer_789",
    status="Approved"
)

# Validation happens automatically!
```

---

## What's Included

### OpenDirect v2.1 Schemas
- `organization.schema.json` — Publisher, Buyer, Advertiser, Agency roles
- `account.schema.json` — Account (Buyer ↔ Advertiser relationship)
- `order.schema.json` — Order with lines, creative, assignments
- `product.schema.json` — Inventory package definition

### OpenRTB 2.6 Schemas
- `bid-request.schema.json` — BidRequest (supply context)
- `bid-response.schema.json` — BidResponse (bids)
- `pmp.schema.json` — Private marketplace deals

### VAST 4.2 Schemas
- `vast-wrapper.schema.json` — VAST wrapper structure
- `vast-inlineadvertisement.schema.json` — Inline ad definitions
- `vast-macros.schema.json` — Macro definitions

### CATS 1.0 Schemas
- `cats-request.schema.json` — CATS bid request
- `cats-response.schema.json` — CATS bid response

### AdCOM 1.3 Schemas
- `adcom-objects.schema.json` — Shared AdCOM objects (Device, User, Content, etc.)

### zbst-tech Extensions
- `zbst-deal.schema.json` — Deal with OpenDirect mapping
- `zbst-revenue-split.schema.json` — Revenue calculation rules
- `zbst-vast-provider.schema.json` — VAST provider config

---

## Schema Structure

Each schema follows JSON Schema Draft 7:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Account",
  "description": "OpenDirect Account (Buyer ↔ Advertiser relationship)",
  "type": "object",
  "properties": {
    "id": {
      "type": "string",
      "description": "Account ID",
      "pattern": "^[a-z0-9_-]+$"
    },
    "status": {
      "type": "string",
      "enum": ["Pending", "Approved", "Live", "Inactive"],
      "default": "Pending"
    }
  },
  "required": ["id", "status"],
  "additionalProperties": false
}
```

**Key features**:
- ✅ Type validation
- ✅ Enum validation
- ✅ Pattern matching (regex)
- ✅ Required fields
- ✅ Default values
- ✅ Custom error messages

---

## Validation Rules

### OpenDirect Account
```json
{
  "constraints": {
    "status_transitions": "Pending → Approved → Live → Inactive",
    "date_constraint": "enddate > startdate",
    "rate_constraint": "rate >= 0"
  }
}
```

### zbst-tech Deal
```json
{
  "constraints": {
    "devices_match": "deal.allowed_devices ⊆ publisher.supported_devices",
    "placements_match": "deal.placements ⊆ publisher.supported_placements",
    "duration_match": "deal.durations ⊆ publisher.ad_durations_sec",
    "revenue_sum": "publisher% + exchange% + dsp% = 100%"
  }
}
```

---

## Model Generation

### Option 1: Using CLI

```bash
# Install generator
pip install datamodel-code-generator

# Generate all models
cd generators
python generate_all.py
```

### Option 2: Using Docker

```bash
docker run --rm -v $(pwd):/work \
  datamodelcode/datamodel-code-generator:v0.18 \
  --input /work/schemas/opendirect/account.schema.json \
  --input-file-type jsonschema \
  --output /work/models/opendirect_account.py
```

### Output

Generated Pydantic model:
```python
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

class AccountStatus(str, Enum):
    Pending = "Pending"
    Approved = "Approved"
    Live = "Live"
    Inactive = "Inactive"

class Account(BaseModel):
    id: str = Field(..., description="Account ID")
    advertiserid: str
    buyerid: str
    status: AccountStatus = Field(default=AccountStatus.Pending)
    
    class Config:
        extra = "forbid"  # No additional properties
```

---

## CI/CD Validation

### Pre-commit Hook

```bash
# .git/hooks/pre-commit
for schema in schemas/**/*.schema.json; do
  python -m jsonschema.validators validate_schema "$schema" || exit 1
done
```

### GitHub Actions

```yaml
name: Validate Schemas

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: python-jsonschema/action@main
        with:
          instance: schemas/
          schema: |
            {
              "$schema": "http://json-schema.org/draft-07/schema#",
              "type": "object"
            }
```

---

## API Usage

### Validate JSON Against Schema

```python
import jsonschema
import json

with open('schemas/opendirect/account.schema.json') as f:
    schema = json.load(f)

data = {
    "id": "acc_123",
    "advertiserid": "adv_456",
    "buyerid": "buyer_789",
    "status": "Approved"
}

# Validate
try:
    jsonschema.validate(instance=data, schema=schema)
    print("✅ Valid!")
except jsonschema.ValidationError as e:
    print(f"❌ Invalid: {e.message}")
```

### REST API (Optional)

```bash
# Start validation server
python validators/api.py

# Validate POST request
curl -X POST http://localhost:8000/validate \
  -H "Content-Type: application/json" \
  -d @data.json \
  -H "X-Schema: opendirect/account"
```

---

## Contributing

### Add a New Schema

1. Create file: `schemas/{category}/{name}.schema.json`
2. Follow JSON Schema Draft 7 standard
3. Add validation rules in `constraints` section
4. Submit pull request
5. CI validates schema syntax
6. Maintainers review

### Schema Template

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://schemas.zbst.io/opendirect/{name}.schema.json",
  "title": "Title",
  "description": "Description",
  "type": "object",
  "properties": {},
  "required": [],
  "additionalProperties": false,
  "examples": [
    {
      "comment": "Example instance"
    }
  ]
}
```

---

## Versioning

### Schema Versioning

Schemas use semantic versioning:
- `v1.0.0` — OpenDirect v2.1 compatible
- `v1.1.0` — Backward compatible additions
- `v2.0.0` — Breaking changes

### Compatibility Matrix

| Schema | OpenDirect | OpenRTB | VAST | CATS | Status |
|--------|-----------|---------|------|------|--------|
| opendirect/* | v2.1 | — | — | — | ✅ v1.0.0 |
| openrtb/* | — | v2.6 | — | — | ✅ v1.0.0 |
| vast/* | — | — | v4.2 | — | ✅ v1.0.0 |
| cats/* | — | — | — | v1.0 | ✅ v1.0.0 |
| adcom/* | AdCOM v1.3 | AdCOM v1.3 | AdCOM v1.3 | AdCOM v1.3 | ✅ v1.0.0 |
| zbst/* | v2.1 | v2.6 | v4.2 | v1.0 | ✅ v1.0.0 |

---

## License

MIT License — See LICENSE file

---

## Documentation

- **Schema Reference**: [docs/SCHEMA_REFERENCE.md](docs/SCHEMA_REFERENCE.md)
- **Integration Guide**: [docs/INTEGRATION_GUIDE.md](docs/INTEGRATION_GUIDE.md)
- **Model Generation**: [docs/MODEL_GENERATION.md](docs/MODEL_GENERATION.md)
- **Validation Rules**: [docs/VALIDATION_RULES.md](docs/VALIDATION_RULES.md)

---

## Support

**Issues**: [GitHub Issues](https://github.com/pv-udpv/zbst-schemas/issues)  
**Discussions**: [GitHub Discussions](https://github.com/pv-udpv/zbst-schemas/discussions)  
**Email**: schemas@zbst.io

---

## Related Projects

- **zbst-phase0-foundation**: [Architecture & ADRs](https://github.com/pv-udpv/zbst-phase0-foundation)
- **zbst-tech**: [Main exchange platform](https://github.com/pv-udpv/zbst-tech)
- **OpenDirect**: [IAB Tech Lab](https://github.com/InteractiveAdvertisingBureau/OpenDirect)
- **OpenRTB**: [IAB Tech Lab](https://www.iab.com/wp-content/uploads/2016/03/OpenRTB-API-Specification-Version-2-6-final.pdf)

---

**zbst-schemas: Making Ad Tech Schema Management Simple** 🎯
