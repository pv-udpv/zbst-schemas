# Integration Guide: Using zbst-schemas in Your Project

## Quick Start (5 minutes)

### 1. Install Dependencies

```bash
pip install datamodel-code-generator jsonschema pydantic
```

### 2. Generate Models

```bash
# Clone the repository
git clone https://github.com/pv-udpv/zbst-schemas.git
cd zbst-schemas

# Generate Pydantic models
python generators/generate_all.py
```

Generated models are in `models/generated/`

### 3. Use in Your Project

```python
from models.generated.opendirect.account import Account
from models.generated.zbst.deal import Deal

# Create and validate
account = Account(
    id="acc_123",
    advertiserid="adv_456",
    buyerid="buyer_789",
    status="Approved"
)

print(account.json())  # Automatic validation!
```

---

## Advanced Usage

### Custom Validation

```python
from pydantic import BaseModel, validator
from models.generated.zbst.deal import Deal

class DealWithValidation(Deal):
    @validator('end_date')
    def end_after_start(cls, v, values):
        if 'start_date' in values and v < values['start_date']:
            raise ValueError('end_date must be after start_date')
        return v
```

### API Request Validation

```python
from fastapi import FastAPI, HTTPException
from models.generated.opendirect.account import Account

app = FastAPI()

@app.post("/accounts")
async def create_account(account: Account):
    # Pydantic validates automatically
    return {"id": account.id, "status": account.status}

# Invalid requests are rejected with 422 Unprocessable Entity
```

### Direct Schema Validation

```python
import json
import jsonschema

with open('schemas/opendirect/account.schema.json') as f:
    schema = json.load(f)

data = {"id": "acc_123", "advertiserid": "adv_456", "buyerid": "buyer_789", "status": "Approved"}

# Validate
jsonschema.validate(instance=data, schema=schema)
print("✅ Valid!")
```

---

## Integration Patterns

### Pattern 1: FastAPI REST API

```python
from fastapi import FastAPI
from models.generated.opendirect.account import Account
from models.generated.opendirect.order import Order

app = FastAPI()

@app.post("/api/accounts")
async def create_account(account: Account):
    # Save to database
    return account.dict()

@app.post("/api/accounts/{account_id}/orders")
async def create_order(account_id: str, order: Order):
    # Validate and save
    return order.dict()
```

### Pattern 2: Database Models

```python
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from models.generated.opendirect.account import Account as AccountModel

Base = declarative_base()

class AccountDB(Base):
    __tablename__ = "accounts"
    
    id = Column(String, primary_key=True)
    advertiserid = Column(String)
    buyerid = Column(String)
    status = Column(String)
    created = Column(DateTime)
    
    def to_pydantic(self) -> AccountModel:
        return AccountModel(**self.__dict__)
```

### Pattern 3: Event Processing

```python
from models.generated.zbst.deal import Deal
import json

def process_deal_event(event_data: dict):
    # Validate against schema
    deal = Deal(**event_data)
    
    # Process
    print(f"Processing deal: {deal.deal_id}")
    print(f"Status: {deal.status}")
    print(f"Publisher: {deal.publisher_id}")
```

---

## Docker Integration

### Dockerfile

```dockerfile
FROM python:3.11

WORKDIR /app

# Install dependencies
RUN pip install datamodel-code-generator jsonschema pydantic

# Copy schemas
COPY schemas/ /app/schemas/
COPY generators/ /app/generators/

# Generate models
RUN python generators/generate_all.py

# Copy your application
COPY . /app/

CMD ["python", "app.py"]
```

### Build and Run

```bash
docker build -t zbst-schemas .
docker run zbst-schemas python generators/validate_schemas.py
```

---

## CI/CD Integration

### GitHub Actions

```yaml
name: Validate and Generate Models

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install jsonschema datamodel-code-generator
      - run: python generators/validate_schemas.py
      - run: python generators/generate_all.py
      - uses: actions/upload-artifact@v2
        with:
          name: generated-models
          path: models/generated/
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Validating schemas..."
python generators/validate_schemas.py || exit 1

echo "Generating models..."
python generators/generate_all.py || exit 1

git add models/generated/
```

---

## Troubleshooting

### Issue: Schema validation fails

**Solution**: Check schema syntax
```bash
python -m json.tool schemas/opendirect/account.schema.json
```

### Issue: Model generation fails

**Solution**: Update generator
```bash
pip install --upgrade datamodel-code-generator
python generators/generate_all.py
```

### Issue: Import errors

**Solution**: Ensure models directory is in Python path
```python
import sys
sys.path.insert(0, '/path/to/models/generated')
from opendirect.account import Account
```

---

## Performance Tips

1. **Cache parsed schemas**: Load once, reuse
2. **Pre-generate models**: Don't generate at runtime
3. **Use model validation only where needed**: Not for every operation
4. **Batch validate**: Validate multiple objects at once

---

## Next Steps

- Read SCHEMA_REFERENCE.md for detailed schema documentation
- Check examples/ directory for more integration patterns
- Join discussions for community support

---

**Need help?** Open an issue on [GitHub](https://github.com/pv-udpv/zbst-schemas/issues)
