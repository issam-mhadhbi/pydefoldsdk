# Message: `VertexAttribute`

### Fields:
- **name**: `str`
- **name_hash**: `int`
- **semantic_type**: `int`
- **element_count**: `int`
- **normalize**: `bool`
- **data_type**: `int`
- **coordinate_space**: `int`
- **step_function**: `int`
- **vector_type**: `int`
- **long_values**: `LongValues`
- **double_values**: `DoubleValues`
- **binary_values**: `bytes`

### Enums:
- **DataType**:
  - `TYPE_BYTE = 1`
  - `TYPE_UNSIGNED_BYTE = 2`
  - `TYPE_SHORT = 3`
  - `TYPE_UNSIGNED_SHORT = 4`
  - `TYPE_INT = 5`
  - `TYPE_UNSIGNED_INT = 6`
  - `TYPE_FLOAT = 7`
- **VectorType**:
  - `VECTOR_TYPE_SCALAR = 1`
  - `VECTOR_TYPE_VEC2 = 2`
  - `VECTOR_TYPE_VEC3 = 3`
  - `VECTOR_TYPE_VEC4 = 4`
  - `VECTOR_TYPE_MAT2 = 5`
  - `VECTOR_TYPE_MAT3 = 6`
  - `VECTOR_TYPE_MAT4 = 7`
- **SemanticType**:
  - `SEMANTIC_TYPE_NONE = 1`
  - `SEMANTIC_TYPE_POSITION = 2`
  - `SEMANTIC_TYPE_TEXCOORD = 3`
  - `SEMANTIC_TYPE_PAGE_INDEX = 4`
  - `SEMANTIC_TYPE_COLOR = 5`
  - `SEMANTIC_TYPE_NORMAL = 6`
  - `SEMANTIC_TYPE_TANGENT = 7`
  - `SEMANTIC_TYPE_WORLD_MATRIX = 8`
  - `SEMANTIC_TYPE_NORMAL_MATRIX = 9`
  - `SEMANTIC_TYPE_BONE_WEIGHTS = 10`
  - `SEMANTIC_TYPE_BONE_INDICES = 11`

---
