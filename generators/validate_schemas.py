#!/usr/bin/env python3
"""
Validate all JSON schemas against JSON Schema Draft 7.

Usage:
    pip install jsonschema
    python generators/validate_schemas.py
"""

import json
from pathlib import Path
import jsonschema
from jsonschema import Draft7Validator, validators

BASE_DIR = Path(__file__).parent.parent
SCHEMAS_DIR = BASE_DIR / "schemas"

def validate_schema(schema_path):
    """Validate a single JSON schema."""
    try:
        with open(schema_path) as f:
            schema = json.load(f)
        
        # Check if schema is valid against Draft 7
        Draft7Validator.check_schema(schema)
        
        print(f"  ✅ Valid: {schema_path.name}")
        return True
    except jsonschema.SchemaError as e:
        print(f"  ❌ Schema error in {schema_path.name}: {e.message}")
        return False
    except json.JSONDecodeError as e:
        print(f"  ❌ JSON error in {schema_path.name}: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Error in {schema_path.name}: {e}")
        return False

def main():
    print("\n🔍 Validating JSON schemas...\n")
    
    valid_count = 0
    error_count = 0
    
    for schema_file in sorted(SCHEMAS_DIR.rglob("*.schema.json")):
        if validate_schema(schema_file):
            valid_count += 1
        else:
            error_count += 1
    
    print(f"\n📊 Results: {valid_count} valid, {error_count} errors\n")
    
    if error_count > 0:
        exit(1)

if __name__ == "__main__":
    main()
