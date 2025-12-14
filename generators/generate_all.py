#!/usr/bin/env python3
"""
Generate Pydantic models from all JSON schemas.

Usage:
    pip install datamodel-code-generator
    python generators/generate_all.py
"""

import os
import json
from pathlib import Path
from datamodel_code_generator.inputs import JsonSchemaInput
from datamodel_code_generator.outputs import PythonOutput

BASE_DIR = Path(__file__).parent.parent
SCHEMAS_DIR = BASE_DIR / "schemas"
MODELS_DIR = BASE_DIR / "models" / "generated"

# Create models directory
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# Schema categories and files
SCHEMAS = {
    "opendirect": [
        "account.schema.json",
        "order.schema.json",
    ],
    "zbst": [
        "deal.schema.json",
        "revenue-split.schema.json",
    ],
}

def generate_model(schema_path, output_path):
    """Generate Pydantic model from JSON schema."""
    print(f"Generating: {schema_path} -> {output_path}")
    
    try:
        input_obj = JsonSchemaInput(Path(schema_path))
        output = PythonOutput(output_path, model_base_class="pydantic.BaseModel")
        output.generate([input_obj])
        print(f"  ✅ Generated: {output_path}")
    except Exception as e:
        print(f"  ❌ Error: {e}")

def main():
    print("\n🔨 Generating Pydantic models from JSON schemas...\n")
    
    # Create __init__.py files
    (MODELS_DIR / "__init__.py").touch()
    
    for category, files in SCHEMAS.items():
        category_dir = SCHEMAS_DIR / category
        output_dir = MODELS_DIR / category
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create __init__.py
        (output_dir / "__init__.py").touch()
        
        for schema_file in files:
            schema_path = category_dir / schema_file
            output_file = schema_file.replace(".schema.json", ".py")
            output_path = output_dir / output_file
            
            if schema_path.exists():
                generate_model(schema_path, output_path)
            else:
                print(f"  ⚠️  Schema not found: {schema_path}")
    
    print(f"\n✅ Done! Generated models in: {MODELS_DIR}\n")

if __name__ == "__main__":
    main()
