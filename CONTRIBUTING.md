# Contributing to zbst-schemas

Thank you for interest in contributing! This guide explains how to add schemas and improve the registry.

---

## Code of Conduct

- Be respectful and inclusive
- Focus on schemas that solve real problems
- Test your schemas before submitting
- Provide clear documentation

---

## How to Contribute

### 1. Add a New Schema

**Step 1**: Create schema file
```bash
touch schemas/{category}/{name}.schema.json
```

**Step 2**: Fill in the template
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://schemas.zbst.io/{category}/{name}.schema.json",
  "title": "Your Title",
  "description": "Clear description of what this schema validates",
  "type": "object",
  "properties": {
    "field1": {
      "type": "string",
      "description": "Field description"
    }
  },
  "required": ["field1"],
  "additionalProperties": false,
  "examples": [
    { "field1": "value1" }
  ]
}
```

**Step 3**: Validate
```bash
python generators/validate_schemas.py
```

**Step 4**: Generate test models
```bash
python generators/generate_all.py
```

**Step 5**: Submit pull request

### 2. Improve Existing Schema

- Add validation constraints
- Improve descriptions
- Add examples
- Fix bugs

### 3. Add Documentation

- Write guides in `docs/`
- Add examples
- Improve README

---

## Schema Best Practices

### ✅ DO:

- Use descriptive field names
- Add clear descriptions for every field
- Include validation constraints (min, max, pattern, enum)
- Provide at least one realistic example
- Use `additionalProperties: false` to prevent surprises
- Link to IAB specs when applicable

### ❌ DON'T:

- Use overly permissive schemas
- Skip descriptions
- Use vague field names
- Add fields without validation rules
- Include circular references
- Use complex nested structures when flat is better

---

## Validation Rules

Always add constraints:

```json
{
  "properties": {
    "email": {
      "type": "string",
      "format": "email",
      "description": "Email address"
    },
    "age": {
      "type": "integer",
      "minimum": 0,
      "maximum": 150,
      "description": "Age in years"
    },
    "status": {
      "type": "string",
      "enum": ["Active", "Inactive"],
      "description": "Status value"
    },
    "id": {
      "type": "string",
      "pattern": "^[a-z0-9_-]+$",
      "description": "Unique identifier"
    }
  }
}
```

---

## Testing Your Schema

### Validate JSON syntax
```bash
python -m json.tool schemas/{category}/{name}.schema.json
```

### Validate schema structure
```bash
python generators/validate_schemas.py
```

### Generate Pydantic model
```bash
python generators/generate_all.py
```

### Test with example
```python
import jsonschema
import json

with open('schemas/{category}/{name}.schema.json') as f:
    schema = json.load(f)

with open('test_data.json') as f:
    data = json.load(f)

jsonschema.validate(instance=data, schema=schema)
print("✅ Valid!")
```

---

## Pull Request Process

1. **Fork** the repository
2. **Create branch**: `git checkout -b feature/add-xyz-schema`
3. **Add schema** in `schemas/{category}/`
4. **Validate**: `python generators/validate_schemas.py`
5. **Test**: Ensure model generation works
6. **Document**: Add description in PR
7. **Push**: `git push origin feature/add-xyz-schema`
8. **Submit PR** with:
   - Clear title
   - Description of schema
   - Use cases
   - Test results

---

## Review Criteria

Schemas are accepted when:
- ✅ Valid JSON Schema Draft 7
- ✅ Clear, descriptive field names
- ✅ All fields documented
- ✅ Validation constraints defined
- ✅ Example(s) provided
- ✅ No unnecessary nesting
- ✅ Follows naming conventions
- ✅ Passes all validation checks

---

## Naming Conventions

### Schema Files
- Lowercase with hyphens: `account.schema.json`, `bid-request.schema.json`
- Organized by category: `schemas/opendirect/`, `schemas/openrtb/`

### Schema Fields
- Lowercase with underscores: `advertiser_id`, `start_date`
- Use full names: `advertisement_id` not `adv_id`
- Be consistent across schemas

### Schema IDs
```
$id: https://schemas.zbst.io/{category}/{name}.schema.json
```

---

## Categories

- **opendirect/** — OpenDirect v2.1 schemas
- **openrtb/** — OpenRTB 2.6 schemas
- **vast/** — VAST 4.2 schemas
- **cats/** — CATS 1.0 schemas
- **adcom/** — AdCOM 1.3 schemas
- **zbst/** — zbst-tech extensions

---

## Resources

- [JSON Schema Draft 7](https://json-schema.org/specification.html)
- [OpenDirect v2.1](https://github.com/InteractiveAdvertisingBureau/OpenDirect)
- [OpenRTB 2.6](https://www.iab.com/wp-content/uploads/2016/03/OpenRTB-API-Specification-Version-2-6-final.pdf)
- [VAST 4.2](https://www.iab.com/wp-content/uploads/2019/06/VAST_4.2_final_june2019.pdf)
- [Pydantic Docs](https://docs.pydantic.dev/)

---

## Questions?

- Open an [issue](https://github.com/pv-udpv/zbst-schemas/issues)
- Join [discussions](https://github.com/pv-udpv/zbst-schemas/discussions)
- Check [existing schemas](https://github.com/pv-udpv/zbst-schemas/tree/main/schemas) for examples

---

**Thank you for contributing!** 🉋
